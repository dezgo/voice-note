import mimetypes
import smtplib
from email.message import EmailMessage
from pathlib import Path


def send_voice_note_email(
    title: str,
    body: str,
    audio_path: str,
    mail_server: str,
    mail_port: int,
    mail_username: str,
    mail_password: str,
    mail_from: str,
    mail_to: str,
) -> None:
    msg = EmailMessage()
    msg["Subject"] = f"Voice note: {title}"
    msg["From"] = mail_from
    msg["To"] = mail_to
    msg.set_content(body)

    path = Path(audio_path)
    if path.is_file():
        mime_type, _ = mimetypes.guess_type(path.name)
        main_type, sub_type = (mime_type or "audio/m4a").split("/", 1)
        msg.add_attachment(
            path.read_bytes(),
            maintype=main_type,
            subtype=sub_type,
            filename=path.name,
        )

    with smtplib.SMTP(mail_server, mail_port) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(mail_username, mail_password)
        smtp.send_message(msg)
