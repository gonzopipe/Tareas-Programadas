# -*- coding: utf-8 -*-

from app import create_app, db
from app.models import add_task, get_tasks, delete_task
from flask_migrate import upgrade
import os

app = create_app()
app.app_context().push()

# Asegurarse de que las migraciones se aplican al iniciar la aplicación
with app.app_context():
    # Ejecutar las migraciones para crear la base de datos si es necesario
    if not os.path.exists('task_manager.db'):
        db.create_all()  # Este método asegura que la base de datos se cree si no existe

if __name__ == "__main__":
    app.run(debug=True)
