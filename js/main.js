document.addEventListener('DOMContentLoaded', () => {

  // â”€â”€â”€ Nav Scroll Effect â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  const nav = document.querySelector('.nav');
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.classList.toggle('scrolled', window.scrollY > 50);
    });
  }

  // â”€â”€â”€ Hero Parallax â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  const heroBg = document.querySelector('.hero-bg');
  if (heroBg) {
    window.addEventListener('scroll', () => {
      const offset = window.scrollY * 0.25;
      heroBg.style.transform = `translateY(${Math.min(offset, 40)}px)`;
    }, { passive: true });
  }

  // â”€â”€â”€ Reading Progress Bar â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
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

  // â”€â”€â”€ Mobile Nav â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  const navToggle = document.getElementById('navToggle');
  const navMenu = document.getElementById('navMenu');
  const navBackdrop = document.getElementById('navBackdrop');

  function toggleNav(open) {
    navToggle.classList.toggle('active', open);
    navMenu.classList.toggle('open', open);
    if (navBackdrop) navBackdrop.classList.toggle('open', open);
    if (nav) nav.classList.toggle('sidebar-open', open);
    document.body.style.overflow = open ? 'hidden' : '';

    // Kill pointer events on nav-link so the browser literally cannot navigate
    document.querySelectorAll('.nav-item').forEach(item => {
      const link = item.querySelector('.nav-link');
      const dropdown = item.querySelector('.nav-dropdown');
      if (link && dropdown) {
        if (open) {
          link.style.pointerEvents = 'none';
        } else {
          link.style.pointerEvents = '';
        }
      }
    });
  }

  if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
      const isOpen = !navMenu.classList.contains('open');
      toggleNav(isOpen);
    });

    if (navBackdrop) {
      navBackdrop.addEventListener('click', () => toggleNav(false));
    }

    // Handle dropdown toggle on the nav-item container (pointer-events still alive)
    navMenu.addEventListener('pointerdown', (e) => {
      const item = e.target.closest('.nav-item');
      if (!item) return;
      const link = item.querySelector('.nav-link');
      const dropdown = item.querySelector('.nav-dropdown');
      if (link && dropdown && navMenu.classList.contains('open')) {
        item.classList.toggle('open');
      }
    });
  }

  // â”€â”€â”€ Fade-in + Stagger Observer â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
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
    document.querySelectorAll('.stagger').forEach(el => observer.observe(el));
  } else {
    document.querySelectorAll('.fade-in').forEach(el => el.classList.add('visible'));
    document.querySelectorAll('.stagger').forEach(el => el.classList.add('visible'));
  }

  // â”€â”€â”€ Scroll to Top â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  const scrollTopBtn = document.querySelector('.scroll-top');
  if (scrollTopBtn) {
    window.addEventListener('scroll', () => {
      scrollTopBtn.classList.toggle('visible', window.scrollY > 500);
    });
    scrollTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // â”€â”€â”€ Cookie Consent â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
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

  // â”€â”€â”€ Active Nav Link + Parent Dropdown â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(link => {
    if (link.getAttribute('href') === currentPage) {
      link.classList.add('active');
      // Pre-open parent dropdown in sidebar
      const parentItem = link.closest('.nav-item');
      if (parentItem && window.innerWidth <= 1024) {
        parentItem.classList.add('open');
      }
    }
  });

  // â”€â”€â”€ Sidebar Scroll Tracking â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  const sidebarLinks = document.querySelectorAll('.doc-sidebar li a');
  if (sidebarLinks.length) {
    const sidebarInner = document.querySelector('.doc-sidebar-inner');
    const headings = [];
    let activeHeading = null;
    let sidebarTimer = null;

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
        const containerTop = sidebarInner.getBoundingClientRect().top;
        const linkTop = active.getBoundingClientRect().top;
        const offset = linkTop - containerTop;
        const targetScroll = sidebarInner.scrollTop + offset - sidebarInner.clientHeight / 2 + active.clientHeight / 2;
        sidebarInner.scrollTo({ top: targetScroll, behavior: 'instant' });
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
            clearTimeout(sidebarTimer);
            sidebarTimer = setTimeout(centerActiveInSidebar, 150);
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

  function easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
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

    // Count-up stats with eased animation
    const stats = container.closest('.constellation-section');
    if (stats) {
      const statEls = stats.querySelectorAll('.constellation-stat-number');
      statEls.forEach(el => {
        const target = parseInt(el.getAttribute('data-target'));
        const suffix = el.getAttribute('data-suffix') || '';
        if (!target) return;
        const duration = Math.min(2000, Math.max(800, target * 4));
        const start = performance.now();
        function tick(now) {
          const elapsed = now - start;
          const progress = Math.min(elapsed / duration, 1);
          const eased = easeOutCubic(progress);
          const current = Math.round(eased * target);
          el.textContent = current.toLocaleString() + suffix;
          if (progress < 1) {
            requestAnimationFrame(tick);
          }
        }
        requestAnimationFrame(tick);
      });
    }
  }

});
