/* ═══════════════════════════════════════════════════════════════════════
   ThinkersPoint — Production JS v2
   ═══════════════════════════════════════════════════════════════════════ */

// Nav scroll
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 40);
  const st = document.getElementById('st');
  if (st) st.classList.toggle('on', window.scrollY > 500);
});

// Mobile nav
const burger = document.getElementById('burger');
const mobNav = document.getElementById('mob-nav');
const mobClose = document.getElementById('mob-close');

if (burger) burger.addEventListener('click', () => mobNav.classList.add('open'));
if (mobClose) mobClose.addEventListener('click', closeNav);
function closeNav() { if (mobNav) mobNav.classList.remove('open'); }
if (mobNav) mobNav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeNav));

// Intersection Observer — fade-in
const obs = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); obs.unobserve(e.target); }});
}, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('.fi').forEach(el => obs.observe(el));

// FAQ accordion
document.querySelectorAll('.faq-item').forEach(item => {
  const q = item.querySelector('.faq-q');
  if (q) q.addEventListener('click', () => {
    const isActive = item.classList.contains('active');
    item.closest('.faq-list').querySelectorAll('.faq-item').forEach(i => i.classList.remove('active'));
    if (!isActive) item.classList.add('active');
  });
});

// Counter animation for stat numbers
const counterObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (!e.isIntersecting) return;
    const el = e.target;
    const text = el.textContent.trim();
    const match = text.match(/^([\d,.]+)/);
    if (!match) return;
    const target = parseFloat(match[1].replace(/,/g, ''));
    if (isNaN(target)) return;
    const suffix = text.replace(match[1], '');
    const duration = 1600;
    const start = performance.now();
    const isDecimal = match[1].includes('.');
    function step(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = eased * target;
      el.textContent = (isDecimal ? current.toFixed(1) : Math.floor(current).toLocaleString()) + suffix;
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
    counterObs.unobserve(el);
  });
}, { threshold: 0.5 });
document.querySelectorAll('.stat-num').forEach(el => counterObs.observe(el));

// Parallax on page hero image
const heroImg = document.querySelector('.page-hero-bg img');
if (heroImg) {
  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    if (y < 800) heroImg.style.transform = `translateY(${y * 0.25}px) scale(1.05)`;
  }, { passive: true });
}

// Form submit simulation
function submitForm(e) {
  e.preventDefault();
  const btn = e.target.querySelector('[type="submit"]');
  if (!btn) return;
  btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
  btn.disabled = true;
  setTimeout(() => {
    btn.innerHTML = '<i class="fas fa-check"></i> Message Sent!';
    btn.style.background = 'linear-gradient(135deg,#10B981,#059669)';
    setTimeout(() => {
      e.target.reset();
      btn.innerHTML = '<i class="fas fa-paper-plane"></i> Send Message';
      btn.style.background = '';
      btn.disabled = false;
    }, 2000);
  }, 1000);
}

// Portfolio filter (for homepage)
document.querySelectorAll('.flt').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.flt').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const f = btn.dataset.f;
    document.querySelectorAll('.pf-card').forEach(card => {
      const show = f === 'all' || (card.dataset.cat || '').includes(f);
      card.style.display = show ? '' : 'none';
    });
  });
});
