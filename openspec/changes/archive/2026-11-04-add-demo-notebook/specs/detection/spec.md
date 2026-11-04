## ADDED Requirements

### Requirement: Vista previa web del vídeo anotado

El sistema SHALL generar, a partir de un vídeo anotado, una vista previa en un formato que los navegadores reproducen (WebM), con los mismos fotogramas y fotogramas por segundo, y reducida a un ancho máximo configurable sin cambiar la proporción; un vídeo más estrecho que ese ancho conserva su tamaño. Por defecto se guarda junto al vídeo anotado con el mismo nombre y extensión `.webm`. Implementa RF-04 y RF-06.

#### Scenario: Vídeo ancho

- **WHEN** se genera la vista previa de un vídeo de 50 fotogramas a 25 fps y 1280×720 con un ancho máximo de 640
- **THEN** se crea un `.webm` de 50 fotogramas a 25 fps y 640×360

#### Scenario: Vídeo estrecho

- **WHEN** se genera la vista previa de un vídeo de 320×240 con un ancho máximo de 640
- **THEN** el `.webm` mantiene 320×240

#### Scenario: Vídeo no válido

- **WHEN** se genera la vista previa de un archivo que no es un vídeo
- **THEN** se produce un error que indica la ruta
