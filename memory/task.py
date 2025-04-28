import logging

from statemachine import StateMachine, State, Event
from models.memory import Task, Status, Id, Events
from util.time import get_now_unixtime

class TaskSM(StateMachine):
    "Task State Machine"

    logger = logging.getLogger("TaskSM")

    # db instance
    inst = None

    # props
    id = ""
    task = ""
    task_desc = ""
    result = ""
    summary = ""
    deepthink_id = None
    propose_time = get_now_unixtime()
    update_time = get_now_unixtime()
    finish_time = 0

    # states
    s_init = State(value=Status.INIT, initial=True)
    s_assigned = State(value=Status.ASSIGNED)
    s_doing = State(value=Status.DOING)
    s_done = State(value=Status.DONE, final=True)
    s_fail = State(value=Status.FAIL)
    s_cancel = State(value=Status.CANCEL)

    cycle = (
        s_init.to(s_assigned, event=Events.ASSIGN)
        | s_assigned.to(s_doing, event=Events.START)
        | s_init.to(s_doing, event=Events.START)
        | s_doing.to(s_fail, event=Events.FAIL)
        | s_doing.to(s_cancel, event=Events.CANCEL)
        | s_fail.to(s_init, event=Events.RETRY)
        | s_cancel.to(s_init, event=Events.RETRY)
        | s_doing.to(s_done, event=Events.DONE)
    )

    def __init__(self, task, deepthink_id, start_value=Status.INIT):
        super().__init__(start_value=start_value)
        self.task = task
        self.deepthink_id = deepthink_id
        if not self.id:
            self.id = Id.new_id()
    
    @property
    def state(self):
        return self.current_state.value
    
    @staticmethod
    def from_model(inst, id=None):
        """
        从数据库中加载task状态机
        """

        if inst is None and id is not None:
            inst = Task.get_or_none(Task.id == id)
        if inst is None:
            raise Exception("TaskSM.from_model, task not found, id: %s" % id)
        instance = TaskSM(task=inst.task, deepthink_id=inst.deepthink, start_value=inst.status)
        instance.inst = inst
        instance.task_desc = inst.task_desc
        instance.result = inst.result
        instance.propose_time = inst.propose_time
        instance.update_time = inst.update_time
        instance.finish_time = inst.finish_time
        instance.id = inst.id
        return instance

    def save_model(self):
        "save task to db"

        if self.inst is None:
            values = Task.get_defaults()
            values.update(dict(
                id = self.id,
                task = self.task,
                deepthink = self.deepthink_id,
            ))
            self.inst = Task.create(**values)
        self.inst.task_desc = self.task_desc
        self.inst.result = self.result
        self.inst.summary = self.summary
        self.inst.status = self.state
        self.inst.update_time = get_now_unixtime()
        if self.state == Status.DONE and self.inst.finish_time == 0:
            self.inst.finish_time = get_now_unixtime()
        save_rows = self.inst.save()
        if save_rows <= 0:
            raise Exception("TaskSM.save_model, save task failed")

    def on_transition(self, event_data, event):
        assert event_data.event == event
        if event.name == "done":
            if not self.result or not self.summary:
                raise Exception("TaskSM.on_transition, when 'done', result|summary MUST NOT be empty")
        msg = "Running Event(%s) from state:%s to state:%s" % (event.name, event_data.transition.source.id, event_data.transition.target.id)
        print(msg)
        self.save_model()
        return (msg)

