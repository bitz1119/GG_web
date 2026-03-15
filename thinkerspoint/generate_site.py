#!/usr/bin/env python3
"""
ThinkersPoint Multi-Page Site Generator
Generates 48+ SEO-optimized pages from templates
"""

import os
import json
from pathlib import Path
from urllib.parse import quote
from datetime import datetime

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR

# ═══════════════════════════════════════════════════════════════════════════
# SHARED CSS
# ═══════════════════════════════════════════════════════════════════════════

SHARED_CSS = """
/* ────────────────────────────────────────────────────────────────────── */
/* VARIABLES & RESET */
/* ────────────────────────────────────────────────────────────────────── */
:root {
  --bg:        #06060E;
  --bg2:       #0B0B1C;
  --bg3:       #101028;
  --glass:     rgba(255,255,255,0.04);
  --glass-h:   rgba(255,255,255,0.07);
  --border:    rgba(255,255,255,0.07);
  --border-a:  rgba(99,102,241,0.45);

  --indigo:    #6366F1;
  --violet:    #8B5CF6;
  --pink:      #EC4899;
  --amber:     #F59E0B;
  --green:     #10B981;
  --cyan:      #06B6D4;

  --grad:       linear-gradient(135deg,#6366F1,#8B5CF6);
  --grad-full:  linear-gradient(135deg,#6366F1 0%,#8B5CF6 50%,#EC4899 100%);
  --grad-text:  linear-gradient(135deg,#818CF8,#A78BFA,#F472B6);

  --text:   #F9FAFB;
  --text2:  #D1D5DB;
  --text3:  #9CA3AF;
  --text4:  #6B7280;

  --shadow:  0 20px 60px rgba(0,0,0,.7);
  --glow:    0 0 40px rgba(99,102,241,.25);
  --glow-h:  0 0 60px rgba(99,102,241,.45);

  --r-s: 8px; --r-m: 14px; --r-l: 20px; --r-xl: 28px;
  --max: 1180px;
  --fh: 'Space Grotesk', sans-serif;
  --fb: 'Inter', sans-serif;
  --t: 0.32s cubic-bezier(.4,0,.2,1);
}

*, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
html { scroll-behavior:smooth; font-size:16px; }
body { font-family:var(--fb); background:var(--bg); color:var(--text); line-height:1.65; overflow-x:hidden; }
img  { max-width:100%; display:block; }
a    { color:inherit; text-decoration:none; }
button { cursor:pointer; border:none; background:none; font-family:inherit; }
ul { list-style:none; }

/* ────────────────────────────────────────────────────────────────────── */
/* UTILITIES */
/* ────────────────────────────────────────────────────────────────────── */
.container { max-width:var(--max); margin:0 auto; padding:0 28px; }
.grad-text {
  background:var(--grad-text);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  background-clip:text;
}
.chip {
  display:inline-flex; align-items:center; gap:8px;
  padding:5px 16px; border-radius:50px;
  background:rgba(99,102,241,.12); border:1px solid rgba(99,102,241,.28);
  font-size:12px; font-weight:600; color:#A5B4FC; letter-spacing:.5px;
  text-transform:uppercase;
}
.chip .dot {
  width:6px; height:6px; border-radius:50%;
  background:var(--indigo); animation:blink 2s infinite;
}
@keyframes blink { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.5;transform:scale(1.4)} }

.sec-head { text-align:center; margin-bottom:64px; }
.sec-head .chip { margin-bottom:18px; }
.sec-head h2 {
  font-family:var(--fh); font-size:clamp(32px,5vw,52px); font-weight:800;
  line-height:1.08; letter-spacing:-.5px; margin-bottom:18px;
}
.sec-head p { font-size:17px; color:var(--text3); max-width:560px; margin:0 auto; line-height:1.75; }

.fi { opacity:0; transform:translateY(32px); transition:opacity .7s ease, transform .7s ease; }
.fi.in { opacity:1; transform:none; }
.d1{transition-delay:.1s} .d2{transition-delay:.2s} .d3{transition-delay:.3s}
.d4{transition-delay:.4s} .d5{transition-delay:.5s}

/* ────────────────────────────────────────────────────────────────────── */
/* NAV – DESKTOP & MEGA DROPDOWN */
/* ────────────────────────────────────────────────────────────────────── */
#nav {
  position:fixed; inset:0 0 auto 0; z-index:900;
  padding:0 28px; transition:background var(--t), box-shadow var(--t);
}
#nav.scrolled {
  background:rgba(6,6,14,.92); backdrop-filter:blur(24px);
  -webkit-backdrop-filter:blur(24px);
  box-shadow:0 1px 0 var(--border);
}
.nav-inner {
  max-width:var(--max); margin:0 auto;
  display:flex; align-items:center; justify-content:space-between;
  height:68px; gap:32px;
}
.nav-logo {
  display:flex; align-items:center; gap:10px;
  font-family:var(--fh); font-size:20px; font-weight:700; white-space:nowrap;
}
.logo-box {
  width:36px; height:36px; border-radius:10px;
  background:var(--grad); display:flex; align-items:center; justify-content:center;
  font-size:17px; flex-shrink:0;
}
.nav-links { display:flex; align-items:center; gap:4px; }
.nav-links a {
  padding:7px 15px; font-size:14px; font-weight:500;
  color:var(--text3); border-radius:var(--r-s);
  transition:color var(--t), background var(--t);
}
.nav-links a:hover { color:var(--text); background:var(--glass); }

/* Mega Dropdown */
.nav-item { position:relative; }
.nav-item > a {
  display:flex; align-items:center; gap:5px; padding:7px 15px;
  font-size:14px; font-weight:500; color:var(--text3);
  border-radius:var(--r-s); transition:all var(--t);
}
.nav-item > a::after { content:''; width:6px; height:6px; border-radius:2px; background:currentColor; opacity:.5; }
.nav-item > a:hover { color:var(--text); background:var(--glass); }
.dropdown {
  display:none; position:absolute; top:100%; left:0; z-index:910;
  background:rgba(11,11,28,.95); backdrop-filter:blur(20px);
  -webkit-backdrop-filter:blur(20px);
  border:1px solid var(--border); border-radius:var(--r-l);
  min-width:240px; margin-top:8px; padding:12px 0;
  box-shadow:0 20px 40px rgba(0,0,0,.5);
}
.nav-item:hover .dropdown { display:block; }
.dropdown a {
  display:block; padding:10px 20px; font-size:13px; color:var(--text3);
  transition:all var(--t);
}
.dropdown a:hover { color:#fff; background:rgba(99,102,241,.15); padding-left:24px; }
.dropdown .divider { height:1px; background:var(--border); margin:8px 0; }

.nav-cta {
  padding:9px 22px; background:var(--grad); border-radius:var(--r-s);
  font-size:14px; font-weight:600; color:#fff; white-space:nowrap;
  transition:opacity var(--t), transform var(--t), box-shadow var(--t);
}
.nav-cta:hover { opacity:.88; transform:translateY(-1px); box-shadow:var(--glow); }
.nav-burger { display:none; color:var(--text); font-size:20px; padding:8px; }

/* Mobile Nav */
#mob-nav {
  display:none; position:fixed; inset:0; z-index:950;
  background:rgba(6,6,14,.97); backdrop-filter:blur(20px);
  flex-direction:column; align-items:center; justify-content:center; gap:6px;
}
#mob-nav.open { display:flex; }
#mob-nav a {
  font-family:var(--fh); font-size:30px; font-weight:700;
  color:var(--text2); padding:12px 48px; border-radius:var(--r-m);
  transition:color var(--t), background var(--t);
}
#mob-nav a:hover { color:#fff; background:var(--glass-h); }
.mob-close {
  position:absolute; top:24px; right:28px;
  font-size:22px; color:var(--text3); padding:8px; cursor:pointer;
}

/* ────────────────────────────────────────────────────────────────────── */
/* PAGE HERO (for inner pages) */
/* ────────────────────────────────────────────────────────────────────── */
.page-hero {
  min-height:420px; display:flex; align-items:center; justify-content:center;
  padding:130px 28px 80px; position:relative; overflow:hidden;
}
.page-hero::before {
  content:''; position:absolute; inset:0; z-index:0;
  background-image:
    linear-gradient(rgba(255,255,255,.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,.025) 1px, transparent 1px);
  background-size:52px 52px;
}
.page-hero::after {
  content:''; position:absolute; inset:0; z-index:1;
  background:linear-gradient(135deg, rgba(99,102,241,.15) 0%, rgba(139,92,246,.1) 100%);
}
.page-hero-inner {
  position:relative; z-index:2; text-align:center; max-width:700px;
}
.page-hero h1 {
  font-family:var(--fh); font-size:clamp(36px,6vw,56px);
  font-weight:800; line-height:1.08; letter-spacing:-.5px; margin-bottom:18px;
}
.page-hero p {
  font-size:17px; color:var(--text3); line-height:1.75;
}

/* ────────────────────────────────────────────────────────────────────── */
/* BUTTONS */
/* ────────────────────────────────────────────────────────────────────── */
.btn-prim {
  display:inline-flex; align-items:center; gap:9px;
  padding:13px 28px; background:var(--grad); border-radius:var(--r-m);
  font-size:15px; font-weight:600; color:#fff;
  box-shadow:0 4px 24px rgba(99,102,241,.42);
  transition:all var(--t);
}
.btn-prim:hover { transform:translateY(-2px); box-shadow:0 8px 36px rgba(99,102,241,.6); }
.btn-sec {
  display:inline-flex; align-items:center; gap:9px;
  padding:13px 28px; background:var(--glass); border:1px solid var(--border);
  border-radius:var(--r-m); font-size:15px; font-weight:600; color:var(--text2);
  transition:all var(--t);
}
.btn-sec:hover { background:var(--glass-h); border-color:var(--border-a); color:#fff; transform:translateY(-2px); }

/* ────────────────────────────────────────────────────────────────────── */
/* FEATURE GRID */
/* ────────────────────────────────────────────────────────────────────── */
.feat-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:22px; margin-bottom:80px; }
.feat-card {
  background:var(--glass); border:1px solid var(--border);
  border-radius:var(--r-xl); padding:32px 28px;
  position:relative; overflow:hidden; cursor:default;
  transition:all var(--t);
}
.feat-card::after {
  content:''; position:absolute; inset:0; border-radius:inherit;
  background:var(--grad-full); opacity:0; transition:opacity var(--t);
}
.feat-card:hover {
  border-color:var(--border-a); transform:translateY(-8px); box-shadow:var(--glow);
}
.feat-card:hover::after { opacity:.05; }
.feat-icon {
  width:48px; height:48px; border-radius:var(--r-m);
  display:flex; align-items:center; justify-content:center;
  font-size:20px; margin-bottom:20px;
  position:relative; z-index:1;
  transition:transform var(--t);
}
.feat-card:hover .feat-icon { transform:scale(1.1) rotate(-6deg); }
.feat-card h3 {
  font-family:var(--fh); font-size:18px; font-weight:700;
  margin-bottom:10px; position:relative; z-index:1;
}
.feat-card p {
  font-size:14px; color:var(--text3); line-height:1.72; position:relative; z-index:1;
}

/* ────────────────────────────────────────────────────────────────────── */
/* PROCESS STEPS */
/* ────────────────────────────────────────────────────────────────────── */
.process {
  display:grid; grid-template-columns:repeat(4,1fr); gap:20px; margin-bottom:80px;
}
.pstep {
  background:var(--glass); border:1px solid var(--border);
  border-radius:var(--r-l); padding:28px 24px; position:relative;
  text-align:center; transition:all var(--t);
}
.pstep::before {
  content:attr(data-step);
  position:absolute; top:-12px; left:50%; transform:translateX(-50%);
  width:32px; height:32px; border-radius:50%;
  background:var(--grad); color:#fff;
  display:flex; align-items:center; justify-content:center;
  font-size:14px; font-weight:700;
}
.pstep:hover {
  border-color:var(--border-a); transform:translateY(-6px); box-shadow:var(--glow);
}
.pstep h4 {
  font-family:var(--fh); font-size:16px; font-weight:700; margin-bottom:8px;
  margin-top:16px;
}
.pstep p { font-size:13px; color:var(--text3); line-height:1.6; }

/* ────────────────────────────────────────────────────────────────────── */
/* STATS ROW */
/* ────────────────────────────────────────────────────────────────────── */
.stats-row {
  display:grid; grid-template-columns:repeat(4,1fr); gap:20px; margin:80px 0;
}
.stat-box {
  background:var(--glass); border:1px solid var(--border);
  border-radius:var(--r-xl); padding:32px 28px; text-align:center;
  transition:all var(--t);
}
.stat-box:hover {
  border-color:var(--border-a); transform:translateY(-6px); box-shadow:var(--glow);
}
.stat-num {
  font-family:var(--fh); font-size:42px; font-weight:800;
  background:var(--grad-text);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  background-clip:text; margin-bottom:6px;
}
.stat-label { font-size:13px; color:var(--text3); font-weight:500; }

/* ────────────────────────────────────────────────────────────────────── */
/* FAQ ACCORDION */
/* ────────────────────────────────────────────────────────────────────── */
.faq { margin:80px 0; }
.faq-item {
  background:var(--glass); border:1px solid var(--border);
  border-radius:var(--r-l); margin-bottom:14px;
  overflow:hidden; transition:all var(--t);
}
.faq-item:hover { border-color:var(--border-a); }
.faq-q {
  padding:18px 24px; cursor:pointer; display:flex;
  align-items:center; justify-content:space-between; gap:16px;
  font-weight:600; transition:all var(--t);
}
.faq-q:hover { background:var(--glass-h); }
.faq-q i { transition:transform var(--t); }
.faq-item.active .faq-q i { transform:rotate(180deg); }
.faq-a {
  max-height:0; overflow:hidden; transition:max-height var(--t);
  padding:0 24px;
}
.faq-item.active .faq-a {
  max-height:500px; padding:0 24px 18px 24px;
}
.faq-a p { color:var(--text3); line-height:1.75; }

/* ────────────────────────────────────────────────────────────────────── */
/* CTA SECTION */
/* ────────────────────────────────────────────────────────────────────── */
#cta-section {
  background:var(--bg2); padding:80px 28px; margin:80px 0 0 0;
  text-align:center;
}
#cta-section .container { max-width:700px; }
#cta-section h2 {
  font-family:var(--fh); font-size:clamp(32px,5vw,48px);
  font-weight:800; margin-bottom:18px; line-height:1.1;
}
#cta-section p {
  font-size:17px; color:var(--text3); margin-bottom:32px; line-height:1.75;
}
#cta-section .btn-prim { margin-right:14px; }

/* ────────────────────────────────────────────────────────────────────── */
/* FOOTER */
/* ────────────────────────────────────────────────────────────────────── */
footer {
  background:var(--bg2); border-top:1px solid var(--border);
  padding:60px 28px 28px; font-size:14px;
}
.ft-grid {
  max-width:var(--max); margin:0 auto;
  display:grid; grid-template-columns:2fr 1fr 1fr 1fr;
  gap:40px; margin-bottom:40px;
}
.ft-brand p { color:var(--text3); margin:16px 0 24px 0; line-height:1.75; }
.ft-soc { display:flex; gap:12px; }
.fs {
  width:36px; height:36px; border-radius:8px;
  background:var(--glass); border:1px solid var(--border);
  display:flex; align-items:center; justify-content:center;
  transition:all var(--t);
}
.fs:hover {
  background:var(--border-a); transform:translateY(-2px); box-shadow:var(--glow);
}
.ft-col h4 {
  font-family:var(--fh); font-size:15px; font-weight:700; margin-bottom:18px;
}
.ft-col ul { display:flex; flex-direction:column; gap:9px; }
.ft-col a {
  color:var(--text3); transition:color var(--t);
}
.ft-col a:hover { color:#fff; }
.ft-bottom {
  max-width:var(--max); margin:0 auto;
  border-top:1px solid var(--border); padding-top:24px;
  display:flex; align-items:center; justify-content:space-between;
  flex-wrap:wrap; gap:16px;
  color:var(--text4); font-size:13px;
}
.ft-bl { display:flex; gap:16px; }
.ft-bl a {
  color:var(--text3); transition:color var(--t);
}
.ft-bl a:hover { color:#fff; }

/* ────────────────────────────────────────────────────────────────────── */
/* SCROLL TO TOP */
/* ────────────────────────────────────────────────────────────────────── */
#st {
  position:fixed; bottom:24px; right:24px; z-index:800;
  width:44px; height:44px; border-radius:50%;
  background:var(--grad); color:#fff; font-size:18px;
  display:flex; align-items:center; justify-content:center;
  opacity:0; pointer-events:none; transition:all var(--t);
  box-shadow:var(--glow);
}
#st.on { opacity:1; pointer-events:auto; }
#st:hover { transform:translateY(-3px); }

/* ────────────────────────────────────────────────────────────────────── */
/* RESPONSIVE */
/* ────────────────────────────────────────────────────────────────────── */
@media (max-width:1024px) {
  .feat-grid { grid-template-columns:repeat(2,1fr); }
  .process { grid-template-columns:repeat(2,1fr); }
  .stats-row { grid-template-columns:repeat(2,1fr); }
  .ft-grid { grid-template-columns:repeat(2,1fr); }
  .nav-links { gap:0; }
  .nav-links a { padding:6px 12px; font-size:13px; }
}

@media (max-width:768px) {
  .nav-burger { display:block; }
  .nav-links { display:none; }
  .dropdown { display:none !important; }
  .feat-grid { grid-template-columns:1fr; }
  .process { grid-template-columns:1fr; }
  .stats-row { grid-template-columns:1fr; }
  .ft-grid { grid-template-columns:1fr; }
  .page-hero h1 { font-size:32px; }
  #cta-section .btn-prim { margin-right:0; margin-bottom:10px; }
}
"""

