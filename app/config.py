import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    
    SQLALCHEMY_DATABASE_URI = (
        os.getenv("DATABASE_URL")
        if not os.getenv("DATABASE_URL", "").startswith("sqlite")
        else f"sqlite:///{os.path.join(basedir, '..', 'secure.db')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    _fernet_key = os.getenv("FERNET_KEY")
    if not _fernet_key:
        raise RuntimeError("FERNET_KEY is not set")

    FERNET_KEY = _fernet_key.encode()
