## Context

- `detection` ofrece `load_model`, `detect_image` y `analyze_video` (#12, #13); `report` ofrece `build_report` y `save_report` (#11). Las detecciones por fotograma de `analyze_video` sirven tal cual a `build_report`.
- El vídeo anotado se escribe con `mp4v`, que el navegador no reproduce. Probado en este equipo: `opencv-python` 5.0 escribe y relee WebM con VP8 (`VP80`) y VP9 (`VP90`); H.264 (`avc1`) no funciona sin la librería openh264.
- `pandas` no está instalado; `IPython.display` sí (Jupyter).
- Los notebooks existentes (`01_quickstart`, `02_training`) son scripts jupytext en formato percent con celdas markdown en español.
- `data/` y `outputs/` están en `.gitignore` y en `.dockerignore`; en Docker el repositorio se monta en `/app`, así que también ven `data/videos/` y `outputs/`.

Motivación en `proposal.md`; comportamiento en `specs/`.

## Goals / Non-Goals

**Goals:**

- Un notebook que se ejecuta de principio a fin sin tocar código, salvo la celda de parámetros.
- Ver el vídeo anotado dentro del notebook, en local y en Docker, sin dependencias nuevas.

**Non-Goals:**

- Interfaz interactiva (widgets, subir archivos): la celda de parámetros basta para la demo.
- Recodificar el `.mp4` anotado a H.264: requeriría ffmpeg u openh264.

## Decisions

- **Vista previa web:** `detection.web_preview(video, output=None, max_width=960) -> Path`. Lee el vídeo anotado con OpenCV, reduce cada fotograma con `cv2.INTER_AREA` si es más ancho que `max_width` (alto proporcional y par) y lo escribe en `.webm` con `VP80`. VP8 frente a VP9: ambos funcionan y los reproducen todos los navegadores; VP8 codifica más rápido, que es lo que importa en una demo en vivo. Se descarta escribir directamente el vídeo anotado en WebM: cambiaría el resultado de #13 (`.mp4`, resolución original) por una necesidad solo de presentación. Mismos errores que `analyze_video` (ruta en el mensaje).
- **Mostrar el vídeo:** `IPython.display.Video` con la ruta relativa al notebook (`../outputs/<vídeo>_annotated.webm`), sin incrustarlo en base64 para no inflar el `.ipynb`; JupyterLab sirve el archivo. También se muestra una cuadrícula de 6 fotogramas con detecciones, elegidos a intervalos regulares entre los que tienen alguna, por si el navegador no reprodujera el vídeo.
- **Tabla del informe:** `IPython.display.Markdown` con una tabla (marca, detectada, segundos con 1 decimal y % con 1 decimal), más duración y umbral. Sin `pandas`: no hace falta una dependencia para una tabla de tres filas. El redondeo es solo de presentación, como decidió #11.
- **Parámetros:** primera celda de código con `IMAGE`, `VIDEO` y `THRESHOLD = config.CONFIDENCE_THRESHOLD`. `IMAGE` por defecto es `60524367.jpg` del test del dataset (la del test de integración de #12); `VIDEO`, `config.VIDEOS_DIR / "demo.mp4"`.
- **Vídeos de ejemplo:** `config.VIDEOS_DIR = DATA_DIR / "videos"`, ya ignorado al estar en `data/`. La persona deja ahí sus vídeos; para la prueba se usa el de su chaqueta y el de 1 minuto montado con imágenes del dataset en #13. No se versionan ni se publican (privacidad y tamaño).
- **Funciones del notebook:** solo orquesta y muestra (ARCHITECTURE §1). La cuadrícula de fotogramas y la tabla son unas pocas líneas de presentación y se quedan en el notebook.
- **Tests:** unitarios de `web_preview` con un vídeo sintético (fotogramas, fps, tamaño reducido y conservado, error con archivo no válido). El notebook se prueba ejecutándolo de punta a punta con `jupyter nbconvert --to notebook --execute` en local y, con Docker Desktop arrancado, dentro del contenedor; no se automatiza en el CI porque necesita pesos y vídeos no versionados.
- **README:** sección «Demo» (pesos, `data/videos/`, `make notebooks`, abrir `03_demo`, parámetros y salidas), un apartado breve para detectar en una imagen propia con `detection.detect_image`, y la sección «Estado» con lo que cubre el Hito 1. Docker: los mismos pasos con `make docker-run`.

## Risks / Trade-offs

- [El `opencv-python` de Linux en Docker podría no traer VP8] → se comprueba en la prueba en Docker; si falla, `web_preview` da un error claro y el notebook sigue mostrando la cuadrícula de fotogramas.
- [Docker Desktop no está arrancado ahora] → la prueba en Docker necesita que la persona lo arranque; si no es posible antes de la entrega, se indica en el PR como no comprobado.
- [Vídeos largos generan una vista previa pesada] → `max_width=960` y VP8 la mantienen en pocos MB por minuto.
