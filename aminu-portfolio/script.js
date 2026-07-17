/* ─────────────────────────────────────────
   AmeeTech Portfolio — script.js
───────────────────────────────────────── */

// ── Theme Toggle (Light Default / Dark on .dark class) ──
const themeToggle = document.getElementById('themeToggle');
const themeIcon   = document.getElementById('themeIcon');

function applyTheme(isDark) {
  if (isDark) {
    document.body.classList.add('dark');
    themeIcon.className = 'fa-solid fa-sun';
    themeToggle.title   = 'Switch to light mode';
  } else {
    document.body.classList.remove('dark');
    themeIcon.className = 'fa-solid fa-moon';
    themeToggle.title   = 'Switch to dark mode';
  }
}

// Load saved preference (default = light)
const savedTheme = localStorage.getItem('ameetech-theme');
applyTheme(savedTheme === 'dark');

themeToggle.addEventListener('click', () => {
  const isDark = !document.body.classList.contains('dark');
  applyTheme(isDark);
  localStorage.setItem('ameetech-theme', isDark ? 'dark' : 'light');
});

// ── Loading Screen ──
window.addEventListener('load', () => {
  const loader = document.getElementById('loader');
  setTimeout(() => loader.classList.add('hidden'), 2200);
});

// ── Scroll Progress Bar ──
const scrollBar = document.getElementById('scroll-progress');
window.addEventListener('scroll', () => {
  const scrollTop   = document.documentElement.scrollTop;
  const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
  scrollBar.style.width = ((scrollTop / totalHeight) * 100) + '%';
}, { passive: true });

// ── Navbar Scroll State ──
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 60);
}, { passive: true });

// ── Hamburger Menu ──
const hamburger  = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobileMenu');

hamburger.addEventListener('click', () => {
  hamburger.classList.toggle('open');
  mobileMenu.classList.toggle('open');
  document.body.style.overflow = mobileMenu.classList.contains('open') ? 'hidden' : '';
});

document.querySelectorAll('.mob-link').forEach(link => {
  link.addEventListener('click', () => {
    hamburger.classList.remove('open');
    mobileMenu.classList.remove('open');
    document.body.style.overflow = '';
  });
});

// ── Typing Effect ──
const phrases = [
  'build AI-Powered Applications.',
  'engineer scalable backends.',
  'lead engineering teams.',
  'design intelligent systems.',
  'launch startup products.',
  'integrate LLMs & AI Agents.',
];

let phraseIndex = 0, charIndex = 0, isDeleting = false;
const typingEl  = document.getElementById('typingText');

function type() {
  const current = phrases[phraseIndex];
  if (isDeleting) {
    charIndex--;
    typingEl.textContent = current.substring(0, charIndex);
    if (charIndex === 0) {
      isDeleting = false;
      phraseIndex = (phraseIndex + 1) % phrases.length;
      setTimeout(type, 400);
      return;
    }
    setTimeout(type, 40);
  } else {
    charIndex++;
    typingEl.textContent = current.substring(0, charIndex);
    if (charIndex === current.length) {
      isDeleting = true;
      setTimeout(type, 2000);
      return;
    }
    setTimeout(type, 60);
  }
}
setTimeout(type, 2400);

// ── Animated Counters ──
let countersStarted = false;

function animateCounter(el, target) {
  let start     = null;
  const duration = 1800;
  const step = (timestamp) => {
    if (!start) start = timestamp;
    const progress = Math.min((timestamp - start) / duration, 1);
    const eased    = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.floor(eased * target);
    if (progress < 1) requestAnimationFrame(step);
    else el.textContent = target;
  };
  requestAnimationFrame(step);
}

function startCounters() {
  if (countersStarted) return;
  countersStarted = true;
  document.querySelectorAll('.stat-num[data-count]').forEach(el => {
    animateCounter(el, parseInt(el.dataset.count, 10));
  });
}
setTimeout(startCounters, 2600);

// ── Intersection Observer: Reveal Sections ──
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

// ── Back to Top ──
const backToTopBtn = document.getElementById('backToTop');
window.addEventListener('scroll', () => {
  backToTopBtn.classList.toggle('visible', window.scrollY > 500);
}, { passive: true });
backToTopBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

// ── Project Card Tilt on Hover ──
document.querySelectorAll('.project-card').forEach(card => {
  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const rotX = ((e.clientY - rect.top  - rect.height / 2) / (rect.height / 2)) * -5;
    const rotY = ((e.clientX - rect.left - rect.width  / 2) / (rect.width  / 2)) * 5;
    card.style.transform = `perspective(800px) rotateX(${rotX}deg) rotateY(${rotY}deg) translateY(-4px)`;
  });
  card.addEventListener('mouseleave', () => { card.style.transform = ''; });
});
