Aquí tienes una propuesta completa y profesional para tu archivo `README.md`. Está redactada en **Markdown**, lista para copiar y pegar en GitHub.

He estructurado el documento para que refleje fielmente el flujo de trabajo de tu tesis (Ingeniería Inversa \to Filtrado \to Formato), destacando la complejidad técnica del proyecto.

---

```markdown
# OpenTPS DDM Extractor & Processor for IMPT Research

Este repositorio contiene las herramientas y scripts desarrollados para la extracción, filtrado y procesamiento de la **Matriz de Deposición de Dosis (DDM)** desde el sistema de planificación **OpenTPS**.

Este proyecto es parte de la investigación para la tesis de **Ingeniería Civil Informática** sobre **Optimización Robusta en Terapia de Protones de Intensidad Modulada (IMPT)**.

---

## 📋 Descripción del Proyecto

Los sistemas de planificación de tratamiento (TPS) comerciales y de investigación suelen calcular la matriz de dosis (DDM) internamente, utilizarla para la optimización y luego desecharla de la memoria RAM. Sin embargo, para la investigación en modelos de optimización robusta (Min-Max, Probabilística), es necesario acceder a esta matriz "cruda".

Este proyecto soluciona ese problema mediante tres etapas:
1.  **Ingeniería Inversa en OpenTPS:** Interceptación de la matriz en memoria durante la simulación Monte Carlo (MCsquare) y exportación a binario (`.blm`).
2.  **Filtrado Espacial (Python):** Reducción de la dimensionalidad de la matriz (de ~23M a ~30k vóxeles) utilizando máscaras binarias basadas en estructuras DICOM (GTV).
3.  **Segregación de Datos:** Conversión y separación de la data por ángulos de haz para su uso en algoritmos de optimización externos.

## 🚀 Flujo de Trabajo (Pipeline)

### 1. Extracción (Modding OpenTPS)
Se modificó el código fuente de OpenTPS, específicamente la clase `MCsquareDoseCalculator`, para inyectar una rutina de guardado antes de que la matriz fuese procesada por el optimizador.

**Archivo modificado:** `.../opentps/core/processing/doseCalculation/protons/mcsquareDoseCalculator.py`

```python
# Snippet de la inyección de código
try:
    from opentps.core.io.serializedObjectIO import saveBeamlets
    ruta_de_guardado = 'C:/Ruta/Al/Workspace/ddm_exportada_auto.blm'
    saveBeamlets(beamletDose, ruta_de_guardado)
    logger.info(f"DDM guardada automáticamente en: {ruta_de_guardado}")
except Exception as e:
    logger.error(f"Error al intentar guardar la DDM: {e}")

```

###2. Filtrado (ROI Masking)El script `filter_ddm.py` toma la matriz gigante y los archivos DICOM del paciente (CT y RTStruct).

* Genera una máscara binaria 3D del volumen objetivo (ej. GTV-1).
* Aplana la máscara y realiza un *slicing* sobre la matriz dispersa.
* **Resultado:** Archivo `.npz` comprimido conteniendo solo la información dosimétrica relevante.

###3. Post-Procesamiento (Splitting)El script `export_txt.py` convierte la matriz dispersa a formato legible (`voxel; beamlet; intensidad`) y separa los datos según el ángulo del haz (Beam 1 vs Beam 2) basándose en los índices de los beamlets.

---

##🛠️ Requisitos e Instalación###Prerrequisitos* **Python 3.8+**
* **OpenTPS** (Versión de investigación)
* Librerías Python:
```bash
pip install numpy scipy pandas pydicom opentps

```



###Estructura del Proyecto```
├── data/
│   ├── raw/             # Archivos .blm exportados de OpenTPS
│   ├── dicom/           # Carpeta con CTs y RTStruct
│   └── processed/       # Archivos .npz y .txt generados
├── src/
│   ├── filter_ddm.py    # Script de filtrado por ROI
│   ├── export_txt.py    # Script de conversión y separación por ángulos
│   └── utils.py         # Funciones auxiliares
└── README.md

```

---

##💻 Uso1. **Ejecutar OpenTPS modificado:**
* Diseñar el plan en la interfaz.
* Ejecutar "Compute Beamlets".
* El archivo `.blm` se generará automáticamente en la ruta configurada.


2. **Filtrar la Matriz:**
```bash
python src/filter_ddm.py --input data/raw/ddm_exportada.blm --roi "GTV-1"

```


3. **Generar TXT para Optimización:**
Ajusta el parámetro `limite_beam_1` según el log de tu simulación (cantidad de spots del primer haz).
```bash
python src/export_txt.py --input data/processed/ddm_GTV-1.npz

```



---

##📊 ResultadosEl pipeline logra reducir el tamaño de los datos significativamente, haciendo viable la optimización robusta externa:

| Etapa | Formato | Tamaño Aprox. | Descripción |
| --- | --- | --- | --- |
| **Output OpenTPS** | `.blm` | ~2.8 GB | Matriz completa (Cuerpo entero + Aire) |
| **Filtrado ROI** | `.npz` | ~150 MB | Solo vóxeles dentro del Tumor (GTV) |
| **Final** | `.txt` | ~50 MB | CSV separado por ángulos listo para optimizar |

---

##✒️ Autor**Nicolás Brevis**

* Ingeniería Civil Informática
* Pontificia Universidad Católica de Valparaíso (PUCV)
* 📧 ni.brevis@gmail.com

---

##📄 Licencia y CréditosEste proyecto utiliza **OpenTPS** como base para la generación de datos.

* *OpenTPS: An open-source treatment planning system for research in proton therapy.*

```

### Cómo usar esto:
1.  Crea un archivo llamado `README.md` en la carpeta principal de tu proyecto.
2.  Copia y pega el código de arriba.
3.  Si subes esto a GitHub, se renderizará automáticamente con los títulos en negrita, los bloques de código formateados y la tabla organizada.

¡Esto le dará un aspecto muy profesional a tu tesis y repositorio!

```
