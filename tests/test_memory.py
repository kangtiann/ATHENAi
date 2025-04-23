import pytest
from memory.vision import VisionSM
from memory.research import ResearchSM
from memory.deepthink import DeepthinkSM
from memory.task import TaskSM
from models.memory import Vision, Research, Deepthink

def test_vision_sm():
    # Create a new VisionSM object
    vision_sm = VisionSM("成为 AI 专家")

    # vision_sm.send("assign")

    vision_sm.send("start")

    print("vision_sm state: ", vision_sm.current_state)

    vision_sm.save_model()

    vision_id = vision_sm.id

    new_vision_sm = VisionSM.from_model(db_model=None, id=vision_id)
    
    print("new_vision_sm state: ", new_vision_sm.state)
    new_vision_sm.send("done")

def test_research_sm():
    vision = Vision.select().where(Vision.vision == "成为 AI 专家").get()
    research_sm = ResearchSM("Transformer 架构如何实现高效的并行计算？", vision_id=vision.id)
    research_sm.send("start")

    print("research_sm state: ", research_sm.current_state)

    research_sm.save_model()

    research_id = research_sm.id

    new_research_sm = ResearchSM.from_model(db_model=None, id=research_id)
    
    print("new_research_sm state: ", new_research_sm.state)
    new_research_sm.result = "Transformer 架构如何实现高效的并行计算的方式包括 1. 多头注意力机制 2. 位置编码 3. 残差网络 4. 层归一化"
    new_research_sm.send("done")

def test_deepthink_sm():
    research = Research.select().where(Research.research == "Transformer 架构如何实现高效的并行计算？").get()
    deepthink_sm = DeepthinkSM("多头注意力为何可以进行高效并行计算？", research_id=research.id)
    deepthink_sm.send("start")

    print("deepthink_sm state: ", deepthink_sm.current_state)

    deepthink_sm.save_model()

    deepthink_id = deepthink_sm.id

    new_deepthink_sm = DeepthinkSM.from_model(db_model=None, id=deepthink_id)
    
    print("new_deepthink_sm state: ", new_deepthink_sm.state)
    new_deepthink_sm.result = "多头注意力可以进行高效的并行计算，因为多个头没有耦合，在计算是是可以并行计算的，因此可以高效并行计算"
    new_deepthink_sm.send("done")


def test_task_sm():
    deepthink = Deepthink.select().where(Deepthink.deepthink == "多头注意力为何可以进行高效并行计算？").get()
    task_sm = TaskSM("分析 Attention is all your need 论文", deepthink_id=deepthink.id)
    task_sm.send("start")

    print("task_sm state: ", task_sm.current_state)

    task_sm.save_model()

    task_id = task_sm.id

    new_task_sm = TaskSM.from_model(db_model=None, id=task_id)
    
    print("new_task_sm state: ", new_task_sm.state)
    new_task_sm.result = "Attention is all your need 论文中提到，多头注意力实现的细节包括 xxxx"
    new_task_sm.summary = "通过分析 Attention is all your need 论文，发现了以下结论：1. 多头注意力可以实现高效的并行计算 2. xxx"
    new_task_sm.send("done")


if __name__ == "__main__":
    test_vision_sm()
