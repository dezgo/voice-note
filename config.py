import os


class Config:
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

    MAIL_SERVER = os.environ["MAIL_SERVER"]
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USERNAME = os.environ["MAIL_USERNAME"]
    MAIL_PASSWORD = os.environ["MAIL_PASSWORD"]
    MAIL_FROM = os.environ["MAIL_FROM"]
    MAIL_TO = os.environ["MAIL_TO"]

    UPLOAD_DIR = os.path.join("instance", "uploads", "voice_notes")
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB
