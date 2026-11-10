# Optimización de presupuesto para e-commerce

## Problema

Este proyecto estima una combinación ilustrativa de equipo y tecnología para construir una plataforma e-commerce en Colombia. El modelo minimiza el costo sujeto a un presupuesto, un tamaño máximo de equipo, capacidad de trabajo, esfuerzo de QA y duración mínima por fases. Los importes, salarios y horas son supuestos sintéticos parametrizables, no cotizaciones ni datos de clientes.

## Enfoque

Se usa programación lineal entera mixta (MIP). Las variables enteras `personas_r` representan personas por rol y las binarias seleccionan una alternativa tecnológica. El calendario de fases es secuencial, por lo que la duración mínima es la ruta crítica:

```text
inicio(descubrimiento y diseño) = 0
inicio(fase siguiente) = inicio(fase actual) + duración mínima(fase actual)
semanas del proyecto >= suma de duraciones mínimas de las fases
```

El orden es descubrimiento y diseño → backend base → catálogo y usuarios → carrito → pagos → pruebas QA y estabilización → despliegue. La tabla de parámetros asigna mínimos de semanas distintos a cada tamaño; el modelo usa su suma como calendario de ruta crítica. Se limita el total de personas al tamaño del caso (4, 7 o 12) y cada rol tiene su propio máximo.

La capacidad de cada rol debe cubrir su proporción del esfuerzo dentro de las semanas de ruta crítica. QA dispone de al menos 20 % de las horas de desarrollo y la fase de pruebas incluye estabilización. La Ley 1581 de 2012 y la integración de facturación electrónica permanecen como horas normativas parametrizadas. El costo hora es `(salario mensual * (1 + 0,52) + auxilio aplicable) / 160`; 0,52 es un factor prestacional ilustrativo. Los costos tecnológicos combinan pago fijo y mensual por semana de proyecto.

La función objetivo minimiza costo más un peso opcional por duración. `--escenario costo` usa peso temporal cero y `--escenario ponderado` usa el valor configurado. El caso pequeño configura tareas de UX, liderazgo técnico y DevOps como responsabilidades compartidas por el equipo reducido; los otros casos conservan la distribución general por rol.

## Cómo ejecutarlo

Requiere Python 3.11 y `uv`. PuLP usa CBC para resolver el MIP.

```bash
uv sync --python 3.11
uv run pytest -q
uv run python -m optimizacion_ecommerce resolver --caso pequena
uv run python -m optimizacion_ecommerce resolver --caso mediana
uv run python -m optimizacion_ecommerce resolver --caso grande
```

Cada resolución imprime estado, semanas, equipo, tecnologías y costos; guarda `resultados/<caso>.csv`, `resultados/<caso>.png` (comparación de costos) y `resultados/<caso>_gantt.png` (fases de ruta crítica). Los PNG de resultados no se versionan.

## Resultados

Medición reproducible ejecutando los tres comandos `uv run python -m optimizacion_ecommerce resolver --caso <caso>` indicados arriba con `datos/parametros.yaml`:

| Caso | Estado | Personas máximas | Semanas | Ruta crítica mínima | Costo optimizado (COP) | Presupuesto (COP) |
|---|---|---:|---:|---:|---:|---:|
| Pequeña | Optimal | 3 de 4 | 9 | 9 | 55.506.000 | 120.000.000 |
| Mediana | Optimal | 6 de 7 | 16 | 16 | 207.792.000 | 250.000.000 |
| Grande | Optimal | 6 de 12 | 24 | 24 | 311.088.000 | 400.000.000 |

La ruta crítica se obtiene sumando los mínimos configurados para las siete fases. Los costos y estados de la tabla son salida medida del modelo; cambiar parámetros puede cambiarlos.

## Limitaciones

Es una aproximación didáctica y no sustituye cotizaciones ni asesoría jurídica, laboral o tributaria. La carga se representa como equipo disponible durante el calendario completo; no se distribuye el equipo por fase ni se modelan solapamientos, riesgos, cambios de alcance o dependencias externas. Las fases y duraciones son supuestos de planificación. La integración de facturación y privacidad se modela como horas, no como evaluación de cumplimiento. El factor prestacional 0,52, SMMLV, salarios, auxilio y tarifas son parámetros ilustrativos que deben verificarse antes de cualquier uso real.

## Origen

Basado en un trabajo académico en equipo de la Universidad ECCI, hecho con mi compañero [**David Alexander Rincón Corredor (Kuronoma)**](https://www.linkedin.com/in/davidalexanderrinconcorredorkuronoma/) y equipo; esta es una reimplementación individual y abierta.
