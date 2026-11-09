"""Modelo MIP ilustrativo de presupuesto, equipo y ruta crítica."""

from typing import Any

import pulp

from .escenarios import esfuerzo_base


def costo_hora(rol: str, salario: float, general: dict[str, Any]) -> float:
    """Calcula costo hora con factor prestacional y auxilio ilustrativos."""
    mensual = salario * (1 + general["factor_prestacional"])
    if salario < general["limite_auxilio_smmlv"] * general["smmlv"]:
        mensual += general["auxilio_transporte"]
    return mensual / (general["horas_semana"] * 4)


def resolver(datos: dict[str, Any], nombre_caso: str, salarios: dict[str, float] | None = None,
             peso_tiempo: float | None = None) -> dict[str, Any]:
    """Optimiza costo con equipo acotado y calendario fijado por la ruta crítica."""
    general = datos["parametros_generales"]
    caso = datos["casos"][nombre_caso]
    roles = datos["roles"]
    salarios = salarios or {rol: item["salario_mensual"] for rol, item in roles.items()}
    fases = caso["fases_semanas"]
    ruta_critica = sum(fases.values())
    if ruta_critica > caso["plazo_maximo_semanas"]:
        return {"estado": "Infeasible", "caso": nombre_caso}

    modelo = pulp.LpProblem(f"ecommerce_{nombre_caso}", pulp.LpMinimize)
    equipo = {rol: pulp.LpVariable(f"personas_{rol}", lowBound=0,
                                   upBound=item["max_personas"], cat="Integer")
              for rol, item in roles.items()}
    modelo += pulp.lpSum(equipo.values()) <= caso["max_personas_equipo"], "tamano_equipo"

    opciones: dict[str, dict[str, pulp.LpVariable]] = {}
    for grupo, alternativas in datos["tecnologias"].items():
        opciones[grupo] = {op: pulp.LpVariable(f"{grupo}_{op}", cat="Binary") for op in alternativas}
        modelo += pulp.lpSum(opciones[grupo].values()) == 1, f"una_opcion_{grupo}"

    factor = pulp.lpSum(opciones["plataforma"][op] * item["factor_esfuerzo"]
                        for op, item in datos["tecnologias"]["plataforma"].items())
    horas_funcionales = sum(caso["modulos_horas"].values())
    horas_normativas = sum(caso["horas_normativas"].values())
    esfuerzo = horas_funcionales * factor + horas_normativas
    distribucion = caso.get("distribucion_esfuerzo", datos["distribucion_esfuerzo"])
    for rol, proporcion in distribucion.items():
        modelo += equipo[rol] * general["horas_semana"] * ruta_critica >= esfuerzo * proporcion, f"horas_{rol}"
    modelo += equipo["qa"] * general["horas_semana"] * ruta_critica >= esfuerzo * general["qa_minimo_desarrollo"], "qa_proporcional"
    modelo += equipo["backend"] * general["horas_semana"] * ruta_critica >= general["minimo_mantenimiento_horas"], "mantenimiento"

    costo_laboral = pulp.lpSum(equipo[rol] * ruta_critica * general["horas_semana"] * costo_hora(rol, salarios[rol], general)
                               for rol in roles)
    costo_tecnologia = pulp.lpSum(opciones[grupo][op] * (item["costo_fijo"] + item["costo_mensual"] * ruta_critica)
                                  for grupo, alternativas in datos["tecnologias"].items()
                                  for op, item in alternativas.items())
    costo = costo_laboral + costo_tecnologia
    modelo += costo <= caso["presupuesto_tope"], "presupuesto_tope"
    peso = general["peso_tiempo"] if peso_tiempo is None else peso_tiempo
    modelo += costo + peso * ruta_critica
    modelo.solve(pulp.PULP_CBC_CMD(msg=False))
    estado = pulp.LpStatus[modelo.status]
    if estado != "Optimal":
        return {"estado": estado, "caso": nombre_caso}

    asignacion = {}
    for rol in roles:
        cantidad = int(round(equipo[rol].value() or 0))
        asignacion[rol] = {"personas": cantidad, "persona_semanas": cantidad * ruta_critica,
                           "semanas_asignadas": ruta_critica if cantidad else 0,
                           "horas": cantidad * ruta_critica * general["horas_semana"]}
    tecnologias = {grupo: next(op for op, variable in variables.items() if variable.value() > 0.5)
                   for grupo, variables in opciones.items()}
    factor_elegido = datos["tecnologias"]["plataforma"][tecnologias["plataforma"]]["factor_esfuerzo"]
    horas_desarrollo = horas_funcionales * factor_elegido + horas_normativas
    horas_qa_asignadas = asignacion["qa"]["horas"]
    costo_real = float(pulp.value(costo))
    tradicional = esfuerzo_base(caso) * general["tarifa_tradicional_hora"]
    return {"estado": estado, "caso": nombre_caso, "productos": caso["productos"],
            "semanas": ruta_critica, "ruta_critica_minima": ruta_critica,
            "max_equipo_semana": sum(item["personas"] for item in asignacion.values()),
            "horas_desarrollo": horas_desarrollo, "horas_qa_asignadas": horas_qa_asignadas,
            "fases": fases, "costo_total": round(costo_real, 2),
            "costo_laboral": round(float(pulp.value(costo_laboral)), 2),
            "costo_tecnologia": round(float(pulp.value(costo_tecnologia)), 2),
            "costo_tradicional": round(tradicional, 2), "horas_base": esfuerzo_base(caso),
            "presupuesto_tope": caso["presupuesto_tope"], "asignacion": asignacion,
            "tecnologias": tecnologias, "horas_normativas": caso["horas_normativas"],
            "ahorro_vs_tradicional": round(tradicional - costo_real, 2)}
