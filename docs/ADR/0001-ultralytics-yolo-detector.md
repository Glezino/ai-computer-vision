# ADR-0001: Ultralytics YOLO como detector, entrenado en Google Colab

- **Estado:** Aceptado
- **Fecha:** 2026-11-03
- **Decisores:** Victor Gonzalez
- **Relacionado:** RF-02, RF-03, RF-04, RNF-02, RNF-03

## Contexto

Hay que reentrenar un detector preentrenado para tres marcas con unas 70 imágenes por marca, mostrar la confianza de cada detección y procesar vídeo, todo en menos de un día. El equipo de desarrollo no tiene GPU.

## Decisión

- Se usa Ultralytics YOLO, variante nano o small preentrenada en COCO, reentrenada por *transfer learning*. La versión exacta del modelo se fija en la historia de entrenamiento.
- El preprocesamiento (redimensionado y normalización) y el aumento de datos (flip, crop/escala, color jitter HSV y mosaic) se configuran con los hiperparámetros de Ultralytics.
- El entrenamiento se ejecuta en Google Colab con GPU gratuita; la inferencia se hace en CPU, en local o en Docker.

## Alternativas consideradas

- **Faster R-CNN (torchvision):** más lento en vídeo y requiere escribir el bucle de entrenamiento y el aumento de datos.
- **Detectron2:** instalación delicada en Windows y más configuración.
- **SSD:** menos preciso con objetos pequeños, como los logos lejanos.
- **Entrenar en CPU local:** demasiado lento para el plazo.

## Consecuencias

- Entrenamiento, métricas (mAP) y aumento de datos listos con muy poco código; resultados con confianza incluida.
- Inferencia en CPU suficiente para vídeos cortos (RNF-02).
- Dependencia de Colab para entrenar: los pesos se copian a mano a `models/`.
- La licencia AGPL-3.0 de Ultralytics es compatible con un proyecto pedagógico abierto.
