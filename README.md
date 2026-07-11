# Portfolio Flask — Capstone Project

Aplikasi web portofolio dinamis yang dibangun dengan Python Flask, SQLite, dan Bootstrap 5.

## Fitur

**Halaman Publik:**
- Home — foto profil, headline, statistik dinamis, featured projects
- About — bio, pendidikan, pengalaman, skill dengan progress bar
- Portfolio — grid semua proyek dengan thumbnail dan tech tags
- Detail Proyek — deskripsi lengkap, tech stack, links GitHub & demo
- Kontak — form yang tersimpan ke database

**Dashboard Admin:**
- Login/logout dengan session Flask
- Statistik: total projects, pesan, skills, pesan belum dibaca
- CRUD proyek (tambah, edit, hapus) + upload gambar
- Edit profil + manajemen skill dinamis
- Kotak masuk pesan + tandai dibaca / hapus

## Instalasi

```bash
# 1. Clone repository
git clone <url-repo>
cd portfolio-flask

# 2. Buat virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Install dependensi
pip install -r requirements.txt

# 4. Jalankan aplikasi
python app.py
```

Buka browser di `http://localhost:5000`

## Akun Demo Admin

| Username | Password  |
|----------|-----------|
| admin    | admin123  |

URL Login: `http://localhost:5000/admin/login`

## Struktur Folder

```
portfolio-flask/
├── app.py            # Entry point + semua routes
├── config.py         # Konfigurasi Flask
├── models.py         # Model database (Project, Message, Profile, Skill)
├── requirements.txt  # Dependensi Python
├── .env              # Environment variables
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   ├── portfolio.html
│   ├── project_detail.html
│   ├── contact.html
│   └── admin/
│       ├── base_admin.html
│       ├── dashboard.html
│       ├── login.html
│       ├── projects.html
│       ├── project_form.html
│       ├── profile.html
│       └── messages.html
└── static/
    ├── css/style.css
    ├── js/main.js
    └── uploads/
```

## Tech Stack

- **Backend:** Python 3, Flask, Flask-SQLAlchemy
- **Database:** SQLite
- **Frontend:** Bootstrap 5, Bootstrap Icons, Poppins (Google Fonts)
- **Template Engine:** Jinja2