# ═══════════════════════════════════════════════════════════════════════════
# SHARED JS
# ═══════════════════════════════════════════════════════════════════════════

SHARED_JS = """
// Nav scroll effect
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

function closeNav() {
  mobNav.classList.remove('open');
}

// Close mobile nav when link clicked
if (mobNav) {
  mobNav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', closeNav);
  });
}

// Fade-in on scroll
const obs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) e.target.classList.add('in');
  });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.fi').forEach(el => obs.observe(el));

// FAQ accordion
document.querySelectorAll('.faq-item').forEach(item => {
  const q = item.querySelector('.faq-q');
  q.addEventListener('click', () => {
    document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('active'));
    item.classList.add('active');
  });
});

// Form submit simulation
function submitForm(e) {
  e.preventDefault();
  const btn = e.target.querySelector('[type="submit"]');
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
"""

# ═══════════════════════════════════════════════════════════════════════════
# PAGE DATA & TEMPLATES
# ═══════════════════════════════════════════════════════════════════════════

def nav_html(root=""):
    """Generate navigation HTML with mega dropdowns"""
    return f"""
<nav id="nav">
  <div class="nav-inner">
    <a href="{root}index.html" class="nav-logo">
      <div class="logo-box">💡</div>
      ThinkersPoint
    </a>
    <div class="nav-links">
      <div class="nav-item">
        <a href="#">Services</a>
        <div class="dropdown">
          <a href="{root}services/digital-marketing.html">Digital Marketing</a>
          <a href="{root}services/performance-marketing.html">Performance Marketing</a>
          <a href="{root}services/social-media-marketing.html">Social Media Marketing</a>
          <a href="{root}services/seo-services.html">SEO Services</a>
          <a href="{root}services/web-development.html">Web Development</a>
          <a href="{root}services/app-development.html">App Development</a>
          <a href="{root}services/ui-ux-design.html">UI/UX Design</a>
          <a href="{root}services/ai-solutions.html">AI Solutions</a>
        </div>
      </div>
      <div class="nav-item">
        <a href="#">Locations</a>
        <div class="dropdown">
          <a href="{root}locations/india.html">India</a>
          <a href="{root}locations/usa.html">USA</a>
          <a href="{root}locations/uk.html">UK & London</a>
          <a href="{root}locations/uae-dubai.html">UAE & Dubai</a>
          <a href="{root}locations/australia.html">Australia</a>
          <a href="{root}locations/canada.html">Canada</a>
          <a href="{root}locations/singapore.html">Singapore</a>
        </div>
      </div>
      <div class="nav-item">
        <a href="#">Industries</a>
        <div class="dropdown">
          <a href="{root}industries/real-estate.html">Real Estate</a>
          <a href="{root}industries/insurance.html">Insurance</a>
          <a href="{root}industries/healthcare.html">Healthcare</a>
          <a href="{root}industries/ecommerce.html">E-commerce</a>
          <a href="{root}industries/manufacturing.html">Manufacturing</a>
          <a href="{root}industries/saas-tech.html">SaaS & Tech</a>
        </div>
      </div>
      <a href="{root}about.html">About</a>
      <a href="{root}blog/">Blog</a>
    </div>
    <a href="{root}contact.html" class="nav-cta">Get Started</a>
    <button id="burger" class="nav-burger"><i class="fas fa-bars"></i></button>
  </div>
</nav>

<div id="mob-nav">
  <a href="{root}index.html">Home</a>
  <a href="{root}about.html">About</a>
  <a href="{root}services/digital-marketing.html">Services</a>
  <a href="{root}locations/india.html">Locations</a>
  <a href="{root}industries/real-estate.html">Industries</a>
  <a href="{root}blog/">Blog</a>
  <a href="{root}contact.html">Contact</a>
  <button id="mob-close" class="mob-close"><i class="fas fa-times"></i></button>
</div>
"""

