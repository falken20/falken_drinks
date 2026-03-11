---
mode: agent
description: Prompt para generar tests JavaScript con Jest siguiendo las convenciones del proyecto
---

Genera tests JavaScript con Jest para el proyecto:

## Configuración
- Framework: Jest con entorno jsdom
- Ubicación: `tests/js/<nombre>.test.js`
- Cobertura de: `static/js/**/*.js`

## Patrón de test
```javascript
/**
 * @jest-environment jsdom
 */

describe('ModuleName', () => {
    beforeEach(() => {
        // Reset DOM
        document.body.innerHTML = '';
        // Setup required DOM elements
        document.body.innerHTML = `
            <div id="container"></div>
        `;
    });

    afterEach(() => {
        jest.restoreAllMocks();
    });

    test('should do something when action happens', () => {
        // Arrange
        const element = document.getElementById('container');

        // Act
        // ... trigger action

        // Assert
        expect(element).toBeTruthy();
    });

    test('should handle error case', () => {
        // Arrange & Act & Assert
        expect(() => {
            // ... action that should fail
        }).toThrow();
    });
});
```

## Reglas
- Usar `describe` para agrupar por módulo/funcionalidad
- Usar `beforeEach` para setup del DOM
- Usar `afterEach` para cleanup de mocks
- Pattern AAA: Arrange, Act, Assert
- Mockear fetch, localStorage, etc. cuando sea necesario
- Ejecutar con: `npm test` o `npm run test:coverage`
