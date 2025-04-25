from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.memory import Vision, Research, Deepthink, Task, Resource, VisionProgress, ResearchProgress, DeepthinkProgress

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LIMIT_ROWS = 10000

@app.get("/api/v1/vision")
def get_vision():
    records = list(Vision.select().limit(LIMIT_ROWS).dicts())
    return records


@app.get("/api/v1/research")
def get_research(vision: Union[str, None] = None):
    if vision is None:
        records = list(Research.select().limit(LIMIT_ROWS).dicts())
    else:
        records = list(Research.select().where(Research.vision == vision).limit(LIMIT_ROWS).dicts())
    return records


@app.get("/api/v1/deepthink")
def get_deepthink(research: Union[str, None] = None):
    if research is None:
        records = list(Deepthink.select().limit(LIMIT_ROWS).dicts())
    else:
        records = list(Deepthink.select().where(Deepthink.research == research).limit(LIMIT_ROWS).dicts())
    return records


@app.get("/api/v1/task")
def get_task(deepthink: Union[str, None] = None):
    if deepthink is None:
        records = list(Task.select().limit(LIMIT_ROWS).dicts())
    else:
        records = list(Task.select().where(Task.research == deepthink).limit(LIMIT_ROWS).dicts())
    return records
