# GameSec Monitor: Sistema de Telemetria y Auditoria de Ciberseguridad

Trabajo Practico Integrador desarrollado en Python para la materia **Taller de Programacion I** de la **Tecnicatura Universitaria en Ciberseguridad** (UNAHUR)[cite: 1].

##  Integrante
* **Ronald Caballero** - DNI: 47.388.880 (Ciberseguridad)

##  Descripcion General
Herramienta de consola modular implementada integramente en Python orientada al monitoreo, procesamiento y analisis forense de registros de telemetria de servidores multijugador. El sistema evalua de forma independiente el rendimiento operativo de los servidores y audita reportes de usuarios y eventos de inicio de sesion para la deteccion de anomalias[cite: 1, 2].

##  Modulos del Sistema
* `main.py`: Interfaz de comandos interactiva mediante bucle de control para la navegacion del usuario.
* `carga.py`: Rutinas de apertura, control de existencia, validacion de integridad estructural y casteo tipado del dataset CSV[cite: 3, 4].
* `procesamiento.py`: Nucleo de calculo estadistico, agrupamientos dinamicos mediante estructuras nativas y motor heuristico de seguridad[cite: 4].

##  Capacidades Funcionales
* Validacion estricta y carga de registros de telemetria desde el archivo de datos (`gamesec_logs.csv`)[cite: 2, 3].
* Computacion de metricas operativas globales de servidores[cite: 2].
* Analisis dinamico de latencia (ping) y rendimiento visual (FPS promedio) por region[cite: 2].
* Clasificacion heuristica de sesiones operativas en estados normales, sospechosas y criticas segen umbrales de seguridad[cite: 2].
* Exportacion automatica de un reporte consolidado en formato de texto plano (`reporte_gamesec.txt`).

##  Requisitos Tecnicos y Entorno
* **Python 3.10 o superior** (diseñado y desarrollado utilizando exclusivamente la libreria estandar del lenguaje: `csv`, `os`, `datetime`)[cite: 1].
* **Cero dependencias externas:** No se emplean librerias de terceros (como Pandas o NumPy), cumpliendo con las pautas tecnicas de la catedra[cite: 1, 3].

##  Instrucciones de Puesta en Marcha
1. Verifique que se encuentra instalado Python 3.10+ en el equipo.
2. Asegurese de que el archivo con el dataset (`gamesec_logs.csv`) se encuentre ubicado en la raiz del directorio del proyecto junto al codigo fuente[cite: 3].
3. Abra una terminal en la ruta de la carpeta y ejecute el sistema mediante el siguiente comando:
   ```bash
   python main.py