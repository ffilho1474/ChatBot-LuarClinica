class BaseFlow:
    def __init__(self):
        self.questions = []
        self.validations = {}

    def get_question(self, step):
        return self.questions[step] if step < len(self.questions) else None

    def validate_answer(self, step, answer):
        if step in self.validations:
            normalized = answer.lower().strip().replace("nao", "não")
            return normalized in self.validations[step]
        return True

    def handle_back(self, session):
        """Volta uma pergunta no fluxo"""
        if session["step"] > 0:
            session["step"] -= 1
            session["answers"].pop()
            return True
        return False
