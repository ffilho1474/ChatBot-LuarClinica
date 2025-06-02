from Fluxos.fluxo_base_info import InfoFlow

CUIDADOS_CONTENT = """
💎 *CUIDADOS PÓS-PERFURAÇÃO* 💎
Após realizar uma perfuração, é essencial seguir alguns cuidados para garantir uma cicatrização adequada e evitar complicações. Aqui estão as orientações:
1️⃣ *Limpeza Diária*: Lave a área da perfuração apenas com soro fisiológico . Evite produtos com álcool/fragrâncias forte.
2️⃣ *Evite Atrito*: Não toque na perfuração com as mãos sujas, tente evitar engatar na toalha, roupa, dormir por cima etc...
3️⃣ *Não Retire a Joia*: Mantenha a joia no local até que a perfuração esteja completamente cicatrizada, geralmente de 6 a 8 semanas.
4️⃣ *Faça compressa*: Com soro fisiológico morno, faça compressa pelomenos 3x na semana.

📞 Dúvidas? Chame-nos pelo WhatsApp (+55 69 9397-9351)\"
💙 Agradecemos sua confiança!

"""
class CuidadosPiercingFlow(InfoFlow):
    def __init__(self):
        super().__init__(CUIDADOS_CONTENT)  # Passa o conteúdo para a classe base