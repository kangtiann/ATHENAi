from pydantic import BaseModel, Field

class VisionModel(BaseModel):
    vision: str
    vision_desc: str = Field(default=None)
    status: str = Field(default=None)


class ResearchModel(BaseModel):
    research: str
    research_desc: str = Field(default=None)
    status: str = Field(default=None)


class DeepthinkModel(BaseModel):
    deepthink: str
    deepthink_desc: str = Field(default=None)
    status: str = Field(default=None)


class TaskModel(BaseModel):
    task: str
    task_desc: str = Field(default=None)
    status: str = Field(default=None)