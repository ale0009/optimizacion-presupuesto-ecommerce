"""Carga y validación de los parámetros ilustrativos en YAML."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class Parametros:
    """Configuración validada del modelo."""

    datos: dict[str, Any]

    @classmethod
    def cargar(cls, ruta: str | Path | None = None) -> "Parametros":
        """Carga el YAML y comprueba consistencia de sus campos principales."""
        archivo = Path(ruta) if ruta else Path(__file__).resolve().parents[2] / "datos" / "parametros.yaml"
        datos = yaml.safe_load(archivo.read_text(encoding="utf-8"))
        requeridos = {"parametros_generales", "roles", "tecnologias", "casos", "distribucion_esfuerzo"}
        if not isinstance(datos, dict) or not requeridos.issubset(datos):
            raise ValueError("El YAML debe contener los bloques principales del modelo.")
        general = datos["parametros_generales"]
        if not 0 <= general["factor_prestacional"] < 2:
            raise ValueError("factor_prestacional debe estar entre 0 y 2.")
        if sum(datos["distribucion_esfuerzo"].values()) != 1.0:
            raise ValueError("La distribución de esfuerzo debe sumar 1.")
        for caso, valores in datos["casos"].items():
            if valores["plazo_maximo_semanas"] <= 0 or valores["presupuesto_tope"] <= 0:
                raise ValueError(f"Plazo y presupuesto deben ser positivos: {caso}.")
        return cls(datos)

    def caso(self, nombre: str) -> dict[str, Any]:
        """Devuelve un caso o informa los nombres válidos."""
        try:
            return self.datos["casos"][nombre]
        except KeyError as exc:
            raise ValueError(f"Caso desconocido: {nombre}. Opciones: {', '.join(self.datos['casos'])}") from exc
