"""
Stop Flask (Ctrl+C), jalankan: python fix_photo.py, lalu python app.py
"""
from app import app, db
from models import Profile, Skill, Project
import os, shutil

with app.app_context():

    # ── Rename foto ───────────────────────────────────────────
    src = 'static/uploads/WhatsApp Image 2026-07-10 at 22.42.46.jpeg'
    dst = 'static/uploads/fadil_profile.jpeg'
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.copy2(src, dst)
        print(f'Foto disalin: {dst}')

    # ── Update Profil ─────────────────────────────────────────
    p = Profile.query.first()
    if not p:
        p = Profile()
        db.session.add(p)
    p.name     = 'Muhamad Fadil Almubarok Khalili'
    p.headline = 'Data Analisis & IT Enthusiast'
    p.about    = ('Saya Muhamad Fadil Almubarok Khalili lahir 05 Februari 2005,seorang mahasiswa yang memiliki ketertarikan mendalam terhadap '
                  'teknologi informasi, khususnya Python, Flask, Web Development, Database, dan Data Analysis. '
                  'Dengan latar belakang yang beragam, saya percaya bahwa pengalaman di luar akademik '
                  'turut membentuk cara saya berpikir dan menyelesaikan masalah secara praktis.\n\n'
                  'Saya memiliki minat besar dalam pengembangan aplikasi web dan analisis data. '
                  'Setiap proyek yang saya kerjakan menjadi kesempatan untuk terus belajar dan berkembang. '
                  'Saya berkomitmen untuk memberikan hasil terbaik dan terus meningkatkan kemampuan '
                  'seiring dengan perkembangan teknologi.')
    p.email    = 'fadil05khalili@gmail.com'
    p.github   = 'https://github.com/fadil05khalili-hub'
    p.linkedin = 'https://linkedin.com/in/fadil05khalili'
    p.location = 'Bandung, Jawa Barat, Indonesia'
    if os.path.exists(dst):
        p.photo = 'fadil_profile.jpeg'
    db.session.commit()
    print(f'Profil  : {p.name}')

    # ── Update Skills ─────────────────────────────────────────
    Skill.query.delete()
    db.session.add_all([
        Skill(name='Teknisi Mobil',   level=80, category='Teknik'),
        Skill(name='Microsoft Excel', level=85, category='Komputer'),
        Skill(name='Microsoft Word',  level=90, category='Komputer'),
        Skill(name='Bahasa Jepang',   level=50, category='Bahasa'),
        Skill(name='Data Entry',      level=85, category='Komputer'),
        Skill(name='Python / Flask',  level=75, category='Programming'),
    ])
    db.session.commit()
    print('Skills  : 6 skill diupdate')

    # ── Update Projects ───────────────────────────────────────
    Project.query.delete()
    db.session.add_all([
        Project(
            title='Web Portofolio Dinamis dengan Python Flask',
            description=('Website portofolio berbasis Python Flask yang menampilkan profil, '
                         'keterampilan, portofolio, dan halaman kontak secara dinamis. '
                         'Dilengkapi dashboard admin untuk mengelola data proyek, profil, '
                         'pesan, serta upload gambar menggunakan database SQLite.'),
            technologies='Python, Flask, SQLite, Bootstrap',
            image_file='porto_flask.jpg',
            github_link='https://github.com/fadil05khalili-hub/Web-Portofolio-Dinamis-dengan-Python-Flask',
            live_link=''
        ),
        Project(
            title='Mini Sistem CLI – Struktur Data & Parsing Log',
            description=('Aplikasi Command Line Interface (CLI) menggunakan Python yang '
                         'mengimplementasikan struktur data dictionary, algoritma Bubble Sort, '
                         'Insertion Sort, Linear Search, Binary Search, serta parsing file log '
                         'untuk analisis aktivitas pengguna.'),
            technologies='Python, CLI, Dictionary, File Handling',
            image_file='mini_cli.jpg',
            github_link='https://github.com/fadil05khalili-hub/-301250033_Muhamad-Fadil-Almubarok-Khalili_TugasPertemuan11_Algo2_05-07-2026-Switch-repository',
            live_link=''
        ),
        Project(
            title='Kalkulator Transformasi Kekinian (Sakura UI)',
            description=('Aplikasi web kalkulator berbasis Python Flask dengan antarmuka modern '
                         'bertema Sakura Anime menggunakan konsep Glassmorphism dan Bento Grid. '
                         'Mendukung operasi aritmatika, konversi sistem bilangan, dan gerbang logika '
                         'dengan arsitektur Flask Modular (Blueprints).'),
            technologies='Python, Flask, HTML/CSS, JavaScript',
            image_file='kalkulator_sakura.jpg',
            github_link='https://github.com/fadil05khalili-hub/Kalulator_Transpormasi_kekinian-.git',
            live_link=''
        ),
    ])
    db.session.commit()
    print('Projects: 3 project diupdate')
    print('\nSELESAI — Jalankan: python app.py')
