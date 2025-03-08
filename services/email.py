import imaplib
import email


class EmailClient:
    def __init__(self, config):
        self.config = config

    def get_verification_code(self, email_user, email_pass):
        mail = imaplib.IMAP4_SSL(self.config.imap_server)
        mail.login(email_user, email_pass)
        mail.select("inbox")

        status, messages = mail.search(None, 'SUBJECT "Код подтверждения"')
        if status != "OK":
            return None

        latest_email_id = messages[0].split()[-1]
        status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode()
                return self._extract_code(body)
        return None

    def _extract_code(self, text):
        return ''.join(filter(str.isdigit, text))[:6]