import time

class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.timeout = 300  # 5 minutos

    def create_session(self, phone, procedure_type):
        self.sessions[phone] = {
            "procedure_type": procedure_type,
            "step": 0,
            "answers": [],
            "last_interaction": time.time()
        }
        print(f"✅ Nova sessão: {self.sessions[phone]}")

    def update_session(self, phone, answer):
        if phone in self.sessions:
            print(f"🔄 Atualizando passo {self.sessions[phone]['step']}")
            self.sessions[phone]["answers"].append(answer)
            self.sessions[phone]["step"] += 1
            self.sessions[phone]["last_interaction"] = time.time()
            print(f"📊 Estado atualizado: {self.sessions[phone]}")

    def check_timeout(self, phone):
        if phone in self.sessions:
            return (time.time() - self.sessions[phone]["last_interaction"]) > self.timeout
        return False

    def get_current_step(self, phone):
        return self.sessions.get(phone, {}).get("step", 0)

    def end_session(self, phone):
        if phone in self.sessions:
            print(f"⏹️ Encerrando sessão de {phone}")
            del self.sessions[phone]