# Contratos

> Interfaces estables entre componentes o con sistemas externos: API, eventos, esquemas de datos y formatos de archivo. [ARCHITECTURE](../ARCHITECTURE.md) los enlaza.

## Reglas

- Un contrato se registra cuando otro componente depende de él. Mientras la interfaz solo cambia dentro de una historia, vive en el `design.md` del cambio.
- Las specs describen comportamiento y enlazan el contrato; no copian sus campos.
- Si existe un artefacto ejecutable (OpenAPI, JSON Schema…), ese archivo es la fuente de verdad. El `.md` lo enlaza y explica lo que el artefacto no cuenta.
- Versionado: un cambio compatible sube la versión MINOR. Uno incompatible sube la MAJOR y exige un ADR o una nota de migración.

## Formato

Archivo `nombre-del-contrato.md`, creado a partir de [`_template.md`](_template.md).

## Índice

| Contrato | Productor → consumidores | Versión | Estado |
|---|---|---|---|
| — | — | — | — |
