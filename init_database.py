from models.db import db
from models.memory import Vision, Research, Deepthink, Task, Resource, VisionProgress, ResearchProgress, DeepthinkProgress, LLMChatHistory


def create_tables():
    db.connect()
    db.create_tables([Vision, Research, Deepthink, 
                      Task, Resource, VisionProgress, 
                      ResearchProgress, DeepthinkProgress, LLMChatHistory])

if __name__ == "__main__":
    create_tables()
