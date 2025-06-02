from Fluxos.fluxo_base import BaseFlow

class PiercingFlow(BaseFlow):
    def __init__(self):
        super().__init__()
        self.questions = [
            "Ótimo, a seguir vamos começar o seu agendamento! Qual seu nome completo?",
            "Qual sua idade?",
            "Em qual local você deseja a perfuração?",
            "Informe o dia e horário desejado para realizar o procedimento.",
            "Você prefere qual material? Titânio ou Aço Cirúrgico?",
            "Agora vamos para algumas perguntas rápidas de saúde. Tudo bem? Responda com 'sim' ou 'não'.",
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
        
        self.validations = {
            4: ["titânio", "aço cirúrgico"],
            **{i: ["sim", "não"] for i in range(5, 22)}
        }

    def get_question(self, step):
        return self.questions[step] if step < len(self.questions) else None

    def validate_answer(self, step, answer):
        if step in self.validations:
            normalized_answer = answer.lower().strip().replace("nao", "não")
            return normalized_answer in self.validations[step]
        return True

    def mask_name(self, name):
        """Mascarar o nome para exibição: primeiro nome e última inicial"""
        parts = name.split()
        if len(parts) > 1:
            return f"{parts[0]} {parts[-1][0]}."
        return parts[0] if parts else name

    def generate_summary(self, answers):
        # Seção 1: Dados Pessoais (mascarados)
        personal_data = (
            "👤 *DADOS PESSOAIS*\n"
            f"• Nome: {self.mask_name(answers[0])}\n"
            f"• Idade: {answers[1]}\n"
        )
        
        # Seção 2: Agendamento
        appointment = (
            "\n📅 *AGENDAMENTO*\n"
            f"• Local da Perfuração: {answers[2]}\n"
            f"• Data/Horário: {answers[3]}\n"
            f"• Material Escolhido: {answers[4].capitalize()}\n"
        )
        
        # Seção 3: Saúde (formatando respostas SIM/NÃO)
        health_questions = [
            "Fumante", "Alergias", "Gravidez", "Hipertensão", "Herpes",
            "Alergia a remédios", "Diabetes", "Hepatite", "Problema cardíaco",
            "Anemia", "Depressão", "Glaucoma", "HIV", "Doença de pele",
            "Câncer", "Tendência a queloide"
        ]
        
        health_responses = "\n".join(
            f"• {q}: {'✅ Sim' if answers[i+5].lower().replace('nao', 'não') == 'sim' else '❌ Não'}"
            for i, q in enumerate(health_questions))
        
        health_data = (
            "\n🏥 *INFORMAÇÕES DE SAÚDE*\n"
            f"{health_responses}"
        )
        
        # Rodapé com informações de proteção
        footer = (
            "\n\n🔹 *PRÓXIMOS PASSOS*\n"
            "📲 Você receberá uma confirmação do agendamento via WhatsApp.\n"
            "📞 Dúvidas? Chame-nos pelo WhatsApp (+55 69 9397-9351)\n"
            "🔒 Seus dados estão protegidos. Para excluí-los, digite *EXCLUIR DADOS*.\n"
            "💙 Agradecemos sua confiança!"
        )
        
        summary = (
            "✨ *RESUMO DO AGENDAMENTO* ✨\n\n"
            f"{personal_data}"
            f"{appointment}"
            f"{health_data}"
            f"{footer}"
        )
        
        return summary