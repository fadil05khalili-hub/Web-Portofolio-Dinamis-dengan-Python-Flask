import os

class Config:
    # Keamanan
    SECRET_KEY = os.environ.get('SECRET_KEY', 'capstone-portfolio-secret-2026')

    # Database SQLite
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'portfolio.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload gambar
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # Akun admin (untuk demo — di produksi gunakan database/env)
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'admin123'
