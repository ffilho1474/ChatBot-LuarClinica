from flask import Flask, request
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

app = Flask(__name__)

usuarios = {}

# Perguntas organizadas
perguntas = [
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

# Etapas que exigem validação de resposta
validacoes = {
    4: ["masculino", "feminino", "outro"],
    7: ["titânio", "aço cirúrgico"],
    **{i: ["sim", "não"] for i in range(9, 25)}
}


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Recebido webhook:", data)

    if data.get("entry"):
        for entry in data["entry"]:
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages")
                if messages:
                    for message in messages:
                        number = message["from"]
                        text = message["text"]["body"]
                        responder_usuario(number, text.lower())  # converte para minúsculo

    return "OK", 200


def responder_usuario(telefone, texto_recebido):
    tempo_atual = time.time()
    texto = ""

    if texto_recebido == "1":
        usuarios[telefone] = {
            "etapa": 0,
            "respostas": [],
            "ultima_interacao": tempo_atual
        }
        texto = perguntas[0]

    elif telefone in usuarios:
        usuario = usuarios[telefone]
        etapa = usuario["etapa"]
        ultima = usuario["ultima_interacao"]

        # Duração da conexão sem resposta
        if tempo_atual - ultima > 300:
            texto = (
                "⏱️ O atendimento foi encerrado por inatividade.\n"
                "Caso deseje iniciar novamente, envie qualquer mensagem ou digite *1*."
            )
            del usuarios[telefone]
        else:
            # Verifica se resposta é válida
            if etapa in validacoes and texto_recebido not in validacoes[etapa]:
                opcoes = "', '".join(validacoes[etapa])
                texto = f"Por favor, responda com uma das opções válidas: '{opcoes}'."
            else:
                usuario["respostas"].append(texto_recebido)
                etapa += 1

                if etapa < len(perguntas):
                    texto = perguntas[etapa]
                    usuario["etapa"] = etapa
                    usuario["ultima_interacao"] = tempo_atual
                else:
                    r = usuario["respostas"]
                    texto = (
                        "✅ *Resumo do seu atendimento:*\n\n"
                        f"👤 *Nome:* {r[0]}\n"
                        f"🪪 *CPF:* {r[1]}\n"
                        f"🎂 *Nascimento:* {r[2]} (Idade: {r[3]})\n"
                        f"🧑 *Sexo:* {r[4]}\n"
                        f"📍 *Perfuração:* {r[5]}\n"
                        f"📅 *Data e horário:* {r[6]}\n"
                        f"🔩 *Material:* {r[7]}\n\n"
                        "📋 *Informações de Saúde:*\n"
                        f"Fumante: {r[9]}\n"
                        f"Alergias: {r[10]}\n"
                        f"Gravidez: {r[11]}\n"
                        f"Hipertensão: {r[12]}\n"
                        f"Herpes: {r[13]}\n"
                        f"Alergia a remédios: {r[14]}\n"
                        f"Diabetes: {r[15]}\n"
                        f"Hepatite: {r[16]}\n"
                        f"Cardiopatia: {r[17]}\n"
                        f"Anemia: {r[18]}\n"
                        f"Depressão: {r[19]}\n"
                        f"Glaucoma: {r[20]}\n"
                        f"HIV: {r[21]}\n"
                        f"Doença de pele: {r[22]}\n"
                        f"Câncer: {r[23]}\n"
                        f"Queloide: {r[24]}\n\n"
                        "📞 Entraremos em contato para confirmar o seu agendamento. Obrigado! 💙"
                    )
                    del usuarios[telefone]

    elif texto_recebido == "2":
        texto = "Você escolheu cancelar um agendamento. Por favor, informe seu nome e a data do agendamento."

    elif texto_recebido == "3":
        texto = "Veja nossos trabalhos e preços no Instagram: https://instagram.com/luarpiercing"

    else:
        texto = (
            "👋 Olá! Bem-vindo à *Luar Clínica*.\n\n"
            "Escolha uma opção:\n"
            "1️⃣ Agendar Perfuração (Apenas maiores de dezoito anos)\n"
            "2️⃣ Cancelar Agendamento\n"
            "3️⃣ Nossos trabalhos e preços\n"
            "4️⃣ Outro assunto"
        )

    enviar_mensagem_whatsapp(telefone, texto)


def enviar_mensagem_whatsapp(telefone, texto):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": telefone,
        "type": "text",
        "text": {"body": texto}
    }

    response = requests.post(url, headers=headers, json=payload)
    print("Resposta API WhatsApp:", response.status_code, response.text)


@app.route("/webhook", methods=["GET"])
def verificar_webhook():
    VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Erro na verificação", 403


if __name__ == "__main__":
    app.run(port=5000, debug=True)
