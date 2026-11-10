# Guía de Contribución

Agradecemos el interés en contribuir a Optimización de presupuesto para e-commerce. Para mantener la consistencia técnica y la calidad del proyecto, solicitamos seguir los siguientes lineamientos.

## Flujo de ramas

1. La rama principal `main` contiene el código en estado de producción y pruebas superadas.
2. Crea ramas descriptivas a partir de `main` con la nomenclatura:
   - `feat/nombre-de-la-caracteristica`
   - `fix/descripcion-del-arreglo`
   - `docs/tema-documentado`
3. Abre un Pull Request dirigido a `main` detallando el contexto del cambio, problema resuelto y verificación efectuada.

## Mensajes de confirmación (Conventional Commits)

Los mensajes de commit deben seguir el estándar de Conventional Commits:

```text
tipo(alcance): descripción en modo imperativo y minúsculas

[cuerpo opcional con justificación técnica]
```

Tipos permitidos:
- `feat`: nueva funcionalidad.
- `fix`: corrección de error.
- `docs`: modificaciones en documentación.
- `style`: ajustes de formato sin impacto funcional.
- `refactor`: reestructuración interna de código.
- `test`: adición o ajuste de pruebas automatizadas.
- `chore`: tareas de mantenimiento o configuración.

## Ejecución de pruebas

Antes de someter cualquier Pull Request, verifica localmente que la suite de pruebas completa se ejecute sin errores:

```bash
uv run pytest -q
```

## Estilo y calidad de código

- Apego a las directrices de PEP 8 para código Python.
- Tipado estático consistente mediante type hints.
- Nombres de funciones y variables claros y descriptivos.

## Código de conducta

Se espera un trato estrictamente respetuoso, constructivo y profesional entre todos los participantes. No se tolerará ningún tipo de discriminación, descalificación ni acoso.
