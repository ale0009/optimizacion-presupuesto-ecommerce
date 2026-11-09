"""Comparación tradicional y simulación de incertidumbre salarial."""

import random
from typing import Any

from .modelo import resolver


def monte_carlo(datos: dict[str, Any], caso: str, iteraciones: int | None = None,
                semilla: int | None = None) -> list[dict[str, float | int | str]]:
    """Reoptimiza con salarios independientes perturbados dentro de ±10 %."""
    general = datos["parametros_generales"]
    n = iteraciones or general["iteraciones_monte_carlo"]
    rng = random.Random(general["semilla"] if semilla is None else semilla)
    base = {rol: item["salario_mensual"] for rol, item in datos["roles"].items()}
    resultados = []
    for indice in range(n):
        salarios = {rol: salario * rng.uniform(1 - general["variacion_salarios"], 1 + general["variacion_salarios"])
                    for rol, salario in base.items()}
        solucion = resolver(datos, caso, salarios=salarios)
        resultados.append({"iteracion": indice + 1, "estado": solucion["estado"], "costo_total": solucion.get("costo_total", float("nan"))})
    return resultados


def resumen_simulacion(resultados: list[dict[str, Any]]) -> dict[str, float]:
    """Resume mínimo, media, máximo y dispersión de los costos simulados."""
    costos = [float(r["costo_total"]) for r in resultados if r["estado"] == "Optimal"]
    if not costos:
        raise ValueError("La simulación no produjo soluciones óptimas.")
    return {"minimo": min(costos), "media": sum(costos) / len(costos), "maximo": max(costos)}
