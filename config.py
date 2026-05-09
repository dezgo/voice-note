import os


class Config:
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

    RESEND_API_KEY = os.environ["RESEND_API_KEY"]
    MAIL_FROM = os.environ["MAIL_FROM"]
    MAIL_TO = os.environ["MAIL_TO"]

    UPLOAD_DIR = os.path.join("instance", "uploads", "voice_notes")
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB
