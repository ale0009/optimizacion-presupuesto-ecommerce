# ADR-0002: Separación de parámetros en archivo YAML declarativo

- **Estado:** Aceptado
- **Fecha:** 2026-11-09
- **Proyecto:** Optimización de presupuesto para e-commerce

## Contexto

Las tarifas del mercado laboral colombiano, prestaciones legales (0.52) y costos de software requieren actualización frecuente.

## Decisión

Aislar todos los supuestos económicos y restricciones de proyecto en datos/parametros.yaml.

## Consecuencias

Permite ajustar salarios y escenarios sin modificar el código matemático ni la lógica del solucionador.
