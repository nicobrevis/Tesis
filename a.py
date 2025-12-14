
import numpy as np
import scipy.sparse
import os
from opentps.core.io.serializedObjectIO import loadBeamlets

from opentps.core.io.dicomIO import readDicomCT, readDicomStruct
from scipy.sparse import save_npz

print("Librerías importadas correctamente...")


# Ruta al archivo DDM 
ruta_archivo_ddm = 'ddm_exportada_auto.blm'

# Ruta a la CARPETA que contiene los archivos CT 
ruta_carpeta_ct = 'bTESTxd' 
# Ruta al ARCHIVO .dcm de las estructuras 
ruta_archivo_rtstruct = '2.000000-NA-99068/1-1.dcm'

lista_de_archivos_dcm = []

try:
    for nombre_archivo in os.listdir(ruta_carpeta_ct):
        
        if nombre_archivo.lower().endswith('.dcm'):
            
            ruta_completa = os.path.join(ruta_carpeta_ct, nombre_archivo)
            
            lista_de_archivos_dcm.append(ruta_completa)

    # Verificamos si encontramos archivos
    if not lista_de_archivos_dcm:
        print(f"No se encontraron archivos .dcm en: {ruta_carpeta_ct}")
    else:
        print(f"Se encontraron {len(lista_de_archivos_dcm)} archivos .dcm. Procesando...")
    
        imagen_ct_resultante = readDicomCT(lista_de_archivos_dcm) 
        
        print("¡Proceso completado exitosamente!")
        # print(imagen_ct_resultante) # Puedes imprimir el resultado

except FileNotFoundError:
    print(f"La carpeta especificada no existe: {ruta_carpeta_ct}")
except NotADirectoryError:
    print(f"La ruta especificada no es una carpeta: {ruta_carpeta_ct}")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")

# Cargar los datos
try:
    beamlets_cargados = loadBeamlets(ruta_archivo_ddm)
    matriz_ddm_completa = beamlets_cargados.toSparseMatrix()
    print(f"DDM completa cargada. Dimensiones: {matriz_ddm_completa.shape}")

    # Cargar la imagen CT desde su carpeta
    ct_image = readDicomCT(lista_de_archivos_dcm)
    print(f"Imagen CT '{ct_image.seriesInstanceUID}' cargada.")
    
    # Cargar las estructuras (ROIs) desde su archivo
    rt_struct = readDicomStruct(ruta_archivo_rtstruct)
    print(f"Archivo de estructuras cargado.")

except Exception as e:
    print(f"Error cargando archivos: {e}")


# Extraer la ROI del Paciente
if 'rt_struct' in locals():
    
    nombre_roi_objetivo = 'GTV-1'
    roi_objetivo = None

    for roi in rt_struct.contours:
        if roi.name == nombre_roi_objetivo:
            roi_objetivo = roi
            break

    if roi_objetivo is None:
        print(f"Error: No se encontró la ROI con el nombre '{nombre_roi_objetivo}'")
        print("Nombres de ROIs disponibles:")
        for roi in rt_struct.contours:
            print(f"- {roi.name}")
    else:
        print(f"ROI '{roi_objetivo.name}' encontrada.")

        # Implementar la Solución de Eliot 
        
        print("Creando máscara 3D usando la CT como plantilla...")
        mascara_3d_objeto = roi_objetivo.getBinaryMask(origin=ct_image.origin, 
                                               gridSize=ct_image.gridSize, 
                                               spacing=ct_image.spacing)
        
        print("Aplanando la máscara...")
        mascara_aplanada = mascara_3d_objeto.imageArray.flatten().astype(bool)
        
# ... (El código anterior sigue igual) ...
        
        print(f"Máscara aplanada creada con {mascara_aplanada.size} elementos.")

        # --- 6. Validar Dimensiones y Aplicar el Filtro (CORREGIDO) ---
        
        n_voxeles_ct = mascara_aplanada.shape[0]
        n_filas_ddm = matriz_ddm_completa.shape[0]

        print(f"\nVerificando dimensiones:")
        print(f" -> Vóxeles en CT (Máscara): {n_voxeles_ct}")
        print(f" -> Filas en DDM: {n_filas_ddm}")

        # Caso 1: Coincidencia Perfecta
        if n_filas_ddm == n_voxeles_ct:
            print("Dimensiones coinciden. Filtrando...")
            ddm_roi = matriz_ddm_completa[mascara_aplanada, :]
            
            # Guardar
            ruta_salida_ddm_roi = 'ddm_GTV-1.npz'
            save_npz(ruta_salida_ddm_roi, ddm_roi)
            print(f"\n¡DDM de la ROI guardada con éxito en: {ruta_salida_ddm_roi}!")

        # Caso 2: La DDM es múltiplo de la Máscara (Tiene múltiples escenarios)
        elif n_filas_ddm > n_voxeles_ct and n_filas_ddm % n_voxeles_ct == 0:
            
            cantidad_escenarios = n_filas_ddm // n_voxeles_ct
            print(f"\n¡ATENCIÓN! La DDM es {cantidad_escenarios} veces más grande que la CT.")
            print("Esto significa que la DDM contiene escenarios de robustez apilados.")
            
            print("Procediendo a extraer solo el PRIMER ESCENARIO (Nominal)...")
            
            # Cortamos la DDM para quedarnos solo con el primer bloque
            ddm_nominal = matriz_ddm_completa[:n_voxeles_ct, :]
            
            # Ahora sí aplicamos la máscara
            ddm_roi = ddm_nominal[mascara_aplanada, :]
            
            print(f"Dimensiones finales extraídas: {ddm_roi.shape}")
            
            # Guardar
            ruta_salida_ddm_roi = 'ddm_GTV-1.npz'
            save_npz(ruta_salida_ddm_roi, ddm_roi)
            print(f"\n¡DDM (Nominal) de la ROI guardada con éxito en: {ruta_salida_ddm_roi}!")

        # Caso 3: Error Real
        else:
            print("\n--- ERROR DE DIMENSIONES ---")
            print(f"El tamaño de la máscara ({n_voxeles_ct}) no coincide con la DDM ({n_filas_ddm}) y no es un múltiplo exacto.")
            print("Revisa si el CT cargado corresponde exactamente a la simulación.")