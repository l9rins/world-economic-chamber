/* =====================================================
   WEC — World Economic Chamber
   Main JavaScript
   ===================================================== */

document.addEventListener('DOMContentLoaded', () => {

  // ─── Scroll Progress Bar ─────────────────────────
  const scrollProgress = document.querySelector('.scroll-progress');
  if (scrollProgress) {
    window.addEventListener('scroll', () => {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
      scrollProgress.style.width = progress + '%';
    });
  }

  // ─── Navigation Scroll Effect ─────────────────────
  const nav = document.querySelector('.nav');
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.classList.toggle('scrolled', window.scrollY > 50);
    });
  }

  // ─── Mobile Navigation Toggle ─────────────────────
  const navToggle = document.getElementById('navToggle');
  const navMenu = document.getElementById('navMenu');

  if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
      navToggle.classList.toggle('active');
      navMenu.classList.toggle('open');
      document.body.style.overflow = navMenu.classList.contains('open') ? 'hidden' : '';
    });

    // Mobile dropdown toggles
    const navItems = navMenu.querySelectorAll('.nav-item');
    navItems.forEach(item => {
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

  // ─── Intersection Observer Animations ─────────────
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -60px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // Observe all animate-able elements
  const animElements = document.querySelectorAll('.fade-in, .fade-in-left, .fade-in-right');
  animElements.forEach(el => observer.observe(el));

  // Stagger children
  const staggerContainers = document.querySelectorAll('.stagger-children');
  staggerContainers.forEach(container => {
    const children = container.children;
    Array.from(children).forEach((child, index) => {
      child.style.transitionDelay = `${index * 0.1}s`;
      observer.observe(child);
    });
  });

  // ─── Stat Counter Animation ───────────────────────
  const statNumbers = document.querySelectorAll('.stat-number');
  const statObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseInt(el.getAttribute('data-target'));
        const suffix = el.getAttribute('data-suffix') || '';
        let current = 0;
        const duration = 2000;
        const step = target / (duration / 16);

        const counter = setInterval(() => {
          current += step;
          if (current >= target) {
            current = target;
            clearInterval(counter);
          }
          el.textContent = Math.floor(current).toLocaleString() + suffix;
        }, 16);

        statObserver.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  statNumbers.forEach(el => statObserver.observe(el));

  // ─── Stat Ring Animation ──────────────────────────
  const statRings = document.querySelectorAll('.stat-ring-fill');
  const ringObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const percent = parseFloat(el.getAttribute('data-percent') || 75);
        const circumference = 2 * Math.PI * 40; // r=40
        const offset = circumference - (percent / 100) * circumference;
        el.style.strokeDashoffset = offset;
        ringObserver.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  statRings.forEach(el => ringObserver.observe(el));

  // ─── Scroll to Top Button ─────────────────────────
  const scrollTopBtn = document.querySelector('.scroll-top');
  if (scrollTopBtn) {
    window.addEventListener('scroll', () => {
      scrollTopBtn.classList.toggle('visible', window.scrollY > 600);
    });
    scrollTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ─── Page Transition ──────────────────────────────
  const pageTransition = document.querySelector('.page-transition');
  if (pageTransition) {
    // Fade in on load
    pageTransition.style.opacity = '1';
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        pageTransition.style.opacity = '0';
      });
    });

    // Fade out on link click
    document.querySelectorAll('a[href]').forEach(link => {
      const href = link.getAttribute('href');
      if (href && href.endsWith('.html') && !href.startsWith('http') && !href.startsWith('#') && !href.startsWith('mailto:')) {
        link.addEventListener('click', (e) => {
          e.preventDefault();
          pageTransition.classList.add('active');
          setTimeout(() => {
            window.location.href = href;
          }, 300);
        });
      }
    });
  }

  // ─── Cookie Consent ───────────────────────────────
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

  // ─── Hero Particles (canvas) ──────────────────────
  const canvas = document.getElementById('heroParticles');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    let particles = [];
    const PARTICLE_COUNT = 50;

    function resizeCanvas() {
      canvas.width = canvas.parentElement.offsetWidth;
      canvas.height = canvas.parentElement.offsetHeight;
    }

    function createParticles() {
      particles = [];
      for (let i = 0; i < PARTICLE_COUNT; i++) {
        particles.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          size: Math.random() * 2 + 0.5,
          speedX: (Math.random() - 0.5) * 0.3,
          speedY: (Math.random() - 0.5) * 0.3,
          opacity: Math.random() * 0.5 + 0.1
        });
      }
    }

    function drawParticles() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      particles.forEach(p => {
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(201, 168, 76, ${p.opacity})`;
        ctx.fill();

        p.x += p.speedX;
        p.y += p.speedY;

        if (p.x < 0) p.x = canvas.width;
        if (p.x > canvas.width) p.x = 0;
        if (p.y < 0) p.y = canvas.height;
        if (p.y > canvas.height) p.y = 0;
      });

      // Draw connections
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 120) {
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.strokeStyle = `rgba(201, 168, 76, ${0.08 * (1 - dist / 120)})`;
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        }
      }

      requestAnimationFrame(drawParticles);
    }

    resizeCanvas();
    createParticles();
    drawParticles();
    window.addEventListener('resize', () => { resizeCanvas(); createParticles(); });
  }

  // ─── Active Nav Link Highlight ────────────────────
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPage) {
      link.classList.add('active');
    }
  });

});
