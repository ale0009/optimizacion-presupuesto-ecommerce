"""Pruebas funcionales del optimizador con datos sintéticos ilustrativos."""

import pytest

from optimizacion_ecommerce.modelo import resolver
from optimizacion_ecommerce.parametros import Parametros
from optimizacion_ecommerce.simulacion import monte_carlo


@pytest.fixture(scope="module")
def datos():
    return Parametros.cargar().datos


@pytest.mark.parametrize("caso", ["pequena", "mediana", "grande"])
def test_casos_factibles_respetan_plazo_y_presupuesto(datos, caso):
    salida = resolver(datos, caso)
    assert salida["estado"] == "Optimal"
    assert salida["semanas"] <= datos["casos"][caso]["plazo_maximo_semanas"]
    assert salida["costo_total"] <= salida["presupuesto_tope"]
    assert salida["tecnologias"]["plataforma"] in {"a_medida", "saas"}
    assert salida["semanas"] >= salida["ruta_critica_minima"]
    assert salida["max_equipo_semana"] <= datos["casos"][caso]["max_personas_equipo"]
    duraciones = list(salida["fases"].values())
    assert salida["ruta_critica_minima"] == sum(duraciones)
    assert all(duracion >= 1 for duracion in duraciones)
    assert list(salida["fases"]) == ["descubrimiento_diseno", "backend_base", "catalogo_usuarios", "carrito", "pagos", "pruebas_qa_estabilizacion", "despliegue"]
    assert salida["horas_qa_asignadas"] >= salida["horas_desarrollo"] * datos["parametros_generales"]["qa_minimo_desarrollo"]


def test_costo_con_prestaciones_supera_tarifa_plana(datos):
    salida = resolver(datos, "mediana")
    assert salida["estado"] == "Optimal"
    assert salida["costo_total"] > salida["costo_tradicional"]


def test_monte_carlo_reproducible(datos):
    assert monte_carlo(datos, "pequena", iteraciones=4, semilla=17) == monte_carlo(datos, "pequena", iteraciones=4, semilla=17)
