from flask import Flask, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

app = Flask(__name__)

# Estado de cada usuário (telefone como chave)
usuarios = {}

# Perguntas na ordem
perguntas = [
    "Qual seu nome completo?",
    "Informe seu CPF:",
    "Qual o tipo de perfuração (ex: orelha, nariz, etc.)?",
    "Escolha o material: Titânio ou Aço Cirúrgico?"
]

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Recebido webhook:", data)

    if data.get("entry"):
        for entry in data["entry"]:
            for change in entry.get("changes", []):
                value = change.get("value", {})
                
                # Só processar se vier mensagens (não responder a status ou outros eventos)
                messages = value.get("messages")
                if messages:
                    for message in messages:
                        number = message["from"]
                        text = message["text"]["body"]
                        responder_usuario(number, text)

    return "OK", 200


def responder_usuario(telefone, texto_recebido):
    # Inicia novo atendimento se digitar 1
    if texto_recebido.strip() == "1":
        usuarios[telefone] = {"etapa": 0, "respostas": []}
        texto = perguntas[0]

    # Continua um atendimento em andamento
    elif telefone in usuarios:
        etapa = usuarios[telefone]["etapa"]
        usuarios[telefone]["respostas"].append(texto_recebido)
        etapa += 1
        if etapa < len(perguntas):
            texto = perguntas[etapa]
            usuarios[telefone]["etapa"] = etapa
        else:
            # Atendimento finalizado: envia resumo
            respostas = usuarios[telefone]["respostas"]
            texto = (
                "✅ Obrigado! Aqui está o resumo do seu agendamento:\n\n"
                f"👤 Nome: {respostas[0]}\n"
                f"🪪 CPF: {respostas[1]}\n"
                f"📍 Perfuração: {respostas[2]}\n"
                f"🔩 Material: {respostas[3]}\n\n"
                "Entraremos em contato para finalizar o agendamento."
            )
            del usuarios[telefone]  # Limpa a sessão

    elif texto_recebido.strip() == "2":
        texto = "Você escolheu cancelar um agendamento. Informe seu nome e data do agendamento."

    elif texto_recebido.strip() == "3":
        texto = "Veja nossos trabalhos e preços no Instagram: https://instagram.com/luarpiercing"

    else:
        texto = (
            "Olá! Bem-vindo à Luar Clínica. Escolha uma opção:\n\n"
            "1 - Agendar Perfuração\n"
            "2 - Cancelar Agendamento\n"
            "3 - Nossos trabalhos e preços\n"
            "4 - Outro assunto"
        )

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