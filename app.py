import logging
import os
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, request

from config import Config
from services.ai_service import curate_transcript
from services.email_service import send_voice_note_email

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)

_upload_dir = Path(app.instance_path) / "uploads" / "voice_notes"
_upload_dir.mkdir(parents=True, exist_ok=True)


@app.route("/api/voice-note", methods=["POST"])
def voice_note():
    transcript = request.form.get("transcript", "").strip()
    if not transcript:
        return jsonify({"ok": False, "error": "Missing transcript"}), 400

    audio_file = request.files.get("audio")
    if not audio_file or not audio_file.filename:
        return jsonify({"ok": False, "error": "Missing audio file"}), 400

    # Save audio with a timestamped filename
    ext = Path(audio_file.filename).suffix or ".m4a"
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    save_name = f"voice_note_{timestamp}{ext}"
    save_path = _upload_dir / save_name
    audio_file.save(save_path)
    logger.info("Saved audio to %s", save_path)

    # Curate with AI
    try:
        result = curate_transcript(transcript, app.config["OPENAI_API_KEY"])
    except Exception as exc:
        logger.exception("AI processing failed")
        return jsonify({"ok": False, "error": f"AI failure: {exc}"}), 502

    # Send email
    try:
        send_voice_note_email(
            title=result["title"],
            body=result["body"],
            audio_path=str(save_path),
            api_key=app.config["RESEND_API_KEY"],
            mail_from=app.config["MAIL_FROM"],
            mail_to=app.config["MAIL_TO"],
        )
    except Exception as exc:
        logger.exception("Email sending failed")
        return jsonify({"ok": False, "error": f"Email failure: {exc}"}), 502

    return jsonify({"ok": True, "title": result["title"], "message": "Voice note processed"})


if __name__ == "__main__":
    app.run(debug=False)
