// ── Navbar scroll effect ─────────────────────────────────────
const navbar = document.querySelector('.navbar-custom');
if (navbar) {
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 20);
  });
}

// ── Active nav link ───────────────────────────────────────────
(function () {
  const links = document.querySelectorAll('.nav-link-custom');
  const path = window.location.pathname;
  links.forEach(link => {
    const href = link.getAttribute('href');
    if (href && path === href) link.classList.add('active');
    else if (href && href !== '/' && path.startsWith(href)) link.classList.add('active');
  });
})();

// ── Progress bar animation (Intersection Observer) ────────────
(function () {
  const fills = document.querySelectorAll('.progress-fill');
  if (!fills.length) return;
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        el.style.width = el.dataset.width || el.style.width;
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.2 });
  fills.forEach(fill => {
    const target = fill.style.width;
    fill.style.width = '0%';
    fill.dataset.width = target;
    observer.observe(fill);
  });
})();

// ── Counter animation ─────────────────────────────────────────
function animateCounter(el, target, duration = 1800) {
  let start = 0;
  const step = target / (duration / 16);
  const timer = setInterval(() => {
    start += step;
    if (start >= target) { el.textContent = target + (el.dataset.suffix || ''); clearInterval(timer); }
    else el.textContent = Math.floor(start) + (el.dataset.suffix || '');
  }, 16);
}
(function () {
  const counters = document.querySelectorAll('.counter-num');
  if (!counters.length) return;
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        animateCounter(el, parseInt(el.dataset.target), 1600);
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.3 });
  counters.forEach(c => observer.observe(c));
})();

// ── Flash message auto-dismiss ─────────────────────────────────
(function () {
  const msgs = document.querySelectorAll('.flash-msg');
  msgs.forEach(msg => {
    setTimeout(() => {
      msg.style.animation = 'slideInRight .3s ease reverse';
      setTimeout(() => msg.remove(), 300);
    }, 4500);
    const closeBtn = msg.querySelector('.flash-close');
    if (closeBtn) closeBtn.addEventListener('click', () => msg.remove());
  });
})();

// ── Portfolio filter ──────────────────────────────────────────
(function () {
  const filterBtns = document.querySelectorAll('.filter-btn');
  if (!filterBtns.length) return;
  filterBtns.forEach(btn => {
    btn.addEventListener('click', function () {
      filterBtns.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      const cat = this.dataset.category;
      const cards = document.querySelectorAll('.portfolio-card-wrap');
      cards.forEach(card => {
        if (cat === 'all' || card.dataset.category === cat) {
          card.style.display = '';
          card.style.animation = 'fadeInUp .4s ease';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
})();

// ── Sidebar mobile toggle ─────────────────────────────────────
(function () {
  const toggleBtn = document.getElementById('sidebar-toggle');
  const sidebar = document.querySelector('.sidebar');
  const overlay = document.getElementById('sidebar-overlay');
  if (!toggleBtn || !sidebar) return;
  function openSidebar() {
    sidebar.classList.add('open');
    if (overlay) overlay.style.display = 'block';
  }
  function closeSidebar() {
    sidebar.classList.remove('open');
    if (overlay) overlay.style.display = 'none';
  }
  toggleBtn.addEventListener('click', () => sidebar.classList.contains('open') ? closeSidebar() : openSidebar());
  if (overlay) overlay.addEventListener('click', closeSidebar);
})();

// ── Image preview on upload ──────────────────────────────────
(function () {
  const inputs = document.querySelectorAll('input[type="file"][data-preview]');
  inputs.forEach(input => {
    input.addEventListener('change', function () {
      const previewId = this.dataset.preview;
      const preview = document.getElementById(previewId);
      if (!preview || !this.files[0]) return;
      const reader = new FileReader();
      reader.onload = e => { preview.src = e.target.result; preview.style.display = 'block'; };
      reader.readAsDataURL(this.files[0]);
    });
  });
})();

// ── Smooth scroll for anchor links ───────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', function (e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  });
});

// ── AOS-like fade-in on scroll ────────────────────────────────
(function () {
  const elements = document.querySelectorAll('[data-animate]');
  if (!elements.length) return;
  elements.forEach(el => { el.style.opacity = '0'; el.style.transform = 'translateY(24px)'; el.style.transition = 'opacity .6s ease, transform .6s ease'; });
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const delay = el.dataset.delay || 0;
        setTimeout(() => { el.style.opacity = '1'; el.style.transform = 'translateY(0)'; }, delay);
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.1 });
  elements.forEach(el => observer.observe(el));
})();
