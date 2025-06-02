from Fluxos.fluxo_base import BaseFlow

class GranulomaFlow(BaseFlow):
    def __init__(self):
        super().__init__()
        self.questions = [
            "🌙 Vamos agendar seu tratamento para granuloma! Qual seu nome completo?",
            "Qual sua idade?",
            "📍 Local do granuloma no corpo:",
            "⏳ Há quanto tempo apareceu? (Ex: 2 semanas, 3 meses)",
            "🩹 Já tentou algum tratamento? Qual?",
            "🔴 Está com sinais de infecção? (vermelhidão, pus, dor) Responda com 'sim' ou 'não'.",
            "💊 Toma algum medicamento atualmente?",
            "⚠️ Tem alergia a algum medicamento? Responda com 'sim' ou 'não'.",
            "📆 Melhor horário para agendamento:",
            "📝 Observações adicionais:"
        ]

        self.validations = {
            5: ["sim", "não"],  # Valida infecção
            7: ["sim", "não"]   # Valida alergia
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
            f"• Local do granuloma: {answers[2]}\n"
            f"• Tempo de aparecimento: {answers[3]}\n"
            f"• Tratamentos anteriores: {answers[4]}\n"
            f"• Sinais de infecção: {answers[5].capitalize()}\n"
            f"• Medicamentos em uso: {answers[6]}\n"
            f"• Alergias: {answers[7].capitalize()}\n"
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
            "✨ *RESUMO PARA TRATAMENTO DE GRANULOMA* ✨\n\n"
            f"{personal_info}"
            f"{medical_info}"
            f"\n📆 *Horário preferencial*: {answers[8]}\n"
            f"📝 *Observações*: {answers[9]}"
            f"{footer}"
        )
        return summary