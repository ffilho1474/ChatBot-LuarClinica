from Chatbot.Fluxos.fluxo_base import BaseFlow

class TattooRemovalFlow(BaseFlow):
    def __init__(self):
        super().__init__()
        self.questions = [
            "🌙 Vamos agendar sua sessão de remoção de tatuagem! Qual seu nome completo?",
            "📄 CPF (apenas números):",
            "📅 Data de nascimento (DD/MM/AAAA):",
            "📍 Local da tatuagem no corpo:",
            "🎨 Cor predominante (preta/colorida):",
            "📏 Tamanho aproximado (Ex: 10x10cm, palma da mão):",
            "⏳ Tempo desde a aplicação (Ex: 1 ano, 5 anos):",
            "💉 Já fez sessões de remoção antes? Quantas?",
            "⚠️ Possui alergia a pigmentos ou anestésicos?",
            "📆 Melhor horário para agendamento:",
            "📝 Observações adicionais:"
        ]

        self.validations = {
            1: lambda x: x.isdigit() and len(x) == 11,  # Valida CPF
            4: ["preta", "colorida"],  # Valida cor da tatuagem
            8: ["sim", "não"]  # Valida alergia
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
            "✨ *RESUMO PARA REMOÇÃO DE TATUAGEM* ✨\n\n"
            f"👤 *Nome*: {answers[0]}\n"
            f"🆔 *CPF*: {answers[1]}\n"
            f"🎂 *Nascimento*: {answers[2]}\n\n"
            f"📍 *Local*: {answers[3]}\n"
            f"🎨 *Cor*: {answers[4].capitalize()}\n"
            f"📏 *Tamanho*: {answers[5]}\n"
            f"⏳ *Tempo de tatuagem*: {answers[6]}\n"
            f"💉 *Sessões anteriores*: {answers[7]}\n"
            f"⚠️ *Alergias*: {answers[8].capitalize()}\n\n"
            "📋 *Observações*:\n"
            f"{answers[10]}\n\n"
            "🔹 *Próximos passos*:\n"
            "📲 Você receberá uma confirmação do agendamento via WhatsApp.\n"
            "📞 Dúvidas? Chame-nos pelo WhatsApp (+55 69 9397-9351)\n"
            "💙 Agradecemos sua confiança!"
        )
        return summary