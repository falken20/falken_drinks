---
mode: agent
description: Prompt para generar modelos SQLAlchemy siguiendo las convenciones del proyecto
---

Genera modelos SQLAlchemy para el proyecto:

## Convenciones de modelos

```python
from datetime import datetime
from falken_drinks.config import now_cet
from falken_drinks import db


class NewModel(db.Model):
    '''Description of the model'''
    __tablename__ = 'new_model'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_date = db.Column(db.DateTime, default=now_cet)
    updated_date = db.Column(db.DateTime, default=now_cet, onupdate=now_cet)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    # Relationships
    user = db.relationship('User', backref=db.backref('new_models', lazy=True))

    def serialize(self):
        '''Serialize model to dictionary'''
        return {
            'id': self.id,
            'name': self.name,
            'is_active': self.is_active,
            'created_date': str(self.created_date),
            'updated_date': str(self.updated_date),
            'user_id': self.user_id,
        }

    def __repr__(self):
        return f'<NewModel {self.name}>'
```

## Reglas
- Timestamps con `now_cet()` para timezone CET
- Incluir `serialize()` para respuestas JSON
- Incluir `__repr__()` para debugging
- Validación con `@validates` y lógica explícita en el modelo
- Foreign keys con `db.ForeignKey` y relationships con `db.relationship`
- Nombres de tabla en snake_case
- Single quotes para strings
