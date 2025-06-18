from Fluxos.fluxo_base import BaseFlow

class PiercingFlow(BaseFlow):
    def __init__(self):
        super().__init__()

        # Lista de perguntas REAIS (as que precisam de resposta do cliente)
        self.questions = [
            "Ótimo, a seguir vamos começar o seu agendamento! Qual seu nome completo?",
            "Qual sua idade?",
            "Em qual local você deseja a perfuração?",
            "Informe o dia e horário desejado para realizar o procedimento.",
            "Você prefere qual material? Titânio ou Aço Cirúrgico?",
            # AVISO: daqui pra frente, inicia a ficha de saúde
            "Você é fumante?",
            "Tem alguma alergia?",
            "Está grávida?",
            "Tem hipertensão?",
            "Tem herpes?",
            "Tem alergia a remédios?",
            "Tem diabetes?",
            "Já teve hepatite?",
            "Tem algum problema no coração?",
            "Tem anemia?",
            "Tem depressão?",
            "Tem glaucoma?",
            "É portador(a) de HIV?",
            "Tem alguma doença de pele?",
            "Já teve câncer?",
            "Tem tendência a queloide?"
        ]

        # Mensagens informativas (são exibidas automaticamente antes de certas perguntas)
        self.informational_messages = {
            5: "Agora vamos fazer 16 perguntas rápidas que são obrigatórias para a sua ficha de saúde. Responda com '*s/n*' para *Sim* ou *Não*"
        }

        self.validations = {
            4: ["titânio", "aço cirúrgico"],
            **{i: ["sim", "s", "não", "n", "nao"] for i in range(5, 21)}
        }

    def get_question(self, step):
        # Primeiro exibe mensagens informativas, se houver
        if step in self.informational_messages:
            return self.informational_messages[step] + "\n" + self.questions[step]
        return self.questions[step] if step < len(self.questions) else None

    def validate_answer(self, step, answer):
        if step in self.validations:
            normalized_answer = answer.lower().strip().replace("nao", "não")
            if normalized_answer in ["s", "sim", "n", "não"]:
                return True
            return normalized_answer in self.validations[step]
        return True

    def mask_name(self, name):
        parts = name.split()
        if len(parts) > 1:
            return f"{parts[0]} {parts[-1][0]}."
        return parts[0] if parts else name

    def normalize_health_answer(self, answer):
        normalized = answer.lower().strip()
        if normalized in ["s", "sim"]:
            return "sim"
        elif normalized in ["n", "nao", "não"]:
            return "não"
        return normalized

    def generate_summary(self, answers):
        personal_data = (
            "👤 *DADOS PESSOAIS*\n"
            f"• Nome: {self.mask_name(answers[0])}\n"
            f"• Idade: {answers[1]}\n"
        )

        appointment = (
            "\n📅 *AGENDAMENTO*\n"
            f"• Local da Perfuração: {answers[2]}\n"
            f"• Data/Horário: {answers[3]}\n"
            f"• Material Escolhido: {answers[4].capitalize()}\n"
        )

        health_questions = [
            "Fumante", "Alergias", "Gravidez", "Hipertensão", "Herpes",
            "Alergia a remédios", "Diabetes", "Hepatite", "Problema cardíaco",
            "Anemia", "Depressão", "Glaucoma", "HIV", "Doença de pele",
            "Câncer", "Tendência a queloide"
        ]

        health_responses = "\n".join(
            f"• {q}: {'✅ Sim' if self.normalize_health_answer(answers[i + 5]) == 'sim' else '❌ Não'}"
            for i, q in enumerate(health_questions))

        health_data = "\n🏥 *INFORMAÇÕES DE SAÚDE*\n" + health_responses

        footer = (
            "\n\n🔹 *PRÓXIMOS PASSOS*\n"
            "📲 Você receberá uma confirmação do agendamento via WhatsApp.\n"
            "📞 Dúvidas? Chame-nos pelo WhatsApp (+55 69 9397-9351)\n"
            "🔒 Seus dados estão protegidos. Para excluí-los, digite *EXCLUIR DADOS*.\n"
            "💙 Agradecemos sua confiança!"
        )

        return "✨ *RESUMO DO AGENDAMENTO* ✨\n\n" + personal_data + appointment + health_data + footer
