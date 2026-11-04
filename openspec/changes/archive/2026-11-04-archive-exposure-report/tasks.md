## 1. Archivo de add-exposure-report

- [x] 1.1 Comprobar que no hay un `.openspec-archive.lock` obsoleto y ejecutar `openspec archive add-exposure-report` con la validación por defecto; verificar que el cambio queda en `openspec/changes/archive/` y que `git diff` no toca `openspec/specs/report/spec.md`
- [x] 1.2 Ejecutar `openspec validate --all --strict`, `make lint` y `make test`; verificar que pasan sin cambios en los resultados
