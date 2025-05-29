from Fluxos.fluxo_base_info import InfoFlow

PIERCING_CONTENT = """
💎 *PREÇOS E LOCAIS DE PERFURAÇÃO* 💎

💉Partes da orelha 50,00. com jóia de aço cirúrgico ou 90,00 com jóia de titânio.

💉Nariz: 50,00 com jóia de aço cirúrgico ou 80,00 com jóia de titânio 

💉Mamilo cada lado 50,00 com piercing de aço cirúrgico ou 90 com piercing de titânio 

💉Umibigo; 50,00 com piercing de aço cirúrgico ou 80,00 com piercing de titânio 

💉Íntimo 80,00 com piercing de aço cirúrgico ou 100 com piercing de titânio 

💉 Septo 80,00 com piercing de aço cirúrgico ou 100,00 com piercing de titânio 

💉 Sombrancelha 60,00 com piercing de aço cirúrgico ou 90 com piercing de titânio.

💉 Microdermal: 120,00 com piercing de aço cirúrgico ou 200,00 com piercing de titânio.

Restante das perfurações 50,00 com piercing de aço cirúrgico e 90 com piercing de titânio.

🌙 *Agendamentos via opção 1*
"📞 Dúvidas? Chame-nos pelo WhatsApp (+55 69 9397-9351)"
"""

class PrecoPiercingFlow(InfoFlow):
    def __init__(self):
        super().__init__(PIERCING_CONTENT)  # Passa o conteúdo para a classe base