## 1. Cálculo del informe (TDD)

- [x] 1.1 Escribir en `tests/test_report.py` los tests de las reglas RD (una fila por marca y no detectadas a 0, umbral en el límite, por debajo y ajustado, un fotograma por marca aunque haya varios logos, varias marcas en un fotograma, tiempo y porcentaje) y de los errores (fps ≤ 0, sin fotogramas, umbral fuera de [0, 1], marca desconocida); verificar que fallan porque `report` no existe
- [x] 1.2 Implementar en `src/logo_detector/report.py` `Detection`, `BrandExposure`, `ExposureReport` y `build_report`; verificar que los tests de 1.1 pasan con `make test`

## 2. Serialización a JSON

- [x] 2.1 Escribir los tests de `save_report` (ruta por defecto en `OUTPUTS_DIR` con la carpeta creada, ruta indicada e ida y vuelta con los mismos valores) y implementarlo; verificar con `make test` y `make lint`

## 3. Documentación

- [x] 3.1 Actualizar ARCHITECTURE §3 (`report` «Actual») con el informe JSON en `outputs/`; verificar que no duplica lo que dice la spec
