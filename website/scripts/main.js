// Navigation Toggle für mobile Ansicht
document.addEventListener("DOMContentLoaded", function () {
  const navToggle = document.getElementById("navToggle");
  const navLinks = document.querySelector(".nav-links");

  if (navToggle) {
    navToggle.addEventListener("click", function () {
      navLinks.classList.toggle("active");

      // Ändere das Aussehen des Toggle-Buttons
      const spans = navToggle.querySelectorAll("span");
      spans.forEach((span) => span.classList.toggle("active"));
    });
  }

  // Sticky Navigation
  window.addEventListener("scroll", function () {
    const nav = document.querySelector("nav");
    if (window.scrollY > 100) {
      nav.classList.add("scrolled");
    } else {
      nav.classList.remove("scrolled");
    }
  });

  // Smooth Scrolling für Anchor-Links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();

      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        window.scrollTo({
          top: target.offsetTop - 80,
          behavior: "smooth",
        });
      }
    });
  });

  // Zufällige Netzwerkanimation für eine dynamischere Darstellung
  animateNetworkNodes();
});

// Funktion für die zufällige Bewegung der Netzwerkknoten
function animateNetworkNodes() {
  const nodes = document.querySelectorAll(".network-node");

  if (nodes.length === 0) return;

  nodes.forEach((node) => {
    // Ursprüngliche Position speichern
    const originalLeft = parseFloat(getComputedStyle(node).left);
    const originalTop = parseFloat(getComputedStyle(node).top);

    // Zufällige Bewegung um die Ursprungsposition
    setInterval(() => {
      const offsetX = Math.random() * 20 - 10; // -10 bis +10 Pixel
      const offsetY = Math.random() * 20 - 10; // -10 bis +10 Pixel

      node.style.left = `${originalLeft + offsetX}px`;
      node.style.top = `${originalTop + offsetY}px`;
    }, 3000 + Math.random() * 2000); // Zufälliges Intervall zwischen 3 und 5 Sekunden
  });
}

// Dynamische Größenanpassung der Netzwerkknoten basierend auf Scrollposition
window.addEventListener("scroll", function () {
  const scrollPosition = window.scrollY;
  const maxScroll = document.body.scrollHeight - window.innerHeight;
  const scrollPercentage = scrollPosition / maxScroll;

  const nodes = document.querySelectorAll(".network-node");

  nodes.forEach((node) => {
    if (node.classList.contains("primary")) {
      // Primärer Knoten wird größer, wenn nach unten gescrollt wird
      const size = 80 + scrollPercentage * 20;
      node.style.width = `${size}px`;
      node.style.height = `${size}px`;
    } else {
      // Sekundäre Knoten werden kleiner, wenn nach unten gescrollt wird
      const baseSize = node.classList.contains("secondary")
        ? 60
        : node.classList.contains("tertiary")
        ? 50
        : node.classList.contains("quaternary")
        ? 40
        : 30;

      const size = baseSize - scrollPercentage * 10;
      node.style.width = `${Math.max(size, 10)}px`; // Mindestgröße von 10px
      node.style.height = `${Math.max(size, 10)}px`;
    }
  });
});

// Fade-In-Effekt für Elemente beim Scrollen
document.addEventListener("DOMContentLoaded", function () {
  const fadeElements = document.querySelectorAll(
    ".feature-card, .process-step, .overview-content"
  );

  const fadeInOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -100px 0px",
  };

  const fadeInObserver = new IntersectionObserver(function (entries, observer) {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("fade-in");
        observer.unobserve(entry.target);
      }
    });
  }, fadeInOptions);

  fadeElements.forEach((element) => {
    element.classList.add("fade-element");
    fadeInObserver.observe(element);
  });
});

// Aktiver Navigationslink basierend auf Scrollposition
document.addEventListener("DOMContentLoaded", function () {
  const sections = document.querySelectorAll("section[id]");
  const navLinks = document.querySelectorAll(".nav-links a");

  window.addEventListener("scroll", function () {
    let current = "";

    sections.forEach((section) => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.clientHeight;

      if (pageYOffset >= sectionTop - 200) {
        current = section.getAttribute("id");
      }
    });

    navLinks.forEach((link) => {
      link.classList.remove("active");
      if (link.getAttribute("href").includes(current)) {
        link.classList.add("active");
      }
    });
  });
});
