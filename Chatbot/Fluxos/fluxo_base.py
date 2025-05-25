from abc import ABC, abstractmethod

class BaseFlow(ABC):
    def __init__(self):
        self.questions = []
        self.validations = {}

    @abstractmethod
    def get_question(self, step):
        pass

    @abstractmethod
    def validate_answer(self, step, answer):
        pass

    @abstractmethod
    def generate_summary(self, answers):
        pass