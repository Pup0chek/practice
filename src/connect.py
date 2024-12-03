from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

engine = create_engine('sqlite:///database.db')
engine.echo = True

Session = sessionmaker(engine, expire_on_commit=False)

Base.metadata.create_all(engine)