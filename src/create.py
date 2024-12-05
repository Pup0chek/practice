from celery.states import state
from sqlalchemy import select

from connect import Session
from models import Tasks, Users


def create_task(task: Tasks, session: Session):
    statement = select(Tasks).where(Tasks.name == task.name)
    result = session.scalar(statement)
    if not result:
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"message": "success"}
    return {"message": "Task with tha same name already exists"}


def get_task(name:str, session):
    statement = select(Tasks).where(Tasks.name == name)
    result = session.scalar(statement)
    return result.value

def create_user(user: Users, session):
    statement = select(Users).where(Users.login == user.login)
    result = session.scalar(statement)
    if not result:
        session.add(user)
        return {"success"}
    return {"users with the same name already exist"}
