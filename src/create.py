from sqlalchemy import select

from connect import Session
from models import Tasks


def create_task(task: Tasks, session: Session):
    statement = select(Tasks).where(Tasks.name == task.name)
    result = session.scalar(statement)
    if not result:
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"message": "success"}
    return {"message": "Task with tha same name already exists"}



