# Instrucciones de testing - Falken Drinks

## Principios generales
- Todo cambio de funcionalidad debe ir acompañado de tests
- Tests deben ser independientes y reproducibles
- Cubrir: happy path, errores, edge cases, autenticación

## Tests Python

### Estructura
```
tests/
├── __init__.py
├── basetest.py           # BaseTestCase con setup común
├── test_app.py           # Tests de creación de app y config
├── test_auth.py          # Tests de autenticación
├── test_controllers.py   # Tests de lógica de negocio
├── test_models.py        # Tests de modelos
├── test_routes.py        # Tests de endpoints API
├── test_config.py        # Tests de configuración
├── test_logger.py        # Tests de logging
├── test_main.py          # Tests de vistas principales
├── test_swagger.py       # Tests de Swagger
└── js/                   # Tests JavaScript
    ├── drink_selector.test.js
    ├── drinks_management.test.js
    └── falken.test.js
```

### BaseTestCase
Todos los tests Python heredan de `BaseTestCase` que proporciona:

| Recurso | Descripción |
|---------|-------------|
| `self.app` | Instancia Flask con config de testing |
| `self.client` | Cliente HTTP de test |
| `self.mock_user` | Objeto User mock |
| `self.MOCK_DRINK` | Dict con datos de bebida mock |
| `self.MOCK_DRINK_LOG` | Dict con datos de registro mock |
| `self.create_user()` | Crea usuario en BD de test |
| `self.login_http()` | Simula login HTTP |
| `setUp()` | Crea todas las tablas |
| `tearDown()` | Destruye todas las tablas |

### Ejecución

```bash
# Todos los tests con cobertura
coverage run -m pytest -v -s

# Un archivo de test específico
pytest -v -s tests/test_auth.py

# Un test específico
pytest -v -s tests/test_auth.py::TestAuth::test_auth_login

# Reporte de cobertura
coverage report --omit="*/tests/*,*/venv/*" -m ./falken_drinks/*.py

# Cobertura HTML
coverage html --omit="*/tests/*,*/venv/*"
```

## Tests JavaScript

### Ejecución
```bash
npm test                  # Todos los tests
npm run test:coverage     # Con cobertura
npm run test:watch        # Watch mode para desarrollo
```

## Linting
```bash
# Errores de sintaxis
flake8 ./falken_drinks/ --count --select=E9,F63,F7,F82 --show-source --statistics

# Estilo completo
flake8 ./falken_drinks/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
```

## Script completo
```bash
./check_app.sh  # Ejecuta tests + linting Python
```
