## Context

- `make data` deja `data/openlogo/data.yaml`, con ruta absoluta, y 1.209, 259 y 260 imágenes en train, val y test.
- `config.py` define `PRETRAINED_MODEL = "yolo26n.pt"`, `IMAGE_SIZE = 640`, `MODELS_DIR` y `SPLIT_SEED`.
- El repositorio es público, así que Colab puede clonarlo sin credenciales.
- En CPU local, `yolo26n` tarda unos 100 ms por imagen de 640 px.
- ADR-0001: entrenamiento en Colab con GPU, inferencia en CPU y la variante (nano o small) se fija en esta historia.

Motivación en `proposal.md`; comportamiento en `specs/training/spec.md`.

## Goals / Non-Goals

**Goals:**

- Un solo código de entrenamiento para Colab y para local; el notebook solo lo orquesta (ADR-0002).
- Configuración explícita, aunque coincida con los valores por defecto de Ultralytics, para que quede documentada y no cambie si cambian esos valores.
- Probar la lógica propia sin GPU ni entrenamiento.

**Non-Goals:**

- Buscar hiperparámetros, o reentrenar en el CI.
- Evaluar sobre test: test se reserva para una comprobación final, no para elegir el modelo.
- Publicar los pesos en una release o en Hugging Face.

## Decisions

- **Modelo base YOLO26 nano.** Con unos 100 ms por fotograma en CPU, un vídeo de 1 minuto a 30 fps (1.800 fotogramas) tarda unos 3 minutos, dentro de RNF-02 (menos de 5). La variante small sería unas 2,5 veces más lenta y lo superaría. Si nano no llega a mAP@0.5 ≥ 0,6 (RNF-03), se entrena small y se documenta el compromiso con RNF-02.
- **`TRAIN_CONFIG`** es un diccionario del módulo `training`, con este preprocesamiento y aumento de datos:

  | Grupo | Parámetros |
  |---|---|
  | Preprocesamiento | `imgsz=config.IMAGE_SIZE` (Ultralytics redimensiona con *letterbox* y normaliza a [0, 1]) |
  | Aumento: flip | `fliplr=0.5`, `flipud=0.0` (los logos invertidos no son realistas) |
  | Aumento: escala, crop y traslación | `scale=0.5`, `translate=0.1`, `mosaic=1.0`, `close_mosaic=10` |
  | Aumento: color | `hsv_h=0.015`, `hsv_s=0.7`, `hsv_v=0.4` |
  | Entrenamiento | `epochs=100`, `patience=20`, `batch=16`, `seed=config.SPLIT_SEED`, `deterministic=True` |

  `train()` acepta *overrides* por argumento, que se combinan sobre `TRAIN_CONFIG`.
- **`train(data_yaml, base_model, **overrides) -> Path`:**
  - carga `MODELS_DIR / base_model`, que Ultralytics descarga si falta, igual que en el inicio rápido;
  - entrena en `runs/brands`, con `exist_ok=True` para que repetir no cree `brands2`, `brands3`…;
  - copia `weights/best.pt` a `models/brands.pt` (`config.BRAND_MODEL`).

  Ultralytics ya guarda en `runs/brands/args.yaml` la configuración exacta de cada entrenamiento.
- **`evaluate(weights, data_yaml, split="val") -> list[MetricsRow]`** llama a `model.val()` y convierte `metrics.box` en filas con precisión, recall, mAP@0.5 y mAP@0.5:0.95: una fila global y una por clase.
  - La conversión (`metrics_rows`) y el formateo de la tabla (`format_metrics`) son funciones puras y tienen tests.
  - Las clases que no aparecen en la partición salen con métricas a cero.
- **Notebook `02_training.py`.** Detecta Colab (`"google.colab" in sys.modules`) y, solo allí, hace la preparación con `subprocess`, en lugar de magias de shell, para que el `.py` siga siendo Python válido para ruff:
  - clona el repositorio en la rama indicada por `BRANCH` (por defecto `dev`);
  - instala el paquete con `pip install -e .`, que respeta el PyTorch con CUDA de Colab porque pip ignora el índice CPU de uv;
  - comprueba la GPU.

  Después, igual en Colab que en local:
  1. muestra `TRAIN_CONFIG`;
  2. prepara el dataset con `dataset.prepare()`;
  3. entrena y muestra la tabla de métricas;
  4. en Colab, descarga `brands.pt` con `google.colab.files`.
- **Comprobación local sin GPU:** un entrenamiento de humo con `epochs=1` y `fraction=0.1` valida todo el camino (entrenar, copiar pesos y evaluar) antes de ir a Colab. Sus métricas no cuentan para RNF-03.
- **Resultados:**
  - la persona ejecuta el notebook en Colab y aporta las métricas y `brands.pt`;
  - las métricas se documentan en ARCHITECTURE §8 («Calidad del modelo»), con la fecha, el modelo base y la revisión del dataset;
  - el README explica cómo obtener los pesos: entrenar en Colab y copiar `brands.pt` a `models/`.

## Risks / Trade-offs

- [Colab usa una versión de Python distinta de 3.12 y `pip install -e .` falla por `requires-python`] → El notebook muestra la versión. Si falla, se instala con `--ignore-requires-python`, porque el paquete no usa nada específico de 3.12, y se documenta.
- [nano no alcanza mAP@0.5 ≥ 0,6] → Se entrena small y se documenta el impacto en RNF-02. Si tampoco llega, se documenta la desviación, como permite la Issue.
- [Una sesión gratuita de Colab se corta durante el entrenamiento] → `patience=20` acorta el entrenamiento. Si se corta, Ultralytics permite `resume=True` desde `runs/brands/weights/last.pt`.
- [Los pesos no están versionados y solo los tiene quien entrena] → Se documenta cómo obtenerlos. Publicarlos como asset de release se propondrá en la fase de release.

## Open Questions

- ¿Se publican los pesos como asset de la release `v0.1.0` (ARCHITECTURE §4)? Se decidirá en la fase de release; no cambia esta historia.
