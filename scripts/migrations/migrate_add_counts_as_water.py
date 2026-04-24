#!/usr/bin/env python3
# Migration script to add counts_as_water column to drinks table

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from falken_drinks.app import create_app, settings
from falken_drinks.models import db
from falken_drinks.logger import Log

def migrate_database():
    """Add counts_as_water column to drinks table"""
    try:
        Log.info("***** Starting database migration *****")
        
        # Create app context
        app = create_app(settings.CONFIG_ENV[settings.CONFIG_MODE])
        
        with app.app_context():
            # Check if column already exists
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('drinks')]
            
            if 'counts_as_water' in columns:
                Log.info("Column 'counts_as_water' already exists. Migration not needed.")
                return
            
            Log.info("Adding 'counts_as_water' column to drinks table...")
            
            # Add the new column with a default value
            # For SQLite, we need to use ALTER TABLE
            with db.engine.connect() as conn:
                # Add column with default True
                conn.execute(db.text(
                    "ALTER TABLE drinks ADD COLUMN counts_as_water BOOLEAN NOT NULL DEFAULT 1"
                ))
                conn.commit()
                
                Log.info("Column added successfully!")
                
                # Update existing rows: set counts_as_water to False where alcohol > 0
                Log.info("Updating existing drinks with alcohol to counts_as_water=False...")
                result = conn.execute(db.text(
                    "UPDATE drinks SET counts_as_water = 0 WHERE drink_alcohol_percentage > 0"
                ))
                conn.commit()
                
                Log.info(f"Updated {result.rowcount} alcoholic drinks")
                
            Log.info("***** Migration completed successfully! *****")
            
    except Exception as e:
        Log.error("Migration failed", err=e, sys=sys)
        raise

if __name__ == '__main__':
    migrate_database()
