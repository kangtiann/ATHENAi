# -*- coding: UTF-8 -*-

import uuid
from typing import List, Tuple
from .db import db
from peewee import *


class BaseModel(Model):
    class Meta:
        database = db
        legacy_table_names = False


class Vision(BaseModel):
    id = CharField(primary_key=True)
    vision = CharField(index=True, unique=True)
    status = CharField(index=True)
    priority = CharField(index=True)
    propose_by = CharField(index=True)
    propose_time = IntegerField()
    update_time = IntegerField()
    finish_time = IntegerField()


class VisionProgress(BaseModel):
    id = CharField(primary_key=True)
    vision = ForeignKeyField(Vision, backref='progress', on_delete='CASCADE')
    content = TextField()
    summary = TextField()
    update_time = IntegerField()


class Research(BaseModel):
    id = CharField(primary_key=True)
    research = CharField(index=True, unique=True)
    vision = ForeignKeyField(Vision, backref='research', on_delete='CASCADE')
    result = TextField()
    report_path = CharField()
    status = CharField(index=True)
    priority = CharField(index=True)
    propose_by = CharField(index=True)
    propose_time = IntegerField()
    update_time = IntegerField()
    finish_time = IntegerField()


class ResearchProgress(BaseModel):
    id = CharField(primary_key=True)
    research = ForeignKeyField(Research, backref='progress', on_delete='CASCADE')
    content = TextField()
    summary = TextField()
    update_time = IntegerField()


class Deepthink(BaseModel):
    id = CharField(primary_key=True)
    deepthink = CharField(index=True)
    research = ForeignKeyField(Research, backref='deepthink', on_delete='CASCADE')
    result = TextField()
    status = CharField(index=True)
    priority = CharField(index=True)
    propose_by = CharField(index=True)
    propose_time = IntegerField()
    update_time = IntegerField()
    finish_time = IntegerField()


class DeepthinkProgress(BaseModel):
    id = CharField(primary_key=True)
    deepthink = ForeignKeyField(Deepthink, backref='progress', on_delete='CASCADE')
    content = TextField()
    summary = TextField()
    update_time = IntegerField()


class Task(BaseModel):
    id = CharField(primary_key=True)
    task_desc = CharField(index=True)
    deepthink = ForeignKeyField(Deepthink, backref='task', on_delete='CASCADE')
    result = TextField()
    status = CharField(index=True)
    summary = TextField()
    propose_time = IntegerField()
    update_time = IntegerField()
    finish_time = IntegerField()


class Resource(BaseModel):
    id = CharField(primary_key=True)
    title = CharField(index=True)
    task = ForeignKeyField(Task, backref='resource', on_delete='CASCADE')
    res_type = CharField(index=True)
    url_links = CharField()
    local_path = CharField(index=True)
    summary = TextField()


# Maybe 这个存图数据库
class EntityGraphModel:
    id: str
    entity: str
    desc: str
    # 关系, 关联实体
    rel = ""


class Status:
    INIT = "init"
    READY = "ready"
    ASSIGNED = "assigned"
    DOING = "doing"
    DONE = "done"
    FAIL = "fail"
    CANCEL = "cancel"
    SUSPENDED = "suspended"
    RESUMED = "resumed"
    PROPOSAL = "proposal"


class ResourceType:
    PDF = "pdf"
    HTML = "html"
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    CODE = "code"


class Events:
    READY = "ready"
    ASSIGN = "assign"
    START = "start"
    FAIL = "fail"
    CANCEL = "cancel"
    SUSPEND = "suspend"
    RESUME = "resume"
    RETRY = "retry"
    DONE = "done"
    PROPOSAL = "proposal"
    ACCEPT = "accept"


class Priority:
    HIGH = "high"
    MIDDLE = "middle"
    LOW = "low"


class Id:
    @staticmethod
    def new_id():
        return str(uuid.uuid4())
