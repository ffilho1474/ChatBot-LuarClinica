import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
from dotenv import load_dotenv

load_dotenv()

class EmailManager:
    def __init__(self):
        
        self.smtp_server = os.getenv("SMTP_SERVER")  
        self.smtp_port = int(os.getenv("SMTP_PORT"))  
        self.email_user = os.getenv("EMAIL_USER")  
        self.email_password = os.getenv("EMAIL_PASSWORD")  
        
        
        self.clinic_email = os.getenv("CLINIC_EMAIL") 

    def _load_template(self, template_path="Templates/agendamento.html"):
        """Carrega o template HTML do e-mail."""
        with open(template_path, "r", encoding="utf-8") as file:
            return Template(file.read())

    def send_booking_email(self, client_phone, summary):
        """Envia o resumo do agendamento para a clínica via Zoho Mail."""
        try:
            # 1. Ofuscação de dados (LGPD)
            masked_phone = f"{client_phone[:5]}...{client_phone[-3:]}"
            
            # 2. Renderiza o template HTML
            template = self._load_template()
            html_content = template.render(
                cliente=masked_phone,
                resumo=summary.replace("\n", "<br>")
            )

            # 3. Configuração do e-mail
            msg = MIMEMultipart()
            msg["From"] = f"Agendamentos Luar Clínica <{self.email_user}>"
            msg["To"] = self.clinic_email
            msg["Subject"] = f"✂️ Novo Agendamento - {masked_phone}"
            msg.attach(MIMEText(html_content, "html"))

            # 4. Envio via SMTP (Zoho)
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(msg)
            
            print(f"📧 E-mail enviado para {self.clinic_email}")
            return True
            
        except Exception as e:
            print(f"🚨 Erro no envio (Zoho): {str(e)}")
            return False