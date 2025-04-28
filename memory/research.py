import logging

from statemachine import StateMachine, State, Event
from models.memory import Research, Status, Id, Events, Priority
from util.time import get_now_unixtime

class ResearchSM(StateMachine):
    "Research State Machine"

    logger = logging.getLogger("ResearchSM")

    # db instance
    inst = None

    # props
    id = ""
    research = ""
    research_desc = ""
    result = ""
    report_path = ""
    vision_id = None
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
    s_rejected_proposal = State(value=Status.REJECTED_PROPOSAL, final=True)
    s_done = State(value=Status.DONE, final=True)


    cycle = (
        s_init.to(s_ready, event=Events.READY)
        | s_init.to(s_proposed, event=Events.PROPOSAL)
        | s_proposed.to(s_ready, event=Events.ACCEPT_PROPOSAL)
        | s_proposed.to(s_rejected_proposal, event=Events.REJECT_PROPOSAL)
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

    def __init__(self, research, vision_id, start_value=Status.INIT):
        super().__init__(start_value=start_value)
        self.research = research
        self.vision_id = vision_id
        if not self.id:
            self.id = Id.new_id()
    
    @property
    def state(self):
        return self.current_state.value
    
    @staticmethod
    def from_model(inst, id=None):
        """
        从数据库中加载research状态机
        """

        if inst is None and id is not None:
            inst = Research.get_or_none(Research.id == id)
        if inst is None:
            raise Exception("ResearchSM.from_model, research not found, id: %s" % id)
        instance = ResearchSM(research=inst.research, vision_id=inst.vision, start_value=inst.status)
        instance.inst = inst
        instance.research = inst.research
        instance.research_desc = inst.research_desc
        instance.result = inst.result
        instance.report_path = inst.report_path
        instance.propose_by = inst.propose_by
        instance.propose_time = inst.propose_time
        instance.update_time = inst.update_time
        instance.finish_time = inst.finish_time
        instance.priority = inst.priority
        instance.tags = inst.tags
        instance.id = inst.id
        return instance

    def save_model(self):
        "save research to db"

        if self.inst is None:
            values = Research.get_defaults()
            values.update(dict(
                id = self.id,
                research = self.research,
                vision=self.vision_id
            ))
            self.inst = Research.create(**values)
        self.inst.research_desc = self.research_desc
        self.inst.propose_by = self.propose_by
        self.inst.priority = self.priority
        self.inst.tags = self.tags
        self.inst.result = self.result
        self.inst.report_path = self.report_path
        self.inst.status = self.state
        self.inst.update_time = get_now_unixtime()
        if self.state == Status.DONE and self.inst.finish_time == 0:
            self.inst.finish_time = get_now_unixtime()
        save_rows = self.inst.save()
        if save_rows <= 0:
            raise Exception("ResearchSM.save_model, save research failed")

    def on_transition(self, event_data, event):
        assert event_data.event == event
        if event.name == "done":
            if not self.result:
                raise Exception("ResearchSM.on_transition, when 'done', result MUST NOT be empty")
        msg = "Running Event(%s) from state:%s to state:%s" % (event.name, event_data.transition.source.id, event_data.transition.target.id)
        print(msg)
        self.save_model()
        return (msg)

