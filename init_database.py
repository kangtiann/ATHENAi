from models.memory import db, Vision, Research, Deepthink, Task, Resource, VisionProgress, ResearchProgress, DeepthinkProgress


def create_tables():
    db.connect()
    db.create_tables([Vision, Research, Deepthink, 
                      Task, Resource, VisionProgress, 
                      ResearchProgress, DeepthinkProgress])

if __name__ == "__main__":
    create_tables()