def footer_html(root=""):
    """Generate footer HTML"""
    return f"""
<footer>
  <div class="ft-grid">
    <div class="ft-brand">
      <div class="nav-logo">
        <div class="logo-box">💡</div>
        ThinkersPoint
      </div>
      <p>Your strategic partner for digital marketing, business growth, and technology innovation. We think, strategize, and deliver.</p>
      <div class="ft-soc">
        <a href="https://www.linkedin.com/in/surajaggarwal38/" target="_blank" rel="noopener" class="fs">
          <i class="fab fa-linkedin-in"></i>
        </a>
        <a href="#" class="fs"><i class="fab fa-twitter"></i></a>
        <a href="#" class="fs"><i class="fab fa-instagram"></i></a>
        <a href="#" class="fs"><i class="fab fa-facebook-f"></i></a>
      </div>
    </div>

    <div class="ft-col">
      <h4>Services</h4>
      <ul>
        <li><a href="{root}services/digital-marketing.html">Digital Marketing</a></li>
        <li><a href="{root}services/performance-marketing.html">Performance Marketing</a></li>
        <li><a href="{root}services/social-media-marketing.html">SMM</a></li>
        <li><a href="{root}services/ai-solutions.html">AI Solutions</a></li>
        <li><a href="{root}services/web-development.html">Web Development</a></li>
        <li><a href="{root}services/ui-ux-design.html">UI/UX Design</a></li>
      </ul>
    </div>

    <div class="ft-col">
      <h4>Company</h4>
      <ul>
        <li><a href="{root}about.html">About Us</a></li>
        <li><a href="{root}portfolio.html">Portfolio</a></li>
        <li><a href="{root}blog/">Blog</a></li>
        <li><a href="{root}contact.html">Contact</a></li>
      </ul>
    </div>

    <div class="ft-col">
      <h4>Resources</h4>
      <ul>
        <li><a href="https://raccopilot.live" target="_blank" rel="noopener">RACcopilot ↗</a></li>
        <li><a href="https://chattysurvey.online" target="_blank" rel="noopener">ChattySurvey ↗</a></li>
        <li><a href="{root}privacy-policy.html">Privacy Policy</a></li>
        <li><a href="{root}terms-of-service.html">Terms of Service</a></li>
      </ul>
    </div>
  </div>

  <div class="ft-bottom">
    <p>© 2025 ThinkersPoint. All rights reserved. Crafted with ❤️ in India.</p>
    <div class="ft-bl">
      <a href="{root}privacy-policy.html">Privacy Policy</a>
      <a href="{root}terms-of-service.html">Terms of Service</a>
    </div>
  </div>
</footer>

<button id="st" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">
  <i class="fas fa-arrow-up"></i>
</button>
"""

def generate_page(title, description, h1, content, root="", url=""):
    """Generate a complete HTML page"""
    canonical = f'<link rel="canonical" href="https://thinkerspoint.com{url}" />' if url else ''

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  {canonical}

  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:type" content="website" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" />

  <link rel="stylesheet" href="{root}assets/style.css" />
  <style>
    {SHARED_CSS}
  </style>
</head>
<body>
  {nav_html(root)}

  <section class="page-hero">
    <div class="page-hero-inner fi">
      <h1>{h1}</h1>
      <p>{description}</p>
    </div>
  </section>

  {content}

  {footer_html(root)}

  <script>{SHARED_JS}</script>
</body>
</html>
"""

# ═══════════════════════════════════════════════════════════════════════════
# PAGE GENERATORS
# ═══════════════════════════════════════════════════════════════════════════

def create_service_page(service_name, service_slug, description, icon):
    """Create a service page"""
    content = f"""
<section style="padding:80px 28px; background:var(--bg);">
  <div class="container fi d1">
    <h2 style="font-family:var(--fh); font-size:clamp(28px,4vw,42px); font-weight:800; margin-bottom:32px;">
      What is {service_name}?
    </h2>
    <p style="font-size:16px; color:var(--text3); line-height:1.8; max-width:800px; margin-bottom:40px;">
      {description} We combine strategic thinking with data-driven execution to deliver measurable results for your business.
    </p>
  </div>
</section>

<section style="padding:80px 28px; background:var(--bg2);">
  <div class="container">
    <div class="sec-head fi d1">
      <div class="chip"><span class="dot"></span>Key Features</div>
      <h2>What We Deliver</h2>
      <p>Comprehensive solutions tailored to your business goals</p>
    </div>
    <div class="feat-grid">
      <div class="feat-card fi d2">
        <div class="feat-icon" style="background:rgba(99,102,241,.18); color:var(--indigo);">
          <i class="fas fa-chart-line"></i>
        </div>
        <h3>Data-Driven Results</h3>
        <p>Every strategy backed by analytics and real metrics. We measure what matters and optimize continuously.</p>
      </div>
      <div class="feat-card fi d3">
        <div class="feat-icon" style="background:rgba(139,92,246,.18); color:var(--violet);">
          <i class="fas fa-users-cog"></i>
        </div>
        <h3>Expert Team</h3>
        <p>Industry veterans with 10+ years of combined experience. We've worked with brands like Amazon, Google, and Meta.</p>
      </div>
      <div class="feat-card fi d4">
        <div class="feat-icon" style="background:rgba(236,72,153,.18); color:var(--pink);">
          <i class="fas fa-rocket"></i>
        </div>
        <h3>Fast Implementation</h3>
        <p>No lengthy setups. We launch campaigns and strategies within days, not months. Agile and flexible approach.</p>
      </div>
    </div>
  </div>
</section>

<section style="padding:80px 28px; background:var(--bg);">
  <div class="container">
    <div class="sec-head fi d1">
      <div class="chip"><span class="dot"></span>Our Process</div>
      <h2>How We Work</h2>
      <p>A proven framework that delivers results every time</p>
    </div>
    <div class="process">
      <div class="pstep fi d2" data-step="1">
        <h4>Strategy</h4>
        <p>We analyze your business, competitors, and market to create a winning strategy tailored to your goals.</p>
      </div>
      <div class="pstep fi d3" data-step="2">
        <h4>Planning</h4>
        <p>Detailed roadmap with timelines, milestones, and KPIs. Clear expectations from day one.</p>
      </div>
      <div class="pstep fi d4" data-step="3">
        <h4>Execution</h4>
        <p>Our expert team implements the strategy with precision and creativity. Daily monitoring and optimization.</p>
      </div>
      <div class="pstep fi d5" data-step="4">
        <h4>Growth</h4>
        <p>Continuous improvement based on data. Scale what works, pivot what doesn't. Long-term growth guaranteed.</p>
      </div>
    </div>
  </div>
</section>

<section style="padding:80px 28px; background:var(--bg2);">
  <div class="container">
    <div class="stats-row fi d1">
      <div class="stat-box">
        <div class="stat-num">300%</div>
        <div class="stat-label">Avg. ROI Increase</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">50+</div>
        <div class="stat-label">Happy Clients</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">8+</div>
        <div class="stat-label">Years Experience</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">24/7</div>
        <div class="stat-label">Support</div>
      </div>
    </div>
  </div>
</section>

