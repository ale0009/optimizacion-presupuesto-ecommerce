# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y este proyecto se adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-01

### Añadido
- Implementación del componente `parametros`: Carga y validación de tarifas salariales, factor prestacional (0.52), duraciones de fases y costos tecnológicos desde datos/parametros.yaml..
- Implementación del componente `modelo`: Construcción formal del problema MIP en PuLP (variables enteras de roles, binarias de tecnología, restricciones de presupuesto, QA y ruta crítica)..
- Implementación del componente `escenarios`: Definición de casos de estudio (pequeña, mediana, grande) y ponderación de funciones objetivo (costo puro frente a penalización temporal)..
- Implementación del componente `simulacion`: Invocación del solver CBC, verificación de optimalidad matemática y extracción estructurada de costos y asignaciones..
- Implementación del componente `cli`: Interfaz de línea de comandos para resolver casos, imprimir resúmenes tabulares y generar diagramas de Gantt y costos..
- Implementación del componente `__main__`: Punto de entrada ejecutable del paquete para delegar la ejecución a la interfaz CLI..
- Configuración de flujo de trabajo de integración continua.
- Documentación técnica, guías de arquitectura y políticas de seguridad.
