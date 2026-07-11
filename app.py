"""
app.py - Entry point Flask Portfolio
"""
import os
from datetime import datetime
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, flash
from extensions import db
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object('config.Config')

if not os.environ.get('VERCEL'):
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
db.init_app(app)

from models import Project, Message, Profile, Skill

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_profile():
    p = Profile.query.first()
    if not p:
        p = Profile()
        db.session.add(p)
        db.session.commit()
    return p


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            flash('Silakan login terlebih dahulu.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated


@app.context_processor
def inject_globals():
    return {
        'current_year': datetime.now().year,
        'profile': get_profile(),
        'unread_count': Message.query.filter_by(is_read=False).count()
    }


# ══ HALAMAN PUBLIK ══════════════════════════════════════════

@app.route('/')
def index():
    profile  = get_profile()
    projects = Project.query.order_by(Project.created_at.desc()).limit(3).all()
    skills   = Skill.query.all()
    return render_template('index.html', profile=profile, projects=projects, skills=skills)


@app.route('/about')
def about():
    profile = get_profile()
    skills  = Skill.query.all()
    education = [
        {'year': '2017 – 2020', 'school': 'SMK Merdeka Soreang',
         'degree': 'Jurusan TKR (Teknik Kendaraan Ringan)',
         'description': 'Mempelajari teknik otomotif dan kendaraan ringan secara teori dan praktik.'},
        {'year': '2014 – 2017', 'school': 'MTS Ppi 31 Banjaran',
         'degree': 'Madrasah Tsanawiyah',
         'description': 'Pendidikan menengah pertama berbasis pesantren.'},
        {'year': '2005 – 2011', 'school': 'SDN Kiangroke 2',
         'degree': 'Sekolah Dasar',
         'description': 'Pendidikan dasar di Bandung, Jawa Barat.'},
    ]
    experience = [
        {'year': '2021 – 2022', 'company': 'Pabrik Bozetro',
         'role': 'Keamanan / Satpam',
         'description': 'Bertanggung jawab menjaga keamanan dan ketertiban lingkungan pabrik.'},
        {'year': '2022 – 2023', 'company': 'Putral Bugel',
         'role': 'Teknisi Mobil',
         'description': 'Melakukan perawatan dan perbaikan kendaraan ringan secara berkala.'},
        {'year': '2023 – Sekarang', 'company': 'Freelance',
         'role': 'Data Entry',
         'description': 'Input data dan pengolahan dokumen menggunakan Microsoft Excel.'},
    ]
    certificates = [
        {'name': 'Microsoft Excel Advanced', 'issuer': 'Pelatihan Mandiri',   'year': '2023'},
        {'name': 'Teknik Kendaraan Ringan',   'issuer': 'SMK Merdeka Soreang', 'year': '2020'},
    ]
    return render_template('about.html', profile=profile, skills=skills,
                           education=education, experience=experience,
                           certificates=certificates)


@app.route('/portfolio')
def portfolio():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('portfolio.html', projects=projects)


@app.route('/portfolio/<int:id>')
def project_detail(id):
    project = Project.query.get_or_404(id)
    return render_template('project_detail.html', project=project)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    profile = get_profile()
    if request.method == 'POST':
        name    = request.form.get('name', '').strip()
        email   = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        if not name or not email or not message:
            flash('Semua kolom wajib diisi.', 'danger')
            return redirect(url_for('contact'))
        db.session.add(Message(name=name, email=email, message=message))
        db.session.commit()
        flash(f'Terima kasih {name}! Pesan Anda telah terkirim.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', profile=profile)


# ══ AUTENTIKASI ══════════════════════════════════════════════

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if 'user' in session:
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if (username == app.config['ADMIN_USERNAME'] and
                password == app.config['ADMIN_PASSWORD']):
            session['user'] = username
            flash('Login berhasil!', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Username atau password salah.', 'danger')
    return render_template('admin/login.html')


@app.route('/dashboard/login')
def login():
    return redirect(url_for('admin_login'))


@app.route('/admin/logout')
def admin_logout():
    session.pop('user', None)
    flash('Anda telah logout.', 'info')
    return redirect(url_for('admin_login'))


# ══ DASHBOARD ════════════════════════════════════════════════

@app.route('/admin')
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    stats = {
        'projects': Project.query.count(),
        'messages': Message.query.count(),
        'unread':   Message.query.filter_by(is_read=False).count(),
        'skills':   Skill.query.count(),
    }
    raw_msgs = Message.query.order_by(Message.created_at.desc()).limit(5).all()
    messages = [{'id': m.id, 'name': m.name, 'email': m.email,
                 'message': m.message, 'read': m.is_read,
                 'date': m.created_at.strftime('%d %b %Y')} for m in raw_msgs]
    projects = Project.query.order_by(Project.created_at.desc()).limit(4).all()
    return render_template('admin/dashboard.html', stats=stats,
                           messages=messages, projects=projects)


@app.route('/admin/projects')
@login_required
def admin_projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    project_list = [{
        'id': p.id, 'title': p.title,
        'short_desc': p.description[:80] + '...' if len(p.description) > 80 else p.description,
        'tech': p.tech_list(), 'category': 'Web App', 'featured': False,
    } for p in projects]
    return render_template('admin/projects.html', projects=project_list)


@app.route('/admin/projects/add', methods=['GET', 'POST'])
@login_required
def admin_add_project():
    if request.method == 'POST':
        title       = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        if not title or not description:
            flash('Judul dan deskripsi wajib diisi.', 'danger')
            return redirect(url_for('admin_add_project'))
        img_name = 'default.jpg'
        file = request.files.get('image')
        if file and file.filename and allowed_file(file.filename):
            img_name = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], img_name))
        db.session.add(Project(
            title=title, description=description,
            technologies=request.form.get('tech', '').strip(),
            image_file=img_name,
            github_link=request.form.get('github', '').strip(),
            live_link=request.form.get('demo', '').strip()
        ))
        db.session.commit()
        flash(f'Proyek "{title}" berhasil ditambahkan!', 'success')
        return redirect(url_for('admin_projects'))
    return render_template('admin/project_form.html', project=None, action='add')


