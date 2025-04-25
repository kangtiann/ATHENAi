class Mentor:
    def run(self):
        visions = self.load_vision_list()
        for vision in visions:
            vision.status = Status.INIT

    def load_vision_list(self):
        pass

    def load_topic_list(self):
        pass

