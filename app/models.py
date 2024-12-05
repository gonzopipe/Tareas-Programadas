from fpdf import FPDF
from io import BytesIO
from app import db
import pandas as pd

# Definición del modelo de la tabla 'tasks'
class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)  # ID único y autoincremental
    name = db.Column(db.String(255), nullable=False)  # Nombre de la tarea
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # Fecha de creación
    due_date = db.Column(db.DateTime, nullable=True)  # Nueva columna para la fecha límite

    def __repr__(self):
        """
        Representación en cadena del modelo para depuración.
        """
        return f"<Task {self.name}>"

# Función para obtener todas las tareas
def get_tasks():
    """
    Obtiene todas las tareas de la base de datos.
    """
    return Task.query.order_by(Task.created_at.desc()).all()

# Función para agregar una tarea
def add_task(name):
    """
    Agrega una nueva tarea a la tabla 'tasks'.
    """
    new_task = Task(name=name)
    db.session.add(new_task)
    db.session.commit()

# Función para eliminar una tarea
def delete_task(task_id):
    """
    Elimina una tarea específica de la tabla 'tasks' usando su ID.
    """
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()

def generate_pdf(tasks):
    """
    Genera un archivo PDF con la lista de tareas en memoria.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Reporte de Tareas", ln=True, align='C')
    pdf.ln(10)

    for i, task in enumerate(tasks, start=1):
        pdf.cell(0, 10, txt=f"{i}. {task.name} (Creada el: {task.created_at})", ln=True)

    # Generar el PDF como un string binario y guardarlo en BytesIO
    pdf_buffer = BytesIO()
    pdf_content = pdf.output(dest="S").encode("latin1")  # Genera el contenido binario del PDF
    pdf_buffer.write(pdf_content)
    pdf_buffer.seek(0)  # Mover el puntero al inicio del buffer

    return pdf_buffer

def generate_excel(tasks):
    """
    Genera un archivo Excel con la lista de tareas en memoria.
    """
    data = [{"ID": task.id, "Nombre": task.name, "Fecha de Creación": task.created_at} for task in tasks]
    df = pd.DataFrame(data)

    # Generar el Excel en memoria
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    excel_buffer.seek(0)  # Mover el puntero al inicio del buffer

    return excel_buffer
