document.addEventListener('DOMContentLoaded', () => {

  // ─── Scroll Progress ─────────────────────────────
  const scrollProgress = document.querySelector('.scroll-progress');
  if (scrollProgress) {
    window.addEventListener('scroll', () => {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      scrollProgress.style.width = docHeight > 0 ? (scrollTop / docHeight) * 100 + '%' : '0%';
    });
  }

  // ─── Nav Scroll Effect ───────────────────────────
  const nav = document.querySelector('.nav');
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.classList.toggle('scrolled', window.scrollY > 50);
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

  // ─── Intersection Observer Animations ────────────
  const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -60px 0px' };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  document.querySelectorAll('.fade-in, .fade-in-left, .fade-in-right').forEach(el => observer.observe(el));

  document.querySelectorAll('.stagger-children').forEach(container => {
    Array.from(container.children).forEach((child, index) => {
      child.style.transitionDelay = `${index * 0.08}s`;
      observer.observe(child);
    });
  });

  // ─── Count-up Animation ──────────────────────────
  const statNumbers = document.querySelectorAll('.stat-number');
  const statObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseInt(el.getAttribute('data-target'));
        const suffix = el.getAttribute('data-suffix') || '';
        const duration = 2200;
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

        statObserver.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  statNumbers.forEach(el => statObserver.observe(el));

  // ─── Stat Ring Animation ─────────────────────────
  document.querySelectorAll('.stat-ring-fill').forEach(el => {
    const ringObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const percent = parseFloat(entry.target.getAttribute('data-percent') || 75);
          const circumference = 2 * Math.PI * 40;
          entry.target.style.strokeDashoffset = circumference - (percent / 100) * circumference;
          ringObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    ringObserver.observe(el);
  });

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

  // ─── Page Transitions ────────────────────────────
  const pageTransition = document.querySelector('.page-transition');
  if (pageTransition) {
    pageTransition.style.opacity = '1';
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        pageTransition.style.opacity = '0';
      });
    });

    document.querySelectorAll('a[href]').forEach(link => {
      const href = link.getAttribute('href');
      if (href && href.endsWith('.html') && !href.startsWith('http') && !href.startsWith('#') && !href.startsWith('mailto:')) {
        link.addEventListener('click', (e) => {
          e.preventDefault();
          pageTransition.classList.add('active');
          setTimeout(() => { window.location.href = href; }, 350);
        });
      }
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

  // ─── Hero Particles ──────────────────────────────
  const canvas = document.getElementById('heroParticles');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    let particles = [];
    const PARTICLE_COUNT = 60;

    function resizeCanvas() {
      canvas.width = canvas.parentElement.offsetWidth;
      canvas.height = canvas.parentElement.offsetHeight;
    }

    const colors = [
      { r: 10, g: 88, b: 166 },
      { r: 17, g: 129, b: 67 },
      { r: 210, g: 38, b: 39 },
      { r: 239, g: 125, b: 0 },
      { r: 201, g: 168, b: 76 }
    ];

    function createParticles() {
      particles = [];
      for (let i = 0; i < PARTICLE_COUNT; i++) {
        const color = colors[Math.floor(Math.random() * colors.length)];
        particles.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          size: Math.random() * 2.5 + 0.5,
          speedX: (Math.random() - 0.5) * 0.4,
          speedY: (Math.random() - 0.5) * 0.4,
          opacity: Math.random() * 0.4 + 0.1,
          color: color,
          pulse: Math.random() * Math.PI * 2
        });
      }
    }

    function drawParticles() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      particles.forEach(p => {
        p.pulse += 0.02;
        const pulseOpacity = p.opacity * (0.6 + 0.4 * Math.sin(p.pulse));

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${p.color.r}, ${p.color.g}, ${p.color.b}, ${pulseOpacity})`;
        ctx.fill();

        p.x += p.speedX;
        p.y += p.speedY;

        if (p.x < -10) p.x = canvas.width + 10;
        if (p.x > canvas.width + 10) p.x = -10;
        if (p.y < -10) p.y = canvas.height + 10;
        if (p.y > canvas.height + 10) p.y = -10;
      });

      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 140) {
            const alpha = 0.06 * (1 - dist / 140);
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.strokeStyle = `rgba(201, 168, 76, ${alpha})`;
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

  // ─── Active Nav Link ─────────────────────────────
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(link => {
    if (link.getAttribute('href') === currentPage) {
      link.classList.add('active');
    }
  });

  // ─── Smooth Anchor Scroll ────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

});
