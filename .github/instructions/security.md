# Instrucciones de seguridad - Falken Drinks

## Gestión de secretos
- Variables sensibles en `.env` (local) y `credentials.yaml` (GAE)
- **Nunca** commitear `.env` ni `credentials.yaml` (deben estar en .gitignore)
- Usar `secrets` de GitHub Actions para CI/CD
- `SECRET_KEY` debe ser única y robusta en producción

## Autenticación
- Flask-Login gestiona sesiones de usuario
- `@login_required` en toda ruta que requiera autenticación
- Passwords hasheadas con `generate_password_hash()` (pbkdf2)
- Verificar con `check_password_hash()`
- No almacenar passwords en texto plano bajo ninguna circunstancia

## Validación de datos
- Validación en modelos con flask-validator (nivel BD)
- Validación adicional con `@validates` de SQLAlchemy
- Validar tipos, longitudes y formatos en el backend
- No confiar en validación del frontend como única barrera

## Prevención de inyecciones
- **SQL**: usar siempre SQLAlchemy ORM, nunca SQL raw sin parametrizar
- **XSS**: Jinja2 escapa automáticamente; no usar `|safe` sin necesidad
- **CSRF**: considerar Flask-WTF para formularios
- **Path traversal**: validar nombres de archivo en uploads

## Headers y configuración
- Configurar headers de seguridad en producción
- No exponer tracebacks ni información de debug en producción
- `CONFIG_MODE=production` desactiva debug automáticamente

## Dependencias
- Mantener dependencias actualizadas
- Revisar vulnerabilidades con `pip audit` o Dependabot
- Usar versiones mínimas pinneadas en `pyproject.toml`
