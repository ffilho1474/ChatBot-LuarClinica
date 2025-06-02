import requests
import os
import re

class WhatsAppAPI:
    def __init__(self):
        self.token = os.getenv("WHATSAPP_TOKEN")
        self.phone_number_id = os.getenv("PHONE_NUMBER_ID")
        self.base_url = f"https://graph.facebook.com/v19.0/{self.phone_number_id}/messages"

    def sanitize_message(self, message):
        """Remove termos sensíveis para conformidade LGPD"""
        sensitive_terms = ["CPF", "documento", "RG", "número do cartão", "endereço completo"]
        for term in sensitive_terms:
            message = message.replace(term, "[DADO PROTEGIDO]")
        return message

    def send_message(self, phone, message):
        sanitized_msg = self.sanitize_message(message)
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": phone,
            "type": "text",
            "text": {"body": sanitized_msg}
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar mensagem: {e}")
            return False