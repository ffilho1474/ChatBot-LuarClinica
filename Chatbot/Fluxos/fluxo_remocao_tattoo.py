from Fluxos.fluxo_base import BaseFlow

class TattooRemovalFlow(BaseFlow):
    def __init__(self):
        super().__init__()
        self.questions = [
            "🌙 Vamos agendar sua sessão de remoção de tatuagem! Qual seu nome completo?",
            "Qual sua idade?",
            "📍 Local da tatuagem no corpo:",
            "🎨 Cor predominante (preta/colorida):",
            "📏 Tamanho aproximado (Ex: 10x10cm, palma da mão):",
            "⏳ Tempo desde a aplicação (Ex: 1 ano, 5 anos):",
            "💉 Já fez sessões de remoção antes? Quantas?",
            "⚠️ Possui alergia a pigmentos ou anestésicos? Responda com 'sim' ou 'não'.",
            "📆 Melhor horário para agendamento:",
            "📝 Observações adicionais:"
        ]

        self.validations = {
            3: ["preta", "colorida"],  # Valida cor da tatuagem
            7: ["sim", "não"]  # Valida alergia
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
        
        # Seção Técnica
        tattoo_info = (
            "\n🎨 *INFORMAÇÕES SOBRE A TATUAGEM*\n"
            f"• Local: {answers[2]}\n"
            f"• Cor predominante: {answers[3].capitalize()}\n"
            f"• Tamanho: {answers[4]}\n"
            f"• Tempo desde aplicação: {answers[5]}\n"
            f"• Sessões anteriores: {answers[6]}\n"
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
            "✨ *RESUMO PARA REMOÇÃO DE TATUAGEM* ✨\n\n"
            f"{personal_info}"
            f"{tattoo_info}"
            f"\n📆 *Horário preferencial*: {answers[8]}\n"
            f"📝 *Observações*: {answers[9]}"
            f"{footer}"
        )
        return summary