@app.route('/admin/projects/edit/<int:project_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    if request.method == 'POST':
        project.title        = request.form.get('title', '').strip()
        project.description  = request.form.get('description', '').strip()
        project.technologies = request.form.get('tech', '').strip()
        project.github_link  = request.form.get('github', '').strip()
        project.live_link    = request.form.get('demo', '').strip()
        file = request.files.get('image')
        if file and file.filename and allowed_file(file.filename):
            img_name = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], img_name))
            project.image_file = img_name
        db.session.commit()
        flash(f'Proyek "{project.title}" berhasil diperbarui!', 'success')
        return redirect(url_for('admin_projects'))
    p = {'id': project.id, 'title': project.title, 'description': project.description,
         'tech': project.tech_list(), 'github': project.github_link or '',
         'demo': project.live_link or ''}
    return render_template('admin/project_form.html', project=p, action='edit')


@app.route('/admin/projects/delete/<int:project_id>', methods=['POST'])
@login_required
def admin_delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    title = project.title
    if project.image_file and project.image_file != 'default.jpg':
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], project.image_file)
        if os.path.exists(img_path):
            os.remove(img_path)
    db.session.delete(project)
    db.session.commit()
    flash(f'Proyek "{title}" berhasil dihapus.', 'success')
    return redirect(url_for('admin_projects'))


@app.route('/admin/profile', methods=['GET', 'POST'])
@login_required
def admin_profile():
    profile = get_profile()
    skills  = Skill.query.all()
    if request.method == 'POST':
        profile.name     = request.form.get('name', '').strip()
        profile.headline = request.form.get('headline', '').strip()
        profile.about    = request.form.get('bio', '').strip()
        profile.email    = request.form.get('email', '').strip()
        profile.github   = request.form.get('github', '').strip()
        profile.linkedin = request.form.get('linkedin', '').strip()
        profile.location = request.form.get('location', '').strip()
        file = request.files.get('photo')
        if file and file.filename and allowed_file(file.filename):
            photo_name = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_name))
            profile.photo = photo_name
        Skill.query.delete()
        for name, cat, level in zip(
                request.form.getlist('skill_name[]'),
                request.form.getlist('skill_cat[]'),
                request.form.getlist('skill_level[]')):
            name = name.strip()
            if name:
                try:
                    lvl = max(0, min(100, int(level)))
                except (ValueError, TypeError):
                    lvl = 80
                db.session.add(Skill(name=name, level=lvl, category=cat.strip() or 'General'))
        db.session.commit()
        flash('Profil berhasil diperbarui!', 'success')
        return redirect(url_for('admin_profile'))
    return render_template('admin/profile.html', profile=profile, skills=skills)


