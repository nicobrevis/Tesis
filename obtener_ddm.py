# INICIO DEL CÓDIGO AÑADIDO PARA GUARDAR DDM 
    try:
        # Importar la función de guardado
        from opentps.core.io.serializedObjectIO import saveBeamlets
        # Importar el logger para ver mensajes en la consola
        import logging
        logger = logging.getLogger(__name__)

        # Ruta de guardado (la guardamos en C:\Script donde sabemos que funciona)
        ruta_de_guardado = 'C:/Script/ddm_exportada_auto.blm'

        # Guardar el objeto de beamlets (que se llama 'beamletDose' en esta función)
        saveBeamlets(beamletDose, ruta_de_guardado)

        logger.info(f"DDM guardada automáticamente en: {ruta_de_guardado}")
    except Exception as e:
        logger.error(f"Error al intentar guardar la DDM automáticamente: {e}")
    # FIN DEL CÓDIGO AÑADIDO
    # Esta línea ya existe en el archivo
    return beamletDose