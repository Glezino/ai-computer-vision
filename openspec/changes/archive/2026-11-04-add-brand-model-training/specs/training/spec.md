## Purpose

Reentrenar un detector preentrenado con el dataset de las tres marcas para obtener unos pesos reutilizables, con una configuración documentada y reproducible y sus métricas de validación (RF-02, RNF-03).

## ADDED Requirements

### Requirement: Pesos reutilizables del modelo de marcas

El sistema SHALL reentrenar un detector preentrenado con el dataset de las tres marcas y dejar sus mejores pesos en `models/brands.pt`. Esos pesos MUST poder cargarse de nuevo para detectar Coca-Cola, Pepsi y Adidas sin volver a entrenar. Implementa RF-02.

#### Scenario: Entrenamiento completo

- **WHEN** se ejecuta el notebook de entrenamiento con el dataset preparado
- **THEN** existe `models/brands.pt` y, al cargarlo, el modelo tiene exactamente las clases Coca-Cola, Pepsi y Adidas

#### Scenario: Reutilización de los pesos

- **WHEN** se copian los pesos `brands.pt` obtenidos en Colab a `models/` de otro equipo
- **THEN** se pueden cargar y evaluar allí sin volver a entrenar

### Requirement: Métricas de validación global y por marca

El sistema SHALL informar, sobre la partición de validación, de la precisión, el recall, el mAP@0.5 y el mAP@0.5:0.95, tanto del conjunto de las tres marcas como de cada marca por separado. Implementa RF-02 y permite comprobar RNF-03.

#### Scenario: Tabla de métricas

- **WHEN** termina el entrenamiento, o se evalúan unos pesos existentes
- **THEN** se muestra una tabla con una fila por marca y una fila global, con precisión, recall, mAP@0.5 y mAP@0.5:0.95

### Requirement: Configuración de entrenamiento documentada y reproducible

El sistema SHALL definir en el código versionado el modelo base, el preprocesamiento (tamaño de imagen) y el aumento de datos (flip, escala/crop y color HSV), junto con las épocas y la semilla. El entrenamiento MUST usar esa configuración salvo que se sobrescriba de forma explícita. Implementa RF-02.

#### Scenario: Configuración visible

- **WHEN** se ejecuta el notebook de entrenamiento
- **THEN** muestra la configuración de preprocesamiento y aumento de datos con la que entrena

#### Scenario: Configuración sobrescrita

- **WHEN** se entrena indicando otro valor para un parámetro, por ejemplo menos épocas
- **THEN** se usa ese valor y el resto de la configuración se mantiene
