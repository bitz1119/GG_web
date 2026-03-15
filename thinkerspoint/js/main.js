(function () {
  var nav = document.getElementById('nav');
  var st = document.getElementById('st');
  if (nav) {
    window.addEventListener('scroll', function () {
      nav.classList.toggle('scrolled', window.scrollY > 40);
      if (st) st.classList.toggle('on', window.scrollY > 500);
    });
  }

  var burger = document.getElementById('burger');
  var mobNav = document.getElementById('mob-nav');
  var mobClose = document.getElementById('mob-close');
  if (burger && mobNav) burger.addEventListener('click', function () { mobNav.classList.add('open'); });
  if (mobClose && mobNav) mobClose.addEventListener('click', function () { mobNav.classList.remove('open'); });
  window.closeNav = function () { if (mobNav) mobNav.classList.remove('open'); };

  var obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) e.target.classList.add('in'); });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.fi').forEach(function (el) { obs.observe(el); });

  document.querySelectorAll('.flt').forEach(function (btn) {
    btn.addEventListener('click', function () {
      document.querySelectorAll('.flt').forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
      var f = btn.dataset.f;
      document.querySelectorAll('.pf-card').forEach(function (card) {
        var show = !f || f === 'all' || (card.dataset.cat || '').includes(f);
        card.style.display = show ? '' : 'none';
      });
    });
  });

  window.submitForm = function (e) {
    e.preventDefault();
    var btn = document.getElementById('fsub');
    if (!btn) return;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
    btn.disabled = true;
    setTimeout(function () {
      btn.innerHTML = '<i class="fas fa-check"></i> Message Sent!';
      btn.style.background = 'linear-gradient(135deg,#10B981,#059669)';
      setTimeout(function () {
        btn.innerHTML = '<i class="fas fa-paper-plane"></i> Send Message';
        btn.style.background = '';
        btn.disabled = false;
        if (e.target && e.target.reset) e.target.reset();
      }, 3200);
    }, 1600);
  };
})();
