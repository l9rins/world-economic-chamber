document.addEventListener('DOMContentLoaded', () => {

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
      child.style.transitionDelay = `${Math.min(index * 0.05, 0.25)}s`;
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

});
