from datetime import datetime,timezone
from sqlalchemy import String,Column,Integer
from sqlalchemy.dialects.sqlite import BOOLEAN
from system.db import db

class Task(db.Model):
    id = Column("id",Integer,primary_key=True,autoincrement=True)
    task_id = Column("task_id",String,unique=True)
    name = Column("name",String)
    link = Column("url",String)
    state = Column("state",BOOLEAN,default=False)