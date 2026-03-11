# Configuración de GitHub Copilot - Falken Drinks

## Contexto del proyecto

Falken Drinks es una aplicación web Flask para gestionar bebidas consumidas diariamente.
Stack: Python 3.11+, Flask, SQLAlchemy, Bootstrap 5, PostgreSQL/SQLite.

## Instrucciones para Copilot

### Al generar código Python
- Usar single quotes para strings
- Seguir PEP 8 con max-line-length=127
- Usar el sistema de logging del proyecto: `from falken_drinks.logger import Log`
- Seguir el patrón MVC: models → controllers → routes
- Timestamps con timezone CET usando `now_cet()` de config

### Al generar tests
- Heredar de `BaseTestCase` en `tests/basetest.py`
- Usar SQLite en memoria (ya configurado en BaseTestCase)
- Incluir tests de autenticación (login_required)
- Nombrar: `test_<funcionalidad>_<escenario>`

### Al generar HTML/Templates
- Extender de `base.html`
- Usar Bootstrap 5
- Soportar modo claro/oscuro
- Responsive design

### Al generar JavaScript
- Vanilla JS (sin frameworks SPA)
- Tests con Jest + jsdom

### No hacer
- No hardcodear credenciales ni secrets
- No usar SQL raw sin parametrizar
- No crear archivos innecesarios
- No añadir dependencias sin justificación
