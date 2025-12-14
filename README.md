# ⚛️ OpenTPS DDM Exporter & Processor

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenTPS](https://img.shields.io/badge/Software-OpenTPS-green)
![Status](https://img.shields.io/badge/Status-Research-orange)

Este repositorio contiene el conjunto de herramientas desarrolladas para **extraer, procesar y optimizar** la Matriz de Deposición de Dosis (DDM) desde el software de planificación de radioterapia [OpenTPS](https://opentps.org/).

El objetivo principal de este proyecto es habilitar la investigación en **Optimización Robusta** permitiendo la exportación de la matriz de influencia $D$, una funcionalidad no disponible nativamente en la interfaz gráfica del software.

---

## 🚀 Funcionalidades Principales

* **🔓 Extracción de Caja Negra:** Modificación del código fuente ("Hook") para interceptar la DDM desde la memoria RAM antes de su eliminación.
* **🎯 Filtrado Espacial Inteligente:** Algoritmo que utiliza máscaras binarias basadas en contornos DICOM para extraer solo los vóxeles del tumor (GTV), reduciendo el tamaño de los datos en un **~99%**.
* **🛡️ Detección de Escenarios Robustos:** El script detecta automáticamente si la simulación incluye múltiples escenarios de incertidumbre y extrae quirúrgicamente el escenario nominal.
* **scikit-sparse & NumPy:** Conversión eficiente a formatos `.npz` y `.txt` separados por ángulos de incidencia.

---

## 🛠️ Instalación y Configuración

### Prerrequisitos
* Entorno conda con **OpenTPS** instalado.
* Librerías Python: `numpy`, `scipy`, `pydicom`.

### Paso 1: Intervención del Código Fuente (El "Hook")
Para exportar la matriz, se debe inyectar un fragmento de código en el motor de cálculo de OpenTPS.

1.  Navega a la ruta de instalación de la librería OpenTPS:
    `.../site-packages/opentps/core/processing/doseCalculation/mcsquareDoseCalculator.py`
2.  Localiza la función: `def computeBeamlets(...)`
3.  Inserta el siguiente código al final de la función, justo **antes** del `return`:

```python
    # --- INICIO MODIFICACIÓN: EXTRACCIÓN AUTOMÁTICA ---
    try:
        from opentps.core.io.serializedObjectIO import saveBeamlets
        import logging
        logger = logging.getLogger(__name__)

        # CAMBIAR ESTA RUTA A TU CARPETA DE TRABAJO
        ruta_exportacion = 'C:/Script/ddm_exportada_auto.blm'

        saveBeamlets(beamletDose, ruta_exportacion)
        logger.info(f"DDM interceptada y guardada en: {ruta_exportacion}")
    except Exception as e:
        logger.error(f"Error crítico exportando DDM: {e}")
    # --- FIN MODIFICACIÓN ---

    return beamletDose  # Código original
