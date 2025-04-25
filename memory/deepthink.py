import logging

from statemachine import StateMachine, State, Event
from models.memory import Deepthink, Priority, Status, Id, Events
from util.time import get_now_unixtime

class DeepthinkSM(StateMachine):
    "Deepthink State Machine"

    logger = logging.getLogger("DeepthinkSM")

    # db instance
    db_model = None

    # props
    id = ""
    deepthink = ""
    result = ""
    research_id = None
    propose_by = ""
    propose_time = get_now_unixtime()
    update_time = get_now_unixtime()
    finish_time = 0
    priority = Priority.LOW
    tags = ""

    # states
    s_init = State(value=Status.INIT, initial=True)
    s_ready = State(value=Status.READY)
    s_assigned = State(value=Status.ASSIGNED)
    s_doing = State(value=Status.DOING)
    s_fail = State(value=Status.FAIL)
    s_cancel = State(value=Status.CANCEL)
    s_suspended = State(value=Status.SUSPENDED)
    s_resumed = State(value=Status.RESUMED)
    s_proposed = State(value=Status.PROPOSED)
    s_done = State(value=Status.DONE, final=True)

    cycle = (
        s_init.to(s_ready, event=Events.READY)
        | s_init.to(s_proposed, event=Events.PROPOSAL)
        | s_proposed.to(s_ready, event=Events.ACCEPT_PROPOSAL)
        | s_ready.to(s_assigned, event=Events.ASSIGN)
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


    def __init__(self, deepthink, research_id, start_value=Status.INIT):
        super().__init__(start_value=start_value)
        self.deepthink = deepthink
        self.research_id = research_id
        if not self.id:
            self.id = Id.new_id()
    
    @property
    def state(self):
        return self.current_state.value
    
    @staticmethod
    def from_model(db_model, id=None):
        """
        从数据库中加载deepthink状态机
        """

        if db_model is None and id is not None:
            db_model = Deepthink.get_or_none(Deepthink.id == id)
        if db_model is None:
            raise Exception("DeepthinkSM.from_model, deepthink not found, id: %s" % id)
        instance = DeepthinkSM(deepthink=db_model.deepthink, research_id=db_model.research, start_value=db_model.status)
        instance.db_model = db_model
        instance.deepthink = db_model.deepthink
        instance.result = db_model.result
        instance.propose_by = db_model.propose_by
        instance.propose_time = db_model.propose_time
        instance.update_time = db_model.update_time
        instance.finish_time = db_model.finish_time
        instance.priority = db_model.priority
        instance.tags = db_model.tags
        instance.id = db_model.id
        return instance

    def save_model(self):
        "save deepthink to db"

        if self.db_model is None:
            self.db_model = Deepthink.create(
                id = self.id,
                deepthink = self.deepthink,
                research = self.research_id,
                status = self.state,
                priority = self.priority,
                tags = self.tags,
                result = self.result,
                propose_by = self.propose_by,
                propose_time = self.propose_time,
                update_time = self.update_time,
                finish_time = self.finish_time,
            )
        self.db_model.propose_by = self.propose_by
        self.db_model.priority = self.priority
        self.db_model.tags = self.tags
        self.db_model.result = self.result
        self.db_model.status = self.state
        self.db_model.update_time = get_now_unixtime()
        if self.state == Status.DONE and self.db_model.finish_time == 0:
            self.db_model.finish_time = get_now_unixtime()
        save_rows = self.db_model.save()
        if save_rows <= 0:
            raise Exception("DeepthinkSM.save_model, save deepthink failed")

    def on_transition(self, event_data, event):
        assert event_data.event == event
        if event.name == "done":
            if not self.result:
                raise Exception("DeepthinkSM.on_transition, when 'done', result MUST NOT be empty")
        msg = "Running Event(%s) from state:%s to state:%s" % (event.name, event_data.transition.source.id, event_data.transition.target.id)
        print(msg)
        self.save_model()
        return (msg)

