## 1. Vista previa web (TDD)

- [ ] 1.1 Escribir en `tests/test_detection.py` los tests de `web_preview` (vídeo ancho reducido a 640×360 con los mismos fotogramas y fps, vídeo estrecho sin cambios, ruta por defecto `.webm` junto al vídeo y error con archivo no válido); verificar que fallan porque `web_preview` no existe
- [ ] 1.2 Implementar `web_preview` en `src/logo_detector/detection.py` y `VIDEOS_DIR` en `config.py`; verificar con `make test` y `make lint`

## 2. Notebook de demo

- [ ] 2.1 Escribir `notebooks/03_demo.py` (parámetros, imagen, vídeo con vista previa y cuadrícula de fotogramas, tabla del informe y JSON); verificar que `make notebooks` genera `03_demo.ipynb`
- [ ] 2.2 Preparar los vídeos de ejemplo en `data/videos/` (el de la persona y el de 1 minuto de #13) y ejecutar el notebook de punta a punta en local con `jupyter nbconvert --execute`; verificar que no hay errores, que se ven la imagen, el vídeo, los fotogramas y la tabla, y que el JSON queda en `outputs/`
- [ ] 2.3 Ejecutar el notebook sin el vídeo indicado y verificar que el error indica la ruta
- [ ] 2.4 Con Docker Desktop arrancado, `make docker-build` y ejecutar el notebook en el contenedor; verificar que funciona, incluida la vista previa WebM (si no se puede, anotarlo en el PR)

## 3. Documentación

- [ ] 3.1 Actualizar el README (demo, vídeos de ejemplo, detección en una imagen propia y estado) y ARCHITECTURE §3, §5, §6 y §8; verificar que los comandos del README funcionan tal como están escritos
