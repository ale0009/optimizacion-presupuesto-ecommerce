# ADR-0001: Modelado mediante Programación Lineal Entera Mixta (MIP) con PuLP y CBC

- **Estado:** Aceptado
- **Fecha:** 2026-11-09
- **Proyecto:** Optimización de presupuesto para e-commerce

## Contexto

Se requiere optimizar de manera exacta decisiones combinatorias discretas (perfiles y tecnologías) sujetas a restricciones operativas.

## Decisión

Formular el problema con PuLP usando variables enteras para personal y binarias para alternativas tecnológicas resueltas por CBC.

## Consecuencias

Asegura obtención de óptimos matemáticos globales con herramientas de código abierto sin depender de solvers comerciales propietarios.
