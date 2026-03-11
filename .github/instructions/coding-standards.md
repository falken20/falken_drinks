# Instrucciones globales de desarrollo - Falken Drinks

## Convenciones de código

### Python
- **Estilo**: PEP 8 con línea máxima de 127 caracteres
- **Strings**: siempre single quotes `'texto'`
- **Naming**: `lowercase_with_underscores` para archivos, variables y funciones
- **Imports**: stdlib → third-party → local, ordenados alfabéticamente
- **Docstrings**: en funciones públicas, concisas y descriptivas
- **Complejidad**: máxima ciclomática de 10 (flake8)

### JavaScript
- **Entorno**: Vanilla JS (no frameworks SPA)
- **DOM**: manipulación directa con getElementById, querySelector
- **Tests**: Jest con jsdom

### HTML/CSS
- **Templates**: Jinja2 extendiendo `base.html`
- **Framework CSS**: Bootstrap 5
- **Temas**: soportar modo claro y oscuro
- **Responsive**: mobile-first con grid Bootstrap

## Arquitectura

### Backend (Flask)
```
Modelo (models.py) → Controlador (controllers.py) → Ruta (routes.py/main.py/auth.py)
```
- **Factory pattern**: `create_app()` en `app.py`
- **Blueprints**: `auth`, `main`, `api_routes`, `swagger_ui`
- **Controladores**: clases con métodos estáticos
- **Config**: Pydantic BaseSettings con tres entornos (dev/test/prod)

### Base de datos
- **ORM**: SQLAlchemy con Flask-SQLAlchemy
- **Desarrollo**: SQLite (archivo local)
- **Testing**: SQLite en memoria
- **Producción**: PostgreSQL
- **Timezone**: CET (Madrid) con helpers `now_cet()`, `today_cet()`

### Autenticación
- Flask-Login con `@login_required`
- Passwords hasheadas con `pbkdf2:sha256` (werkzeug)
- Session-based authentication

## Testing

### Python (pytest + unittest)
- Base class: `BaseTestCase` en `tests/basetest.py`
- BD en memoria para aislamiento total
- Ejecutar: `coverage run -m pytest -v -s`
- Cobertura: `coverage report --omit="*/tests/*,*/venv/*" -m`

### JavaScript (Jest)
- Entorno: jsdom
- Ubicación: `tests/js/`
- Ejecutar: `npm test` o `npm run test:coverage`

### Verificación completa
```bash
./check_app.sh  # Linting + tests Python
npm test         # Tests JavaScript
```

## Logging
- Módulo propio: `falken_drinks.logger.Log`
- Métodos: `Log.debug()`, `Log.info()`, `Log.warning()`, `Log.error()`
- Errores: incluir siempre `sys.exc_info()` como segundo parámetro
- Control via variable `LEVEL_LOG` en `.env`

## Seguridad
- Nunca hardcodear credenciales; usar `.env` y `credentials.yaml`
- Validar inputs en modelos con `@validates` y comprobaciones explícitas
- Usar ORM para queries (nunca SQL raw sin parametrizar)
- `SECRET_KEY` obligatoria en producción
- No exponer tracebacks en producción

## Despliegue
- **Plataforma**: Google App Engine
- **Config**: `app.yaml`
- **Entrypoint**: `gunicorn -b:$PORT 'falken_drinks.app:create_app()'`
- **CI/CD**: GitHub Actions (`.github/workflows/`)
