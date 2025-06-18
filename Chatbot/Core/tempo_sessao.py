import time

class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self, phone, procedure_type):
        self.sessions[phone] = {
            "procedure_type": procedure_type,
            "step": 0,
            "answers": [],
            "start_time": time.time()
        }

    def end_session(self, phone):
        if phone in self.sessions:
            del self.sessions[phone]

    def reset_to_menu(self, phone):
        """Reseta apenas o fluxo, preservando a sessão"""
        if phone in self.sessions:
            self.sessions[phone]["procedure_type"] = "menu"
            self.sessions[phone]["step"] = 0
            self.sessions[phone]["answers"] = []
            self.sessions[phone].pop("waiting_feedback", None)
            self.sessions[phone].pop("chosen_flow", None)
            self.sessions[phone].pop("consentimento_saude", None)

    def check_timeout(self, phone, timeout=1800):
        if phone not in self.sessions:
            return False
        start_time = self.sessions[phone].get("start_time", time.time())
        if time.time() - start_time > timeout:
            self.end_session(phone)
            return True
        return False

    def update_session(self, phone, message):
        self.sessions[phone]["answers"].append(message)
        self.sessions[phone]["step"] += 1
