import csv
import os

def cargar_telemetria(ruta_archivo: str) -> list[dict]:
    """
    Lee el archivo CSV de telemetria, valida su existencia y contenido,
    realiza el casteo explicito de tipos y devuelve una lista de diccionarios. 
    """
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo '{ruta_archivo}' no fue encontrado.")
    
    sesiones = []
    
    with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        
        filas = list(lector)
        if not filas:
            raise ValueError(f"El archivo '{ruta_archivo}' esta vacio.")
        
        for fila in filas:
            sesion = {
                "id_sesion": int(fila["id_sesion"]),
                "servidor": fila["servidor"].strip(),
                "jugador_id": fila["jugador_id"].strip(),
                "tipo_partida": fila["tipo_partida"].strip(),
                "ping_promedio": int(fila["ping_promedio"]),
                "fps_promedio": int(fila["fps_promedio"]),
                "duracion_minutos": float(fila["duracion_minutos"]),
                "intentos_fallidos": int(fila["intentos_fallidos"]),
                "reportes_trampa": int(fila["reportes_trampa"])
            }
            sesiones.append(sesion)
            
    return sesiones