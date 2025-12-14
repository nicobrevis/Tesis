# ⚛️ OpenTPS DDM Exporter & Processor for IMPT

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenTPS](https://img.shields.io/badge/Software-OpenTPS-green)
![Status](https://img.shields.io/badge/Status-Research-orange)

Herramientas de ingeniería inversa y procesamiento de datos para habilitar la **Optimización Robusta** en Terapia de Protones de Intensidad Modulada (IMPT) utilizando [OpenTPS](https://opentps.org/).

Este proyecto resuelve la limitación de la "Caja Negra" de OpenTPS, permitiendo la extracción de la **Matriz de Deposición de Dosis (DDM)** directamente desde la memoria, filtrándola por regiones de interés (ROI) y preparándola para solvers de optimización externos.
Los archivos del paciente se encuentran en https://www.mediafire.com/file/ho5pmana3ax99ra/Script.rar/file

---

## 🚀 Funcionalidades Clave

* **🔓 Extracción de DDM:** "Hook" en el código fuente de OpenTPS para exportar la matriz de influencia $D$ antes de que sea desechada por el sistema.
* **🎯 Filtrado Espacial (ROI):** Algoritmo de voxelización que utiliza contornos DICOM para extraer solo los datos del tumor (GTV), reduciendo el peso de los archivos en un **~99%**.
* **🛡️ Manejo de Robustez:** Detección automática de escenarios de incertidumbre. Si la simulación incluye múltiples escenarios, el script extrae quirúrgicamente el escenario nominal.
* **📐 Separación Angular:** Conversión de datos a formato `.txt` dividiendo los beamlets por ángulo de incidencia (Haces), listo para optimización matemática.

---

## 🛠️ Guía de Instalación y Modificación

Para utilizar estas herramientas, es necesario realizar una pequeña intervención en el código fuente de OpenTPS instalado en tu entorno.

### Paso 1: Localizar el Motor de Cálculo
Navega a la carpeta de instalación de tu entorno Python/Conda y busca el archivo:
`.../site-packages/opentps/core/processing/doseCalculation/mcsquareDoseCalculator.py`

### Paso 2: Inyectar el Código de Exportación
Abre el archivo, busca la función `computeBeamlets` y añade el siguiente bloque justo antes de la línea `return beamletDose`:

```python
    # --- INICIO MODIFICACIÓN: EXTRACCIÓN AUTOMÁTICA DDM ---
    try:
        from opentps.core.io.serializedObjectIO import saveBeamlets
        import logging
        logger = logging.getLogger(__name__)

        # CAMBIA ESTA RUTA A TU CARPETA DE PREFERENCIA
        ruta_salida = 'C:/Script/ddm_exportada_auto.blm'

        saveBeamlets(beamletDose, ruta_salida)
        logger.info(f"DDM interceptada y guardada en: {ruta_salida}")
    except Exception as e:
        logger.error(f"Error crítico exportando DDM: {e}")
    # --- FIN MODIFICACIÓN ---

    return beamletDose  # Línea original del archivo
