from Fluxos.fluxo_base import BaseFlow

class PiercingFlow(BaseFlow):
    def __init__(self):
        super().__init__()
        self.questions = [
            "Ótimo, a seguir vamos começar o seu agendamento! Qual seu nome completo?",
            "Perfeito. Agora me diga seu CPF:",
            "Qual sua data de nascimento?",
            "Qual sua idade?",
            "Qual seu sexo (masculino, feminino, outro)?",
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
            4: ["masculino", "feminino", "outro"],
            7: ["titânio", "aço cirúrgico"],
            **{i: ["sim", "não"] for i in range(9, 25)}  # Mantemos só "não" como padrão
        }

    def get_question(self, step):
        return self.questions[step] if step < len(self.questions) else None

    def validate_answer(self, step, answer):
        if step in self.validations:
            # Normaliza a resposta
            normalized_answer = answer.lower().strip().replace("nao", "não")
            return normalized_answer in self.validations[step]
        return True

    def generate_summary(self, answers):
        # Seção 1: Dados Pessoais
        personal_data = (
            "👤 *DADOS PESSOAIS*\n"
            f"• Nome Completo: {answers[0]}\n"
            f"• CPF: {answers[1]}\n"
            f"• Data de Nascimento: {answers[2]} (Idade: {answers[3]})\n"
            f"• Sexo: {answers[4].capitalize()}\n"
        )
        
        # Seção 2: Agendamento
        appointment = (
            "\n📅 *AGENDAMENTO*\n"
            f"• Local da Perfuração: {answers[5]}\n"
            f"• Data/Horário: {answers[6]}\n"
            f"• Material Escolhido: {answers[7].capitalize()}\n"
        )
        
        # Seção 3: Saúde (formatando respostas SIM/NÃO)
        health_questions = [
            "Fumante", "Alergias", "Gravidez", "Hipertensão", "Herpes",
            "Alergia a remédios", "Diabetes", "Hepatite", "Problema cardíaco",
            "Anemia", "Depressão", "Glaucoma", "HIV", "Doença de pele",
            "Câncer", "Tendência a queloide"
        ]
        
        # Normaliza respostas antes de exibir
        health_responses = "\n".join(
            f"• {q}: {'✅ Sim' if answers[i+9].lower().replace('nao', 'não') == 'sim' else '❌ Não'}"
            for i, q in enumerate(health_questions))
        
        health_data = (
            "\n🏥 *INFORMAÇÕES DE SAÚDE*\n"
            f"{health_responses}"
        )
        
        # Rodapé
        footer = (
            "\n\n🔹 *PRÓXIMOS PASSOS*\n"
            "📲 Você receberá uma confirmação do agendamento via WhatsApp.\n"
            "📞 Dúvidas? Chame-nos pelo WhatsApp (+55 69 9397-9351)\n"
            "💙 Agradecemos sua confiança!"
        )
        
        # Montagem final com formatação responsiva
        summary = (
            "✨ *RESUMO DO AGENDAMENTO* ✨\n\n"
            f"{personal_data}"
            f"{appointment}"
            f"{health_data}"
            f"{footer}"
        )
        
        return summary