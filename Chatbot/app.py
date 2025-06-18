from flask import Flask, request, jsonify
from Core.whatsapp_api import WhatsAppAPI
from Core.tempo_sessao import SessionManager
from Core.email_envio import EmailManager

from Fluxos.fluxo_piercing import PiercingFlow
from Fluxos.fluxo_queloide import KeloidFlow
from Fluxos.fluxo_remocao_tattoo import TattooRemovalFlow
from Fluxos.fluxo_glanuloma import GranulomaFlow
from Fluxos.fluxo_pierc_preco import PrecoPiercingFlow
from Fluxos.fluxo_pierc_cuidados import CuidadosPiercingFlow
from Fluxos.fluxo_sugestão import SugestaoFlow

import os
import time
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
whatsapp = WhatsAppAPI()
sessions = SessionManager()
email_manager = EmailManager()

flows = {
    "perfuração": PiercingFlow(),
    "queloide": KeloidFlow(),
    "tatuagem": TattooRemovalFlow(),
    "granuloma": GranulomaFlow(),
    "precos_piercing": PrecoPiercingFlow(),
    "cuidados_piercing": CuidadosPiercingFlow(),
    "sugestao": SugestaoFlow()
}

health_flows = ["queloide", "granuloma", "tatuagem"]

@app.route("/")
def home():
    return "🌙 Chatbot Luar Clínica 🌙", 200

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if mode == "subscribe" and token == os.getenv("VERIFY_TOKEN"):
        print("✅ Webhook verificado!")
        return challenge, 200
    print("❌ Falha na verificação")
    return "Erro na verificação", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print(f"📩 Evento recebido")
    
    if data.get("entry"):
        for entry in data["entry"]:
            for change in entry.get("changes", []):
                if messages := change.get("value", {}).get("messages"):
                    for message in messages:
                        if "text" in message:
                            clean_message = ''.join(e for e in message["text"]["body"] if e.isalnum() or e in ' .?!/,;:')
                            handle_message(message["from"], clean_message.lower())
    return "OK", 200

def handle_message(phone, message):
    if phone in sessions.sessions and sessions.sessions[phone].get("waiting_feedback"):
        if message.strip():
            email_manager.send_feedback_email(phone, message)
            whatsapp.send_message(phone, "💙 Muito obrigado pelo seu feedback! Tenha um ótimo dia 🌙")
            sessions.end_session(phone)
        else:
            whatsapp.send_message(phone, "Por favor, digite seu feedback ou envie uma mensagem.")
        return

    if message == "excluir dados":
        sessions.end_session(phone)
        whatsapp.send_message(phone, "✅ Seus dados foram excluídos com sucesso!")
        return

    if phone not in sessions.sessions:
        if message == "1":
            sessions.create_session(phone, "consentimento")
            whatsapp.send_message(phone, 
                "🔒 *PROTEÇÃO DE DADOS*\nLeia nossa política completa:\nhttps://luarclinica.com.br/\n\nPara agendamento coletaremos:\n- Nome completo\n- Idade\n- Local do procedimento\n\n*Digite ACEITO para continuar ou CANCELAR para sair*"
            )
        else:
            whatsapp.send_message(phone, "Olá! Bem-vindo à Luar Clínica 🌙. Digite *1* para iniciar.")
        return

    if sessions.check_timeout(phone):
        whatsapp.send_message(phone, "⏱️ Atendimento encerrado por inatividade. Digite *1* para recomeçar.")
        sessions.end_session(phone)
        return

    session = sessions.sessions[phone]

    if session["procedure_type"] == "consentimento":
        if message == "aceito":
            session["procedure_type"] = "menu"
            whatsapp.send_message(phone, 
                "Escolha alguma das opções abaixo:\n1️⃣ Agendar Perfuração\n2️⃣ Agendar Remoção de Queloide\n3️⃣ Agendar Remoção de Tatuagem\n4️⃣ Agendar Tratamento de Granuloma\n5️⃣ Preços da Perfuração\n6️⃣ Cuidados pós-perfuração\n7️⃣ Sugestões de Melhorias"
            )
        else:
            whatsapp.send_message(phone, "Agendamento cancelado. Obrigada!")
            sessions.end_session(phone)
        return

    if session["procedure_type"] == "consentimento_saude":
        if message == "concordo":
            chosen_flow = session.get("chosen_flow")
            if chosen_flow in health_flows:
                session["procedure_type"] = chosen_flow
                session["step"] = 0
                process_flow(phone, "", chosen_flow)
            else:
                session["procedure_type"] = "menu"
                whatsapp.send_message(phone, "Ocorreu um erro. Por favor, escolha novamente.")
        else:
            whatsapp.send_message(phone, "Agendamento cancelado. Obrigada!")
            sessions.end_session(phone)
        return

    if session["procedure_type"] == "menu":
        if message in ["1", "2", "3", "4", "5", "6", "7"]:
            procedure_types = {
                "1": "perfuração",
                "2": "queloide",
                "3": "tatuagem",
                "4": "granuloma",
                "5": "precos_piercing",
                "6": "cuidados_piercing",
                "7": "sugestao"
            }
            chosen_flow = procedure_types[message]
            session["procedure_type"] = chosen_flow
            if message in ["5", "6"]:
                flow = flows[chosen_flow]
                whatsapp.send_message(phone, flow.generate_summary([]))
                sessions.end_session(phone)
            else:
                if chosen_flow in health_flows:
                    session["procedure_type"] = "consentimento_saude"
                    session["chosen_flow"] = chosen_flow
                    whatsapp.send_message(phone, 
                        "⚠️ *CONSENTIMENTO PARA DADOS DE SAÚDE*\nPara o procedimento escolhido, precisamos coletar informações de saúde.\nEstes dados são essenciais para sua segurança durante o procedimento.\n\n*Digite CONCORDO para continuar ou CANCELAR para sair*"
                    )
                else:
                    session["step"] = 0
                    process_flow(phone, "", chosen_flow)
        else:
            whatsapp.send_message(phone, "Opção inválida. Digite um número de 1 a 7.")
        return

    process_flow(phone, message, session["procedure_type"])

