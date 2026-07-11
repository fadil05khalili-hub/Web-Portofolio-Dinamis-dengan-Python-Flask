from extensions import db
from datetime import datetime


class Project(db.Model):
    """Model untuk menyimpan data proyek portofolio."""
    __tablename__ = 'project'

    id           = db.Column(db.Integer, primary_key=True)
    title        = db.Column(db.String(150), nullable=False)
    description  = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(300))          # Disimpan dipisah koma
    image_file   = db.Column(db.String(120), default='default.jpg')
    github_link  = db.Column(db.String(200))
    live_link    = db.Column(db.String(200))
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    def tech_list(self):
        """Kembalikan list teknologi dari string yang dipisah koma."""
        if self.technologies:
            return [t.strip() for t in self.technologies.split(',') if t.strip()]
        return []

    def __repr__(self):
        return f'<Project {self.title}>'


class Message(db.Model):
    """Model untuk pesan dari form kontak."""
    __tablename__ = 'message'

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(120), nullable=False)
    message    = db.Column(db.Text, nullable=False)
    is_read    = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Message from {self.name}>'


class Profile(db.Model):
    """Model untuk data profil pemilik portofolio (satu baris)."""
    __tablename__ = 'profile'

    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(100), default='Nama Anda')
    headline = db.Column(db.String(200), default='Full Stack Developer')
    about    = db.Column(db.Text, default='Deskripsi singkat tentang Anda.')
    photo    = db.Column(db.String(120), default='default_profile.jpg')
    email    = db.Column(db.String(120), default='email@example.com')
    github   = db.Column(db.String(200), default='')
    linkedin = db.Column(db.String(200), default='')
    location = db.Column(db.String(100), default='Indonesia')

    def __repr__(self):
        return f'<Profile {self.name}>'


class Skill(db.Model):
    """Model untuk daftar skill/keahlian."""
    __tablename__ = 'skill'

    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(100), nullable=False)
    level    = db.Column(db.Integer, default=80)       # 0–100
    category = db.Column(db.String(50), default='General')

    def __repr__(self):
        return f'<Skill {self.name} {self.level}%>'
