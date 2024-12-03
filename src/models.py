from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pass



class Tasks(Base):
    __tablename__ = "Tasks"
    name: Mapped[str] = mapped_column(String(30))
    value: Mapped[str] = mapped_column(String(100))

class Users(Base):
    __tablename__ = "Users"
    login: Mapped[str] = mapped_column(String(30))
    token: Mapped[str] = mapped_column(String(30))