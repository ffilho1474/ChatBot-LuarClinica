from Fluxos.fluxo_base_info import InfoFlow

PIERCING_CONTENT = """
💎 *PREÇOS E LOCAIS DE PERFURAÇÃO* 💎

💉 Partes da orelha: R$ 50,00 (aço) ou R$ 90,00 (titânio)
💉 Nariz: R$ 50,00 (aço) ou R$ 80,00 (titânio)
💉 Mamilo: R$ 50,00 (aço) ou R$ 90,00 (titânio)
💉 Umbigo: R$ 50,00 (aço) ou R$ 80,00 (titânio)
💉 Íntimo: R$ 80,00 (aço) ou R$ 100,00 (titânio)
💉 Septo: R$ 80,00 (aço) ou R$ 100,00 (titânio)
💉 Sobrancelha: R$ 60,00 (aço) ou R$ 90,00 (titânio)
💉 Microdermal: R$ 120,00 (aço) ou R$ 200,00 (titânio)

🌙 *Agendamentos via opção 1*
📞 Dúvidas? Chame-nos pelo WhatsApp (+55 69 9397-9351)
🔒 Seus dados estão protegidos. Para exclusão, digite EXCLUIR DADOS.
"""

class PrecoPiercingFlow(InfoFlow):
    def __init__(self):
        super().__init__(PIERCING_CONTENT)