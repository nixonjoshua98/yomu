import smtplib
from email.message import EmailMessage


def _create_message(
    subject: str, from_email: str, to_email: str, content: str
) -> EmailMessage:

    msg = EmailMessage()

    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    msg.set_content(content)

    return msg


def send_email(
    subject: str, from_email: str, to_email: str, password: str, content: str
):

    msg = _create_message(subject, from_email, to_email, content)

    with smtplib.SMTP("smtp.gmail.com", 587) as svr:
        svr.starttls()

        svr.login(from_email, password)

        svr.send_message(msg)
