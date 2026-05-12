import os


class Config:

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-secret-change-in-production")

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    if os.environ.get("DATABASE_URL"):
        uri = os.environ.get("DATABASE_URL")
        if uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = uri
    elif os.environ.get("VERCEL"):
        SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/flowrix.db"
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'flowrix.db')}"

    UPLOAD_FOLDER = "/tmp/uploads" if os.environ.get("VERCEL") else os.path.join(BASE_DIR, "uploads")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
