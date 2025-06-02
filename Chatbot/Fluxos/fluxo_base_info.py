from Fluxos.fluxo_base import BaseFlow

class InfoFlow(BaseFlow):
    """
    Classe base para fluxos que apenas exibem informações (sem perguntas).
    Basta passar o conteúdo no __init__()
    """
    def __init__(self, content):
        super().__init__()
        self.content = content
        self.questions = []
        self.validations = {}

    def get_question(self, step):
        return None

    def validate_answer(self, step, answer):
        return True

    def generate_summary(self, answers):
        return self.content