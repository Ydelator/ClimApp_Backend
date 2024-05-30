from typing import List
from app.models import Task

# Datos de ejemplo
tasks = [
    Task(id=1, title='Comprar comida', description='Leche, Queso, Pan', done=False),
    Task(id=2, title='Aprender Python', description='Necesito aprender FastAPI para hacer una API', done=False)
]


def get_tasks() -> List[Task]:
    return tasks


def get_task(task_id: int) -> Task:
    return next((task for task in tasks if task.id == task_id), None)


def create_task(task: Task) -> Task:
    task.id = tasks[-1].id + 1 if tasks else 1
    tasks.append(task)
    return task


def update_task(task_id: int, updated_task: Task) -> Task:
    task = get_task(task_id)
    if task:
        task.title = updated_task.title
        task.description = updated_task.description
        task.done = updated_task.done
    return task


def delete_task(task_id: int) -> bool:
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    return True
