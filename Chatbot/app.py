from flask import Flask, request
from Core.whatsapp_api import WhatsAppAPI
from Core.tempo_sessao import SessionManager
from Fluxos.fluxo_piercing import PiercingFlow
from Fluxos.fluxo_queloide import KeloidFlow
from Fluxos.fluxo_remocao_tattoo import TattooRemovalFlow
from Fluxos.fluxo_glanuloma import GranulomaFlow
from Fluxos.fluxo_pierc_preco import PrecoPiercingFlow
from Fluxos.fluxo_pierc_cuidados import CuidadosPiercingFlow

import os
import time
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
whatsapp = WhatsAppAPI()
sessions = SessionManager()

flows = {
    "perfuração": PiercingFlow(),
    "queloide": KeloidFlow(),
    "tatuagem": TattooRemovalFlow(),
    "granuloma": GranulomaFlow(),
    "precos_piercing": PrecoPiercingFlow(),
    "cuidados_piercing": CuidadosPiercingFlow()
}

# Fluxos que requerem consentimento de saúde
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
    print(f"📩 Evento recebido")  # Não logar conteúdo sensível
    
    if data.get("entry"):
        for entry in data["entry"]:
            for change in entry.get("changes", []):
                if messages := change.get("value", {}).get("messages"):
                    for message in messages:
                        if "text" in message:
                            # Limpeza básica da mensagem
                            clean_message = ''.join(e for e in message["text"]["body"] if e.isalnum() or e in ' .?!/,;:')
                            handle_message(message["from"], clean_message.lower())
    return "OK", 200

def handle_message(phone, message):
    print(f"📞 Mensagem de {phone[:5]}...")  # Não logar o número completo

    # Comando para exclusão de dados
    if message == "excluir dados":
        sessions.end_session(phone)
        whatsapp.send_message(phone, "✅ Seus dados foram excluídos com sucesso!")
        return

    if phone not in sessions.sessions:
        if message == "1":
            sessions.create_session(phone, "consentimento")
            # Modifique esta mensagem em app.py
            whatsapp.send_message(phone, 
                "🔒 *PROTEÇÃO DE DADOS*\n"
                "Leia nossa política completa:\n"
                "https://luarclinica.com.br/\n\n"
                "Para agendamento coletaremos:\n"
                "- Nome completo\n"
                "- Idade\n"
                "- Local do procedimento\n\n"
                "*Digite ACEITO para continuar ou CANCELAR para sair*"
            )
        else:
            whatsapp.send_message(phone, "Olá! Bem-vindo à Luar Clínica 🌙. Digite *1* para iniciar.")
        return

    if sessions.check_timeout(phone):
        whatsapp.send_message(phone, "⏱️ Atendimento encerrado por inatividade. Digite *1* para recomeçar.")
        sessions.end_session(phone)
        return

    session = sessions.sessions[phone]

    # Estado de consentimento
    if session["procedure_type"] == "consentimento":
        if message == "aceito":
            session["procedure_type"] = "menu"
            whatsapp.send_message(phone, 
                "Escolha alguma das opções abaixo, em caso de agendamento vamos pedir alguns dados pessoais para cadastrarmos na sua ficha de paciente: (Atendimento apenas para maiores de 18 anos) \n"
                "1️⃣ Agendar Perfuração\n"
                "2️⃣ Agendar Remoção de Queloide\n"
                "3️⃣ Agendar Remoção de Tatuagem\n"
                "4️⃣ Agendar Tratamento de Granuloma\n"
                "5️⃣ Preços da Perfuração\n"
                "6️⃣ Cuidados pós-perfuração"
            )
        else:
            whatsapp.send_message(phone, "Agendamento cancelado. Obrigada!")
            sessions.end_session(phone)
        return

    # Novo estado: consentimento para dados de saúde
    if session["procedure_type"] == "consentimento_saude":
        if message == "concordo":
            # Recupera o fluxo escolhido que estava temporariamente armazenado
            chosen_flow = session.get("chosen_flow")
            if chosen_flow in health_flows:
                session["procedure_type"] = chosen_flow
                session["step"] = 0
                flow = flows[chosen_flow]
                whatsapp.send_message(phone, flow.get_question(0))
            else:
                # Caso não seja um fluxo de saúde, volta ao menu (não deveria acontecer)
                session["procedure_type"] = "menu"
                whatsapp.send_message(phone, "Ocorreu um erro. Por favor, escolha novamente.")
        else:
            whatsapp.send_message(phone, "Agendamento cancelado. Obrigada!")
            sessions.end_session(phone)
        return

    if session["procedure_type"] == "menu":
        if message in ["1", "2", "3", "4", "5", "6"]:
            procedure_types = {
                "1": "perfuração",
                "2": "queloide",
                "3": "tatuagem",
                "4": "granuloma",
                "5": "precos_piercing",
                "6": "cuidados_piercing"
            }
            chosen_flow = procedure_types[message]
            session["procedure_type"] = chosen_flow
            # Fluxos informativos (opções 5/6)
            if message in ["5", "6"]:
                flow = flows[chosen_flow]
                whatsapp.send_message(phone, flow.generate_summary([]))
                sessions.end_session(phone)
            else:
                # Verifica se é um fluxo que requer consentimento de saúde
                if chosen_flow in health_flows:
                    # Vamos para o estado de consentimento de saúde
                    session["procedure_type"] = "consentimento_saude"
                    session["chosen_flow"] = chosen_flow  # Armazena temporariamente
                    whatsapp.send_message(phone, 
                        "⚠️ *CONSENTIMENTO PARA DADOS DE SAÚDE*\n"
                        "Para o procedimento escolhido, precisamos coletar informações de saúde.\n"
                        "Estes dados são essenciais para sua segurança durante o procedimento.\n\n"
                        "*Digite CONCORDO para continuar ou CANCELAR para sair*"
                    )
                else:
                    # Fluxos com perguntas (opções 1 e 4) que não são de saúde
                    session["step"] = 0
                    flow = flows[chosen_flow]
                    whatsapp.send_message(phone, flow.get_question(0))
        else:
            whatsapp.send_message(phone, 
                "Opção inválida. Escolha:\n"
                "1️⃣ Perfuração\n"
                "2️⃣ Remoção de Queloide\n"
                "3️⃣ Remoção de Tatuagem\n"
                "4️⃣ Tratamento de Granuloma\n"
                "5️⃣ Preços da Perfuração\n"
                "6️⃣ Cuidados pós-perfuração"
            )
        return

    process_flow(phone, message, session["procedure_type"])

def process_flow(phone, message, flow_type):
    print(f"🔍 Processando fluxo {flow_type} para {phone[:5]}...")
    flow = flows[flow_type]
    session = sessions.sessions[phone]
    step = session["step"]
    
    if not flow.validate_answer(step, message):
        error_msg = "Resposta inválida."
        if step in flow.validations:
            options = "/".join(flow.validations[step])
            error_msg = f"Por favor, responda com: {options}"
        whatsapp.send_message(phone, error_msg)
        return

    sessions.update_session(phone, message)
    
    if next_question := flow.get_question(session["step"]):
        whatsapp.send_message(phone, next_question)
    else:
        summary = flow.generate_summary(session["answers"])
        whatsapp.send_message(phone, summary)
        sessions.end_session(phone)

if __name__ == "__main__": 
    print("🚀 Iniciando servidor Flask...")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)