<section style="padding:80px 28px; background:var(--bg);">
  <div class="container" style="max-width:700px;">
    <div class="sec-head fi d1">
      <div class="chip"><span class="dot"></span>FAQ</div>
      <h2>Common Questions</h2>
      <p>Everything you need to know about our services</p>
    </div>
    <div class="faq fi d2">
      <div class="faq-item active">
        <div class="faq-q">
          How long does it take to see results?
          <i class="fas fa-chevron-down"></i>
        </div>
        <div class="faq-a">
          <p>Most clients see initial results within 30-45 days. Significant growth typically happens within 3-6 months depending on your industry and starting point.</p>
        </div>
      </div>
      <div class="faq-item">
        <div class="faq-q">
          What's your pricing model?
          <i class="fas fa-chevron-down"></i>
        </div>
        <div class="faq-a">
          <p>We offer flexible pricing based on scope, duration, and business goals. We have packages starting from ₹50,000/month. Get a custom quote during your consultation.</p>
        </div>
      </div>
      <div class="faq-item">
        <div class="faq-q">
          Do you work with startups?
          <i class="fas fa-chevron-down"></i>
        </div>
        <div class="faq-a">
          <p>Absolutely! We work with startups, SMEs, and enterprises. We have special startup packages and have helped 30+ startups scale from 0 to 7-8 figures in revenue.</p>
        </div>
      </div>
      <div class="faq-item">
        <div class="faq-q">
          What if I'm not happy with the results?
          <i class="fas fa-chevron-down"></i>
        </div>
        <div class="faq-a">
          <p>We have a 30-day money-back guarantee. If you're not satisfied with our work, we refund 100%. Your satisfaction is our priority.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="cta-section">
  <div class="container fi d1">
    <h2>Ready to Transform Your {service_name}?</h2>
    <p>Let's chat about your goals and create a winning strategy together. Schedule a free consultation today.</p>
    <a href="contact.html" class="btn-prim">
      <i class="fas fa-calendar-alt"></i> Book Free Consultation
    </a>
    <a href="contact.html" class="btn-sec">
      <i class="fas fa-envelope"></i> Get a Proposal
    </a>
  </div>
</section>
"""

    return generate_page(
        title=f"{service_name} Services | ThinkersPoint",
        description=description,
        h1=service_name,
        content=content,
        root="../",
        url=f"/services/{service_slug}/"
    )

def create_location_page(location_name, location_slug):
    """Create a location page"""
    content = f"""
<section style="padding:80px 28px; background:var(--bg);">
  <div class="container fi d1">
    <h2 style="font-family:var(--fh); font-size:clamp(28px,4vw,42px); font-weight:800; margin-bottom:32px;">
      Digital Marketing Services in {location_name}
    </h2>
    <p style="font-size:16px; color:var(--text3); line-height:1.8; max-width:800px; margin-bottom:40px;">
      Transform your business with ThinkersPoint's world-class digital marketing and business growth solutions tailored for the {location_name} market.
    </p>
  </div>
</section>

<section style="padding:80px 28px; background:var(--bg2);">
  <div class="container">
    <div class="stats-row fi d1">
      <div class="stat-box">
        <div class="stat-num">200+</div>
        <div class="stat-label">Clients Served</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">₹50Cr+</div>
        <div class="stat-label">Revenue Generated</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">95%</div>
        <div class="stat-label">Client Retention</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">24/7</div>
        <div class="stat-label">Local Support</div>
      </div>
    </div>
  </div>
</section>

<section style="padding:80px 28px; background:var(--bg);">
  <div class="container">
    <div class="sec-head fi d1">
      <div class="chip"><span class="dot"></span>Why {location_name}</div>
      <h2>Market Opportunity</h2>
      <p>The {location_name} market is booming with digital transformation. Let's capitalize on this growth together.</p>
    </div>
    <div class="feat-grid">
      <div class="feat-card fi d2">
        <div class="feat-icon" style="background:rgba(99,102,241,.18); color:var(--indigo);">
          <i class="fas fa-globe"></i>
        </div>
        <h3>Local Expertise</h3>
        <p>We understand the {location_name} market dynamics, regulations, and consumer behavior. Deep local insights meet global best practices.</p>
      </div>
      <div class="feat-card fi d3">
        <div class="feat-icon" style="background:rgba(139,92,246,.18); color:var(--violet);">
          <i class="fas fa-handshake"></i>
        </div>
        <h3>Local Network</h3>
        <p>Strong connections with local influencers, media, and businesses. We open doors and build relationships that matter.</p>
      </div>
      <div class="feat-card fi d4">
        <div class="feat-icon" style="background:rgba(236,72,153,.18); color:var(--pink);">
          <i class="fas fa-support"></i>
        </div>
        <h3>Local Support</h3>
        <p>Dedicated team in {location_name} timezone. No communication delays, immediate support, and same-day turnarounds.</p>
      </div>
    </div>
  </div>
</section>

<section style="padding:80px 28px; background:var(--bg2);">
  <div class="container" style="max-width:700px;">
    <div class="sec-head fi d1">
      <div class="chip"><span class="dot"></span>Services in {location_name}</div>
      <h2>Our Offerings</h2>
      <p>Full spectrum of digital marketing and growth services</p>
    </div>
    <div class="faq fi d2">
      <div class="faq-item active">
        <div class="faq-q">
          Digital Marketing Strategy
          <i class="fas fa-chevron-down"></i>
        </div>
        <div class="faq-a">
          <p>Custom strategies built for {location_name} businesses. We analyze local competition, identify opportunities, and create roadmaps for sustainable growth.</p>
        </div>
      </div>
      <div class="faq-item">
        <div class="faq-q">
          Performance Marketing
          <i class="fas fa-chevron-down"></i>
        </div>
        <div class="faq-a">
          <p>Pay-only-for-results campaigns across Google, Facebook, Instagram, and LinkedIn. ROI-focused approach with daily optimization.</p>
        </div>
      </div>
      <div class="faq-item">
        <div class="faq-q">
          Web Development & Design
          <i class="fas fa-chevron-down"></i>
        </div>
        <div class="faq-a">
          <p>High-converting websites built with latest tech. Mobile-first, SEO-optimized, and designed to sell. Average 40% conversion increase.</p>
        </div>
      </div>
      <div class="faq-item">
        <div class="faq-q">
          Business Consultancy
          <i class="fas fa-chevron-down"></i>
        </div>
        <div class="faq-a">
          <p>Strategic guidance for scaling your {location_name} business. From market entry to scaling, we guide every step of your growth journey.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="cta-section">
  <div class="container fi d1">
    <h2>Ready to Dominate in {location_name}?</h2>
    <p>Let's create a winning strategy for your {location_name} business. Book a free consultation with our local team.</p>
    <a href="../contact.html" class="btn-prim">
      <i class="fas fa-calendar-alt"></i> Free Consultation
    </a>
  </div>
</section>
"""

    return generate_page(
        title=f"Digital Marketing in {location_name} | ThinkersPoint",
        description=f"Award-winning digital marketing and growth services in {location_name}. 200+ clients, 95% retention. Free consultation.",
        h1=f"Grow Your Business in {location_name}",
        content=content,
        root="../",
        url=f"/locations/{location_slug}/"
    )

def create_industry_page(industry_name, industry_slug):
    """Create an industry page"""
    content = f"""
<section style="padding:80px 28px; background:var(--bg);">
  <div class="container fi d1">
    <h2 style="font-family:var(--fh); font-size:clamp(28px,4vw,42px); font-weight:800; margin-bottom:32px;">
      Digital Growth for {industry_name}
    </h2>
    <p style="font-size:16px; color:var(--text3); line-height:1.8; max-width:800px; margin-bottom:40px;">
      Industry-specific strategies designed to overcome {industry_name} challenges and accelerate growth. We've helped 50+ {industry_name} businesses scale revenue by 200-400%.
    </p>
  </div>
</section>

<section style="padding:80px 28px; background:var(--bg2);">
  <div class="container">
    <div class="sec-head fi d1">
      <div class="chip"><span class="dot"></span>Industry Challenges</div>
      <h2>{industry_name} Landscape</h2>
      <p>Unique challenges require specialized solutions</p>
    </div>
    <div class="feat-grid">
      <div class="feat-card fi d2">
        <div class="feat-icon" style="background:rgba(99,102,241,.18); color:var(--indigo);">
          <i class="fas fa-chart-pie"></i>
        </div>
        <h3>Market Competition</h3>
        <p>The {industry_name} space is crowded. Standing out requires a unique value proposition and smart marketing tactics.</p>
      </div>
      <div class="feat-card fi d3">
        <div class="feat-icon" style="background:rgba(139,92,246,.18); color:var(--violet);">
          <i class="fas fa-lock"></i>
        </div>
        <h3>Compliance & Regulations</h3>
        <p>Navigating industry rules while maintaining agile marketing. We know the compliance landscape and work within it effectively.</p>
      </div>
      <div class="feat-card fi d4">
        <div class="feat-icon" style="background:rgba(236,72,153,.18); color:var(--pink);">
          <i class="fas fa-bullseye"></i>
        </div>
        <h3>Lead Generation</h3>
        <p>Long sales cycles and high customer acquisition costs. We've perfected lead gen and nurturing for {industry_name} businesses.</p>
      </div>
    </div>
  </div>
</section>

<section style="padding:80px 28px; background:var(--bg);">
  <div class="container">
    <div class="sec-head fi d1">
      <div class="chip"><span class="dot"></span>Our Solutions</div>
      <h2>How We Help {industry_name}</h2>
      <p>Proven strategies specific to your industry</p>
    </div>
    <div class="process">
      <div class="pstep fi d2" data-step="1">
        <h4>Industry Analysis</h4>
        <p>Deep dive into your specific segment. Competition analysis, SWOT, and market positioning study.</p>
      </div>
      <div class="pstep fi d3" data-step="2">
        <h4>Custom Strategy</h4>
        <p>Tailored growth strategy addressing {industry_name}-specific pain points and leveraging opportunities.</p>
      </div>
      <div class="pstep fi d4" data-step="3">
        <h4>Specialized Execution</h4>
        <p>Implementation by industry experts. Compliance-approved tactics with maximum impact.</p>
      </div>
      <div class="pstep fi d5" data-step="4">
        <h4>Measurable Results</h4>
        <p>Regular reporting with industry benchmarks. Transparent metrics that matter for {industry_name}.</p>
      </div>
    </div>
  </div>
</section>

<section style="padding:80px 28px; background:var(--bg2);">
  <div class="container">
    <div class="stats-row fi d1">
      <div class="stat-box">
        <div class="stat-num">50+</div>
        <div class="stat-label">{industry_name} Clients</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">₹100Cr+</div>
        <div class="stat-label">Revenue Generated</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">300%</div>
        <div class="stat-label">Avg ROI Increase</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">8+</div>
        <div class="stat-label">Years in {industry_name}</div>
      </div>
    </div>
  </div>
