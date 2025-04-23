import logging

from statemachine import StateMachine, State, Event
from models.memory import Task, Status, Id, Events
from util.time import get_now_unixtime

class TaskSM(StateMachine):
    "Task State Machine"

    logger = logging.getLogger("TaskSM")

    # db instance
    db_model = None

    # props
    id = ""
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

    def __init__(self, task_desc, deepthink_id, start_value=Status.INIT):
        super().__init__(start_value=start_value)
        self.task_desc = task_desc
        self.deepthink_id = deepthink_id
        if not self.id:
            self.id = Id.new_id()
    
    @property
    def state(self):
        return self.current_state.value
    
    @staticmethod
    def from_model(db_model, id=None):
        """
        从数据库中加载task状态机
        """

        if db_model is None and id is not None:
            db_model = Task.get_or_none(Task.id == id)
        if db_model is None:
            raise Exception("TaskSM.from_model, task not found, id: %s" % id)
        instance = TaskSM(task_desc=db_model.task_desc, deepthink_id=db_model.deepthink, start_value=db_model.status)
        instance.db_model = db_model
        instance.task_desc = db_model.task_desc
        instance.result = db_model.result
        instance.propose_time = db_model.propose_time
        instance.update_time = db_model.update_time
        instance.finish_time = db_model.finish_time
        instance.id = db_model.id
        return instance

    def save_model(self):
        "save task to db"

        if self.db_model is None:
            self.db_model = Task.create(
                id = self.id,
                task_desc = self.task_desc,
                deepthink = self.deepthink_id,
                status = self.state,
                result = self.result,
                summary = self.summary,
                propose_time = self.propose_time,
                update_time = self.update_time,
                finish_time = self.finish_time,
            )
        self.db_model.result = self.result
        self.db_model.summary = self.summary
        self.db_model.status = self.state
        self.db_model.update_time = get_now_unixtime()
        if self.state == Status.DONE and self.db_model.finish_time == 0:
            self.db_model.finish_time = get_now_unixtime()
        save_rows = self.db_model.save()
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

