"""Interfaz de línea de comandos."""

import argparse
import csv
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .modelo import resolver
from .parametros import Parametros
from .simulacion import monte_carlo, resumen_simulacion


def guardar_resultados(salida: dict[str, Any], directorio: Path) -> None:
    """Escribe asignación en CSV y una gráfica comparativa de costos."""
    directorio.mkdir(parents=True, exist_ok=True)
    ruta_csv = directorio / f"{salida['caso']}.csv"
    with ruta_csv.open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["rol", "personas", "persona_semanas", "semanas_asignadas", "horas"])
        for rol, valores in salida["asignacion"].items():
            escritor.writerow([rol, valores["personas"], valores["persona_semanas"], valores["semanas_asignadas"], valores["horas"]])
    etiquetas = ["Optimizado", "Tradicional"]
    valores = [salida["costo_total"], salida["costo_tradicional"]]
    fig, eje = plt.subplots(figsize=(7, 4))
    eje.bar(etiquetas, valores, color=["#2563eb", "#9ca3af"])
    eje.set_ylabel("Costo (COP)")
    eje.set_title(f"Costo estimado: caso {salida['caso']}")
    eje.ticklabel_format(axis="y", style="plain")
    fig.tight_layout()
    fig.savefig(directorio / f"{salida['caso']}.png", dpi=140)
    plt.close(fig)
    fases = salida["fases"]
    inicio = 0
    fig, eje = plt.subplots(figsize=(10, max(3, len(fases) * 0.45)))
    for indice, (fase, duracion) in enumerate(fases.items()):
        eje.barh(indice, duracion, left=inicio, color="#2563eb")
        eje.text(inicio + duracion / 2, indice, f"{duracion} sem", va="center", ha="center", color="white", fontsize=8)
        inicio += duracion
    eje.set_yticks(range(len(fases)), [fase.replace("_", " ") for fase in fases])
    eje.invert_yaxis()
    eje.set_xlabel("Semanas desde el inicio")
    eje.set_title(f"Ruta crítica mínima: caso {salida['caso']} ({inicio} semanas)")
    eje.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(directorio / f"{salida['caso']}_gantt.png", dpi=140)
    plt.close(fig)


def main() -> None:
    """Ejecuta resolución y opcionalmente la simulación Monte Carlo."""
    parser = argparse.ArgumentParser(description="Optimización ilustrativa de presupuesto e-commerce")
    subparsers = parser.add_subparsers(dest="comando", required=True)
    resolver_parser = subparsers.add_parser("resolver", help="Resuelve un caso")
    resolver_parser.add_argument("--caso", choices=["pequena", "mediana", "grande"], required=True)
    resolver_parser.add_argument("--escenario", choices=["costo", "ponderado"], default="costo")
    resolver_parser.add_argument("--simular", action="store_true", help="Ejecuta 40 perturbaciones salariales")
    resolver_parser.add_argument("--salida", type=Path, default=Path("resultados"))
    args = parser.parse_args()
    datos = Parametros.cargar().datos
    peso = 0 if args.escenario == "costo" else None
    salida = resolver(datos, args.caso, peso_tiempo=peso)
    if salida["estado"] != "Optimal":
        raise SystemExit(f"No se encontró una solución óptima: {salida['estado']}")
    guardar_resultados(salida, args.salida)
    print(f"Estado: {salida['estado']} | caso: {args.caso} | semanas: {salida['semanas']}")
    for rol, valores in salida["asignacion"].items():
        print(f"{rol}: {valores['personas']} personas, {valores['horas']} h")
    print(f"Tecnologías: {salida['tecnologias']}")
    print(f"Costo optimizado: COP {salida['costo_total']:,.0f} | tradicional: COP {salida['costo_tradicional']:,.0f} | tope: COP {salida['presupuesto_tope']:,.0f}")
    if args.simular:
        resumen = resumen_simulacion(monte_carlo(datos, args.caso))
        print(f"Monte Carlo (40 iteraciones): mínimo COP {resumen['minimo']:,.0f}; media COP {resumen['media']:,.0f}; máximo COP {resumen['maximo']:,.0f}")


if __name__ == "__main__":
    main()
