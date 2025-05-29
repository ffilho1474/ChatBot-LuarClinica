from Fluxos.fluxo_base import BaseFlow

class KeloidFlow(BaseFlow):
    def __init__(self):
        super().__init__()
        self.questions = [
            "🌙 Vamos agendar sua avaliação para remoção de queloide! Qual seu nome completo?",
            "Qual sua idade?",
            "📍 Em qual região está o queloide?",
            "⏳ Há quanto tempo você tem esse queloide?",
            "📏 Qual o tamanho aproximado? (Ex: 1cm, do tamanho de uma moeda)",
            "🩹 Já fez algum tratamento anterior? (Ex: injeção, laser, cirurgia)",
            "💊 Tem alergia a algum medicamento ou anestésico? Responda com 'sim' ou 'não'.",
            "📆 Qual sua disponibilidade para avaliação? (Ex: Dia e hora)",
            "📝 Alguma observação adicional que devamos saber?"
        ]

        self.validations = {
            6: ["sim", "não"]  # Valida alergia
        }

    def mask_name(self, name):
        """Mascarar o nome para exibição: primeiro nome e última inicial"""
        parts = name.split()
        if len(parts) > 1:
            return f"{parts[0]} {parts[-1][0]}."
        return parts[0] if parts else name

    def get_question(self, step):
        return self.questions[step] if step < len(self.questions) else None

    def validate_answer(self, step, answer):
        if step in self.validations:
            normalized_answer = answer.lower().strip().replace("nao", "não")
            return normalized_answer in self.validations[step]
        return True

    def generate_summary(self, answers):
        # Seção de Dados Protegidos
        personal_info = (
            "👤 *DADOS PESSOAIS*\n"
            f"• Nome: {self.mask_name(answers[0])}\n"
            f"• Idade: {answers[1]}\n"
        )
        
        # Seção Médica
        medical_info = (
            "\n🏥 *INFORMAÇÕES MÉDICAS*\n"
            f"• Local do queloide: {answers[2]}\n"
            f"• Tempo: {answers[3]}\n"
            f"• Tamanho: {answers[4]}\n"
            f"• Tratamentos anteriores: {answers[5]}\n"
            f"• Alergias: {answers[6].capitalize()}\n"
        )
        
        # Rodapé com informações de proteção
        footer = (
            "\n🔹 *PRÓXIMOS PASSOS*\n"
            "📲 Você receberá uma confirmação do agendamento via WhatsApp.\n"
            "📞 Dúvidas? Chame-nos pelo WhatsApp (+55 69 9397-9351)\n"
            "🔒 Seus dados estão protegidos. Para excluí-los, digite *EXCLUIR DADOS*.\n"
            "💙 Agradecemos sua confiança!"
        )
        
        summary = (
            "✨ *RESUMO PARA REMOÇÃO DE QUELOIDE* ✨\n\n"
            f"{personal_info}"
            f"{medical_info}"
            f"\n📆 *Disponibilidade*: {answers[7]}\n"
            f"📝 *Observações*: {answers[8]}"
            f"{footer}"
        )
        return summary