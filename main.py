from datetime import datetime
from carga import cargar_telemetria
from procesamiento import (
    calcular_estadisticas_globales,
    analizar_por_servidor,
    clasificar_incidentes
)

def exportar_reporte(sesiones: list[dict], ruta_salida: str = "reporte_gamesec.txt"):
    """
    Genera y exporta el reporte en un archivo de texto.
    """
    # Calcular todos los datos necesarios
    globales = calcular_estadisticas_globales(sesiones)
    por_servidor = analizar_por_servidor(sesiones)
    frecuencias, eventos_criticos = clasificar_incidentes(sesiones)
    
    total = globales["total_sesiones"]
    
    # Calcular porcentajes de seguridad
    pct_normal = round((frecuencias["Normal"] / total) * 100, 2) if total > 0 else 0
    pct_sospechoso = round((frecuencias["Sospechoso"] / total) * 100, 2) if total > 0 else 0
    pct_critico = round((frecuencias["Critico"] / total) * 100, 2) if total > 0 else 0
    
    fecha_actual = datetime.now().strftime("%D/%m/%Y")
    
    # Construir el contenido del reporte
    lineas = []
    lineas.append("REPORTE DE AUDITORIA Y TELEMETRIA - GAMESEC")
    lineas.append("=============================================================")
    lineas.append(f"Fecha de generacion: {fecha_actual}")
    lineas.append("")
    lineas.append("[1] RESUMEN GLOBAL OPERATIVO")
    lineas.append(f"Total de sesiones procesadas: {globales['total_sesiones']}")
    lineas.append(f"Ping promedio global: {globales['ping_promedio']} ms")
    lineas.append(f"Duracion media de partida: {globales['duracion_promedio']} min")
    lineas.append(f"Partidas de alta competencia (Ranked/Torneo): {globales['porcentaje_competitivas']:.2f}%")
    lineas.append("")
    lineas.append("[2] RENDIMIENTO REGIONAL POR SERVIDOR")
    lineas.append(f"{'Servidor':<18} {'Sesiones':<10} {'Ping Promedio':<15} {'FPS Promedio'}")
    
    for srv, datos in por_servidor.items():
        lineas.append(f"{srv:<18} {datos['cantidad']:<10} {datos['ping_promedio']:<15.2f} ms {datos['fps_promedio']:.2f} fps")
        
    lineas.append("")
    lineas.append("[3] AUDITORIA DE SEGURIDAD E INCIDENTES")
    lineas.append("Distribucion de estados de seguridad:")
    lineas.append(f"• Normales:    {frecuencias['Normal']} sesiones ({pct_normal}%)")
    lineas.append(f"• Sospechosos: {frecuencias['Sospechoso']} sesiones ({pct_sospechoso}%)")
    lineas.append(f"• Criticos:    {frecuencias['Critico']} sesiones ({pct_critico}%)")
    lineas.append("")
    lineas.append("Detalle de Sesiones Criticas Detectadas:")
    
    if eventos_criticos:
        for ev in eventos_criticos:
            lineas.append(f"[!] Sesion #{ev['id_sesion']} | Jugador: {ev['jugador_id']} | Servidor: {ev['servidor']}")
            lineas.append(f"Motivo: {ev['motivo']}")
    else:
        lineas.append("No se registraron sesiones críticas.")
        
    lineas.append("")
    lineas.append("[4] CONCLUSIONES TECNICAS DEL EQUIPO")
    lineas.append("1. Las regiones de servidores en Europa y Norteamerica presentan una latencia superior a los 150 ms, lo que impacta directamente en la experiencia de juego fluida.")
    lineas.append("2. El sistema permitio apartar correctamente a un grupo reducido de usuarios maliciosos al combinar las denuncias con los errores de acceso.")
    lineas.append("3. Se recomienda usar un sistema que ayude a mantener la conexion estable para evitar tirones o picos de latencia, ademas de reforzar los controles de seguridad al entrar a las partidas competitivas.")
    lineas.append("")
    lineas.append("=============================================================")
    lineas.append("FIN DEL REPORTE GAMESEC")
    lineas.append("=============================================================")
    
    # Escribir el archivo fisico
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))
        
    print(f"\n[Exito] Reporte exportado correctamente en '{ruta_salida}'.")