def process_flow(phone, message, flow_type):
    print(f"🔍 Processando fluxo {flow_type} para {phone[:5]}...")
    flow = flows[flow_type]
    session = sessions.sessions[phone]

    # Instrução no início do fluxo
    if message == "":
        instructions = (
            "ℹ️ *DICA:* A qualquer momento você pode digitar:\n"
            "*menu* → para retornar ao menu\n"
            "*voltar* → para voltar uma pergunta"
        )
        whatsapp.send_message(phone, instructions)
        whatsapp.send_message(phone, flow.get_question(0))
        return

    step = session["step"]

    # Comandos especiais
    if message.lower() == "menu":
        session["procedure_type"] = "menu"
        whatsapp.send_message(phone, 
            "Você voltou ao menu principal. Escolha uma opção:\n1⃣ Perfuração\n2⃣ Remoção de Queloide\n3⃣ Remoção de Tatuagem\n4⃣ Tratamento de Granuloma\n5⃣ Preços da Perfuração\n6⃣ Cuidados pós-perfuração\n7⃣ Sugestões de Melhorias"
        )
        return

    if message.lower() == "voltar":
        if step > 0:
            session["step"] -= 1
            previous_question = flow.get_question(session["step"])
            whatsapp.send_message(phone, previous_question)
        else:
            whatsapp.send_message(phone, "⚠️ Você já está na primeira pergunta.")
        return

    if not flow.validate_answer(step, message):
        error_msg = "Resposta inválida."
        if step in flow.validations:
            options = "/".join(flow.validations[step])
            error_msg = f"Por favor, responda com: {options}"
        whatsapp.send_message(phone, error_msg)
        return

    sessions.update_session(phone, message)
    next_question = flow.get_question(session["step"])

    if next_question:
        whatsapp.send_message(phone, next_question)
    else:
        summary = flow.generate_summary(session["answers"])
        whatsapp.send_message(phone, summary)

        # 🚀 ENVIO DE E-MAIL AQUI
        if flow_type in ["perfuração", "queloide", "tatuagem", "granuloma"]:
            email_manager.send_booking_email(phone, summary)

        if flow_type == "sugestao":
            email_manager.send_feedback_email(phone, session["answers"][0])
            whatsapp.send_message(phone, "💙 Sua sugestão foi enviada com sucesso! Muito obrigado 🌙")
            sessions.end_session(phone)
        else:
            feedback_message = (
                "\n✨ O que achou do nosso atendimento?\n"
                "Sua opinião é muito importante para nós!\n"
                "Caso queira, envie sugestões ou melhorias. 💙"
            )
            whatsapp.send_message(phone, feedback_message)
            sessions.sessions[phone]["waiting_feedback"] = True

if __name__ == "__main__": 
    print("🚀 Iniciando servidor Flask...")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
