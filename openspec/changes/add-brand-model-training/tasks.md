## 1. Componente training

- [x] 1.1 Añadir `BRAND_MODEL = "brands.pt"` y `RUNS_DIR` a `config.py`; verificar que `make lint` y `make test` pasan
- [x] 1.2 Escribir con TDD `metrics_rows` y `format_metrics` (fila global y una por marca, clases ausentes a cero); verificar con tests en `tests/test_training.py`
- [x] 1.3 Definir `TRAIN_CONFIG` y la combinación con *overrides*; verificar con tests que incluye el tamaño de imagen y el aumento de datos, y que un *override* cambia solo ese parámetro
- [x] 1.4 Escribir `train()` (entrena en `runs/brands` y copia `best.pt` a `models/brands.pt`) y `evaluate()`; verificar con un entrenamiento de humo en CPU (`epochs=1`, `fraction=0.1`) que se crean los pesos, que al cargarlos tienen las tres clases y que se muestra la tabla

## 2. Notebook de entrenamiento

- [x] 2.1 Escribir `notebooks/02_training.py` (preparación solo en Colab, configuración visible, dataset, entrenamiento, métricas y descarga de los pesos); verificar con `make lint` y `make notebooks`
- [x] 2.2 Ejecutar el notebook en local con un *override* de humo; verificar que termina sin errores

## 3. Entrenamiento real (persona, en Colab)

- [x] 3.1 Ejecutar `02_training` en Colab con GPU desde la rama de la historia, y obtener `brands.pt` y la tabla de métricas de validación
- [x] 3.2 Copiar `brands.pt` a `models/` y comprobar en local con `evaluate()` que da las mismas métricas; si mAP@0.5 < 0,6, entrenar small o documentar la desviación

## 4. Documentación

- [x] 4.1 Actualizar ARCHITECTURE §3 (`training` «Actual»), §7 (entrenamiento y pesos) y §8 (métricas obtenidas frente a RNF-03), y explicar en el README cómo obtener los pesos
