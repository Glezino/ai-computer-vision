# CONTRIBUTING

Convenciones para personas y agentes de IA. El flujo y sus paradas están en [`WORKFLOW.md`](WORKFLOW.md); las reglas propias de la IA, en [`AGENTS.md`](AGENTS.md).

## 1. Idioma

- **Español:** documentación, Issues, PRs y artefactos de OpenSpec, salvo las palabras clave de formato que valida el CLI (encabezados, `SHALL`/`MUST`, `WHEN`/`THEN`).
- **Inglés:** código, identificadores, ramas, commits y etiquetas.

## 2. Modelo de trabajo

```text
Épica          (Issue · epic; agrupada por hitos en docs/ROADMAP.md)
└── Historia   (Issue · story · sub-issue de la épica)
    └── [ ] tarea
```

- **Épica:** capacidad de producto acotada. Se cierra con el PR de su última historia (`Closes #E`).
- **Historia:** incremento pequeño y observable de una capa (o de un contrato) que la deja funcionando. **Una historia = una rama = un PR = un cambio de OpenSpec.**
- **Tarea:** casilla dentro de la historia; no es una Issue ni lleva etiqueta.
- **Bug:** historia de tipo `fix`, con la plantilla de bug. Cuelga de una épica si pertenece a una.

Las historias se dividen por capas, con el contrato primero ([WORKFLOW §5](WORKFLOW.md#trabajo-por-capas)). La jerarquía (sub-issues) y los bloqueos (*blocked by*) se registran con las relaciones nativas de GitHub, que son su fuente de verdad. La jerarquía no implica orden: un bloqueo solo existe cuando una Issue no puede avanzar sin otra.

### Definición de Ready

Una historia está lista (`ready`) cuando:

- cuelga de su épica o es un bug independiente;
- cita los requisitos que implementa (`RF`, `RNF`, `RD`) o explica por qué no aplica ninguno;
- tiene objetivo, alcance y criterios de aceptación observables;
- no tiene bloqueos abiertos.

### Definición de Done

Una historia está terminada cuando:

- `verify` no deja discrepancias con los artefactos aprobados, las specs están sincronizadas y `openspec validate` pasa;
- los tests y checks del proyecto pasan, en local y en el CI;
- la documentación afectada está actualizada ([WORKFLOW §2](WORKFLOW.md#qué-actualizar-cuando-algo-cambia));
- el PR está revisado, con el archive como último commit y `Closes #N`, y la persona lo ha mergeado en `dev`.

## 3. Ramas

```text
feature/*  ─┐
fix/*       │
refactor/*  ├──→ dev ───→ main
docs/*      │
test/*      │
chore/*    ─┘
```

- `main`: producción. Solo recibe promociones desde `dev`.
- `dev`: integración y rama por defecto del repositorio, para que `Closes #N` cierre las Issues al mergear en ella.
- Las ramas de trabajo salen de `dev` y vuelven a `dev` por PR; `dev` llega a `main` por un PR de promoción. No se hace push directo a `dev` ni a `main`.

Formato: `<tipo>/<issue>-<descripcion>` en kebab-case, por ejemplo `feature/12-briefing-form` o `fix/31-empty-response`. Solo el trabajo sin Issue omite el número, como `docs/project-definition`.

## 4. Tipos de trabajo

El tipo se elige en la Issue y determina la rama y el tipo principal de commit:

| Etiqueta de la Issue | Rama | Commit principal |
|---|---|---|
| `feature`, `enhancement` | `feature/` | `feat` |
| `fix` | `fix/` | `fix` |
| `refactor` | `refactor/` | `refactor` |
| `docs` | `docs/` | `docs` |
| `test` | `test/` | `test` |
| `chore` | `chore/` | `chore` |

Una rama puede incluir commits de otros tipos (`test`, `docs`, `perf`, `ci`, `build`) cuando forman parte de la misma historia.

## 5. Commits

[Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/), sin prefijos propios:

```text
type(scope): description
```

- `type`: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci` o `build`.
- `scope`: opcional; el componente de [ARCHITECTURE §3](docs/ARCHITECTURE.md#3-componentes), el módulo o la capacidad afectada.
- `description`: en imperativo, en minúscula y sin punto final.
- Cambio incompatible: `!` tras el tipo (`feat(api)!: …`) y pie `BREAKING CHANGE: …`.
- Pie `Refs #N` cuando el commit pertenece a una historia.

```text
feat(api): add generation endpoint
fix(editor): prevent empty submission
docs(specs): sync add-generation-endpoint
chore(openspec): archive add-generation-endpoint
```

Cada commit es un bloque lógico que se entiende y se revisa por sí solo. No mezcles componentes (frontend y backend, por ejemplo) ni código y documentación en el mismo commit.

## 6. Issues

- Plantillas en `.github/ISSUE_TEMPLATE/`: épica, historia y bug. Etiquetas en [`docs/ISSUE_LABELS.md`](docs/ISSUE_LABELS.md).
- Cada Issue lleva exactamente una etiqueta de nivel (`epic` o `story`) y al menos una de tipo.
- La Issue es el contexto principal de su trabajo.
- Historias y épicas se cierran con `Closes` al mergear su PR en `dev` (§7). Las descartadas se cierran como *not planned*, con un comentario que explique el motivo.

## 7. Pull requests

### Historia → `dev`

- Un PR por historia, con la plantilla de PR.
- Se abre con `Refs #N`. Tras la revisión, la IA añade el archive como último commit y cambia a `Closes #N`, más `Closes #E` si es la última historia abierta de su épica ([WORKFLOW §6](WORKFLOW.md#6-fase-3--ejecución-de-una-historia)).
- Merge con **Rebase and merge**, para conservar los commits; squash fundiría el archive y los commits enfocados en uno solo.

### Promoción `dev` → `main`

- Indica la versión y lista las historias incluidas con `Refs #N`.
- Merge con **Create a merge commit**, para que `main` y `dev` no diverjan.

### Correcciones urgentes

Siguen el camino de cualquier historia (`fix/` → `dev`), seguido de una promoción inmediata.

### Revisión

La persona revisa el PR y lo mergea con el CI en verde. Los agentes de IA no mergean.

## 8. Calidad y CI

El CI ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)) ejecuta `openspec validate` en cada PR y comenta la versión prevista (§9). Trae bloques comentados para Python (uv o pip), Node (TypeScript, React…) y Docker. El walking skeleton descomenta los del stack y los ajusta a las herramientas de [ARCHITECTURE §8](docs/ARCHITECTURE.md#8-calidad-tests-ci-y-observabilidad). Los checks que aún no están en el CI se ejecutan en local.

## 9. Versiones y releases

Las versiones siguen [Semantic Versioning](https://semver.org/lang/es/) según los tipos de commit:

- `MAJOR`: cambio incompatible (`!` o `BREAKING CHANGE`). Mientras `MAJOR` sea 0, sube `MINOR`.
- `MINOR`: `feat`.
- `PATCH`: `fix` y `perf`.
- `docs`, `refactor`, `test`, `chore`, `ci` y `build` no cambian la versión.

La primera versión es `0.1.0`; la persona decide cuándo se publica `1.0.0`.

| Al mergear | Tag | Dónde | Release de GitHub |
|---|---|---|---|
| En `dev`, un PR que cambia la versión | `vX.Y.Z-beta.N` | Último commit de `dev` | No |
| En `main`, una promoción | `vX.Y.Z` | Commit de merge en `main` | Sí, con notas generadas desde el último tag estable |

- Los tags y las releases los crea el CI ([`.github/workflows/tags.yml`](.github/workflows/tags.yml)); no se crean a mano.
- **Revisión humana:** en cada PR a `dev`, el CI comenta el tag beta previsto y los commits que lo causan; la persona lo aprueba en la Parada 4 ([WORKFLOW §6](WORKFLOW.md#6-fase-3--ejecución-de-una-historia)). Si no es el esperado, se corrigen los tipos de commit antes del merge.
- **`X.Y.Z` del tag beta:** la siguiente versión estable según los commits desde el último tag estable, o `0.1.0` si no hay ninguno. **`N`** empieza en 1, sube con cada beta y vuelve a 1 cuando cambia `X.Y.Z`.
- **El tag estable** es el último tag beta sin el sufijo.
- No hay CHANGELOG manual: las notas de versión son las GitHub Releases.

## 10. Reglas generales

- Mantén los cambios enfocados.
- No subas secretos ni credenciales.
