# Proyecto de Visualización de Datos de Energías Renovables y Combustibles  Fósiles

Este proyecto forma parte del trabajo final de la asignatura **Visualización, Procesamiento y Almacenamiento de Datos**.
El proyecto consiste en una aplicación interactiva para analizar y visualizar datos energéticos globales.

Desarrollado por **Carmen Linares Vázquez**, **María Millán Gordillo** y **Pablo Téllez López**.

---

## Descripción

El proyecto permite explorar la generación de energía renovable y no renovable a nivel global, así como comparar tendencias entre países y analizar la situación de la Unión Europea.

La aplicación incluye diferentes secciones para **Generación de energía por territorio**, **Comparativas** y**Energía en la Unión Europea**.
---

## Ejecución

Para ejecutar la aplicación, usar el siguiente comando:

```bash
streamlit run main.py
```

---

## Dataset

El conjunto de datos utilizado proviene de [Kaggle: Global Energy Generation & Capacity (IMF)](https://www.kaggle.com/datasets/pinuto/global-energy-generation-and-capacity-imf). Contiene información sobre:

- Generación de energía (GWh) por país.
- Tecnologías utilizadas (hidroeléctrica, combustibles fósiles, solar, eólica, etc.).
- Capacidad instalada por país y tecnología.
- Datos anuales desde el año 2000 hasta 2022.

---

## Estructura del Proyecto

El código se organiza en un archivo principal:

- **`main.py`**: Contiene la aplicación principal de Streamlit.

Otros archivos:

- **`requirements.txt`**: Lista de dependencias y librerías necesarias para ejecutar el proyecto.

---

## Funcionalidades

### 1. Generación de energía por territorio

- Selecciona un país y una tecnología específica para visualizar los datos.
- Elige un rango de años para analizar tendencias.
- Representa los datos en gráficos de barras.

### 2. Comparativas

- Compara países seleccionados.
- Analiza tipos de energía renovable, no renovable o el total.
- Genera gráficos de líneas con los datos seleccionados.

### 3. Energía en la Unión Europea

- Filtra datos por países de la Unión Europea.
- Visualiza la distribución porcentual entre los países.
- Analiza tecnologías específicas o el total.

---

## Autores

- **Carmen Linares Vázquez**
- **María Millán Gordillo**
- **Pablo Téllez López**
