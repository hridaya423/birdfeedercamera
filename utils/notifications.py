from plyer import notification
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Notifier:
    def __init__(self, email_config=None):
        self.email_config = email_config

    def send_desktop_notification(self, title, message):
        notification.notify(title=title, message=message, timeout=5)

    def send_email_notification(self, subject, body, to_email):
        if not self.email_config:
            return False
        msg = MIMEMultipart()
        msg['From'] = self.email_config['from_email']
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        try:
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['from_email'], self.email_config['password'])
            text = msg.as_string()
            server.sendmail(self.email_config['from_email'], to_email, text)
            server.quit()
            return True
        except Exception as e:
            print(f"[ERROR] Email notification failed: {e}")
            return False
