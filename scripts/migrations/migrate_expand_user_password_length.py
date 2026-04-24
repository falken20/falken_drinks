#!/usr/bin/env python3
"""Expand the users.password column to support modern password hashes."""

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from falken_drinks.app import create_app, settings
from falken_drinks.models import db
from falken_drinks.logger import Log


def migrate_database():
    """Expand users.password from VARCHAR(100) to VARCHAR(255)."""
    try:
        Log.info('***** Starting user password length migration *****')

        app = create_app(settings.CONFIG_ENV[settings.CONFIG_MODE])

        with app.app_context():
            inspector = db.inspect(db.engine)
            columns = {col['name']: col for col in inspector.get_columns('users')}
            password_column = columns.get('password')

            if not password_column:
                raise RuntimeError("Column 'password' was not found in table 'users'")

            current_length = getattr(password_column['type'], 'length', None)
            Log.info(f'Current users.password length: {current_length}')

            if current_length is not None and current_length >= 255:
                Log.info('Column users.password already supports 255 characters. Migration not needed.')
                return

            dialect = db.engine.dialect.name
            Log.info(f'Applying migration for dialect: {dialect}')

            with db.engine.connect() as conn:
                if dialect == 'postgresql':
                    conn.execute(db.text('ALTER TABLE users ALTER COLUMN password TYPE VARCHAR(255)'))
                elif dialect == 'sqlite':
                    Log.info('SQLite does not enforce VARCHAR length strictly. Migration not required.')
                    return
                else:
                    raise RuntimeError(f'Unsupported database dialect for this migration: {dialect}')

                conn.commit()

            Log.info('***** User password length migration completed successfully! *****')

    except Exception as err:
        Log.error('Migration failed', err=err, sys=sys)
        raise


if __name__ == '__main__':
    migrate_database()