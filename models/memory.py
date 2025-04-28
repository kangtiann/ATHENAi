# -*- coding: UTF-8 -*-

import uuid
from typing import List, Tuple
from .db import db
from peewee import *
from util.time import get_now_unixtime


class BaseModel(Model):
    class Meta:
        database = db
        legacy_table_names = False


class Vision(BaseModel):
    id = CharField(primary_key=True)
    vision = CharField(index=True, unique=True)
    vision_desc = TextField()
    status = CharField(index=True)
    priority = CharField(index=True)
    tags = CharField()
    propose_by = CharField(index=True)
    propose_time = IntegerField()
    update_time = IntegerField()
    finish_time = IntegerField()

    @staticmethod
    def get_defaults():
        return dict(
            id=Id.new_id(),
            vision_desc = "",
            status = Status.INIT,
            priority = Priority.LOW,
            tags = "",
            propose_by = "",
            propose_time = get_now_unixtime(),
            update_time = get_now_unixtime(),
            finish_time = 0
        )


class VisionProgress(BaseModel):
    id = CharField(primary_key=True)
    vision = ForeignKeyField(Vision, backref='progress', on_delete='CASCADE')
    propose_by = CharField(index=True)
    propose_time = IntegerField()
    title = TextField()
    content = TextField()


class Research(BaseModel):
    id = CharField(primary_key=True)
    research = CharField(index=True, unique=True)
    research_desc = TextField()
    vision = ForeignKeyField(Vision, backref='research', on_delete='CASCADE')
    result = TextField()
    report_path = CharField()
    status = CharField(index=True)
    priority = CharField(index=True)
    tags = CharField()
    propose_by = CharField(index=True)
    propose_time = IntegerField()
    update_time = IntegerField()
    finish_time = IntegerField()

    @staticmethod
    def get_defaults():
        return dict(
            id=Id.new_id(),
            research_desc = "",
            status = Status.INIT,
            priority = Priority.LOW,
            result = "",
            report_path = "",
            tags = "",
            propose_by = "",
            propose_time = get_now_unixtime(),
            update_time = get_now_unixtime(),
            finish_time = 0
        )


class ResearchProgress(BaseModel):
    id = CharField(primary_key=True)
    research = ForeignKeyField(Research, backref='progress', on_delete='CASCADE')
    propose_by = CharField(index=True)
    propose_time = IntegerField()
    title = TextField()
    content = TextField()


class Deepthink(BaseModel):
    id = CharField(primary_key=True)
    deepthink = CharField(index=True)
    deepthink_desc = TextField()
    research = ForeignKeyField(Research, backref='deepthink', on_delete='CASCADE')
    result = TextField()
    status = CharField(index=True)
    priority = CharField(index=True)
    tags = CharField()
    propose_by = CharField(index=True)
    propose_time = IntegerField()
    update_time = IntegerField()
    finish_time = IntegerField()
    
    @staticmethod
    def get_defaults():
        return dict(
            id=Id.new_id(),
            deepthink_desc = "",
            status = Status.INIT,
            priority = Priority.LOW,
            result = "",
            tags = "",
            propose_by = "",
            propose_time = get_now_unixtime(),
            update_time = get_now_unixtime(),
            finish_time = 0
        )


class DeepthinkProgress(BaseModel):
    id = CharField(primary_key=True)
    deepthink = ForeignKeyField(Deepthink, backref='progress', on_delete='CASCADE')
    propose_by = CharField(index=True)
    propose_time = IntegerField()
    title = TextField()
    content = TextField()


class Task(BaseModel):
    id = CharField(primary_key=True)
    task = CharField(index=True)
    task_desc = TextField()
    deepthink = ForeignKeyField(Deepthink, backref='task', on_delete='CASCADE')
    result = TextField()
    status = CharField(index=True)
    summary = TextField()
    propose_time = IntegerField()
    update_time = IntegerField()
    finish_time = IntegerField()

    @staticmethod
    def get_defaults():
        return dict(
            id=Id.new_id(),
            task_desc = "",
            result = "",
            status = Status.INIT,
            priority = Priority.LOW,
            summary = "",
            propose_time = get_now_unixtime(),
            update_time = get_now_unixtime(),
            finish_time = 0
        )


class Resource(BaseModel):
    id = CharField(primary_key=True)
    title = CharField(index=True)
    task = ForeignKeyField(Task, backref='resource', on_delete='CASCADE')
    res_type = CharField(index=True)
    url_links = CharField()
    local_path = CharField(index=True)
    summary = TextField()


class LLMChatHistory(BaseModel):
    id = CharField(primary_key=True)
    vision = ForeignKeyField(Vision, backref='chat_history', on_delete='CASCADE')
    propose_by = CharField(index=True)
    message = TextField()
    propose_time = IntegerField()
    cost_ms = IntegerField()
    tags = CharField()


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
    PROPOSED = "proposed"
    REJECTED_PROPOSAL = "rejected_proposal"

    COMMITTED = "committed"
    IMPERFECT_COMMIT = "imperfect_commit"
    ACCEPTED_COMMIT = "accepted_commit"
    REJECTED_COMMIT = "rejected_commit"
    ACCEPTED_BY_HUMEN = "accepted_by_humen"
    REJECTED_BY_HUMEN = "rejected_by_humen"


class ResourceType:
    PDF = "pdf"
    HTML = "html"
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    CODE = "code"
    CARD = "card"  # 知识卡片


class Events:
    READY = "ready" # 已准备好
    ASSIGN = "assign"
    START = "start"
    FAIL = "fail"
    CANCEL = "cancel"
    SUSPEND = "suspend"
    RESUME = "resume"
    RETRY = "retry"
    DONE = "done"
    
    PROPOSAL = "proposal" # 提案
    ACCEPT_PROPOSAL = "accept_proposal" # 接受提案
    REJECT_PROPOSAL = "reject_proposal" # 拒绝提案
    
    COMMIT = "commit" # 提交初步结果
    IMPERFECT_COMMIT = "imperfect_commit" # 超过提交次数，Alice 认定为不完美提交
    ACCEPT_COMMIT = "accept_commit" # Alice 接受提交
    REJECT_COMMIT = "reject_commit" # Alice 拒绝提交
    
    ACCEPT_BY_HUMEN = "accept_by_humen" # 人类接受提交
    REJECT_BY_HUMEN = "reject_by_humen" # 人类拒绝提交


class Priority:
    HIGH = "high"
    MIDDLE = "middle"
    LOW = "low"


class ProposalBy:
    HUMEN = "humen"
    ALICE = "alice"
    THINKER = "thinker"
    LLM = "LLM"


class Id:
    @staticmethod
    def new_id():
        return str(uuid.uuid4())
