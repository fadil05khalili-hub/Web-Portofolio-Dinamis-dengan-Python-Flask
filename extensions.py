"""
extensions.py — Inisialisasi ekstensi Flask (db, dll.)
Dipisah dari app.py untuk menghindari circular import.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