@app.route('/admin/messages')
@login_required
def admin_messages():
    raw = Message.query.order_by(Message.created_at.desc()).all()
    messages = [{'id': m.id, 'name': m.name, 'email': m.email,
                 'message': m.message, 'read': m.is_read,
                 'date': m.created_at.strftime('%d %b %Y, %H:%M')} for m in raw]
    return render_template('admin/messages.html', messages=messages)


@app.route('/admin/messages/read/<int:msg_id>', methods=['POST'])
@login_required
def admin_read_message(msg_id):
    msg = Message.query.get_or_404(msg_id)
    msg.is_read = True
    db.session.commit()
    flash('Pesan ditandai sudah dibaca.', 'success')
    return redirect(url_for('admin_messages'))


@app.route('/admin/messages/delete/<int:msg_id>', methods=['POST'])
@login_required
def admin_delete_message(msg_id):
    msg = Message.query.get_or_404(msg_id)
    db.session.delete(msg)
    db.session.commit()
    flash('Pesan berhasil dihapus.', 'success')
    return redirect(url_for('admin_messages'))


# ══ SEED DATA ════════════════════════════════════════════════

def seed_data():
    if not Profile.query.first():
        db.session.add(Profile(
            name='Muhamad Fadil Almubarok Khalili',
            headline='Data Analisis & IT Enthusiast',
            about=('Saya Muhamad Fadil Almubarok Khalili, mahasiswa yang sedang menekuni dunia '
                   'teknologi informasi, khususnya Python, Flask, Web Development, Database, dan Data Analysis. '
                   'Dengan latar belakang yang beragam, saya percaya bahwa pengalaman di luar akademik '
                   'turut membentuk cara saya berpikir dan menyelesaikan masalah secara praktis.\n\n'
                   'Saya memiliki minat besar dalam pengembangan aplikasi web dan analisis data. '
                   'Setiap proyek yang saya kerjakan menjadi kesempatan untuk terus belajar dan berkembang. '
                   'Saya berkomitmen untuk memberikan hasil terbaik dan terus meningkatkan kemampuan '
                   'seiring dengan perkembangan teknologi.'),
            email='fadil05khalili@gmail.com',
            github='https://github.com/fadil05khalili-hub',
            linkedin='https://linkedin.com/in/fadil05khalili',
            location='Bandung, Jawa Barat, Indonesia'
        ))
    if not Skill.query.first():
        db.session.add_all([
            Skill(name='Teknisi Mobil',   level=80, category='Teknik'),
            Skill(name='Microsoft Excel', level=85, category='Komputer'),
            Skill(name='Microsoft Word',  level=90, category='Komputer'),
            Skill(name='Bahasa Jepang',   level=50, category='Bahasa'),
            Skill(name='Data Entry',      level=85, category='Komputer'),
            Skill(name='Python / Flask',  level=75, category='Programming'),
        ])
    if not Project.query.first():
        db.session.add_all([
            Project(
                title='Web Portofolio Dinamis dengan Python Flask',
                description=('Website portofolio berbasis Python Flask yang menampilkan profil, '
                             'keterampilan, portofolio, dan halaman kontak secara dinamis. '
                             'Dilengkapi dashboard admin untuk mengelola data proyek, profil, '
                             'pesan, serta upload gambar menggunakan database SQLite.'),
                technologies='Python, Flask, SQLite, Bootstrap',
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
                github_link='https://github.com/fadil05khalili-hub/-301250033_Muhamad-Fadil-Almubarok-Khalili_TugasPertemuan11_Algo2_05-07-2026-Switch-repository',
                live_link=''
            ),
            Project(
                title='Kalkulator Transformasi Kekinian (Sakura UI)',
                description=('Aplikasi web kalkulator berbasis Python Flask dengan antarmuka modern '
                             'bertema Sakura Anime menggunakan konsep Glassmorphism dan Bento Grid. '
                             'Mendukung operasi aritmatika, konversi sistem bilangan, gerbang logika, '
                             'dengan arsitektur Flask Modular (Blueprints).'),
                technologies='Python, Flask, HTML/CSS, JavaScript',
                github_link='https://github.com/fadil05khalili-hub/Kalulator_Transpormasi_kekinian-.git',
                live_link=''
            ),
        ])
    db.session.commit()


# ══ ENTRY POINT ══════════════════════════════════════════════
    with app.app_context():
        db.create_all()

    if __name__ == '__main__':
        seed_data()
        app.run(debug=True)
