import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from config import SENDER_EMAIL, APP_PASSWORD

def send_email_with_attachment(to_email, subject, body_text, filepath):
    msg = MIMEMultipart()
    msg['From'] = f"Legal Documentation Bot <{SENDER_EMAIL}>"
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body_text, 'plain'))
    
    filename = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        attachment_bytes = f.read()
        
    part = MIMEApplication(attachment_bytes, Name=filename)
    part['Content-Disposition'] = f'attachment; filename="{filename}"'
    msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
