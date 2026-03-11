---
mode: agent
description: Prompt para realizar code review siguiendo los estándares del proyecto
---

Realiza una revisión de código exhaustiva verificando:

## Checklist de revisión

### 1. Estilo y convenciones
- [ ] PEP 8 con max-line-length=127
- [ ] Single quotes para strings
- [ ] Nombres descriptivos en lowercase_with_underscores
- [ ] Imports ordenados: stdlib → third-party → local
- [ ] Comentarios claros donde sea necesario

### 2. Arquitectura
- [ ] Sigue el patrón: models → controllers → routes/blueprints
- [ ] Controladores usan métodos estáticos
- [ ] Rutas protegidas con `@login_required`
- [ ] Respuestas JSON con formato `{'status': ..., 'data': ...}`

### 3. Seguridad
- [ ] No hay credenciales hardcodeadas
- [ ] Validación de inputs del usuario
- [ ] No hay SQL injection (usar ORM)
- [ ] No hay XSS en templates (Jinja2 escaping)
- [ ] CSRF protection habilitado

### 4. Testing
- [ ] Hay tests para los cambios
- [ ] Tests cubren happy path y error cases
- [ ] Tests heredan de BaseTestCase
- [ ] Tests son independientes entre sí

### 5. Logging y errores
- [ ] Usa el módulo `Log` del proyecto
- [ ] try/except con logging adecuado
- [ ] No se silencian errores (bare except)
- [ ] Mensajes de error informativos

### 6. UI (si aplica)
- [ ] Compatible con modo claro y oscuro
- [ ] Responsive (Bootstrap grid)
- [ ] Accesibilidad básica

Proporciona feedback constructivo con ejemplos de corrección para cada issue encontrado.