def main():
    sesiones = []
    dataset_cargado = False
    
    while True:
        print("\n=============================================================")
        print("GAMESEC MONITOR - PANEL DE CONTROL")
        print("=============================================================")
        print("1. Cargar y validar dataset")
        print("2. Ver estadisticas globales de servidores")
        print("3. Ver rendimiento por region de servidor")
        print("4. Auditar incidentes de seguridad (Criticos y Sospechosos)")
        print("5. Exportar reporte consolidado (reporte_gamesec.txt)")
        print("6. Salir")
        print("=============================================================")
        
        opcion = input("Seleccione una opcion: ").strip()
        
        if opcion == "1":
            try:
                ruta = "gamesec_logs.csv"
                sesiones = cargar_telemetria(ruta)
                dataset_cargado = True
                print(f"\n[Exito] Dataset cargado correctamente. Total de registros: {len(sesiones)}")
            except Exception as e:
                print(f"\n[Error] No se pudo cargar el archivo: {e}")
                
        elif opcion == "2":
            if not dataset_cargado:
                print("\n[Aviso] Primero debe cargar el dataset (Opcion 1).")
                continue
            stats = calcular_estadisticas_globales(sesiones)
            print("\n--- ESTADISTICAS GLOBALES OPERATIVAS ---")
            print(f"Total de sesiones: {stats['total_sesiones']}")
            print(f"Ping promedio global: {stats['ping_promedio']} ms")
            print(f"Duracion media de partida: {stats['duracion_minutos'] if 'duracion_minutos' in stats else stats['duracion_promedio']} min")
            print(f"Porcentaje de partidas competitivas/torneo: {stats['porcentaje_competitivas']}%")
            
        elif opcion == "3":
            if not dataset_cargado:
                print("\n[Aviso] Primero debe cargar el dataset (Opcion 1).")
                continue
            por_srv = analizar_por_servidor(sesiones)
            print("\n--- RENDIMIENTO POR REGION DE SERVIDOR ---")
            for srv, d in por_srv.items():
                print(f"  - Servidor: {srv}")
                print(f"  - Cantidad de sesiones: {d['cantidad']}")
                print(f"  - Ping promedio: {d['ping_promedio']} ms")
                print(f"  - FPS promedio: {d['fps_promedio']} fps")
                
        elif opcion == "4":
            if not dataset_cargado:
                print("\n[Aviso] Primero debe cargar el dataset (Opcion 1).")
                continue
            frecuencias, criticos = clasificar_incidentes(sesiones)
            print("\n--- AUDITORIA DE SEGURIDAD E INCIDENTES ---")
            print(f"Distribucion: Normales: {frecuencias['Normal']} | Sospechosos: {frecuencias['Sospechoso']} | Criticos: {frecuencias['Critico']}")
            print(f"\nSe detectaron {len(criticos)} eventos criticos:")
            for c in criticos:
                print(f"  [!] Sesion #{c['id_sesion']} | Jugador: {c['jugador_id']} | Servidor: {c['servidor']}")
                print(f"      Motivo: {c['motivo']}")
                
        elif opcion == "5":
            if not dataset_cargado:
                print("\n[Aviso] Primero debe cargar el dataset (Opcion 1).")
                continue
            exportar_reporte(sesiones, ruta_salida="reporte_gamesec.txt")
            
        elif opcion == "6":
            print("\nSaliendo del sistema Gamesec Monitor. ¡Hasta luego!")
            break
        else:
            print("\n[Error] Opcion invalida. Por favor, ingrese un numero del 1 al 6.")

if __name__ == "__main__":
    main()