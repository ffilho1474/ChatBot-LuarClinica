from Chatbot.Fluxos.fluxo_base import BaseFlow

class KeloidFlow(BaseFlow):
    def __init__(self):
        super().__init__()
        self.questions = [
            "🌙 Vamos agendar sua avaliação para remoção de queloide! Qual seu nome completo?",
            "📄 CPF (apenas números):",
            "📅 Qual sua data de nascimento? (DD/MM/AAAA)",
            "📍 Em qual região está o queloide?",
            "⏳ Há quanto tempo você tem esse queloide?",
            "📏 Qual o tamanho aproximado? (Ex: 1cm, do tamanho de uma moeda)",
            "🩹 Já fez algum tratamento anterior? (Ex: injeção, laser, cirurgia)",
            "💊 Tem alergia a algum medicamento ou anestésico?",
            "📆 Qual sua disponibilidade para avaliação? (Ex: Dia e hora)",
            "📝 Alguma observação adicional que devamos saber?"
        ]

        # Validações específicas
        self.validations = {
            1: lambda x: x.isdigit() and len(x) == 11,  # CPF
            2: lambda x: len(x.split('/')) == 3,  # Data básica
            7: ["sim", "não"]  # Alergia a medicamentos
        }

    def get_question(self, step):
        return self.questions[step] if step < len(self.questions) else None

    def validate_answer(self, step, answer):
        if step in self.validations:
            if callable(self.validations[step]):
                return self.validations[step](answer)
            return answer.lower() in self.validations[step]
        return True

    def generate_summary(self, answers):
        summary = (
            "🌙 *RESUMO PARA REMOÇÃO DE QUELOIDE*\n\n"
            f"👤 *Nome*: {answers[0]}\n"
            f"🆔 *CPF*: {answers[1]}\n"
            f"📅 *Nascimento*: {answers[2]}\n\n"
            f"📍 *Local do queloide*: {answers[3]}\n"
            f"⏳ *Tempo de queloide*: {answers[4]}\n"
            f"📏 *Tamanho*: {answers[5]}\n"
            f"🩹 *Tratamentos anteriores*: {answers[6]}\n"
            f"💊 *Alergias*: {answers[7]}\n\n"
            "📋 *Observações*:\n"
            f"{answers[9]}\n\n"
            "📲 *Entraremos em contato para confirmar o agendamento!*\n"
            "📞 Dúvidas? Chame-nos pelo WhatsApp (+55 69 9397-9351) \n"
            "💙 Agradecemos sua confiança!"
        )
        return summary