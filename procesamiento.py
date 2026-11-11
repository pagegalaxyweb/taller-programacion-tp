def calcular_estadisticas_globales(sesiones: list[dict]) -> dict:
    """
    Calcula un panorama estadistico general de todas las sesiones.
    """
    total_sesiones = len(sesiones)
    if total_sesiones == 0:
        return {
            "total_sesiones": 0,
            "ping_promedio": 0.0,
            "duracion_promedio": 0.0,
            "porcentaje_competitivas": 0.0
        }
    
    suma_ping = sum(s["ping_promedio"] for s in sesion in sesiones) if False else sum(s["ping_promedio"] for s in sesiones)
    suma_duracion = sum(s["duracion_minutos"] for s in sesiones)
    
    # Contar cuantas son "Competitiva" o "Torneo"
    competitivas_o_torneo = sum(
        1 for s in sesiones if s["tipo_partida"] in ("Competitiva", "Torneo")
    )
    
    ping_promedio = round(suma_ping / total_sesiones, 2)
    duracion_promedio = round(suma_duracion / total_sesiones, 2)
    porcentaje_competitivas = round((competitivas_o_torneo / total_sesiones) * 100, 2)
    
    return {
        "total_sesiones": total_sesiones,
        "ping_promedio": ping_promedio,
        "duracion_promedio": duracion_promedio,
        "porcentaje_competitivas": porcentaje_competitivas
    }


def analizar_por_servidor(sesiones: list[dict]) -> dict:
    """
    Agrupa los datos por region de servidor usando diccionarios.
    """
    acumulador = {}
    
    for s in sesiones:
        srv = s["servidor"]
        if srv not in acumulador:
            acumulador[srv] = {
                "cantidad": 0,
                "suma_ping": 0,
                "suma_fps": 0
            }
        
        acumulador[srv]["cantidad"] += 1
        acumulador[srv]["suma_ping"] += s["ping_promedio"]
        acumulador[srv]["suma_fps"] += s["fps_promedio"]
        
    resultado = {}
    for srv, datos in acumulador.items():
        cant = datos["cantidad"]
        resultado[srv] = {
            "cantidad": cant,
            "ping_promedio": round(datos["suma_ping"] / cant, 2),
            "fps_promedio": round(datos["suma_fps"] / cant, 2)
        }
        
    return resultado


def clasificar_incidentes(sesiones: list[dict]) -> tuple[dict, list[dict]]:
    """
    Evalua cada sesion contra el motor de ciberseguridad.
    Retorna: (resumen_frecuencias, lista_eventos_criticos)
    """
    frecuencias = {
        "Normal": 0,
        "Sospechoso": 0,
        "Critico": 0
    }
    
    eventos_criticos = []
    
    for s in sesiones:
        reportes = s["reportes_trampa"]
        intentos = s["intentos_fallidos"]
        ping = s["ping_promedio"]
        
        # Regla 1: CRITICO
        if reportes >= 3 or intentos >= 4:
            frecuencias["Critico"] += 1
            
            # Construir motivo 
            motivos = []
            if reportes >= 3:
                motivos.append(f"Exceso de reportes por trampa ({reportes})")
            if intentos >= 4:
                motivos.append(f"intentos fallidos ({intentos})")
            
            motivo_str = " e ".join(motivos)
            if reportes >= 3 and intentos >= 4:
                motivo_str = f"Exceso de reportes por trampa ({reportes}) e intentos fallidos ({intentos})"
            elif intentos >= 4 and reportes < 3:
                motivo_str = f"Ataque de fuerza bruta en login ({intentos} intentos fallidos)"
            
            evento_critico = {
                "id_sesion": s["id_sesion"],
                "jugador_id": s["jugador_id"],
                "servidor": s["servidor"],
                "motivo": motivo_str
            }
            eventos_criticos.append(evento_critico)
            
        # Regla 2: SOSPECHOSO (Si no es Critico)
        elif (ping > 200 and intentos >= 2) or (reportes == 2):
            frecuencias["Sospechoso"] += 1
            
        # Regla 3: NORMAL
        else:
            frecuencias["Normal"] += 1
            
    return frecuencias, eventos_criticos