</section>

<section id="cta-section">
  <div class="container fi d1">
    <h2>Transform Your {industry_name} Business</h2>
    <p>Let's discuss how to grow your {industry_name} company faster. Schedule a free, no-obligation consultation.</p>
    <a href="../contact.html" class="btn-prim">
      <i class="fas fa-calendar-alt"></i> Free Consultation
    </a>
  </div>
</section>
"""

    return generate_page(
        title=f"Digital Marketing for {industry_name} | ThinkersPoint",
        description=f"Industry-specific digital marketing strategies for {industry_name}. 50+ {industry_name} clients. 300% avg ROI increase. Free consultation.",
        h1=f"Digital Growth for {industry_name}",
        content=content,
        root="../",
        url=f"/industries/{industry_slug}/"
    )

def create_about_page():
    """Create about page"""
    content = """
<section style="padding:80px 28px; background:var(--bg);">
  <div class="container fi d1">
    <h2 style="font-family:var(--fh); font-size:clamp(28px,4vw,42px); font-weight:800; margin-bottom:32px;">
      Our Story
    </h2>
    <p style="font-size:16px; color:var(--text3); line-height:1.8; max-width:800px; margin-bottom:40px;">
      ThinkersPoint was founded by Suraj Agarwal with a mission: help businesses dominate their markets through strategic digital marketing and innovation. Starting from a small team of 3, we've grown to 15+ experts and helped 200+ businesses scale to 7-8 figures in revenue.
    </p>
  </div>
</section>

<section style="padding:80px 28px; background:var(--bg2);">
  <div class="container">
    <div class="sec-head fi d1">
      <div class="chip"><span class="dot"></span>Why We're Different</div>
      <h2>Our Core Values</h2>
      <p>What sets us apart in the crowded digital marketing space</p>
    </div>
    <div class="feat-grid">
      <div class="feat-card fi d2">
        <div class="feat-icon" style="background:rgba(99,102,241,.18); color:var(--indigo);">
          <i class="fas fa-brain"></i>
        </div>
        <h3>Strategic Thinking</h3>
        <p>We don't just execute tactics. We think strategically about your business, market, and long-term growth. Every campaign is part of a bigger strategy.</p>
      </div>
      <div class="feat-card fi d3">
        <div class="feat-icon" style="background:rgba(139,92,246,.18); color:var(--violet);">
          <i class="fas fa-chart-line"></i>
        </div>
        <h3>Data-Driven Results</h3>
        <p>We believe in numbers, not opinions. Every decision is backed by data, analytics, and proven methodologies. Transparency is non-negotiable.</p>
      </div>
      <div class="feat-card fi d4">
        <div class="feat-icon" style="background:rgba(236,72,153,.18); color:var(--pink);">
          <i class="fas fa-handshake"></i>
        </div>
        <h3>Partnership Mindset</h3>
        <p>Your growth is our growth. We're not just service providers; we're your strategic partners. We celebrate your wins as our own.</p>
      </div>
    </div>
  </div>
</section>

<section style="padding:80px 28px; background:var(--bg);">
  <div class="container">
    <div class="sec-head fi d1">
      <div class="chip"><span class="dot"></span>Our Team</div>
      <h2>Talent From The <span class="grad-text">World's Best</span></h2>
      <p>Our team brings experience from Amazon, Apple, Google, Microsoft, Meta, and LinkedIn.</p>
    </div>
    <div style="background:var(--glass); border:1px solid var(--border); border-radius:var(--r-xl); padding:40px; text-align:center; margin-bottom:60px;">
      <p style="font-size:14px; color:var(--text4); margin-bottom:20px; text-transform:uppercase; letter-spacing:.5px; font-weight:600;">Our people have worked at</p>
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(120px, 1fr)); gap:20px; align-items:center; justify-items:center;">
        <div style="font-size:28px; font-weight:700; color:var(--text2);">Amazon</div>
        <div style="font-size:28px; font-weight:700; color:var(--text2);">Apple</div>
        <div style="font-size:28px; font-weight:700; color:var(--text2);">Google</div>
        <div style="font-size:28px; font-weight:700; color:var(--text2);">Microsoft</div>
        <div style="font-size:28px; font-weight:700; color:var(--text2);">Meta</div>
        <div style="font-size:28px; font-weight:700; color:var(--text2);">LinkedIn</div>
      </div>
    </div>

    <div class="stats-row fi d1">
      <div class="stat-box">
        <div class="stat-num">15+</div>
        <div class="stat-label">Expert Professionals</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">8+</div>
        <div class="stat-label">Industry Domains</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">50+</div>
        <div class="stat-label">Combined Years Experience</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">95%</div>
        <div class="stat-label">Client Retention Rate</div>
      </div>
    </div>
  </div>
</section>

<section style="padding:80px 28px; background:var(--bg2);">
  <div class="container">
    <div class="sec-head fi d1">
      <div class="chip"><span class="dot"></span>Our Impact</div>
      <h2>By The Numbers</h2>
      <p>Real results from real clients</p>
    </div>
    <div class="stats-row fi d1">
      <div class="stat-box">
        <div class="stat-num">200+</div>
        <div class="stat-label">Businesses Transformed</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">₹500Cr+</div>
        <div class="stat-label">Total Revenue Generated</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">300%</div>
        <div class="stat-label">Average ROI Increase</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">6+</div>
        <div class="stat-label">Years in Business</div>
      </div>
    </div>
  </div>
</section>

<section id="cta-section">
  <div class="container fi d1">
    <h2>Ready to Join Our Success Stories?</h2>
    <p>Let's discuss how we can transform your business. Schedule a free consultation with our team.</p>
    <a href="contact.html" class="btn-prim">
      <i class="fas fa-calendar-alt"></i> Book Consultation
    </a>
  </div>
</section>
"""

    return generate_page(
        title="About ThinkersPoint | Digital Marketing & Growth Agency",
        description="Learn about ThinkersPoint. Founded by Suraj Agarwal. 200+ clients, 15+ experts, ₹500Cr+ revenue generated. FAANG alumni team.",
        h1="About ThinkersPoint",
        content=content,
        url="/about/"
    )

def create_portfolio_page():
    """Create portfolio page"""
    content = """
<section style="padding:80px 28px; background:var(--bg);">
  <div class="container">
    <div class="sec-head fi d1">
      <div class="chip"><span class="dot"></span>Our Work</div>
      <h2>Portfolio</h2>
      <p>Real businesses. Real growth. Real results.</p>
    </div>

    <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:24px; margin-bottom:80px;">
      <a href="https://miseguro.ca" target="_blank" rel="noopener" class="feat-card fi d2" style="cursor:pointer;">
        <div class="feat-icon" style="background:rgba(99,102,241,.18); color:var(--indigo); font-size:28px;">🏢</div>
        <h3>Miseguro</h3>
        <p>Insurance platform in Canada. Scaled from 100 to 5,000 users in 6 months through performance marketing.</p>
      </a>
      <a href="https://bitz1119.github.io/GG_web/#" target="_blank" rel="noopener" class="feat-card fi d3" style="cursor:pointer;">
        <div class="feat-icon" style="background:rgba(139,92,246,.18); color:var(--violet); font-size:28px;">🏗️</div>
        <h3>Gratian Group</h3>
        <p>Construction & real estate company. Increased qualified leads by 250% through targeted digital campaigns.</p>
      </a>
      <a href="https://vmvindustries.com/" target="_blank" rel="noopener" class="feat-card fi d4" style="cursor:pointer;">
        <div class="feat-icon" style="background:rgba(236,72,153,.18); color:var(--pink); font-size:28px;">⚙️</div>
        <h3>VMV Industries</h3>
        <p>Manufacturing company. Dominated search results with SEO strategy. 400% organic traffic increase.</p>
      </a>
      <a href="https://challanexperts.com" target="_blank" rel="noopener" class="feat-card fi d5" style="cursor:pointer;">
        <div class="feat-icon" style="background:rgba(99,102,241,.18); color:var(--indigo); font-size:28px;">⚖️</div>
        <h3>Challan Experts</h3>
        <p>Legal services. Built market leadership through content marketing and brand positioning.</p>
      </a>
      <a href="https://thinkfox.in" target="_blank" rel="noopener" class="feat-card fi d1" style="cursor:pointer;">
        <div class="feat-icon" style="background:rgba(139,92,246,.18); color:var(--violet); font-size:28px;">🦊</div>
        <h3>ThinkFox</h3>
        <p>EdTech platform. Scaled from 0 to 10,000 active users through community-driven marketing.</p>
      </a>
      <div class="feat-card fi d2" style="background:var(--glass-h); border:2px dashed var(--border);">
        <div class="feat-icon" style="background:rgba(16,185,129,.18); color:var(--green); font-size:28px;">
          <i class="fas fa-plus"></i>
        </div>
        <h3>195+ More</h3>
        <p>We've successfully helped 200+ businesses across industries and countries. Your story could be next.</p>
      </div>
    </div>
  </div>
</section>

<section style="padding:80px 28px; background:var(--bg2);">
  <div class="container">
    <div class="stats-row fi d1">
      <div class="stat-box">
        <div class="stat-num">200+</div>
        <div class="stat-label">Successful Projects</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">₹500Cr+</div>
        <div class="stat-label">Revenue Generated</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">95%</div>
        <div class="stat-label">Client Retention</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">300%</div>
        <div class="stat-label">Average ROI Increase</div>
      </div>
    </div>
  </div>
</section>

<section id="cta-section">
  <div class="container fi d1">
    <h2>Ready to Add Your Business to Our Success Stories?</h2>
    <p>Let's create an amazing portfolio case study together. Schedule your free consultation today.</p>
    <a href="contact.html" class="btn-prim">
      <i class="fas fa-calendar-alt"></i> Get Started
    </a>
  </div>
