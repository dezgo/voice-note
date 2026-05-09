import base64
import mimetypes
from pathlib import Path

import resend


def send_voice_note_email(
    title: str,
    body: str,
    audio_path: str,
    api_key: str,
    mail_from: str,
    mail_to: str,
) -> None:
    resend.api_key = api_key

    params: resend.Emails.SendParams = {
        "from": mail_from,
        "to": [mail_to],
        "subject": f"Voice note: {title}",
        "text": body,
    }

    path = Path(audio_path) if audio_path else None
    if path and path.is_file():
        mime_type, _ = mimetypes.guess_type(path.name)
        params["attachments"] = [
            {
                "filename": path.name,
                "content": base64.b64encode(path.read_bytes()).decode(),
                "content_type": mime_type or "audio/m4a",
            }
        ]

    resend.Emails.send(params)
