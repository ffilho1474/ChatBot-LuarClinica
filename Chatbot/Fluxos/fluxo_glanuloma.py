from Chatbot.Fluxos.fluxo_base import BaseFlow

class GranulomaFlow(BaseFlow):
    def __init__(self):
        super().__init__()
        self.questions = [
            "🌙 Vamos agendar seu tratamento para granuloma! Qual seu nome completo?",
            "📄 CPF (apenas números):",
            "📅 Data de nascimento (DD/MM/AAAA):",
            "📍 Local do granuloma no corpo:",
            "⏳ Há quanto tempo apareceu? (Ex: 2 semanas, 3 meses)",
            "🩹 Já tentou algum tratamento? Qual?",
            "🔴 Está com sinais de infecção? (vermelhidão, pus, dor)",
            "💊 Toma algum medicamento atualmente?",
            "⚠️ Tem alergia a algum medicamento?",
            "📆 Melhor horário para agendamento:",
            "📝 Observações adicionais:"
        ]

        self.validations = {
            1: lambda x: x.isdigit() and len(x) == 11,  # Valida CPF
            6: ["sim", "não"],  # Valida infecção
            8: ["sim", "não"]   # Valida alergia
        }

    def get_question(self, step):
        return self.questions[step] if step < len(self.questions) else None

    def validate_answer(self, step, answer):
        if step in self.validations:
            normalized_answer = answer.lower().strip().replace("nao", "não")
            if callable(self.validations[step]):
                return self.validations[step](normalized_answer)
            return normalized_answer in self.validations[step]
        return True

    def generate_summary(self, answers):
        summary = (
            "✨ *RESUMO PARA TRATAMENTO DE GRANULOMA* ✨\n\n"
            f"👤 *Nome*: {answers[0]}\n"
            f"🆔 *CPF*: {answers[1]}\n"
            f"🎂 *Nascimento*: {answers[2]}\n\n"
            f"📍 *Local do granuloma*: {answers[3]}\n"
            f"⏳ *Tempo desde o aparecimento*: {answers[4]}\n"
            f"🩹 *Tratamentos anteriores*: {answers[5]}\n"
            f"🔴 *Sinais de infecção*: {answers[6].capitalize()}\n"
            f"💊 *Medicamentos em uso*: {answers[7]}\n"
            f"⚠️ *Alergias*: {answers[8].capitalize()}\n\n"
            "📋 *Observações*:\n"
            f"{answers[10]}\n\n"
            "🔹 *Próximos passos*:\n"
            "📲 Você receberá uma confirmação do agendamento via WhatsApp.\n"
            "📞 Dúvidas? Chame-nos pelo WhatsApp (+55 69 9397-9351)\n"
            "💙 Agradecemos sua confiança!"
        )
        return summary