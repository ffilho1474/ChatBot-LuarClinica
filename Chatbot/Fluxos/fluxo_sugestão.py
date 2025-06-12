# Fluxos/fluxo_sugestao.py
from Fluxos.fluxo_base import BaseFlow

class SugestaoFlow(BaseFlow):
    def __init__(self):
        super().__init__()
        self.questions = ["Por favor, digite sua sugestão ou melhoria:"]

    def get_question(self, step):
        if step < len(self.questions):
            return self.questions[step]
        return None

    def validate_answer(self, step, answer):
        # Qualquer resposta é válida
        return True

    def generate_summary(self, answers):
        return f"Sugestão recebida: {answers[0]}"
