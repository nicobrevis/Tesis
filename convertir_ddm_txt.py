import numpy as np
import scipy.sparse
import pandas as pd # Usaremos pandas para guardar rápido en txt/csv

# --- CONFIGURACIÓN ---
# 1. Nombre del archivo .npz de la ROI que quieres convertir
archivo_entrada = 'ddm_GTV-1.npz'

# 2. Define el punto de corte de tus beamlets (según tus logs anteriores)
# Beam 1 va de 0 a 4587. Beam 2 empieza en 4588.
limite_beam_1 = 4588 

# ---------------------

print(f"Cargando {archivo_entrada}...")
try:
    # Cargar la matriz
    ddm = scipy.sparse.load_npz(archivo_entrada)
    
    # Convertir a formato de coordenadas (COO) que es ideal para listas:
    # (fila, columna, valor) -> (voxel, beamlet, intensidad)
    ddm_coo = ddm.tocoo()
    
    print(f"Matriz cargada. Total de elementos no nulos: {ddm_coo.nnz}")
    
    # Crear un DataFrame temporal para facilitar el filtrado
    df = pd.DataFrame({
        'voxel': ddm_coo.row,
        'beamlet': ddm_coo.col,
        'intensidad': ddm_coo.data
    })
    
    # --- SEPARAR POR ÁNGULOS ---
    
    # Ángulo 1: Beamlets menores al límite
    print(f"Filtrando Ángulo 1 (Beamlets 0 a {limite_beam_1 - 1})...")
    df_angulo1 = df[df['beamlet'] < limite_beam_1]
    
    nombre_salida_1 = f"{archivo_entrada.replace('.npz', '')}_Angulo1.txt"
    # Guardar en TXT: Separador ';', sin índice, con encabezados
    df_angulo1.to_csv(nombre_salida_1, sep=';', index=False)
    print(f"--> Guardado: {nombre_salida_1} ({len(df_angulo1)} líneas)")

    # Ángulo 2: Beamlets mayores o iguales al límite
    print(f"Filtrando Ángulo 2 (Beamlets {limite_beam_1} en adelante)...")
    df_angulo2 = df[df['beamlet'] >= limite_beam_1]
    
    nombre_salida_2 = f"{archivo_entrada.replace('.npz', '')}_Angulo2.txt"
    df_angulo2.to_csv(nombre_salida_2, sep=';', index=False)
    print(f"--> Guardado: {nombre_salida_2} ({len(df_angulo2)} líneas)")
    
    print("\n¡Conversión completada!")

except FileNotFoundError:
    print("Error: No se encontró el archivo .npz. Asegúrate de estar en la carpeta correcta.")
except Exception as e:
    print(f"Ocurrió un error: {e}")