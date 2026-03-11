---
mode: agent
description: Prompt para generar código Python siguiendo las convenciones del proyecto
---

Genera código Python que cumpla estrictamente estas convenciones:

## Estilo
- PEP 8 con max-line-length=127
- Single quotes para strings: `'texto'`
- Nombres en lowercase_with_underscores
- Docstrings en funciones públicas

## Patrones del proyecto
- Logging: usar `from falken_drinks.logger import Log` y `Log.info()`, `Log.error()`, etc.
- Config: acceder via `from falken_drinks.config import settings`
- Modelos: heredar de `db.Model`, incluir `serialize()`
- Controladores: métodos estáticos en clases `Controller*`
- Errores: try/except con `Log.error(f'Error: {e}', sys.exc_info())`

## Imports
- Agrupar: stdlib → third-party → local
- Ordenar alfabéticamente dentro de cada grupo
- Una línea en blanco entre grupos

## Ejemplo de estructura
```python
import sys
from datetime import datetime

from flask import jsonify, request
from flask_login import login_required

from falken_drinks.controllers import ControllerDrinks
from falken_drinks.logger import Log


@login_required
def get_drinks():
    '''Get all drinks from the database'''
    try:
        drinks = ControllerDrinks.get_all()
        return jsonify({'status': 'ok', 'data': [d.serialize() for d in drinks]})
    except Exception as e:
        Log.error(f'Error getting drinks: {e}', sys.exc_info())
        return jsonify({'status': 'error', 'message': str(e)}), 500
```