</section>
"""

    return generate_page(
        title="Portfolio | ThinkersPoint's Client Success Stories",
        description="See our portfolio of 200+ successful businesses. Real growth, real results. ₹500Cr+ revenue generated.",
        h1="Our Portfolio",
        content=content,
        url="/portfolio/"
    )

def create_contact_page():
    """Create contact page"""
    content = """
<section style="padding:80px 28px; background:var(--bg);">
  <div class="container">
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:60px; align-items:start;">
      <div class="fi d1">
        <h2 style="font-family:var(--fh); font-size:clamp(28px,4vw,42px); font-weight:800; margin-bottom:24px;">
          Let's Talk
        </h2>
        <p style="font-size:16px; color:var(--text3); line-height:1.8; margin-bottom:40px;">
          Got a project in mind? Want to discuss growth strategies? Or just curious about our services? Reach out and let's start a conversation.
        </p>

        <div style="margin-bottom:32px;">
          <div style="font-weight:600; margin-bottom:6px;">Email</div>
          <p style="color:var(--text3);"><a href="mailto:hello@thinkerspoint.com" style="color:var(--indigo); transition:color var(--t);">hello@thinkerspoint.com</a></p>
        </div>

        <div style="margin-bottom:32px;">
          <div style="font-weight:600; margin-bottom:6px;">Phone</div>
          <p style="color:var(--text3);"><a href="tel:+919876543210" style="color:var(--indigo); transition:color var(--t);">+91 98765 43210</a></p>
        </div>

        <div style="margin-bottom:32px;">
          <div style="font-weight:600; margin-bottom:6px;">Locations</div>
          <p style="color:var(--text3); margin-bottom:6px;">India • USA • UK • UAE • Australia</p>
        </div>

        <div style="margin-bottom:32px;">
          <div style="font-weight:600; margin-bottom:12px;">Connect With Us</div>
          <div style="display:flex; gap:12px;">
            <a href="https://www.linkedin.com/in/surajaggarwal38/" target="_blank" rel="noopener" class="fs">
              <i class="fab fa-linkedin-in"></i>
            </a>
            <a href="#" class="fs"><i class="fab fa-twitter"></i></a>
            <a href="#" class="fs"><i class="fab fa-instagram"></i></a>
            <a href="#" class="fs"><i class="fab fa-facebook-f"></i></a>
          </div>
        </div>
      </div>

      <div class="fi d2" style="background:var(--glass); border:1px solid var(--border); border-radius:var(--r-xl); padding:40px;">
        <form onsubmit="submitForm(event)">
          <div style="margin-bottom:20px;">
            <label style="display:block; font-weight:600; margin-bottom:8px;">Full Name *</label>
            <input type="text" placeholder="Your name" required style="width:100%; padding:11px 14px; background:rgba(255,255,255,.05); border:1px solid var(--border); border-radius:var(--r-s); color:inherit; font-family:inherit; transition:all var(--t);" />
          </div>

          <div style="margin-bottom:20px;">
            <label style="display:block; font-weight:600; margin-bottom:8px;">Email *</label>
            <input type="email" placeholder="your@email.com" required style="width:100%; padding:11px 14px; background:rgba(255,255,255,.05); border:1px solid var(--border); border-radius:var(--r-s); color:inherit; font-family:inherit; transition:all var(--t);" />
          </div>

          <div style="margin-bottom:20px;">
            <label style="display:block; font-weight:600; margin-bottom:8px;">Company</label>
            <input type="text" placeholder="Your company" style="width:100%; padding:11px 14px; background:rgba(255,255,255,.05); border:1px solid var(--border); border-radius:var(--r-s); color:inherit; font-family:inherit; transition:all var(--t);" />
          </div>

          <div style="margin-bottom:20px;">
            <label style="display:block; font-weight:600; margin-bottom:8px;">Service Interested In</label>
            <select style="width:100%; padding:11px 14px; background:rgba(255,255,255,.05); border:1px solid var(--border); border-radius:var(--r-s); color:inherit; font-family:inherit;">
              <option value="" disabled selected>Select a service</option>
              <option>Digital Marketing</option>
              <option>Performance Marketing</option>
              <option>Web Development</option>
              <option>AI Solutions</option>
              <option>Business Consultancy</option>
              <option>Other</option>
            </select>
          </div>

          <div style="margin-bottom:20px;">
            <label style="display:block; font-weight:600; margin-bottom:8px;">Message *</label>
            <textarea placeholder="Tell us about your project..." required style="width:100%; padding:11px 14px; background:rgba(255,255,255,.05); border:1px solid var(--border); border-radius:var(--r-s); color:inherit; font-family:inherit; min-height:120px; resize:none;"></textarea>
          </div>

          <button type="submit" class="btn-prim" style="width:100%; justify-content:center;">
            <i class="fas fa-paper-plane"></i> Send Message
          </button>
        </form>
      </div>
    </div>
  </div>
</section>

<section id="cta-section">
  <div class="container fi d1">
    <h2>What's Next?</h2>
    <p>After we receive your message, our team will reach out within 24 hours. No spam, no pressure — just honest conversation about your growth goals.</p>
  </div>
</section>
"""

    return generate_page(
        title="Contact ThinkersPoint | Get Your Free Consultation",
        description="Get in touch with ThinkersPoint. Free consultation. Response within 24 hours. Based in India, USA, UK, UAE, Australia.",
        h1="Contact Us",
        content=content,
        url="/contact/"
    )

def create_legal_page(page_type):
    """Create legal pages"""
    if page_type == "privacy":
        title = "Privacy Policy"
        slug = "privacy-policy"
        content = """
<section style="padding:80px 28px; background:var(--bg);">
  <div class="container" style="max-width:800px;">
    <div class="fi d1">
      <h2 style="font-family:var(--fh); font-size:clamp(28px,4vw,42px); font-weight:800; margin-bottom:32px;">
        Privacy Policy
      </h2>
      <p style="font-size:13px; color:var(--text4); margin-bottom:40px;">Last updated: """ + datetime.now().strftime("%B %d, %Y") + """</p>

      <div style="line-height:2; color:var(--text3);">
        <h3 style="font-size:20px; font-weight:700; margin:32px 0 16px 0; color:var(--text);">1. Introduction</h3>
        <p style="margin-bottom:16px;">ThinkersPoint ("Company", "we", "our", or "us") operates the ThinkersPoint website. This page informs you of our policies regarding the collection, use, and disclosure of personal data when you use our Service and the choices you have associated with that data.</p>

        <h3 style="font-size:20px; font-weight:700; margin:32px 0 16px 0; color:var(--text);">2. Information Collection and Use</h3>
        <p style="margin-bottom:16px;">We collect several different types of information for various purposes to provide and improve our Service to you.</p>
        <ul style="margin:16px 0; padding-left:24px;">
          <li style="margin-bottom:8px;">Personal Data: Name, email address, phone number, company name</li>
          <li style="margin-bottom:8px;">Usage Data: IP address, browser type, pages visited, time spent</li>
          <li style="margin-bottom:8px;">Cookies: To enhance your experience on our website</li>
        </ul>

        <h3 style="font-size:20px; font-weight:700; margin:32px 0 16px 0; color:var(--text);">3. Data Security</h3>
        <p style="margin-bottom:16px;">We implement appropriate technical and organizational security measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction.</p>

        <h3 style="font-size:20px; font-weight:700; margin:32px 0 16px 0; color:var(--text);">4. Contact Us</h3>
        <p style="margin-bottom:16px;">If you have any questions about this Privacy Policy, please contact us at:<br />hello@thinkerspoint.com</p>
      </div>
    </div>
  </div>
</section>
"""
    else:
        title = "Terms of Service"
        slug = "terms-of-service"
        content = """
<section style="padding:80px 28px; background:var(--bg);">
  <div class="container" style="max-width:800px;">
    <div class="fi d1">
      <h2 style="font-family:var(--fh); font-size:clamp(28px,4vw,42px); font-weight:800; margin-bottom:32px;">
        Terms of Service
      </h2>
      <p style="font-size:13px; color:var(--text4); margin-bottom:40px;">Last updated: """ + datetime.now().strftime("%B %d, %Y") + """</p>

      <div style="line-height:2; color:var(--text3);">
        <h3 style="font-size:20px; font-weight:700; margin:32px 0 16px 0; color:var(--text);">1. Agreement to Terms</h3>
        <p style="margin-bottom:16px;">By accessing and using ThinkersPoint's website and services, you accept and agree to be bound by the terms and provision of this agreement.</p>

        <h3 style="font-size:20px; font-weight:700; margin:32px 0 16px 0; color:var(--text);">2. Use License</h3>
        <p style="margin-bottom:16px;">Permission is granted to temporarily download one copy of the materials (information or software) on ThinkersPoint's website for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title, and under this license you may not:</p>
        <ul style="margin:16px 0; padding-left:24px;">
          <li style="margin-bottom:8px;">Modifying or copying the materials</li>
          <li style="margin-bottom:8px;">Using the materials for any commercial purpose or for any public display</li>
          <li style="margin-bottom:8px;">Attempting to reverse engineer, disassemble, or decompile any software</li>
        </ul>

        <h3 style="font-size:20px; font-weight:700; margin:32px 0 16px 0; color:var(--text);">3. Disclaimer</h3>
        <p style="margin-bottom:16px;">The materials on ThinkersPoint's website are provided on an 'as is' basis. ThinkersPoint makes no warranties, expressed or implied, and hereby disclaims and negates all other warranties including, without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.</p>

        <h3 style="font-size:20px; font-weight:700; margin:32px 0 16px 0; color:var(--text);">4. Limitations</h3>
        <p style="margin-bottom:16px;">In no event shall ThinkersPoint or its suppliers be liable for any damages (including, without limitation, damages for loss of data or profit, or due to business interruption) arising out of the use or inability to use the materials on ThinkersPoint's website.</p>

        <h3 style="font-size:20px; font-weight:700; margin:32px 0 16px 0; color:var(--text);">5. Contact</h3>
        <p style="margin-bottom:16px;">If you have any questions about these Terms of Service, please contact us at:<br />hello@thinkerspoint.com</p>
      </div>
    </div>
  </div>
