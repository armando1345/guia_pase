// Return to the previous page when it belongs to this local guide.
// The HTML link remains a direct route to the index for bookmarked pages.
document.querySelectorAll('[data-back]').forEach((link) => {
  link.addEventListener('click', (event) => {
    if (document.referrer && new URL(document.referrer).origin === location.origin && history.length > 1) {
      event.preventDefault();
      history.back();
    }
  });
});

// Reveal sections as they enter the viewport. Without JS, all text stays visible.
if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const sections = document.querySelectorAll('.intro, .chapter, .appendix, .archetype-list article');
  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    }
  }, { rootMargin: '0px 0px -36px 0px', threshold: 0.06 });

  for (const section of sections) {
    if (section.getBoundingClientRect().top > window.innerHeight - 36) {
      section.classList.add('reveal-target');
      observer.observe(section);
    }
  }
}
