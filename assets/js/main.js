(() => {
  const header = document.querySelector(".site-header");
  const toggle = document.querySelector(".nav-toggle");
  const links = document.querySelector(".nav-links");

  const onScroll = () => {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 12);
  };

  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  if (toggle && links) {
    toggle.addEventListener("click", () => {
      const open = links.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });

    links.querySelectorAll("a").forEach((a) => {
      a.addEventListener("click", () => {
        links.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  document.querySelectorAll(
    ".article-body section, .article-body .diagram-block, .article-body .hld-panel-grid, .article-body .hld-boe, .article-body .callout, .article-body .compare-grid, .article-hero .prose-wrap"
  ).forEach((el) => el.classList.add("reveal"));

  const revealTargets = document.querySelectorAll(".reveal, .diagram-block");
  revealTargets.forEach((el, i) => {
    if (!el.style.transitionDelay) {
      const parent = el.parentElement;
      const siblings = parent ? [...parent.querySelectorAll(".reveal")].indexOf(el) : i;
      const delay = siblings >= 0 ? siblings * 90 : i * 90;
      el.style.transitionDelay = `${delay}ms`;
    }
  });

  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    revealTargets.forEach((el) => io.observe(el));
  } else {
    revealTargets.forEach((el) => el.classList.add("is-visible"));
  }

  const year = document.querySelector("[data-year]");
  if (year) year.textContent = String(new Date().getFullYear());
})();
