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

    def _load_template(self, template_path="Templates_HTML\agendamento.html"):
        with open(template_path, "r", encoding="utf-8") as file:
            return Template(file.read())

    def send_booking_email(self, client_phone, summary):
        try:
            masked_phone = f"{client_phone[:5]}...{client_phone[-3:]}"
            template = self._load_template()
            html_content = template.render(
                cliente=masked_phone,
                resumo=summary.replace("\n", "<br>")
            )

            msg = MIMEMultipart()
            msg["From"] = f"Agendamentos Luar Clínica <{self.email_user}>"
            msg["To"] = self.clinic_email
            msg["Subject"] = f"✂️ Novo Agendamento - {masked_phone}"
            msg.attach(MIMEText(html_content, "html"))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(msg)
            
            print(f"📧 Agendamento enviado para {self.clinic_email}")
            return True
            
        except Exception as e:
            print(f"🚨 Erro no envio de agendamento: {str(e)}")
            return False

    def send_feedback_email(self, client_phone, feedback_text):
        try:
            print("Capturando feedback do cliente")
            masked_phone = f"{client_phone[:5]}...{client_phone[-3:]}"
            html_content = (
                f"<h3>✨ Novo Feedback Recebido</h3>"
                f"<p><strong>Cliente:</strong> {masked_phone}</p>"
                f"<p><strong>Feedback:</strong><br>{feedback_text}</p>"
                "<p style='font-size:12px; color:#666;'>🔒 Dados protegidos pela LGPD.</p>"
            )
            print("feedback do cliente recebido ✅")
            
            print("iniciando validação das variáveis de ambiente ✨")
            msg = MIMEMultipart()
            msg["From"] = self.email_user
            msg["To"] = self.clinic_email
            msg["Subject"] = f"✨ Feedback recebido - {masked_phone}"
            msg.attach(MIMEText(html_content, "html"))
            print("variáveis inicializadas corretamente ✅"
                  + str(self.smtp_server) + " |" + str(self.smtp_port) + " |" + str(self.email_user) + " |" + str(self.email_password) + " |" + str(self.clinic_email)
                  )
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.sendmail(self.email_user,self.clinic_email,msg.as_string())

            print(f"📧 Feedback enviado para {self.clinic_email}")
            return True

        except Exception as e:
            print(f"🚨 Erro no envio de feedback: {str(e)}")
            return False
