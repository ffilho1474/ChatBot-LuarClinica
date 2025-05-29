import time

class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.timeout = 300  # 5 minutos
        self.max_retention = 24 * 3600  # 24 horas

    def create_session(self, phone, procedure_type):
        self.sessions[phone] = {
            "procedure_type": procedure_type,
            "step": 0,
            "answers": [],
            "last_interaction": time.time(),
            "created_at": time.time()
        }
        print(f"✅ Nova sessão criada para {phone[:5]}...")

    def update_session(self, phone, answer):
        if phone in self.sessions:
            self.sessions[phone]["answers"].append(answer)
            self.sessions[phone]["step"] += 1
            self.sessions[phone]["last_interaction"] = time.time()
            print(f"🔄 Sessão atualizada: {phone[:5]}... (passo {self.sessions[phone]['step']})")

    def check_timeout(self, phone):
        if phone in self.sessions:
            # Verificar inatividade
            if (time.time() - self.sessions[phone]["last_interaction"]) > self.timeout:
                return True
            
            # Verificar tempo máximo de retenção
            if (time.time() - self.sessions[phone]["created_at"]) > self.max_retention:
                return True
        return False

    def end_session(self, phone):
        if phone in self.sessions:
            # Destruição segura: substituir respostas por lixo
            self.sessions[phone]["answers"] = ["DADO REMOVIDO"] * len(self.sessions[phone]["answers"])
            del self.sessions[phone]
            print(f"⏹️ Sessão de {phone[:5]}... encerrada e dados destruídos")