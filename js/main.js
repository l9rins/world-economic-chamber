document.addEventListener('DOMContentLoaded', () => {

  // ─── Nav Scroll Effect ───────────────────────────
  const nav = document.querySelector('.nav');
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.classList.toggle('scrolled', window.scrollY > 50);
    });
  }

  // ─── Reading Progress Bar ─────────────────────────
  const progressBar = document.getElementById('readingProgress');
  if (progressBar && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    window.addEventListener('scroll', () => {
      const docContent = document.querySelector('.doc-content');
      if (docContent) {
        const rect = docContent.getBoundingClientRect();
        const total = docContent.scrollHeight;
        const visible = window.innerHeight;
        const scrolled = Math.abs(rect.top);
        const percent = Math.min(scrolled / (total - visible), 1) * 100;
        progressBar.style.width = percent + '%';
      }
    });
  }

  // ─── Mobile Nav ──────────────────────────────────
  const navToggle = document.getElementById('navToggle');
  const navMenu = document.getElementById('navMenu');

  if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
      navToggle.classList.toggle('active');
      navMenu.classList.toggle('open');
      document.body.style.overflow = navMenu.classList.contains('open') ? 'hidden' : '';
    });

    navMenu.querySelectorAll('.nav-item').forEach(item => {
      const link = item.querySelector('.nav-link');
      const dropdown = item.querySelector('.nav-dropdown');
      if (link && dropdown) {
        link.addEventListener('click', (e) => {
          if (window.innerWidth <= 1024) {
            e.preventDefault();
            item.classList.toggle('open');
          }
        });
      }
    });
  }

  // ─── Fade-in Observer (single quiet moment) ──────
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });

    document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
  } else {
    document.querySelectorAll('.fade-in').forEach(el => el.classList.add('visible'));
  }

  // ─── Scroll to Top ───────────────────────────────
  const scrollTopBtn = document.querySelector('.scroll-top');
  if (scrollTopBtn) {
    window.addEventListener('scroll', () => {
      scrollTopBtn.classList.toggle('visible', window.scrollY > 500);
    });
    scrollTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ─── Cookie Consent ──────────────────────────────
  const cookieConsent = document.getElementById('cookieConsent');
  if (cookieConsent) {
    if (!localStorage.getItem('wec-cookie-consent')) {
      setTimeout(() => cookieConsent.classList.add('visible'), 2000);
    } else {
      cookieConsent.classList.add('hidden');
    }

    const acceptBtn = cookieConsent.querySelector('[data-cookie-accept]');
    if (acceptBtn) {
      acceptBtn.addEventListener('click', () => {
        localStorage.setItem('wec-cookie-consent', 'true');
        cookieConsent.classList.remove('visible');
        setTimeout(() => cookieConsent.classList.add('hidden'), 500);
      });
    }
  }

  // ─── Active Nav Link ─────────────────────────────
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(link => {
    if (link.getAttribute('href') === currentPage) {
      link.classList.add('active');
    }
  });

  // ─── Sidebar Scroll Tracking ──────────────────────
  const sidebarLinks = document.querySelectorAll('.doc-sidebar li a');
  if (sidebarLinks.length) {
    const sidebarInner = document.querySelector('.doc-sidebar-inner');
    const headings = [];
    let activeHeading = null;

    sidebarLinks.forEach(link => {
      const href = link.getAttribute('href');
      if (href && href.startsWith('#')) {
        const el = document.getElementById(href.slice(1));
        if (el) headings.push({ el, link });
      }
    });

    function centerActiveInSidebar() {
      const active = sidebarInner.querySelector('a.active');
      if (active) {
        active.scrollIntoView({ block: 'center', behavior: 'smooth' });
      }
    }

    const sidebarObserver = new IntersectionObserver((entries) => {
      let visible = [];
      entries.forEach(entry => {
        if (entry.isIntersecting) visible.push(entry.target);
      });
      if (visible.length) {
        const top = visible.reduce((a, b) => a.getBoundingClientRect().top < b.getBoundingClientRect().top ? a : b);
        if (top !== activeHeading) {
          activeHeading = top;
          sidebarLinks.forEach(l => l.classList.remove('active'));
          const match = headings.find(h => h.el === top);
          if (match) {
            match.link.classList.add('active');
            centerActiveInSidebar();
          }
        }
      }
    }, { threshold: 0.2, rootMargin: '-80px 0px -60% 0px' });

    headings.forEach(h => sidebarObserver.observe(h.el));

    sidebarLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        const href = link.getAttribute('href');
        if (href && href.startsWith('#')) {
          e.preventDefault();
          const target = document.getElementById(href.slice(1));
          if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        }
      });
    });
  }

  // ─── Constellation Map Draw-in ───────────────────
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const constellations = document.querySelectorAll('.constellation-draw-in');
  if (constellations.length && !reduceMotion) {
    const constObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          drawConstellation(entry.target);
          constObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });

    constellations.forEach(el => constObserver.observe(el));
  } else {
    constellations.forEach(el => el.querySelectorAll('.const-line').forEach(l => l.style.opacity = '1'));
  }

  function drawConstellation(container) {
    const lines = container.querySelectorAll('.const-line');
    const dots = container.querySelectorAll('.const-dot');
    const hubDot = container.querySelector('.const-dot-hub');

    lines.forEach((line, i) => {
      const length = line.getTotalLength();
      line.style.strokeDasharray = length;
      line.style.strokeDashoffset = length;
      line.style.opacity = '1';
      line.animate([
        { strokeDashoffset: length },
        { strokeDashoffset: 0 }
      ], {
        duration: 1200 + i * 100,
        delay: i * 80,
        easing: 'ease-out',
        fill: 'forwards'
      });
    });

    dots.forEach((dot, i) => {
      const isHub = dot.classList.contains('const-dot-hub');
      dot.style.opacity = '0';
      setTimeout(() => {
        dot.animate([
          { opacity: 0 },
          { opacity: 1 }
        ], {
          duration: isHub ? 600 : 400,
          easing: 'ease-out',
          fill: 'forwards'
        });
        if (isHub) {
          setTimeout(() => dot.classList.add('animated'), 600);
        }
      }, 600 + i * 60);
    });

    // Count-up stats
    const stats = container.closest('.constellation-section');
    if (stats) {
      const statEls = stats.querySelectorAll('.constellation-stat-number');
      statEls.forEach(el => {
        const target = parseInt(el.getAttribute('data-target'));
        const suffix = el.getAttribute('data-suffix') || '';
        if (!target) return;
        const duration = 1800;
        const step = target / (duration / 16);
        let current = 0;
        const counter = setInterval(() => {
          current += step;
          if (current >= target) {
            current = target;
            clearInterval(counter);
          }
          el.textContent = Math.floor(current).toLocaleString() + suffix;
        }, 16);
      });
    }
  }

});
