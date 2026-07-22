document.addEventListener('DOMContentLoaded', () => {
    // Add micro-animations and interactivity

    // Header scroll effect
    const header = document.querySelector('.main-header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.style.background = 'rgba(255, 255, 255, 0.98)';
            header.style.boxShadow = '0 4px 20px rgba(0,0,0,0.1)';
        } else {
            header.style.background = '#ffffff';
            header.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)';
        }
    });

    // Fade-in animation for elements as they scroll into view
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Apply animation to document content blocks
    const docParagraphs = document.querySelectorAll('.doc-content p, .doc-content h2, .home-card');
    docParagraphs.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = `opacity 0.6s ease-out, transform 0.6s ease-out`;
        el.style.transitionDelay = `${(index % 5) * 0.1}s`;
        observer.observe(el);
    });
});