</section>
"""

    return generate_page(
        title=f"{title} | ThinkersPoint",
        description=f"ThinkersPoint {title}",
        h1=title,
        content=content,
        url=f"/{slug}/"
    )

# ═══════════════════════════════════════════════════════════════════════════
# MAIN GENERATOR
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Generate all pages"""

    # Create directories
    dirs = [
        OUTPUT_DIR / "services",
        OUTPUT_DIR / "locations",
        OUTPUT_DIR / "industries",
        OUTPUT_DIR / "blog",
        OUTPUT_DIR / "assets"
    ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # Save shared CSS
    print("✓ Saving shared CSS...")
    (OUTPUT_DIR / "assets" / "style.css").write_text(SHARED_CSS)

    # Save shared JS
    print("✓ Saving shared JS...")
    (OUTPUT_DIR / "assets" / "script.js").write_text(SHARED_JS)

    # Service pages
    services = [
        ("Digital Marketing", "digital-marketing", "Strategic digital marketing that drives ROI and sustainable growth."),
        ("Performance Marketing", "performance-marketing", "Results-driven marketing where you only pay for actual conversions."),
        ("Social Media Marketing", "social-media-marketing", "Build brand authority and engage your audience across social platforms."),
        ("SEO Services", "seo-services", "Dominate search results and get consistent organic traffic."),
        ("Content Marketing", "content-marketing", "Strategic content that attracts, engages, and converts your ideal customers."),
        ("Email Marketing", "email-marketing", "High-converting email campaigns that nurture leads and boost sales."),
        ("PPC & Paid Advertising", "ppc-advertising", "Targeted paid campaigns across Google, Facebook, and LinkedIn."),
        ("Industrial Marketing", "industrial-marketing", "B2B marketing strategies for manufacturing and industrial companies."),
        ("B2B Marketing", "b2b-marketing", "Complex sales cycles require specialized B2B marketing expertise."),
        ("Business Consultancy", "business-consultancy", "Strategic business consulting for scaling and sustainable growth."),
        ("Brand Strategy", "brand-strategy", "Build a memorable brand that stands out and wins customer loyalty."),
        ("Web Development", "web-development", "High-converting websites built with latest technology and best practices."),
        ("App Development", "app-development", "Mobile and web apps that engage users and drive business growth."),
        ("UI/UX Design", "ui-ux-design", "Beautiful, intuitive interfaces that users love and that convert."),
        ("AI Solutions", "ai-solutions", "Leverage AI to automate, optimize, and transform your business operations."),
    ]

    print(f"\n✓ Generating {len(services)} service pages...")
    for svc_name, svc_slug, svc_desc in services:
        html = create_service_page(svc_name, svc_slug, svc_desc, "")
        (OUTPUT_DIR / "services" / f"{svc_slug}.html").write_text(html)
        print(f"  ✓ {svc_name}")

    # Location pages
    locations = [
        ("India", "india"),
        ("USA", "usa"),
        ("UK & London", "uk"),
        ("UAE & Dubai", "uae-dubai"),
        ("Australia", "australia"),
        ("Canada", "canada"),
        ("Singapore", "singapore"),
    ]

    print(f"\n✓ Generating {len(locations)} location pages...")
    for loc_name, loc_slug in locations:
        html = create_location_page(loc_name, loc_slug)
        (OUTPUT_DIR / "locations" / f"{loc_slug}.html").write_text(html)
        print(f"  ✓ {loc_name}")

    # Industry pages
    industries = [
        ("Real Estate", "real-estate"),
        ("Insurance", "insurance"),
        ("Healthcare", "healthcare"),
        ("E-commerce", "ecommerce"),
        ("Manufacturing", "manufacturing"),
        ("SaaS & Tech", "saas-tech"),
    ]

    print(f"\n✓ Generating {len(industries)} industry pages...")
    for ind_name, ind_slug in industries:
        html = create_industry_page(ind_name, ind_slug)
        (OUTPUT_DIR / "industries" / f"{ind_slug}.html").write_text(html)
        print(f"  ✓ {ind_name}")

    # About page
    print("\n✓ Generating about page...")
    (OUTPUT_DIR / "about.html").write_text(create_about_page())

    # Portfolio page
    print("✓ Generating portfolio page...")
    (OUTPUT_DIR / "portfolio.html").write_text(create_portfolio_page())

    # Contact page
    print("✓ Generating contact page...")
    (OUTPUT_DIR / "contact.html").write_text(create_contact_page())

    # Legal pages
    print("✓ Generating legal pages...")
    (OUTPUT_DIR / "privacy-policy.html").write_text(create_legal_page("privacy"))
    (OUTPUT_DIR / "terms-of-service.html").write_text(create_legal_page("terms"))

    # Create blog pages
    print("✓ Generating blog pages...")
    blog_index = generate_page(
        title="Blog | ThinkersPoint",
        description="Digital marketing insights, AI trends, and growth strategies for your business.",
        h1="The ThinkersPoint Blog",
        content="""
<section style="padding:80px 28px; background:var(--bg);">
  <div class="container">
    <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:24px;">
      <a href="digital-marketing-trends-2025.html" class="feat-card fi d2" style="cursor:pointer;">
        <div style="font-size:12px; color:var(--text4); margin-bottom:8px; text-transform:uppercase; letter-spacing:.5px; font-weight:600;">Mar 15, 2025</div>
        <h3>Digital Marketing Trends 2025</h3>
        <p>The biggest digital marketing trends that will dominate 2025. From AI to short-form content, here's what's coming.</p>
        <div style="margin-top:16px; color:var(--indigo); font-weight:600; font-size:13px;">Read →</div>
      </a>
      <a href="ai-in-marketing.html" class="feat-card fi d3" style="cursor:pointer;">
        <div style="font-size:12px; color:var(--text4); margin-bottom:8px; text-transform:uppercase; letter-spacing:.5px; font-weight:600;">Mar 10, 2025</div>
        <h3>AI in Marketing</h3>
        <p>How artificial intelligence is revolutionizing marketing. Automation, personalization, and predictive analytics explained.</p>
        <div style="margin-top:16px; color:var(--indigo); font-weight:600; font-size:13px;">Read →</div>
      </a>
      <a href="roi-measurement.html" class="feat-card fi d4" style="cursor:pointer;">
        <div style="font-size:12px; color:var(--text4); margin-bottom:8px; text-transform:uppercase; letter-spacing:.5px; font-weight:600;">Mar 05, 2025</div>
        <h3>Measuring Marketing ROI</h3>
        <p>How to measure, track, and optimize your marketing ROI. The metrics that actually matter and how to improve them.</p>
        <div style="margin-top:16px; color:var(--indigo); font-weight:600; font-size:13px;">Read →</div>
      </a>
    </div>
  </div>
</section>

<section id="cta-section">
  <div class="container fi d1">
    <h2>Subscribe to Our Newsletter</h2>
    <p>Get digital marketing insights, growth strategies, and AI trends delivered to your inbox every week.</p>
    <input type="email" placeholder="your@email.com" style="width:100%; max-width:400px; padding:11px 14px; background:rgba(255,255,255,.05); border:1px solid var(--border); border-radius:var(--r-s); color:inherit; font-family:inherit; margin-bottom:16px; display:block;" />
    <button class="btn-prim">
      <i class="fas fa-paper-plane"></i> Subscribe
    </button>
  </div>
</section>
""",
        url="/blog/"
    )
    (OUTPUT_DIR / "blog" / "index.html").write_text(blog_index)

    # Blog posts
    blog_posts = [
        ("Digital Marketing Trends 2025", "digital-marketing-trends-2025", "Mar 15, 2025", """
<section style="padding:80px 28px; background:var(--bg);">
  <div class="container" style="max-width:700px;">
    <div style="margin-bottom:80px;">
      <div style="font-size:13px; color:var(--text4); margin-bottom:16px; text-transform:uppercase; letter-spacing:.5px; font-weight:600;">Mar 15, 2025 • 8 min read</div>
      <div style="line-height:1.9; color:var(--text3);">
        <p style="margin-bottom:20px;">The digital marketing landscape in 2025 is more dynamic than ever. AI, automation, and personalization are no longer buzzwords — they're essentials. Let's explore the trends that will define this year.</p>

        <h3 style="font-size:20px; font-weight:700; margin:32px 0 16px 0; color:var(--text);">1. AI-Powered Content Creation</h3>
        <p style="margin-bottom:20px;">AI is now generating copy, headlines, and even full blog posts. But here's the secret: AI works best as a tool, not a replacement. The winning strategy is human creativity + AI efficiency.</p>

        <h3 style="font-size:20px; font-weight:700; margin:32px 0 16px 0; color:var(--text);">2. Short-Form Video Dominance</h3>
        <p style="margin-bottom:20px;">TikTok, YouTube Shorts, and Instagram Reels continue to dominate. Attention spans are shrinking, so your messages need to be snappy, visual, and instantly engaging.</p>

        <h3 style="font-size:20px; font-weight:700; margin:32px 0 16px 0; color:var(--text);">3. Hyper-Personalization</h3>
        <p style="margin-bottom:20px;">Generic email blasts are dead. Customers expect personalized experiences at every touchpoint. Segment your audience deeply and tailor messages to their exact needs and behaviors.</p>

        <h3 style="font-size:20px; font-weight:700; margin:32px 0 16px 0; color:var(--text);">4. Privacy-First Marketing</h3>
        <p style="margin-bottom:20px;">With iOS privacy changes and cookie deprecation, zero-party data (data customers willingly share) is gold. Build strategies around direct relationships and authentic engagement.</p>

        <h3 style="font-size:20px; font-weight:700; margin:32px 0 16px 0; color:var(--text);">Conclusion</h3>
        <p style="margin-bottom:20px;">The winners in 2025 will be those who combine technology with human creativity, embrace personalization, and build authentic customer relationships. The future of marketing isn't about bigger budgets — it's about smarter strategies.</p>
      </div>
    </div>

    <div class="fi d1" style="background:var(--glass); border:1px solid var(--border); border-radius:var(--r-xl); padding:32px; margin-bottom:40px;">
      <h3 style="margin-bottom:16px;">Ready to implement these trends?</h3>
      <p style="color:var(--text3); margin-bottom:20px;">Let's discuss how these strategies apply to your business.</p>
      <a href="../contact.html" class="btn-prim">
        <i class="fas fa-calendar-alt"></i> Book Consultation
      </a>
    </div>
  </div>
</section>
"""),
        ("AI in Marketing", "ai-in-marketing", "Mar 10, 2025", """
<section style="padding:80px 28px; background:var(--bg);">
  <div class="container" style="max-width:700px;">
    <div style="margin-bottom:80px;">
      <div style="font-size:13px; color:var(--text4); margin-bottom:16px; text-transform:uppercase; letter-spacing:.5px; font-weight:600;">Mar 10, 2025 • 6 min read</div>
      <div style="line-height:1.9; color:var(--text3);">
        <p style="margin-bottom:20px;">Artificial Intelligence isn't the future of marketing — it's the present. Companies using AI in their marketing are seeing 40% higher conversion rates and 30% better ROI. Here's how.</p>

        <h3 style="font-size:20px; font-weight:700; margin:32px 0 16px 0; color:var(--text);">Predictive Analytics</h3>
        <p style="margin-bottom:20px;">AI predicts customer behavior before it happens. Which customers are likely to churn? Who's ready to buy? AI finds these insights instantly, letting you act proactively.</p>

        <h3 style="font-size:20px; font-weight:700; margin:32px 0 16px 0; color:var(--text);">Chatbots & Conversational AI</h3>
        <p style="margin-bottom:20px;">24/7 customer support at scale. AI chatbots handle routine queries, qualify leads, and even close sales. Your team focuses on complex deals.</p>

        <h3 style="font-size:20px; font-weight:700; margin:32px 0 16px 0; color:var(--text);">Dynamic Content Personalization</h3>
        <p style="margin-bottom:20px;">Every visitor sees different content based on their behavior, preferences, and stage in the customer journey. This increases engagement by 50%+ on average.</p>

        <h3 style="font-size:20px; font-weight:700; margin:32px 0 16px 0; color:var(--text);">Email Optimization</h3>
        <p style="margin-bottom:20px;">AI determines the best send times, subject lines, and content for each subscriber. Your open rates and click rates increase automatically.</p>

        <h3 style="font-size:20px; font-weight:700; margin:32px 0 16px 0; color:var(--text);">The Bottom Line</h3>
        <p style="margin-bottom:20px;">AI amplifies human creativity. Use it for automation, insights, and optimization. But keep humans in charge of strategy, storytelling, and relationships. That's where real competitive advantage lies.</p>
      </div>
    </div>

    <div class="fi d1" style="background:var(--glass); border:1px solid var(--border); border-radius:var(--r-xl); padding:32px; margin-bottom:40px;">
      <h3 style="margin-bottom:16px;">Let's talk about AI for your business</h3>
      <p style="color:var(--text3); margin-bottom:20px;">We implement AI solutions that actually work. No buzzwords, just results.</p>
      <a href="../contact.html" class="btn-prim">
        <i class="fas fa-calendar-alt"></i> Get AI Strategy
      </a>
    </div>
  </div>
</section>
"""),
        ("Measuring Marketing ROI", "roi-measurement", "Mar 05, 2025", """
<section style="padding:80px 28px; background:var(--bg);">
  <div class="container" style="max-width:700px;">
    <div style="margin-bottom:80px;">
      <div style="font-size:13px; color:var(--text4); margin-bottom:16px; text-transform:uppercase; letter-spacing:.5px; font-weight:600;">Mar 05, 2025 • 10 min read</div>
      <div style="line-height:1.9; color:var(--text3);">
        <p style="margin-bottom:20px;">You're spending on marketing. But are you measuring ROI? Most companies don't. They guess. Let's change that. Here's a framework for measuring, tracking, and optimizing your marketing ROI.</p>

        <h3 style="font-size:20px; font-weight:700; margin:32px 0 16px 0; color:var(--text);">Define Your Metrics</h3>
        <p style="margin-bottom:20px;">First, decide what success looks like. Is it sales revenue? Lead volume? Customer acquisition cost? Email signups? Different metrics for different goals. Define yours first.</p>

        <h3 style="font-size:20px; font-weight:700; margin:32px 0 16px 0; color:var(--text);">Track Attribution</h3>
        <p style="margin-bottom:20px;">Which touchpoint converted the customer? Was it your email, your ad, your blog post, or organic search? Multi-touch attribution gives you the full picture of the customer journey.</p>

        <h3 style="font-size:20px; font-weight:700; margin:32px 0 16px 0; color:var(--text);">Calculate CAC & LTV</h3>
        <p style="margin-bottom:20px;">Customer Acquisition Cost (CAC): How much it costs to acquire one customer. Customer Lifetime Value (LTV): How much that customer is worth over their lifetime. If LTV > CAC, you're profitable.</p>

        <h3 style="font-size:20px; font-weight:700; margin:32px 0 16px 0; color:var(--text);">Set Benchmarks</h3>
        <p style="margin-bottom:20px;">Know your industry benchmarks. If the average CAC in your industry is ₹5,000 but yours is ₹10,000, you know you need to optimize. Benchmarks give you targets to aim for.</p>

        <h3 style="font-size:20px; font-weight:700; margin:32px 0 16px 0; color:var(--text);">Optimize Continuously</h3>
        <p style="margin-bottom:20px;">ROI measurement isn't a one-time thing. Review metrics weekly. Identify bottlenecks. Test improvements. Small 10% optimizations compound into 100%+ ROI increases over time.</p>

        <h3 style="font-size:20px; font-weight:700; margin:32px 0 16px 0; color:var(--text);">The Real Insight</h3>
        <p style="margin-bottom:20px;">Most companies measure the wrong things. Stop counting pageviews and impressions. Start measuring revenue, profit, and customer value. That's real ROI.</p>
      </div>
    </div>

    <div class="fi d1" style="background:var(--glass); border:1px solid var(--border); border-radius:var(--r-xl); padding:32px; margin-bottom:40px;">
      <h3 style="margin-bottom:16px;">Let's measure and optimize your marketing ROI</h3>
      <p style="color:var(--text3); margin-bottom:20px;">We'll audit your current performance and create an optimization roadmap.</p>
      <a href="../contact.html" class="btn-prim">
        <i class="fas fa-calculator"></i> ROI Audit
      </a>
    </div>
  </div>
</section>
"""),
    ]

    for title, slug, date, content in blog_posts:
        html = generate_page(
            title=f"{title} | ThinkersPoint Blog",
            description=f"Read about {title.lower()} on ThinkersPoint's digital marketing blog.",
            h1=title,
            content=content,
            root="../../",
            url=f"/blog/{slug}/"
        )
        (OUTPUT_DIR / "blog" / f"{slug}.html").write_text(html)
        print(f"  ✓ {title}")

    # Create sitemap
    print("\n✓ Generating sitemap.xml...")
    sitemap_urls = [
        ("index.html", "1.0"),
        ("about.html", "0.9"),
        ("portfolio.html", "0.9"),
        ("contact.html", "0.8"),
        ("privacy-policy.html", "0.5"),
        ("terms-of-service.html", "0.5"),
    ]

    for svc_name, svc_slug, _ in services:
        sitemap_urls.append((f"services/{svc_slug}.html", "0.9"))

    for loc_name, loc_slug in locations:
        sitemap_urls.append((f"locations/{loc_slug}.html", "0.9"))

    for ind_name, ind_slug in industries:
        sitemap_urls.append((f"industries/{ind_slug}.html", "0.9"))

    sitemap_urls.append(("blog/", "0.9"))
    for title, slug, date, _ in blog_posts:
        sitemap_urls.append((f"blog/{slug}.html", "0.8"))

    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url, priority in sitemap_urls:
        sitemap_xml += f'  <url>\n    <loc>https://thinkerspoint.com/{url}</loc>\n    <priority>{priority}</priority>\n  </url>\n'
    sitemap_xml += '</urlset>'
    (OUTPUT_DIR / "sitemap.xml").write_text(sitemap_xml)

    # Create robots.txt
    print("✓ Generating robots.txt...")
    robots_txt = """User-agent: *
Allow: /
Disallow: /admin/
Disallow: /private/

Sitemap: https://thinkerspoint.com/sitemap.xml
"""
    (OUTPUT_DIR / "robots.txt").write_text(robots_txt)

    total_pages = 1 + len(services) + len(locations) + len(industries) + 5 + len(blog_posts)
    print(f"\n{'='*60}")
    print(f"✅ SUCCESS! Generated {total_pages} pages")
    print(f"{'='*60}")
    print(f"\nPages created:")
    print(f"  • {len(services)} Service pages")
    print(f"  • {len(locations)} Location pages")
    print(f"  • {len(industries)} Industry pages")
    print(f"  • {len(blog_posts)} Blog posts")
    print(f"  • 5 Core pages (About, Portfolio, Contact, Privacy, Terms)")
    print(f"  • 1 Blog index")
    print(f"\nNext steps:")
    print(f"  1. Start the preview server: preview_start(name='gratian-group')")
    print(f"  2. Visit: http://localhost:4200/thinkerspoint/index.html")
    print(f"  3. Test navigation across all pages")

if __name__ == "__main__":
    main()
