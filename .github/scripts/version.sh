# Próximo tag beta de HEAD (CONTRIBUTING §9). Lo usan tags.yml y ci.yml con `source`.
# next_beta deja en $tag el tag (vacío si lo nuevo no cambia la versión) y en $reason el motivo.

# Commits que cambian la versión: incompatibles, feat, fix o perf.
VERSIONED='^[a-z]+(\([^)]*\))?!:|^(feat|fix|perf)(\([^)]*\))?:'

# Nivel de cambio de un rango de commits: major, minor, patch o none.
bump() {
  local log
  log=$(git log --format='%s%n%b' "$1")
  if grep -qE '^[a-z]+(\([^)]*\))?!:|^BREAKING[ -]CHANGE:' <<< "$log"; then echo major
  elif grep -qE '^feat(\([^)]*\))?:' <<< "$log"; then echo minor
  elif grep -qE '^(fix|perf)(\([^)]*\))?:' <<< "$log"; then echo patch
  else echo none
  fi
}

next_beta() {
  local prev range last level version major minor patch n commits
  tag='' reason=''

  # Solo hay tag si lo nuevo desde el último beta cambia la versión.
  prev=$(git describe --tags --abbrev=0 --match 'v*-beta.*' 2>/dev/null || true)
  range="${prev:+$prev..}HEAD"
  if [ "$(bump "$range")" = none ]; then return 0; fi

  # Siguiente versión estable según los commits desde el último tag estable.
  last=$(git tag --list 'v[0-9]*' --sort=-v:refname | grep -v -- - | head -n 1 || true)
  if [ -z "$last" ]; then
    version=0.1.0
    level="primera versión"
  else
    level=$(bump "$last..HEAD")
    IFS=. read -r major minor patch <<< "${last#v}"
    case "$level" in
      major)
        if [ "$major" -eq 0 ]; then minor=$((minor + 1)); else major=$((major + 1)); minor=0; fi
        patch=0 ;;
      minor) minor=$((minor + 1)); patch=0 ;;
      *) patch=$((patch + 1)) ;;
    esac
    version="$major.$minor.$patch"
    level="$level desde $last"
  fi

  n=$(git tag --list "v$version-beta.*" | sed 's/.*-beta\.//' | sort -n | tail -n 1)
  tag="v$version-beta.$(( ${n:-0} + 1 ))"
  commits=$(git log --format='%s' "$range" | grep -E "$VERSIONED" | sed 's/^/- /' || true)
  reason="$level"$'\n'"$commits"
}
