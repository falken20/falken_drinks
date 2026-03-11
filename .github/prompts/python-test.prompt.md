---
mode: agent
description: Prompt para generar tests Python con pytest/unittest siguiendo las convenciones del proyecto
---

Genera tests Python que sigan estas convenciones:

## Estructura base
- Heredar de `BaseTestCase` de `tests.basetest`
- Nombre de archivo: `tests/test_<modulo>.py`
- Nombre de clase: `Test<Modulo>(BaseTestCase)`
- Nombre de método: `test_<funcionalidad>_<escenario>`

## Recursos disponibles en BaseTestCase
- `self.app`: instancia de la aplicación Flask
- `self.client`: cliente de test HTTP
- `self.mock_user`: usuario mock para tests
- `self.MOCK_DRINK`: datos mock de bebida
- `self.MOCK_DRINK_LOG`: datos mock de registro de bebida
- `self.create_user()`: crea usuario en BD de test
- `self.login_http()`: simula login HTTP
- `setUp()`: crea tablas en SQLite en memoria
- `tearDown()`: destruye tablas

## Patrón de test
```python
import unittest
from tests.basetest import BaseTestCase


class TestExample(BaseTestCase):
    '''Tests for example module'''

    def test_feature_happy_path(self):
        '''Test feature works with valid data'''
        self.create_user()
        self.login_http()
        response = self.client.get('/api/endpoint')
        self.assertEqual(response.status_code, 200)

    def test_feature_unauthorized(self):
        '''Test feature requires authentication'''
        response = self.client.get('/api/endpoint')
        self.assertNotEqual(response.status_code, 200)

    def test_feature_invalid_data(self):
        '''Test feature handles invalid data'''
        self.create_user()
        self.login_http()
        response = self.client.post('/api/endpoint', json={})
        self.assertIn(response.status_code, [400, 500])


if __name__ == '__main__':
    unittest.main()
```

## Reglas
- Cada test debe ser independiente (BD se resetea en cada setUp/tearDown)
- Usar single quotes para strings
- Cubrir: happy path, errores, edge cases, autenticación
- Ejecutar con: `coverage run -m pytest -v -s`
