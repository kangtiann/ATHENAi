import logging

from statemachine import StateMachine, State, Event
from models.memory import Vision, Status, Id, Events, Priority
from util.time import get_now_unixtime

class VisionSM(StateMachine):
    "Vision State Machine"

    logger = logging.getLogger("VisionSM")

    # db instance
    inst = None

    # props
    id = ""
    vision = ""
    vision_desc = ""
    propose_by = ""
    propose_time = None
    update_time = None
    finish_time = None
    priority = Priority.LOW
    tags = ""

    # states
    s_init = State(value=Status.INIT, initial=True)
    s_assigned = State(value=Status.ASSIGNED)
    s_doing = State(value=Status.DOING)
    s_done = State(value=Status.DONE, final=True)
    s_fail = State(value=Status.FAIL)
    s_cancel = State(value=Status.CANCEL)
    s_suspended = State(value=Status.SUSPENDED)
    s_resumed = State(value=Status.RESUMED)

    cycle = (
        s_init.to(s_assigned, event=Events.ASSIGN)
        | s_assigned.to(s_doing, event=Events.START)
        | s_init.to(s_doing, event=Events.START)
        | s_doing.to(s_fail, event=Events.FAIL)
        | s_doing.to(s_cancel, event=Events.CANCEL)
        | s_doing.to(s_suspended, event=Events.SUSPEND)
        | s_suspended.to(s_resumed, event=Events.RESUME)
        | s_resumed.to(s_assigned, event=Events.ASSIGN)
        | s_resumed.to(s_doing, event=Events.START)
        | s_fail.to(s_init, event=Events.RETRY)
        | s_cancel.to(s_init, event=Events.RETRY)
        | s_doing.to(s_done, event=Events.DONE)
    )

    def __init__(self, vision, start_value=Status.INIT):
        super().__init__(start_value=start_value)
        self.vision = vision
        if not self.id:
            self.id = Id.new_id()
    
    @property
    def state(self):
        return self.current_state.value
    
    @staticmethod
    def from_model(inst, id=None):
        """
        从数据库中加载vision状态机
        """

        if inst is None and id is not None:
            inst = Vision.get_or_none(Vision.id == id)
        if inst is None:
            raise Exception("VisionSM.from_model, vision not found, id: %s" % id)
        instance = VisionSM(vision=inst.vision, start_value=inst.status)
        instance.inst = inst
        instance.vision = inst.vision
        instance.vision_desc = inst.vision_desc
        instance.propose_by = inst.propose_by
        instance.propose_time = inst.propose_time
        instance.update_time = inst.update_time
        instance.finish_time = inst.finish_time
        instance.priority = inst.priority
        instance.tags = inst.tags
        instance.id = inst.id
        return instance

    def save_model(self):
        "save vision to db"

        if self.inst is None:
            values = Vision.get_defaults()
            values.update(dict(vision=self.vision, id=self.id))
            self.inst = Vision.create(**values)
        self.inst.vision_desc = self.vision_desc
        self.inst.propose_by = self.propose_by
        self.inst.priority = self.priority
        self.inst.tags = self.tags
        self.inst.status = self.state
        self.inst.update_time = get_now_unixtime()
        if self.state == Status.DONE and self.inst.finish_time == 0:
            self.inst.finish_time = get_now_unixtime()
        save_rows = self.inst.save()
        if save_rows <= 0:
            raise Exception("VisionSM.save_model, save vision failed")

    def on_transition(self, event_data, event):
        assert event_data.event == event
        msg = "Running Event(%s) from state:%s to state:%s" % (event.name, event_data.transition.source.id, event_data.transition.target.id)
        print(msg)
        self.save_model()
        return (msg)

