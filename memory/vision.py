import logging

from statemachine import StateMachine, State, Event
from models.memory import Vision, Status, Id, Events, Priority
from util.time import get_now_unixtime

class VisionSM(StateMachine):
    "Vision State Machine"

    logger = logging.getLogger("VisionSM")

    # db instance
    db_model = None

    # props
    id = ""
    vision = ""
    propose_by = ""
    propose_time = None
    update_time = None
    finish_time = None
    priority = Priority.LOW

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
    def from_model(db_model, id=None):
        """
        从数据库中加载vision状态机
        """

        if db_model is None and id is not None:
            db_model = Vision.get_or_none(Vision.id == id)
        if db_model is None:
            raise Exception("VisionSM.from_model, vision not found, id: %s" % id)
        instance = VisionSM(vision=db_model.vision, start_value=db_model.status)
        instance.db_model = db_model
        instance.vision = db_model.vision
        instance.propose_by = db_model.propose_by
        instance.propose_time = db_model.propose_time
        instance.update_time = db_model.update_time
        instance.finish_time = db_model.finish_time
        instance.priority = db_model.priority
        instance.id = db_model.id
        return instance

    def save_model(self):
        "save vision to db"

        if self.db_model is None:
            self.db_model = Vision.create(
                id = self.id,
                vision = self.vision,
                status = self.state,
                priority = self.priority,
                propose_by = self.propose_by,
                propose_time = get_now_unixtime(),
                update_time = get_now_unixtime(),
                finish_time = 0,
            )
        self.db_model.propose_by = self.propose_by
        self.db_model.priority = self.priority
        self.db_model.status = self.state
        self.db_model.update_time = get_now_unixtime()
        if self.state == Status.DONE and self.db_model.finish_time == 0:
            self.db_model.finish_time = get_now_unixtime()
        save_rows = self.db_model.save()
        if save_rows <= 0:
            raise Exception("VisionSM.save_model, save vision failed")

    def on_transition(self, event_data, event):
        assert event_data.event == event
        msg = "Running Event(%s) from state:%s to state:%s" % (event.name, event_data.transition.source.id, event_data.transition.target.id)
        print(msg)
        self.save_model()
        return (msg)

