## Why

Historia [#23](https://github.com/Glezino/ai-computer-vision/issues/23), de la épica E3 (#4). El PR #21 de la historia #11 se mergeó sin el commit de archive (WORKFLOW §6, paso 7), probablemente porque un `.openspec-archive.lock` obsoleto bloqueaba `openspec archive`. Por eso `openspec/changes/add-exposure-report/` sigue activo en `dev`, y #11 y E3 siguen abiertas aunque su código y su spec ya están en `dev`. No implementa ningún requisito.

## What Changes

- Archivar `add-exposure-report` con la validación por defecto de `openspec archive`. Su spec `report` ya está sincronizada, así que el archive no debe cambiarla.
- Cerrar #11 y E3 (#4) desde el PR de esta historia con `Closes`, ya que fue la última historia abierta de E3.

Fuera de alcance: cualquier cambio en `report`, en su spec o en el código.

## Capabilities

### New Capabilities

Ninguna.

### Modified Capabilities

Ninguna. Sin delta de specs (`skip_specs`): no cambia el comportamiento.

## Impact

- **Código:** ninguno.
- **OpenSpec:** `openspec/changes/add-exposure-report/` pasa a `openspec/changes/archive/<fecha>-add-exposure-report/`; `openspec/specs/report/spec.md` no cambia.
- **Documentación, contratos y ADR:** ninguno.
