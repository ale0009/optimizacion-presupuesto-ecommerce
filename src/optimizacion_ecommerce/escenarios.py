"""Construcción de esfuerzo y cotas por caso."""

from typing import Any


def esfuerzo_base(caso: dict[str, Any]) -> int:
    """Suma esfuerzo de módulos y tareas obligatorias."""
    return sum(caso["modulos_horas"].values()) + sum(caso["horas_normativas"].values())


def esfuerzo_por_rol(caso: dict[str, Any], distribucion: dict[str, float], factor: float) -> dict[str, int]:
    """Reparte las horas y redondea hacia arriba para no perder trabajo requerido."""
    total = esfuerzo_base(caso) * factor
    salida = {rol: int(total * proporcion) for rol, proporcion in distribucion.items()}
    salida["backend"] += round(total) - sum(salida.values())
    return salida
