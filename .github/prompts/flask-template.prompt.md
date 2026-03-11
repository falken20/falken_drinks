---
mode: agent
description: Prompt para generar templates HTML con Flask/Jinja2 y Bootstrap 5
---

Genera templates HTML siguiendo las convenciones del proyecto:

## Estructura base
- Extender de `base.html`: `{% extends 'base.html' %}`
- Definir bloques: `{% block content %}...{% endblock %}`
- Ubicación: `templates/<nombre>.html`

## Bootstrap 5
- Usar componentes Bootstrap para UI consistente
- Grid system para layouts responsive
- Cards, tables, forms, modals según necesidad
- Iconos si ya están disponibles en el proyecto

## Modo claro/oscuro
- Usar clases CSS compatibles con el toggle de tema
- Evitar colores hardcodeados; usar variables CSS o clases Bootstrap
- Probar que el template se ve bien en ambos modos

## Patrón de template
```html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-12">
            <h2>Título de la página</h2>
        </div>
    </div>

    <div class="row mt-3">
        <div class="col-md-8">
            <!-- Contenido principal -->
        </div>
        <div class="col-md-4">
            <!-- Sidebar o contenido secundario -->
        </div>
    </div>
</div>
{% endblock %}
```

## Reglas
- HTML semántico
- Responsive: mobile-first con breakpoints Bootstrap
- Accesibilidad: labels en forms, alt en imágenes, roles ARIA
- Flash messages: usar el sistema de Flask `get_flashed_messages()`
- Single quotes en atributos Jinja2, double quotes en HTML
