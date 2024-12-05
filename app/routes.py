from flask import Blueprint, render_template, request, redirect, url_for, send_file, flash
from app.models import get_tasks, add_task, delete_task, generate_pdf, generate_excel, db, Task
import pandas as pd
from fpdf import FPDF
from io import BytesIO
from datetime import datetime


# Crear un Blueprint para las rutas
routes = Blueprint('routes', __name__)

# Ruta para la página principal (lista de tareas)
@routes.route('/')
def home():
    tasks = Task.query.all()
    for task in tasks:
        if task.due_date and task.due_date < datetime.utcnow():
            task.is_overdue = True  # Añade un atributo temporal para tareas vencidas
    return render_template('task.html', tasks=tasks)

# Ruta para agregar una nueva tarea
@routes.route('/add', methods=['POST'])
def add_task():
    task_name = request.form['task']
    new_task = Task(name=task_name)
    db.session.add(new_task)
    db.session.commit()
    flash('Tarea agregada exitosamente!')
    return redirect(url_for('routes.home'))  # Redirige a la página principal

# Ruta para eliminar una tarea
@routes.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    """
    Elimina una tarea específica por ID.
    """
    delete_task(task_id)
    return redirect(url_for('routes.home'))

@routes.route('/download/pdf', methods=['GET'])
def download_pdf():
    tasks = get_tasks()  # Obtener las tareas
    pdf_buffer = generate_pdf(tasks)  # Generar el PDF en memoria
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name="reporte_tareas.pdf",
        mimetype="application/pdf"
    )


@routes.route('/download/excel', methods=['GET'])
def download_excel():
    tasks = get_tasks()  # Obtener las tareas
    excel_buffer = generate_excel(tasks)  # Generar el Excel en memoria
    return send_file(
        excel_buffer,
        as_attachment=True,
        download_name="reporte_tareas.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
