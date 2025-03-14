// Technical Page Specific JavaScript

// Globale Variablen
let networkData = null;
let networkSvg = null;
let nodeElements = null;
let linkElements = null;
let selectedHoneypot = "Essen";
let showAllNodes = false;
let highlightFocus = true;

// Globale Variablen für die Wort-Visualisierung
let wordsVisible = {};
let expandedNode = null;
let wordsSimulation = null;

// Globale Variablen für die dynamische Netzwerkvisualisierung
let dynamicNetworkData = null;
let dynamicSimulation = null;
let dynamicSvg = null;
let dynamicNodes = null;
let dynamicLinks = null;
let currentFocusNode = null;
let focusAnimationInterval = null;
let currentEnergyLevel = 50;
let selectedHoneypotType = "Nahrung";
let showAllConnections = true;
let enableAutoFocusTransition = true;

document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM vollständig geladen, initialisiere Visualisierungen");

  // Überprüfe, ob D3.js verfügbar ist
  if (typeof d3 === "undefined") {
    console.error(
      "FEHLER: D3.js ist nicht verfügbar! Visualisierungen können nicht initialisiert werden."
    );
    return;
  } else {
    console.log("D3.js Version:", d3.version, "gefunden");
  }

  // Debug-Funktion, um zu überprüfen, ob alle Container existieren
  function debugContainers() {
    console.log("Debugging Container...");

    const containers = [
      { id: "focusNetwork", name: "Fokus-Netzwerk" },
      { id: "dynamic-network", name: "Dynamisches Netzwerk" },
      { id: "energyWave", name: "Energie-Welle" },
      { id: "honeypotWave", name: "Honeypot-Welle" },
      { id: "focusRadar", name: "Fokus-Radar" },
    ];

    containers.forEach((container) => {
      const element = document.getElementById(container.id);
      if (element) {
        console.log(`${container.name} (${container.id}) gefunden:`, {
          width: element.clientWidth,
          height: element.clientHeight,
          display: window.getComputedStyle(element).display,
          visibility: window.getComputedStyle(element).visibility,
        });
      } else {
        console.error(`${container.name} (${container.id}) NICHT gefunden!`);
      }
    });
  }

  // Debug-Ausgabe
  debugContainers();

  // Diese Funktion ist ein Platzhalter und wird später implementiert
  function initArchitectureDiagrams() {
    console.log(
      "Architekturdiagramme werden nicht initialisiert (noch nicht implementiert)"
    );
  }

  // Diese Funktion ist ein Platzhalter für die Fokus-Radar-Initialisierung
  function initFocusRadar() {
    console.log(
      "Fokus-Radar wird nicht initialisiert (noch nicht implementiert)"
    );
    // Der Radar-Canvas ist vorhanden, aber noch nicht implementiert
    const focusRadarCanvas = document.getElementById("focusRadar");
    if (focusRadarCanvas) {
      console.log(
        "Fokus-Radar-Canvas gefunden, aber Initialisierung übersprungen"
      );
    }
  }

  // Initialisierung der Architekturdiagramme
  initArchitectureDiagrams();

  // Initialisierung der Energiecharts
  initEnergyCharts();

  // Initialisierung der Prozessschritte
  initProcessSteps();

  // Initialisierung des Fokus-Radars
  initFocusRadar();

  // Prüfe, ob die Container für die Visualisierungen existieren
  const focusNetworkContainer = document.getElementById("focusNetwork");
  if (focusNetworkContainer) {
    console.log(
      "Fokus-Netzwerk-Container gefunden, initialisiere Fokus-Netzwerk"
    );
    initFocusNetwork();
  }

  // Initialisiere die dynamische Netzwerkvisualisierung, falls der Container existiert
  const dynamicNetworkContainer = document.getElementById("dynamic-network");
  if (dynamicNetworkContainer) {
    console.log(
      "Dynamisches Netzwerk-Container gefunden, initialisiere dynamisches Netzwerk"
    );
    initDynamicNetwork();
  }

  // Autofluctuation für die Energiewellen starten/stoppen
  const autoFluctuateControl = document.getElementById("autoFluctuate");
  if (autoFluctuateControl) {
    autoFluctuateControl.addEventListener("change", function () {
      if (this.checked) {
        startAutoFluctuate();
      } else {
        stopAutoFluctuate();
      }
    });
  }
});

// Architecture Diagram Animation
function initArchitectureDiagram() {
  const diagram = document.querySelector(".diagram");
  if (!diagram) return;

  const nodes = diagram.querySelectorAll(".diagram-node:not(.central)");
  const centralNode = diagram.querySelector(".diagram-node.central");

  // Verbesserte Animation für den zentralen Knoten
  if (centralNode) {
    centralNode.innerHTML += '<div class="pulse-ring"></div>';

    // Füge pulsierenden Effekt hinzu
    const pulseRing = centralNode.querySelector(".pulse-ring");
    pulseRing.style.cssText = `
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      border-radius: 50%;
      box-shadow: 0 0 0 20px rgba(99, 102, 241, 0.1);
      animation: pulse 2s infinite;
    `;
  }

  // Add data connection flows between nodes
  nodes.forEach((node) => {
    // Get original position
    const originalTop = parseFloat(node.style.top);
    const originalLeft = parseFloat(node.style.left);

    // Füge eine Beschriftung für die Funktion der Komponente hinzu
    const componentFunction = node.getAttribute("data-desc");
    const label = document.createElement("div");
    label.className = "component-function";
    label.textContent = componentFunction;
    label.style.cssText = `
      position: absolute;
      opacity: 0;
      transition: opacity 0.3s;
      font-size: 12px;
      background: rgba(0,0,0,0.7);
      color: white;
      padding: 5px 10px;
      border-radius: 4px;
      pointer-events: none;
      z-index: 100;
    `;

    // Zeige die Beschreibung beim Hover an
    node.addEventListener("mouseenter", () => {
      label.style.opacity = "1";
    });

    node.addEventListener("mouseleave", () => {
      label.style.opacity = "0";
    });

    // Subtile Bewegung für lebendiges Aussehen - sanfter und weniger chaotisch
    const moveInterval = setInterval(() => {
      const offsetY = (Math.random() - 0.5) * 3; // Reduzierte Bewegung
      const offsetX = (Math.random() - 0.5) * 3; // Reduzierte Bewegung

      node.style.top = `${originalTop + offsetY}%`;
      node.style.left = `${originalLeft + offsetX}%`;

      // Sanfte Rückführung zur Originalposition
      setTimeout(() => {
        node.style.transition = "top 2s, left 2s";
        node.style.top = `${originalTop}%`;
        node.style.left = `${originalLeft}%`;

        // Transition zurücksetzen für die nächste zufällige Bewegung
        setTimeout(() => {
          node.style.transition = "";
        }, 2000);
      }, 3000);
    }, 8000 + Math.random() * 4000); // Längere Intervalle für weniger Chaos
  });

  // Erstelle verbesserte Verbindungslinien
  createConnectionLines(diagram);

  // Füge eine Erklärung der Diagrammfunktion hinzu
  const descriptionEl = document.querySelector(".diagram-description");
  if (descriptionEl) {
    // Zeige die Beschreibung mit Verzögerung an
    setTimeout(() => {
      descriptionEl.classList.add("visible");
    }, 1000);
  }
}

// Create dynamic connection lines between nodes
function createConnectionLines(diagram) {
  const centralNode = diagram.querySelector(".diagram-node.central");
  const nodes = diagram.querySelectorAll(".diagram-node:not(.central)");

  if (!centralNode) return;

  // Get diagram dimensions
  const diagramRect = diagram.getBoundingClientRect();

  // Create SVG element for lines
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("width", "100%");
  svg.setAttribute("height", "100%");
  svg.style.position = "absolute";
  svg.style.top = "0";
  svg.style.left = "0";
  svg.style.zIndex = "2";
  svg.style.pointerEvents = "none";

  // Add SVG definition for gradient and markers
  const defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");

  // Pfeilspitzen für die Verbindungen
  const marker = document.createElementNS(
    "http://www.w3.org/2000/svg",
    "marker"
  );
  marker.setAttribute("id", "arrowhead");
  marker.setAttribute("markerWidth", "10");
  marker.setAttribute("markerHeight", "7");
  marker.setAttribute("refX", "9");
  marker.setAttribute("refY", "3.5");
  marker.setAttribute("orient", "auto");

  const polygon = document.createElementNS(
    "http://www.w3.org/2000/svg",
    "polygon"
  );
  polygon.setAttribute("points", "0 0, 10 3.5, 0 7");
  polygon.setAttribute("fill", "#6366f1");

  marker.appendChild(polygon);
  defs.appendChild(marker);
  svg.appendChild(defs);

  // Verbindungen zwischen dem zentralen Knoten und anderen Knoten
  nodes.forEach((node) => {
    // Zentrale Knotenposition
    const centralRect = centralNode.getBoundingClientRect();
    const centralX =
      centralRect.left + centralRect.width / 2 - diagramRect.left;
    const centralY = centralRect.top + centralRect.height / 2 - diagramRect.top;

    // Andere Knotenposition
    const nodeRect = node.getBoundingClientRect();
    const nodeX = nodeRect.left + nodeRect.width / 2 - diagramRect.left;
    const nodeY = nodeRect.top + nodeRect.height / 2 - diagramRect.top;

    // Verbindungslinien vom Zentrum nach außen
    const lineOut = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "line"
    );
    lineOut.setAttribute("x1", centralX);
    lineOut.setAttribute("y1", centralY);
    lineOut.setAttribute("x2", nodeX);
    lineOut.setAttribute("y2", nodeY);
    lineOut.setAttribute("stroke", "rgba(99, 102, 241, 0.6)");
    lineOut.setAttribute("stroke-width", "2");
    lineOut.setAttribute("marker-end", "url(#arrowhead)");

    // Daten-Fluss-Animation
    const animateOut = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "animate"
    );
    animateOut.setAttribute("attributeName", "stroke-dasharray");
    animateOut.setAttribute(
      "values",
      "0,200;30,150;60,120;90,90;120,60;150,30;200,0"
    );
    animateOut.setAttribute("dur", "3s");
    animateOut.setAttribute("repeatCount", "indefinite");
    lineOut.appendChild(animateOut);

    svg.appendChild(lineOut);

    // Verbindungen von anderen Knoten zum Zentrum
    const lineIn = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "line"
    );
    lineIn.setAttribute("x1", nodeX);
    lineIn.setAttribute("y1", nodeY);
    lineIn.setAttribute("x2", centralX);
    lineIn.setAttribute("y2", centralY);
    lineIn.setAttribute("stroke", "rgba(79, 70, 229, 0.4)");
    lineIn.setAttribute("stroke-width", "1.5");
    lineIn.setAttribute("stroke-dasharray", "6,4");

    // Animation der eingehenden Daten
    const animateIn = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "animate"
    );
    animateIn.setAttribute("attributeName", "stroke-dashoffset");
    animateIn.setAttribute("values", "0;-100");
    animateIn.setAttribute("dur", "8s");
    animateIn.setAttribute("repeatCount", "indefinite");
    lineIn.appendChild(animateIn);

    svg.appendChild(lineIn);
  });

  diagram.appendChild(svg);

  // Animation für die verschiedenen Verbindungstypen
  const style = document.createElement("style");
  style.textContent = `
    @keyframes pulse {
      0% { transform: scale(0.92); opacity: 1; }
      70% { transform: scale(1.1); opacity: 0; }
      100% { transform: scale(0.98); opacity: 0; }
    }
  `;
  document.head.appendChild(style);
}

// Energy Charts Animation mit Wellenform
function initEnergyCharts() {
  // DOM-Elemente
  const energyWaveCanvas = document.getElementById("energyWave");
  const honeypotWaveCanvas = document.getElementById("honeypotWave");
  const energyLevelDisplay = document.getElementById("energyLevelDisplay");
  const honeypotIntensityDisplay = document.getElementById(
    "honeypotIntensityDisplay"
  );
  const energyLevelControl = document.getElementById("energyLevelControl");
  const autoFluctuateControl = document.getElementById("autoFluctuateControl");
  const focusRadarCanvas = document.getElementById("focusRadar");

  // Debug-Ausgabe, um zu prüfen, ob die Elemente gefunden wurden
  console.log("Canvas-Elemente:", {
    energyWaveCanvas,
    honeypotWaveCanvas,
    energyLevelDisplay,
    honeypotIntensityDisplay,
    focusRadarCanvas,
  });

  // Überprüfen, ob die Elemente existieren
  if (!energyWaveCanvas || !honeypotWaveCanvas) {
    console.error("Canvas-Elemente für Wellenanimation nicht gefunden!");
    return;
  }

  // Canvas-Kontexte für das Zeichnen der Wellenformen
  let energyCtx = null;
  let honeypotCtx = null;
  let radarCtx = null;

  try {
    energyCtx = energyWaveCanvas.getContext("2d");
    honeypotCtx = honeypotWaveCanvas.getContext("2d");
    if (focusRadarCanvas) {
      radarCtx = focusRadarCanvas.getContext("2d");
    }

    if (!energyCtx || !honeypotCtx) {
      console.error("Canvas-Kontext konnte nicht initialisiert werden");
      return;
    }

    console.log("Canvas-Kontexte erfolgreich initialisiert");
  } catch (error) {
    console.error("Fehler beim Initialisieren der Canvas-Kontexte:", error);
    return;
  }

  // Animation-Parameter
  let direction = 1;
  let energyValue = 75; // Der tatsächliche Energiewert des Systems
  let autoFluctuateInterval;
  let animationFrameId;
  let isAutoFluctuate = true; // Standardmäßig automatisch fluktuieren
  let frameCounter = 0; // Zähler für Frames, um Bewegungen zu verlangsamen

  // Persistente Kontexte und Honeypots für das Radar
  let radarContexts = [];
  let radarHoneypots = [];
  let radarInitialized = false;

  // Sinus-Wellen-Parameter
  const waveParams = {
    energy: {
      amplitude: 20, // Höhe der Welle
      frequency: 0.02, // Frequenz der Welle
      phase: 0, // Phase (wird animiert)
      speed: 0.05, // Geschwindigkeit der Animation
      noise: 2, // Zufallsrauschen für natürlichere Bewegung
    },
    honeypot: {
      amplitude: 15,
      frequency: 0.03,
      phase: 0,
      speed: 0.03,
      noise: 3,
    },
  };

  // Farben für verschiedene Energie-Level
  const colors = {
    low: "#ef4444", // Rot für niedrige Energie
    medium: "#f59e0b", // Orange für mittlere Energie
    high: "#10b981", // Grün für hohe Energie
  };

  // Hilfsfunktion zum Aktualisieren der Anzeigen
  function updateDisplays() {
    // Energielevel-Anzeige aktualisieren
    if (energyLevelDisplay) {
      energyLevelDisplay.textContent = `${Math.round(energyValue)}%`;

      // CSS-Klassen für Farbkodierung
      energyLevelDisplay.classList.remove("low", "medium", "high");
      if (energyValue < 40) {
        energyLevelDisplay.classList.add("low");
      } else if (energyValue < 70) {
        energyLevelDisplay.classList.add("medium");
      } else {
        energyLevelDisplay.classList.add("high");
      }
    }

    // Honeypot-Suche basierend auf Energielevel berechnen
    let searchIntensity;
    if (energyValue < 40) {
      searchIntensity = 80 - energyValue; // Höhere Intensität bei niedrigerer Energie
    } else {
      searchIntensity = 10 + (70 - energyValue) / 3; // Niedriger Basiswert bei höherer Energie
    }

    // Begrenze auf sinnvolle Werte
    searchIntensity = Math.max(5, Math.min(80, searchIntensity));

    // Honeypot-Intensitätsanzeige aktualisieren
    if (honeypotIntensityDisplay) {
      honeypotIntensityDisplay.textContent = `${Math.round(searchIntensity)}%`;
    }

    // Wellen-Amplitude basierend auf Energielevel und Suchintensität anpassen
    waveParams.energy.amplitude = 10 + (energyValue / 100) * 20;
    waveParams.honeypot.amplitude = 5 + (searchIntensity / 100) * 25;

    // Wellengeschwindigkeit basierend auf Werten anpassen
    waveParams.energy.speed = 0.03 + (energyValue / 100) * 0.04;
    waveParams.honeypot.speed = 0.02 + (searchIntensity / 100) * 0.06;

    // Fokus-Radar aktualisieren, wenn vorhanden
    if (radarCtx && focusRadarCanvas) {
      // Nur alle 10 Frames die Kontexte aktualisieren (Verlangsamung auf 1/10)
      const shouldUpdatePositions = frameCounter % 10 === 0;
      drawFocusRadar(
        radarCtx,
        energyValue,
        searchIntensity,
        shouldUpdatePositions
      );
    }

    // Schieberegler synchronisieren, aber nur wenn wir nicht gerade eine manuelle Änderung vornehmen
    if (
      energyLevelControl &&
      !energyLevelControl.classList.contains("user-adjusting")
    ) {
      energyLevelControl.value = energyValue;
    }
  }

  // Funktion zum Zeichnen einer Sinuswelle
  function drawWave(ctx, params, value, canvasWidth, canvasHeight) {
    try {
      // Canvas löschen
      ctx.clearRect(0, 0, canvasWidth, canvasHeight);

      // Aktuelle Farbe basierend auf Wert bestimmen
      let waveColor;
      if (value < 40) {
        waveColor = colors.low;
      } else if (value < 70) {
        waveColor = colors.medium;
      } else {
        waveColor = colors.high;
      }

      // Gradient erstellen
      const gradient = ctx.createLinearGradient(0, 0, 0, canvasHeight);
      gradient.addColorStop(0, waveColor);
      gradient.addColorStop(1, `${waveColor}50`); // Halbtransparente Version

      // Zeichnungspfad beginnen
      ctx.beginPath();

      // Startpunkt ist links unten
      ctx.moveTo(0, canvasHeight);

      // Sinuskurve durch den Canvas zeichnen
      for (let x = 0; x < canvasWidth; x++) {
        // Basisfüllhöhe basierend auf Wert (0-100%)
        const baseHeight = canvasHeight - (value / 100) * canvasHeight;

        // Sinuswelle mit etwas Rauschen für natürlicheres Aussehen
        const noise = (Math.random() - 0.5) * params.noise;
        const y =
          baseHeight +
          Math.sin(x * params.frequency + params.phase) * params.amplitude +
          noise;

        ctx.lineTo(x, y);
      }

      // Pfad vervollständigen (zum unteren Rand und zurück zum Start)
      ctx.lineTo(canvasWidth, canvasHeight);
      ctx.lineTo(0, canvasHeight);
      ctx.closePath();

      // Welle füllen
      ctx.fillStyle = gradient;
      ctx.fill();

      // Optional: Wellenkontur zeichnen
      ctx.strokeStyle = waveColor;
      ctx.lineWidth = 1.5;
      ctx.stroke();

      // Phase für Animation aktualisieren
      params.phase += params.speed;
    } catch (error) {
      console.error("Fehler beim Zeichnen der Welle:", error);
    }
  }

  // Funktion zum Initialisieren der Radar-Daten
  function initializeRadarData(width, height) {
    const centerX = width / 2;
    const centerY = height / 2;
    const maxRadius = Math.min(width, height) * 0.4;

    // Honeypots initialisieren
    radarHoneypots = [];
    const numHoneypots = 3;
    const honeypotRadius = 10;

    for (let i = 0; i < numHoneypots; i++) {
      const angle = (i * Math.PI * 2) / numHoneypots;
      const distanceFromCenter = maxRadius * 0.6; // Honeypots sind etwas näher am Zentrum

      const x = centerX + Math.cos(angle) * distanceFromCenter;
      const y = centerY + Math.sin(angle) * distanceFromCenter;

      radarHoneypots.push({
        x,
        y,
        radius: honeypotRadius,
        pulsePhase: Math.random() * Math.PI * 2, // Zufällige Startphase für Pulsen
      });
    }

    // Kontexte initialisieren
    radarContexts = [];
    const numContexts = 40;

    for (let i = 0; i < numContexts; i++) {
      const angle = Math.random() * Math.PI * 2;
      const distance = Math.random() * maxRadius;

      const x = centerX + Math.cos(angle) * distance;
      const y = centerY + Math.sin(angle) * distance;

      // Distanz zum nächsten Honeypot berechnen
      let minDistanceToHoneypot = Infinity;
      for (const honeypot of radarHoneypots) {
        const dx = x - honeypot.x;
        const dy = y - honeypot.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        minDistanceToHoneypot = Math.min(minDistanceToHoneypot, distance);
      }

      // Radius basierend auf Distanz zu Honeypots
      const radius = 3 + Math.random() * 4;

      radarContexts.push({
        x,
        y,
        radius,
        originalX: x, // Original-Position speichern
        originalY: y,
        distanceToHoneypot: minDistanceToHoneypot,
        distanceFromCenter: distance,
        movementAngle: Math.random() * Math.PI * 2, // Zufälliger Bewegungswinkel
        movementSpeed: 0.2 + Math.random() * 0.3, // Langsame Bewegungsgeschwindigkeit
      });
    }

    radarInitialized = true;
  }

  // Funktion zum schrittweisen Aktualisieren der Kontext-Positionen
  function updateContextPositions(centerX, centerY, maxRadius) {
    for (const context of radarContexts) {
      // Nur minimale Bewegung
      const movementScale = 0.5; // Bewegungsskalierung (niedrigere Werte = langsamere Bewegung)

      // Berechne neue Position mit kleiner zufälliger Änderung
      context.movementAngle += (Math.random() - 0.5) * 0.2; // Leichte Richtungsänderung

      const dx =
        Math.cos(context.movementAngle) * context.movementSpeed * movementScale;
      const dy =
        Math.sin(context.movementAngle) * context.movementSpeed * movementScale;

      // Neue Position
      let newX = context.x + dx;
      let newY = context.y + dy;

      // Prüfen, ob die neue Position innerhalb des Radarkreises liegt
      const distFromCenter = Math.sqrt(
        Math.pow(newX - centerX, 2) + Math.pow(newY - centerY, 2)
      );

      // Wenn zu weit vom Zentrum entfernt, Richtung umkehren
      if (distFromCenter > maxRadius) {
        context.movementAngle += Math.PI; // Richtung umkehren
        newX = context.x;
        newY = context.y;
      }

      // Position aktualisieren
      context.x = newX;
      context.y = newY;

      // Distanz zum nächsten Honeypot neu berechnen
      let minDistanceToHoneypot = Infinity;
      for (const honeypot of radarHoneypots) {
        const dx = newX - honeypot.x;
        const dy = newY - honeypot.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        minDistanceToHoneypot = Math.min(minDistanceToHoneypot, distance);
      }

      context.distanceToHoneypot = minDistanceToHoneypot;
      context.distanceFromCenter = distFromCenter;
    }
  }

  // Neue Funktion: Fokus-Radar zeichnen - Visualisiert den Zusammenhang zwischen Energielevel und Kontext-Fokus
  function drawFocusRadar(
    ctx,
    energyValue,
    searchIntensity,
    updatePositions = false
  ) {
    try {
      // Größe des Canvas holen
      const width = ctx.canvas.width;
      const height = ctx.canvas.height;

      // Canvas löschen
      ctx.clearRect(0, 0, width, height);

      // Hintergrund zeichnen
      ctx.fillStyle = "#f8fafc";
      ctx.fillRect(0, 0, width, height);

      // Zentrum des Radars
      const centerX = width / 2;
      const centerY = height / 2;

      // Radius für verschiedene Komponenten
      const maxRadius = Math.min(width, height) * 0.4;

      // Initialisiere Radar-Daten, wenn noch nicht geschehen
      if (!radarInitialized) {
        initializeRadarData(width, height);
      }

      // Aktualisiere Kontext-Positionen, falls gewünscht
      if (updatePositions) {
        updateContextPositions(centerX, centerY, maxRadius);
      }

      // Gitter zeichnen
      ctx.strokeStyle = "#e2e8f0";
      ctx.lineWidth = 1;

      // Konzentrische Kreise
      for (let r = maxRadius / 4; r <= maxRadius; r += maxRadius / 4) {
        ctx.beginPath();
        ctx.arc(centerX, centerY, r, 0, Math.PI * 2);
        ctx.stroke();
      }

      // Radiale Linien
      for (let angle = 0; angle < Math.PI * 2; angle += Math.PI / 6) {
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(
          centerX + Math.cos(angle) * maxRadius,
          centerY + Math.sin(angle) * maxRadius
        );
        ctx.stroke();
      }

      // Berechne den Fokusbereich basierend auf Energielevel
      // Bei niedrigem Energielevel: Fokus auf Honeypots
      // Bei hohem Energielevel: Fokus weitet sich aus

      // Radius des Fokusbereichs für niedrige Energie (in Prozent des maxRadius)
      const lowEnergyFocusRadius = maxRadius * 0.7;

      // Zusätzlicher Radius für hohe Energie
      const highEnergyExtraRadius = maxRadius * 0.3 * (energyValue / 100);

      // Zeichne zuerst den erweiterten Fokusbereich für hohe Energie
      if (energyValue > 40) {
        ctx.beginPath();
        ctx.arc(
          centerX,
          centerY,
          lowEnergyFocusRadius + highEnergyExtraRadius,
          0,
          Math.PI * 2
        );
        ctx.fillStyle = `rgba(16, 185, 129, ${0.2 + (energyValue - 40) / 150})`; // Grün mit Alphakanal
        ctx.fill();
      }

      // Zeichne den Basis-Fokusbereich für niedrige Energie
      ctx.beginPath();
      ctx.arc(centerX, centerY, lowEnergyFocusRadius, 0, Math.PI * 2);

      // Farbe basierend auf Energielevel
      let focusColor;
      if (energyValue < 40) {
        focusColor = `rgba(239, 68, 68, ${0.3 + (40 - energyValue) / 100})`; // Intensiveres Rot bei niedrigerer Energie
      } else {
        focusColor = `rgba(245, 158, 11, 0.3)`; // Orange für mittlere Energie
      }

      ctx.fillStyle = focusColor;
      ctx.fill();

      // Verbindungslinien zwischen Honeypots und nahen Kontexten zeichnen
      // Intensität hängt vom Energielevel ab
      const connectionThreshold = maxRadius * 0.25;
      const connectionOpacity = energyValue < 40 ? 0.7 : 0.3; // Stärkere Verbindungen bei niedrigem Energielevel

      for (const context of radarContexts) {
        for (const honeypot of radarHoneypots) {
          const dx = context.x - honeypot.x;
          const dy = context.y - honeypot.y;
          const distance = Math.sqrt(dx * dx + dy * dy);

          if (distance < connectionThreshold) {
            // Je näher am Honeypot, desto stärker die Verbindung
            const strength = 1 - distance / connectionThreshold;

            ctx.beginPath();
            ctx.moveTo(honeypot.x, honeypot.y);
            ctx.lineTo(context.x, context.y);
            ctx.strokeStyle = `rgba(249, 115, 22, ${
              strength * connectionOpacity
            })`;
            ctx.lineWidth = 1 + strength;
            ctx.stroke();
          }
        }
      }

      // Zeichne die Kontexte mit unterschiedlichen Farben basierend auf Fokusbereich
      for (const context of radarContexts) {
        ctx.beginPath();
        ctx.arc(context.x, context.y, context.radius, 0, Math.PI * 2);

        // Ist der Kontext im Fokusbereich?
        const distanceFromCenter = context.distanceFromCenter;

        // Unterschiedliche Farben für Kontexte je nach Position
        if (distanceFromCenter <= lowEnergyFocusRadius) {
          // Im niedrigen Energiebereich
          if (context.distanceToHoneypot < maxRadius * 0.2) {
            // Nahe bei Honeypots und im niedrigen Energiebereich = hohes Interesse
            ctx.fillStyle = "#ef4444"; // Rot
            ctx.strokeStyle = "#b91c1c";
          } else {
            // Im niedrigen Energiebereich, aber nicht nah an Honeypots
            ctx.fillStyle = "#f97316"; // Orange
            ctx.strokeStyle = "#c2410c";
          }
        } else if (
          distanceFromCenter <=
          lowEnergyFocusRadius + highEnergyExtraRadius
        ) {
          // Im hohen Energiebereich (nur aktiv bei hoher Energie)
          ctx.fillStyle = "#10b981"; // Grün
          ctx.strokeStyle = "#047857";
        } else {
          // Außerhalb des Fokusbereichs = geringes Interesse
          ctx.fillStyle = "#cbd5e1"; // Hellgrau
          ctx.strokeStyle = "#94a3b8";
        }

        ctx.fill();
        ctx.lineWidth = 1;
        ctx.stroke();
      }

      // Honeypots zeichnen (Energiequellen)
      const time = Date.now() / 1000;

      for (const honeypot of radarHoneypots) {
        // Pulsierender Effekt um die Honeypots
        const pulseSize = 5 + (searchIntensity / 20) * 15; // Größerer Puls bei höherer Suchintensität

        ctx.beginPath();
        const pulseRadius =
          honeypot.radius +
          pulseSize * Math.abs(Math.sin(time * (2 + searchIntensity / 40))); // Schnellerer Puls bei höherer Intensität

        ctx.arc(honeypot.x, honeypot.y, pulseRadius, 0, Math.PI * 2);
        ctx.strokeStyle = `rgba(249, 115, 22, ${
          0.7 * Math.abs(Math.sin(time * 2))
        })`; // Pulsierender Alphakanal
        ctx.lineWidth = 2;
        ctx.stroke();

        // Honeypot selbst zeichnen
        ctx.beginPath();
        ctx.arc(honeypot.x, honeypot.y, honeypot.radius, 0, Math.PI * 2);
        ctx.fillStyle = "#f97316"; // Orange für Honeypots
        ctx.fill();
        ctx.strokeStyle = "#c2410c";
        ctx.lineWidth = 2;
        ctx.stroke();

        // Honeypot-Icons: stilisiertes Bienenwaben-Muster
        ctx.beginPath();
        ctx.moveTo(honeypot.x - 5, honeypot.y);
        ctx.lineTo(honeypot.x - 2.5, honeypot.y - 4);
        ctx.lineTo(honeypot.x + 2.5, honeypot.y - 4);
        ctx.lineTo(honeypot.x + 5, honeypot.y);
        ctx.lineTo(honeypot.x + 2.5, honeypot.y + 4);
        ctx.lineTo(honeypot.x - 2.5, honeypot.y + 4);
        ctx.closePath();
        ctx.strokeStyle = "#fff";
        ctx.lineWidth = 1;
        ctx.stroke();
      }

      // Energiebalken am unteren Rand
      const barHeight = 10;
      const barWidth = width * 0.8;
      const barX = (width - barWidth) / 2;
      const barY = height - 20;

      // Hintergrund
      ctx.fillStyle = "#e2e8f0";
      ctx.fillRect(barX, barY, barWidth, barHeight);

      // Füllstand
      let barColor;
      if (energyValue < 40) {
        barColor = colors.low;
      } else if (energyValue < 70) {
        barColor = colors.medium;
      } else {
        barColor = colors.high;
      }

      ctx.fillStyle = barColor;
      ctx.fillRect(barX, barY, barWidth * (energyValue / 100), barHeight);

      // Rahmen
      ctx.strokeStyle = "#94a3b8";
      ctx.lineWidth = 1;
      ctx.strokeRect(barX, barY, barWidth, barHeight);

      // Beschriftung
      ctx.fillStyle = "#334155";
      ctx.font = "12px Arial";
      ctx.textAlign = "center";
      ctx.fillText(
        `Energielevel: ${Math.round(energyValue)}%`,
        width / 2,
        barY - 5
      );
    } catch (error) {
      console.error("Fehler beim Zeichnen des Fokus-Radars:", error);
    }
  }

  // Funktion zum Animieren der Wellen
  function animateWaves() {
    try {
      // Frame-Zähler erhöhen
      frameCounter++;

      // Canvas-Abmessungen aktualisieren
      const energyWidth = energyWaveCanvas.offsetWidth || 600;
      const energyHeight = energyWaveCanvas.offsetHeight || 100;
      const honeypotWidth = honeypotWaveCanvas.offsetWidth || 600;
      const honeypotHeight = honeypotWaveCanvas.offsetHeight || 100;

      // Canvas-Größen setzen
      energyWaveCanvas.width = energyWidth;
      energyWaveCanvas.height = energyHeight;
      honeypotWaveCanvas.width = honeypotWidth;
      honeypotWaveCanvas.height = honeypotHeight;

      // Radar-Canvas-Größe aktualisieren, wenn vorhanden
      if (focusRadarCanvas) {
        focusRadarCanvas.width = focusRadarCanvas.offsetWidth || 500;
        focusRadarCanvas.height = focusRadarCanvas.offsetHeight || 300;
      }

      // Energie-Welle zeichnen
      drawWave(
        energyCtx,
        waveParams.energy,
        energyValue,
        energyWaveCanvas.width,
        energyWaveCanvas.height
      );

      // Honeypot-Suche-Intensität berechnen
      let searchIntensity;
      if (energyValue < 40) {
        searchIntensity = 80 - energyValue; // Höhere Intensität bei niedrigerer Energie
      } else {
        searchIntensity = 10 + (70 - energyValue) / 3; // Niedriger Basiswert bei höherer Energie
      }
      searchIntensity = Math.max(5, Math.min(80, searchIntensity));

      // Honeypot-Welle zeichnen
      drawWave(
        honeypotCtx,
        waveParams.honeypot,
        searchIntensity,
        honeypotWaveCanvas.width,
        honeypotWaveCanvas.height
      );

      // Fokus-Radar aktualisieren, wenn vorhanden
      if (radarCtx && focusRadarCanvas) {
        // Nur alle 10 Frames die Kontexte aktualisieren (Verlangsamung auf 1/10)
        const shouldUpdatePositions = frameCounter % 10 === 0;
        drawFocusRadar(
          radarCtx,
          energyValue,
          searchIntensity,
          shouldUpdatePositions
        );
      }

      // Animation fortsetzen
      animationFrameId = requestAnimationFrame(animateWaves);
    } catch (error) {
      console.error("Fehler in der Wellenanimation:", error);
    }
  }

  // Automatische Fluktuation starten
  function startAutoFluctuate() {
    if (autoFluctuateInterval) clearInterval(autoFluctuateInterval);

    isAutoFluctuate = true;

    autoFluctuateInterval = setInterval(() => {
      // Richtung gelegentlich zufällig ändern
      if (Math.random() < 0.3) {
        direction *= -1;
      }

      // Energie mit kleinen zufälligen Änderungen aktualisieren
      energyValue += direction * (Math.random() * 2);

      // Innerhalb der Grenzen halten
      if (energyValue > 90) {
        energyValue = 90;
        direction = -1;
      } else if (energyValue < 30) {
        energyValue = 30;
        direction = 1;
      }

      // Anzeigen aktualisieren
      updateDisplays();
    }, 1000); // Häufigere Aktualisierung für bessere Sichtbarkeit der Änderungen
  }

  // Automatische Fluktuation stoppen
  function stopAutoFluctuate() {
    clearInterval(autoFluctuateInterval);
    isAutoFluctuate = false;
  }

  // Wenn der Energie-Schieberegler vorhanden ist, Event-Listener hinzufügen
  if (energyLevelControl) {
    // Beim Beginn der Interaktion
    energyLevelControl.addEventListener("mousedown", function () {
      this.classList.add("user-adjusting");
      // Automatische Fluktuation stoppen
      stopAutoFluctuate();

      // Checkbox deaktivieren
      if (autoFluctuateControl) {
        autoFluctuateControl.checked = false;
      }
    });

    // Für Touch-Geräte
    energyLevelControl.addEventListener("touchstart", function () {
      this.classList.add("user-adjusting");
      stopAutoFluctuate();

      if (autoFluctuateControl) {
        autoFluctuateControl.checked = false;
      }
    });

    // Beim Ändern des Wertes
    energyLevelControl.addEventListener("input", function () {
      const newEnergyLevel = parseFloat(this.value);
      energyValue = newEnergyLevel; // Aktuellen Energiewert aktualisieren
      updateDisplays();
    });

    // Nach Ende der Interaktion
    energyLevelControl.addEventListener("mouseup", function () {
      this.classList.remove("user-adjusting");
    });

    // Für Touch-Geräte
    energyLevelControl.addEventListener("touchend", function () {
      this.classList.remove("user-adjusting");
    });
  }

  // Wenn die Auto-Fluktuations-Checkbox vorhanden ist, Event-Listener hinzufügen
  if (autoFluctuateControl) {
    // Dieser Event-Listener wird bereits im DOMContentLoaded-Event gesetzt,
    // daher hier nur überprüfen, ob die Checkbox aktiv ist
    if (autoFluctuateControl.checked) {
      startAutoFluctuate(); // Auto-Fluktuation starten
    } else {
      stopAutoFluctuate();
    }
  }

  // Fenstergrößenänderung behandeln
  window.addEventListener("resize", () => {
    // Kurz Animation stoppen und neu starten für korrekte Canvas-Größe
    cancelAnimationFrame(animationFrameId);
    console.log(
      "Fenstergrößenänderung erkannt, Canvas-Größen werden neu berechnet"
    );
    animateWaves();
  });

  // Initial die Anzeigen aktualisieren
  updateDisplays();

  // Animation starten
  console.log("Starte Wellenanimation...");
  animateWaves();
} // Ende der initEnergyCharts-Funktion

// Process Steps Interaction
function initProcessSteps() {
  const steps = document.querySelectorAll(".process-step");

  steps.forEach((step) => {
    step.addEventListener("mouseenter", () => {
      // Highlight the step
      step.style.borderLeft = "4px solid var(--primary-color)";

      // Show code snippet with fade-in
      const codeSnippet = step.querySelector(".code-snippet");
      if (codeSnippet) {
        codeSnippet.style.opacity = "0";
        codeSnippet.style.display = "block";

        // Fade in
        setTimeout(() => {
          codeSnippet.style.transition = "opacity 0.5s ease";
          codeSnippet.style.opacity = "1";
        }, 50);
      }
    });

    step.addEventListener("mouseleave", () => {
      // Reset highlighting
      step.style.borderLeft = "";
    });
  });

  // Add connection lines between steps
  const processSteps = document.querySelector(".process-diagram");
  if (processSteps) {
    for (let i = 0; i < steps.length - 1; i++) {
      const currentStep = steps[i];
      const nextStep = steps[i + 1];

      // Create connection line
      const connector = document.createElement("div");
      connector.classList.add("step-connector");
      connector.style.position = "absolute";
      connector.style.width = "2px";
      connector.style.backgroundColor = "var(--primary-light)";
      connector.style.opacity = "0.5";
      connector.style.zIndex = "1";

      // Position the connector
      const currentStepRect = currentStep.getBoundingClientRect();
      const nextStepRect = nextStep.getBoundingClientRect();
      const processRect = processSteps.getBoundingClientRect();

      connector.style.top = `${currentStepRect.bottom - processRect.top}px`;
      connector.style.left = `${
        (currentStepRect.left + currentStepRect.right) / 2 - processRect.left
      }px`;
      connector.style.height = `${nextStepRect.top - currentStepRect.bottom}px`;

      processSteps.appendChild(connector);
    }
  }
}

// Add fade-in effect for sections when scrolling
function addFadeInEffect() {
  const sections = document.querySelectorAll("section");

  const fadeOptions = {
    threshold: 0.2,
    rootMargin: "0px 0px -100px 0px",
  };

  const fadeObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        // Add fade-in class
        entry.target.classList.add("fade-in-section");

        // Start animations inside the section
        animateSection(entry.target);

        // Stop observing once animation is done
        observer.unobserve(entry.target);
      }
    });
  }, fadeOptions);

  // Add initial styling and start observing sections
  sections.forEach((section) => {
    section.style.opacity = "0";
    section.style.transform = "translateY(50px)";
    section.style.transition = "opacity 0.8s ease, transform 0.8s ease";

    fadeObserver.observe(section);
  });
}

// Start animations within a section
function animateSection(section) {
  section.style.opacity = "1";
  section.style.transform = "translateY(0)";

  // Animate elements inside the section with cascading delay
  const elements = section.querySelectorAll(
    "h3, .code-block, .honeypot, .process-step, .chart-container, .diagram-node"
  );

  elements.forEach((element, index) => {
    element.style.opacity = "0";
    element.style.transform = "translateY(20px)";
    element.style.transition = "opacity 0.5s ease, transform 0.5s ease";

    // Add cascading delay
    setTimeout(() => {
      element.style.opacity = "1";
      element.style.transform = "translateY(0)";
    }, 100 + index * 100); // 100ms base delay + 100ms per element
  });
}

// Funktion zur Initialisierung des Fokus-Netzwerks
function initFocusNetwork() {
  console.log("Initialisiere Fokus-Netzwerk mit semantischen Sätzen");

  // Gültigen Container prüfen
  const container = document.getElementById("focusNetwork");
  if (!container) {
    console.error("Container #focusNetwork nicht gefunden!");
    // Fallback-Content hinzufügen, falls die Visualisierung nicht geladen werden kann
    container.innerHTML = `
      <div class="fallback-content">
        <div class="fallback-icon"><i class="fas fa-project-diagram"></i></div>
        <h3>Netzwerk-Visualisierung</h3>
        <p>Die Visualisierung konnte nicht geladen werden. Bitte aktualisieren Sie die Seite.</p>
      </div>
    `;
    return;
  }

  // D3.js-Verfügbarkeit prüfen
  if (!window.d3) {
    console.error("D3.js ist nicht verfügbar!");
    container.innerHTML = `
      <div class="fallback-content">
        <div class="fallback-icon"><i class="fas fa-exclamation-triangle"></i></div>
        <h3>D3.js fehlt</h3>
        <p>Die erforderliche D3.js-Bibliothek wurde nicht geladen.</p>
      </div>
    `;
    return;
  } else {
    console.log("D3.js-Version:", d3.version);
  }

  console.log("Container gefunden:", container);

  // Größe auf sinnvollen Wert setzen
  const width = Math.max(container.clientWidth, 300);
  const height = Math.max(container.clientHeight, 300);

  console.log("Container-Größe:", width, "x", height);

  // Bestehende SVG-Elemente entfernen, falls vorhanden
  d3.select(container).selectAll("svg").remove();
  console.log("Bestehende SVG-Elemente entfernt");

  try {
    // SVG-Element erstellen
    const svg = d3
      .select(container)
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto;");

    // Haupt-Gruppe für Zooming und Panning
    const g = svg.append("g");

    // Zoom-Verhalten hinzufügen
    const zoom = d3
      .zoom()
      .scaleExtent([0.1, 4])
      .on("zoom", (event) => {
        g.attr("transform", event.transform);
      });

    // Zoom-Verhalten auf SVG anwenden
    svg.call(zoom);

    // Standardmäßig in die Mitte zoomen
    svg.call(
      zoom.transform,
      d3.zoomIdentity.translate(width / 4, height / 4).scale(0.8)
    );

    // Semantische Satz-Knoten definieren
    const nodes = [
      // Schlüsselkonzepte
      { id: "Apfel", group: "object", label: "🍎 Apfel" },
      { id: "schmeckt", group: "verb", label: "schmeckt" },
      { id: "Farbe", group: "property", label: "Farbe" },
      { id: "rote", group: "property", label: "rote" },
      { id: "hat", group: "verb", label: "hat" },
      { id: "ich", group: "pronoun", label: "ich" },
      { id: "mir", group: "pronoun", label: "mir" },
      { id: "was", group: "pronoun", label: "was" },
      { id: "esse", group: "action", label: "esse" },
      { id: "lecker", group: "property", label: "lecker" },
      { id: "eine", group: "article", label: "eine" },

      // Kategorie und Honeypot
      { id: "Essen", group: "category", label: "🍽️ Essen" },
      { id: "Honeypot", group: "honeypot", label: "🍯 Grundbedürfnis" },
    ];

    // Objekt zur Verfolgung der Knotengrößen
    const nodeRadii = {};
    nodes.forEach((node) => {
      if (node.group === "honeypot") nodeRadii[node.id] = 30;
      else if (node.group === "category") nodeRadii[node.id] = 25;
      else if (node.group === "sentence") nodeRadii[node.id] = 20;
      else nodeRadii[node.id] = 15;
    });

    const links = [
      // Verbindungen zwischen Wörtern und Sätzen
      {
        source: "Apfel",
        target: "schmeckt",
        value: 2,
        type: "part_of",
      },
      {
        source: "schmeckt",
        target: "lecker",
        value: 2,
        type: "part_of",
      },

      {
        source: "Apfel",
        target: "hat",
        value: 2,
        type: "part_of",
      },
      {
        source: "hat",
        target: "eine",
        value: 2,
        type: "part_of",
      },
      {
        source: "eine",
        target: "rote",
        value: 2,
        type: "part_of",
      },
      {
        source: "rote",
        target: "Farbe",
        value: 2,
        type: "part_of",
      },

      {
        source: "mir",
        target: "schmeckt",
        value: 2,
        type: "part_of",
      },
      {
        source: "schmeckt",
        target: "Apfel",
        value: 2,
        type: "part_of",
      },

      {
        source: "ich",
        target: "esse",
        value: 2,
        type: "part_of",
      },
      {
        source: "esse",
        target: "was",
        value: 2,
        type: "part_of",
      },
      {
        source: "was",
        target: "mir",
        value: 2,
        type: "part_of",
      },
      {
        source: "mir",
        target: "schmeckt",
        value: 2,
        type: "part_of",
      },

      // Verbindungen zu Essen und Honeypot
      { source: "esse", target: "Essen", value: 3, type: "category" },

      //{ source: "Apfel", target: "Essen", value: 2, type: "category" },
      { source: "Essen", target: "Honeypot", value: 4, type: "honeypot" },
    ];

    // Kraftsimulation erstellen
    const simulation = d3
      .forceSimulation(nodes)
      .force(
        "link",
        d3
          .forceLink(links)
          .id((d) => d.id)
          .distance((d) => {
            // Setze unterschiedliche Abstände je nach Verbindungstyp
            if (d.type === "honeypot") return 150;
            if (d.type === "category") return 120;
            if (d.type === "semantic") return 100;
            if (d.type === "part_of") return 70;
            return 80;
          })
      )
      .force("charge", d3.forceManyBody().strength(-400))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force(
        "collision",
        d3.forceCollide().radius((d) => {
          // Verschiedene Größen für verschiedene Knotentypen
          return nodeRadii[d.id] || 15;
        })
      );

    // Container für Links erstellen
    const link = g
      .append("g")
      .attr("class", "links")
      .selectAll("line")
      .data(links)
      .enter()
      .append("line")
      .attr("class", (d) => `link ${d.type}`)
      .attr("stroke-width", (d) => Math.sqrt(d.value) * 1.5);

    // Container für Nodes erstellen
    const node = g
      .append("g")
      .attr("class", "nodes")
      .selectAll(".node")
      .data(nodes)
      .enter()
      .append("g")
      .attr("class", (d) => `node ${d.group}`)
      .call(
        d3
          .drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended)
      );

    // Kreise für die Nodes hinzufügen
    node
      .append("circle")
      .attr("r", (d) => nodeRadii[d.id] || 15)
      .on("click", handleNodeClick);

    // Labels für die Nodes hinzufügen
    node
      .append("text")
      .attr("dy", (d) => (d.group === "sentence" ? "0.35em" : "0.35em"))
      .attr("text-anchor", "middle")
      .text((d) => d.label)
      .style("font-size", (d) => {
        if (d.group === "honeypot") return "14px";
        if (d.group === "category") return "12px";
        if (d.group === "sentence") return "10px";
        return "10px";
      })
      .style("fill", (d) => {
        const lightTextGroups = [
          "honeypot",
          "category",
          "sentence",
          "object",
          "action",
        ];
        return lightTextGroups.includes(d.group) ? "white" : "black";
      });

    // Tooltips für bessere Benutzerfreundlichkeit
    node.append("title").text((d) => `${d.label} (${d.group})`);

    // Mausrad-Event für die Knotengrößenänderung
    svg.on("wheel", function (event) {
      // Wenn die Umschalttaste gedrückt ist, Knotengröße ändern
      if (event.shiftKey) {
        event.preventDefault();

        // Das ausgewählte Element identifizieren (wenn vorhanden)
        const selectedElement = document.querySelector(".node circle.selected");
        if (selectedElement) {
          const selectedNodeId = selectedElement.__data__.id;

          // Delta-Wert bestimmen (Vergrößern oder Verkleinern)
          const delta = event.deltaY < 0 ? 1 : -1;

          // Neue Größe berechnen (mit Grenzen)
          nodeRadii[selectedNodeId] = Math.max(
            5,
            Math.min(60, (nodeRadii[selectedNodeId] || 15) + delta)
          );

          // Größe aktualisieren
          d3.select(selectedElement).attr("r", nodeRadii[selectedNodeId]);

          // Force-Kollision neu berechnen
          simulation.force(
            "collision",
            d3.forceCollide().radius((d) => nodeRadii[d.id] || 15)
          );
          simulation.alpha(0.3).restart();
        }
      }
    });

    // Hinweistext für Zoom und Größenänderung
    const helpText = svg
      .append("text")
      .attr("x", 10)
      .attr("y", 20)
      .attr("class", "help-text")
      .style("font-size", "12px")
      .style("fill", "#666")
      .text(
        "Maus: Ziehen zum Verschieben, Mausrad zum Zoomen, Shift+Mausrad für Knotengröße"
      );

    // Simulation starten und bei jedem Tick aktualisieren
    simulation.on("tick", () => {
      link
        .attr("x1", (d) => d.source.x)
        .attr("y1", (d) => d.source.y)
        .attr("x2", (d) => d.target.x)
        .attr("y2", (d) => d.target.y);

      node.attr("transform", (d) => {
        // Beschränke die Position auf den sichtbaren Bereich
        d.x = Math.max(20, Math.min(width - 20, d.x));
        d.y = Math.max(20, Math.min(height - 20, d.y));
        return `translate(${d.x}, ${d.y})`;
      });
    });

    // Speichere Referenzen für spätere Verwendung
    networkData = {
      simulation: simulation,
      nodes: nodes,
      links: links,
      nodeElements: node,
      linkElements: link,
      svg: svg,
      container: container,
    };

    // Informationsfeld für Benutzerhinweise anzeigen
    const infoPanel = document.getElementById("contextInfo");
    if (infoPanel) {
      infoPanel.innerHTML = `
        <div class="network-help">
          <h3>Interaktives Netzwerk</h3>
          <p>• Ziehen Sie mit der Maus zum Verschieben des gesamten Netzwerks</p>
          <p>• Mausrad zum Zoomen des Netzwerks</p>
          <p>• Knoten durch Ziehen bewegen</p>
          <p>• Knoten anklicken für Details</p>
          <p>• Shift + Mausrad zum Ändern der Knotengröße</p>
        </div>
      `;
    }

    console.log("Fokus-Netzwerk erfolgreich initialisiert");
  } catch (error) {
    console.error("Fehler bei der Initialisierung des Fokus-Netzwerks:", error);
    container.innerHTML = `
      <div class="fallback-content">
        <div class="fallback-icon"><i class="fas fa-bug"></i></div>
        <h3>Visualisierung fehlgeschlagen</h3>
        <p>Fehler: ${error.message}</p>
      </div>
    `;
  }
}

// Drag-Funktionen für interaktive Knoten
function dragstarted(event, d) {
  // Verhindern, dass das Zoom-Verhalten aktiviert wird während des Ziehens
  if (event.sourceEvent.stopPropagation) event.sourceEvent.stopPropagation();

  // Alpha-Ziel setzen, um die Simulation zu erwärmen
  if (!event.active) networkData.simulation.alphaTarget(0.3).restart();

  // Position fixieren
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(event, d) {
  // Position entsprechend der aktuellen Mausposition aktualisieren
  // Berücksichtige die aktuelle Transformation (Zoom und Pan)
  const transform = d3.zoomTransform(networkData.svg.node());
  d.fx = (event.x - transform.x) / transform.k;
  d.fy = (event.y - transform.y) / transform.k;
}

function dragended(event, d) {
  // Alpha-Ziel zurücksetzen
  if (!event.active) networkData.simulation.alphaTarget(0);

  // Position freigeben (optional, auskommentiert um die Position zu erhalten)
  // d.fx = null;
  // d.fy = null;
}

// Knoten-Klick-Handler
function handleNodeClick(event, d) {
  console.log("Knoten angeklickt:", d);

  // Highlight des ausgewählten Knotens
  d3.selectAll(".node circle").classed("selected", false);
  d3.select(this).classed("selected", true);

  // Verbindungen hervorheben
  highlightConnections(d);

  // Kontext-Informationen anzeigen
  showContextInfo(d);
}

// Hilfsfunktion zur Bestimmung des Verbindungstyp-Namens
function getConnectionTypeName(type) {
  switch (type) {
    case "part_of":
      return "Teil von";
    case "semantic":
      return "Semantische Verbindung";
    case "category":
      return "Kategorisierung";
    case "honeypot":
      return "Grundbedürfnis";
    case "color":
      return "Farbeigenschaft";
    case "taste":
      return "Geschmackseigenschaft";
    case "property":
      return "Eigenschaft";
    default:
      return type;
  }
}

// Funktion zum Generieren der Netzwerkdaten
function generateNetworkData() {
  console.log("Generating network data...");

  // Definiere die Knoten
  const nodes = [
    // Honeypot und Kategorie
    { id: "Honeypot", group: "honeypot", label: "🍯 Grundbedürfnis" },
    { id: "Essen", group: "category", label: "🍽️ Essen" },

    // Wörter aus "Ich esse was mir schmeckt"
    { id: "ich", group: "pronoun", label: "ich" },
    { id: "esse", group: "verb", label: "esse" },
    { id: "was", group: "pronoun", label: "was" },
    { id: "mir", group: "pronoun", label: "mir" },
    { id: "schmeckt", group: "verb", label: "schmeckt" },

    // Wörter aus "Ein Apfel schmeckt lecker"
    { id: "ein", group: "article", label: "ein" },
    { id: "Apfel", group: "object", label: "🍎 Apfel" },
    { id: "lecker", group: "property", label: "lecker" },

    // Wörter aus "Ein Apfel hat eine rote Farbe"
    { id: "hat", group: "verb", label: "hat" },
    { id: "eine", group: "article", label: "eine" },
    { id: "rote", group: "property", label: "rote" },
    { id: "Farbe", group: "object", label: "🎨 Farbe" },
  ];

  // Definiere die Verbindungen
  const links = [
    // Verbindungen zum Honeypot
    { source: "Honeypot", target: "Essen", value: 3, type: "honeypot" },

    // Sequenz 1: "Ich esse was mir schmeckt"
    { source: "ich", target: "esse", value: 1, type: "part_of" },
    { source: "esse", target: "was", value: 1, type: "part_of" },
    { source: "was", target: "mir", value: 1, type: "part_of" },
    { source: "mir", target: "schmeckt", value: 1, type: "part_of" },

    // Sequenz 2: "Ein Apfel schmeckt lecker"
    { source: "ein", target: "Apfel", value: 1, type: "part_of" },
    { source: "Apfel", target: "schmeckt", value: 1, type: "part_of" },
    { source: "schmeckt", target: "lecker", value: 1, type: "part_of" },

    // Sequenz 3: "Ein Apfel hat eine rote Farbe"
    { source: "ein", target: "Apfel", value: 1, type: "part_of" },
    { source: "Apfel", target: "hat", value: 1, type: "part_of" },
    { source: "hat", target: "eine", value: 1, type: "part_of" },
    { source: "eine", target: "rote", value: 1, type: "part_of" },
    { source: "rote", target: "Farbe", value: 1, type: "part_of" },

    // Verbindungen zur Kategorie
    { source: "Apfel", target: "Essen", value: 2, type: "category" },
  ];

  // Setze die Positionen der Knoten
  nodes.forEach((node, i) => {
    // Honeypot oben
    if (node.id === "Honeypot") {
      node.x = 400;
      node.y = 50;
    }
    // Kategorie darunter
    else if (node.id === "Essen") {
      node.x = 400;
      node.y = 150;
    }
    // Wörter aus "Ich esse was mir schmeckt"
    else if (["ich", "esse", "was", "mir", "schmeckt"].includes(node.id)) {
      node.x =
        200 + ["ich", "esse", "was", "mir", "schmeckt"].indexOf(node.id) * 100;
      node.y = 250;
    }
    // Wörter aus "Ein Apfel schmeckt lecker"
    else if (["ein", "Apfel", "lecker"].includes(node.id)) {
      node.x = 300 + ["ein", "Apfel", "lecker"].indexOf(node.id) * 100;
      node.y = 350;
    }
    // Wörter aus "Ein Apfel hat eine rote Farbe"
    else if (["hat", "eine", "rote", "Farbe"].includes(node.id)) {
      node.x = 250 + ["hat", "eine", "rote", "Farbe"].indexOf(node.id) * 100;
      node.y = 450;
    }
  });

  return { nodes, links };
}

// Funktion zum Aktualisieren des Netzwerks
function updateNetwork() {
  // Gültigen Container prüfen
  const container = document.getElementById("focusNetwork");
  if (!container) return;

  // Bestehende SVG-Elemente überprüfen, falls nicht vorhanden, neu erstellen
  if (!networkSvg) {
    const width = container.clientWidth;
    const height = container.clientHeight || 500;

    networkSvg = d3
      .select(container)
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto;");

    // Definiere Marker für Pfeilspitzen
    networkSvg
      .append("defs")
      .selectAll("marker")
      .data(["end"])
      .enter()
      .append("marker")
      .attr("id", (d) => d)
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", 23)
      .attr("refY", 0)
      .attr("markerWidth", 6)
      .attr("markerHeight", 6)
      .attr("orient", "auto")
      .append("path")
      .attr("fill", "#999")
      .attr("d", "M0,-5L10,0L0,5");

    // Gruppen für Links und Nodes
    networkSvg.append("g").attr("class", "links");
    networkSvg.append("g").attr("class", "nodes");

    // Erstelle Simulationsdaten
    networkData = generateNetworkData();

    // Links erstellen
    linkElements = networkSvg
      .select(".links")
      .selectAll("line")
      .data(networkData.links)
      .enter()
      .append("line")
      .attr("class", (d) => `link ${d.type}`)
      .attr("stroke", "#999")
      .attr("stroke-width", 1.5)
      .attr("stroke-opacity", 0.6);

    // Node-Gruppen erstellen
    const nodeGroups = networkSvg
      .select(".nodes")
      .selectAll("g")
      .data(networkData.nodes)
      .enter()
      .append("g")
      .attr("class", (d) => `node ${d.group}`)
      .call(
        d3
          .drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended)
      );

    // Kreise für die Nodes
    nodeGroups
      .append("circle")
      .attr("r", (d) => {
        if (d.group === "fruit") return 30;
        if (d.group === "property") return 25;
        if (d.group === "color") return 20;
        if (d.group === "taste") return 20;
        return 15;
      })
      .attr("fill", (d) => {
        if (d.group === "fruit") return "#3b82f6"; // Blau für Früchte
        if (d.group === "property") return "#22c55e"; // Grün für Eigenschaften
        if (d.group === "color") return "#f97316"; // Orange für Farben
        if (d.group === "taste") return "#f97316"; // Orange für Geschmack
        return "#a855f7"; // Lila für andere
      })
      .attr("stroke", "#fff")
      .attr("stroke-width", 1.5)
      .on("click", handleNodeClick);

    // Labels für die Nodes
    nodeGroups
      .append("text")
      .text((d) => d.label)
      .attr("x", 0)
      .attr("y", (d) => {
        if (d.group === "fruit") return 3;
        return 3;
      })
      .attr("text-anchor", "middle")
      .attr("dominant-baseline", "middle")
      .attr("font-size", (d) => {
        if (d.group === "fruit") return "12px";
        return "10px";
      })
      .attr("fill", "#fff")
      .attr("pointer-events", "none");

    // Erstelle die Simulation
    simulation = d3
      .forceSimulation(networkData.nodes)
      .force(
        "link",
        d3
          .forceLink(networkData.links)
          .id((d) => d.id)
          .distance(100)
      )
      .force("charge", d3.forceManyBody().strength(-200))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collide", d3.forceCollide().radius(40).strength(0.2))
      .on("tick", ticked);

    // Positioniere die Nodes anfänglich an den definierten Positionen
    networkData.nodes.forEach((node) => {
      if (node.x && node.y) {
        node.fx = node.x;
        node.fy = node.y;
      }
    });

    // Nach kurzer Zeit die feste Position lösen, damit die Knoten sich bewegen können
    setTimeout(() => {
      networkData.nodes.forEach((node) => {
        node.fx = null;
        node.fy = null;
      });
      simulation.alpha(0.3).restart();
    }, 2000);

    // Tick-Funktion für die Simulation
    function ticked() {
      linkElements
        .attr("x1", (d) => d.source.x)
        .attr("y1", (d) => d.source.y)
        .attr("x2", (d) => d.target.x)
        .attr("y2", (d) => d.target.y);

      networkSvg
        .selectAll(".node")
        .attr("transform", (d) => `translate(${d.x}, ${d.y})`);
    }

    // Zeige den Hilfstext an
    const expandHint = document.createElement("div");
    expandHint.className = "expand-hint";
    expandHint.innerHTML =
      "<i class='fas fa-info-circle'></i> Klicken Sie auf einen Knoten, um Details anzuzeigen";
    container.appendChild(expandHint);

    nodeElements = nodeGroups;
  }
}

// Funktion zur Initialisierung der dynamischen Netzwerkvisualisierung
function initDynamicNetwork() {
  console.log(
    "Initialisiere dynamisches Netzwerk mit vereinfachter Implementierung"
  );

  // Gültigen Container prüfen
  const container = document.getElementById("dynamic-network");
  if (!container) {
    console.error("Container #dynamic-network nicht gefunden!");
    return;
  }

  console.log("Container gefunden:", container);
  console.log(
    "Container-Größe:",
    container.clientWidth,
    "x",
    container.clientHeight
  );

  // Größe auf sinnvollen Wert setzen, falls zu klein
  const width = container.clientWidth || 600;
  const height = container.clientHeight || 400;

  if (width < 100 || height < 100) {
    console.warn("Container-Größe ist zu klein:", width, "x", height);
    console.warn("Verwende Standard-Größe: 600 x 400");
  }

  try {
    // Bestehende SVG-Elemente entfernen, falls vorhanden
    d3.select(container).selectAll("svg").remove();
    console.log("Bestehende SVG-Elemente entfernt");

    // SVG-Element erstellen
    const svg = d3
      .select(container)
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: 100%;");

    // Haupt-Gruppe für Zooming und Panning
    const g = svg.append("g");

    // Zoom-Verhalten hinzufügen
    const zoom = d3
      .zoom()
      .scaleExtent([0.1, 4])
      .on("zoom", (event) => {
        g.attr("transform", event.transform);
      });

    // Zoom-Verhalten auf SVG anwenden
    svg.call(zoom);

    // Standardmäßig in die Mitte zoomen
    svg.call(
      zoom.transform,
      d3.zoomIdentity.translate(width / 4, height / 4).scale(0.8)
    );

    console.log("SVG-Element erstellt:", svg.node());

    // Einfache Testdaten - nur ein paar Honeypots und Kontexte
    const nodes = [
      {
        id: "honeypot1",
        type: "honeypot",
        label: "Essen",
        x: width / 2,
        y: height / 2,
      },
      {
        id: "context1",
        type: "essential",
        label: "Hunger",
        x: width / 2 - 120,
        y: height / 2 - 80,
      },
      {
        id: "context2",
        type: "essential",
        label: "Nahrung",
        x: width / 2 + 120,
        y: height / 2 - 80,
      },
      {
        id: "context3",
        type: "related",
        label: "Kochen",
        x: width / 2 - 80,
        y: height / 2 + 100,
      },
      {
        id: "context4",
        type: "related",
        label: "Gesundheit",
        x: width / 2 + 80,
        y: height / 2 + 100,
      },
      {
        id: "context5",
        type: "distant",
        label: "Kultur",
        x: width / 2 - 200,
        y: height / 2 + 20,
      },
    ];

    // Objekt zur Verfolgung der Knotengrößen
    const nodeRadii = {};
    nodes.forEach((node) => {
      if (node.type === "honeypot") nodeRadii[node.id] = 25;
      else if (node.type === "essential") nodeRadii[node.id] = 20;
      else if (node.type === "related") nodeRadii[node.id] = 15;
      else nodeRadii[node.id] = 12;
    });

    const links = [
      { source: "honeypot1", target: "context1", type: "essential" },
      { source: "honeypot1", target: "context2", type: "essential" },
      { source: "context1", target: "context3", type: "related" },
      { source: "context2", target: "context4", type: "related" },
      { source: "context3", target: "context5", type: "distant" },
    ];

    // Kraft-Simulation erstellen für interaktive Bewegung
    const simulation = d3
      .forceSimulation(nodes)
      .force(
        "link",
        d3
          .forceLink(links)
          .id((d) => d.id)
          .distance((d) => {
            if (d.type === "essential") return 120;
            if (d.type === "related") return 100;
            return 80;
          })
      )
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force(
        "collision",
        d3.forceCollide().radius((d) => nodeRadii[d.id] || 12)
      );

    // Verbindungen erstellen
    const link = g
      .append("g")
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("class", (d) => `dynamic-link ${d.type}`);

    // Knoten erstellen
    const node = g
      .append("g")
      .selectAll("g")
      .data(nodes)
      .join("g")
      .attr("class", (d) => `dynamic-node-group ${d.type}`)
      .call(
        d3
          .drag()
          .on("start", dragStartDynamic)
          .on("drag", dragDynamic)
          .on("end", dragEndDynamic)
      );

    // Kreise für die Knoten
    node
      .append("circle")
      .attr("class", (d) => `dynamic-node ${d.type}`)
      .attr("r", (d) =>
        d.type === "honeypot"
          ? 25
          : d.type === "essential"
          ? 20
          : d.type === "related"
          ? 15
          : 12
      );

    // Labels für die Knoten
    node
      .append("text")
      .attr("text-anchor", "middle")
      .attr("dy", (d) => (d.type === "honeypot" ? 35 : 25))
      .text((d) => d.label)
      .attr("font-size", (d) => (d.type === "honeypot" ? 12 : 10))
      .attr("font-weight", "bold")
      .attr("fill", "#333")
      .attr("pointer-events", "none");

    console.log("Dynamisches Netzwerk erstellt");

    // Markiere einen Knoten als fokussiert
    svg
      .selectAll(".dynamic-node")
      .filter((d, i) => i === 1)
      .classed("focused", true);

    // Markiere entsprechende Verbindungen als fokussiert
    svg
      .selectAll(".dynamic-link")
      .filter((d, i) => i === 0)
      .classed("focused", true);
  } catch (error) {
    console.error("Fehler beim Erstellen des dynamischen Netzwerks:", error);
  }
}

// Diese Funktion wird aufgerufen, wenn die Seite vollständig geladen ist
window.onload = function () {
  console.log("Window.onload Event ausgelöst");

  // Direkter Aufruf der Visualisierungsfunktionen als Fallback
  if (document.getElementById("focusNetwork")) {
    console.log("Direkter Aufruf von initFocusNetwork");
    initFocusNetwork();
  }

  if (document.getElementById("dynamic-network")) {
    console.log("Direkter Aufruf von initDynamicNetwork");
    initDynamicNetwork();
  }
};

// Hilfsfunktion zum Generieren einer Kontextbeschreibung
function generateContextDescription(node) {
  if (!node)
    return {
      emoji: "❓",
      description: "Kein Knoten ausgewählt",
      connectionType: "Unbekannt",
    };

  let emoji = "";
  let description = "";
  let connectionType = "";

  switch (node.group) {
    case "fruit":
      emoji = "🍎";
      description = `${node.label} ist eine Frucht mit spezifischen Eigenschaften wie Farbe und Geschmack.`;
      connectionType = "Frucht";
      break;
    case "color":
      emoji = "🎨";
      description = `${node.label} ist eine Farbe, die bestimmten Objekten zugeordnet werden kann.`;
      connectionType = "Farbe";
      break;
    case "taste":
      emoji = "👅";
      description = `${node.label} ist ein Geschmack, der von bestimmten Früchten oder Lebensmitteln wahrgenommen wird.`;
      connectionType = "Geschmack";
      break;
    case "sentence":
      emoji = "📝";
      description = `"${node.label}" ist ein vollständiger Satz, der einen Gedanken oder eine Beziehung zwischen Konzepten ausdrückt.`;
      connectionType = "Satz";
      break;
    case "object":
      emoji = "🍎";
      description = `${node.label} ist ein konkretes Objekt in unserem Sprachmodell, das Eigenschaften haben und in Beziehungen zu anderen Konzepten stehen kann.`;
      connectionType = "Objekt";
      break;
    case "verb":
      emoji = "🏃";
      description = `${node.label} ist ein Verb, das eine Handlung oder einen Zustand beschreibt und Subjekte mit Objekten verbindet.`;
      connectionType = "Verb";
      break;
    case "pronoun":
      emoji = "👤";
      description = `${node.label} ist ein Pronomen, das auf eine Person oder Entität verweist, ohne sie direkt zu benennen.`;
      connectionType = "Pronomen";
      break;
    case "property":
      emoji = "🏷️";
      description = `${node.label} ist eine Eigenschaft, die Objekte oder Konzepte näher beschreibt.`;
      connectionType = "Eigenschaft";
      break;
    case "action":
      emoji = "🔧";
      description = `${node.label} repräsentiert eine konkrete Handlung, die ein Subjekt ausführen kann.`;
      connectionType = "Handlung";
      break;
    case "category":
      emoji = "🍽️";
      description = `${node.label} ist eine Kategorie, die verschiedene Konzepte zusammenfasst. Es repräsentiert ein grundlegendes Bedürfnis des Bewusstseins und ist mit einem Honeypot verbunden.`;
      connectionType = "Kategorie";
      break;
    case "honeypot":
      emoji = "🍯";
      description = `${node.label} repräsentiert ein elementares Grundbedürfnis des künstlichen Bewusstseins. Honeypots sind zentrale Energiequellen, zu denen das Bewusstsein bei niedrigem Energiestand zurückkehrt.`;
      connectionType = "Honeypot";
      break;
    default:
      emoji = "❓";
      description = `${node.label} ist ein unbekannter Kontexttyp.`;
      connectionType = "Unbekannt";
  }

  return {
    emoji,
    description,
    connectionType,
  };
}

// Funktion zum Hervorheben von Verbindungen eines Knotens
function highlightConnections(node) {
  // Links hervorheben, die mit diesem Knoten verbunden sind
  const connectedLinks = networkData.links.filter(
    (link) =>
      (typeof link.source === "object"
        ? link.source.id === node.id
        : link.source === node.id) ||
      (typeof link.target === "object"
        ? link.target.id === node.id
        : link.target === node.id)
  );

  d3.selectAll(".link").classed("highlighted", false);
  d3.selectAll(".link")
    .filter((link) => connectedLinks.includes(link))
    .classed("highlighted", true);

  // Verbundene Knoten ebenfalls visuell hervorheben
  const connectedNodeIds = new Set();

  connectedLinks.forEach((link) => {
    const sourceId =
      typeof link.source === "object" ? link.source.id : link.source;
    const targetId =
      typeof link.target === "object" ? link.target.id : link.target;

    if (sourceId === node.id) {
      connectedNodeIds.add(targetId);
    } else {
      connectedNodeIds.add(sourceId);
    }
  });

  d3.selectAll(".node").classed(
    "connected",
    (d) => connectedNodeIds.has(d.id) && d.id !== node.id
  );
}

// Funktion zum Anzeigen von Kontext-Informationen
function showContextInfo(node) {
  // Info-Panel anzeigen
  const infoPanel = document.querySelector(".node-info-panel");
  const contextInfo = document.getElementById("contextInfo");

  if (infoPanel && contextInfo) {
    // Kontextbeschreibung generieren
    const contextData = generateContextDescription(node);

    // Finde verbundene Knoten
    const connectedNodes = [];
    if (networkData) {
      networkData.links.forEach((link) => {
        if (link.source.id === node.id || link.source === node.id) {
          const target =
            typeof link.target === "object"
              ? link.target
              : networkData.nodes.find((n) => n.id === link.target);
          if (target && !connectedNodes.some((n) => n.id === target.id)) {
            connectedNodes.push({
              node: target,
              type: link.type,
            });
          }
        } else if (link.target.id === node.id || link.target === node.id) {
          const source =
            typeof link.source === "object"
              ? link.source
              : networkData.nodes.find((n) => n.id === link.source);
          if (source && !connectedNodes.some((n) => n.id === source.id)) {
            connectedNodes.push({
              node: source,
              type: link.type,
            });
          }
        }
      });
    }

    // Generiere Liste der verbundenen Knoten mit ihren Typen
    const connectedNodesList = connectedNodes
      .map((conn) => {
        const typeName = getConnectionTypeName(conn.type);
        return `<li><span class="context-type ${conn.node.group}">${conn.node.group}</span> ${conn.node.label} <small>(${typeName})</small></li>`;
      })
      .join("");

    // HTML für die Kontextinformation erstellen
    contextInfo.innerHTML = `
      <div class="context-details">
        <div class="context-header">
          <span class="context-emoji">${contextData.emoji}</span>
          <h4>${node.label}</h4>
          <span class="context-type ${node.group}">${
      contextData.connectionType
    }</span>
        </div>
        <div class="context-body">
          <p>${contextData.description}</p>
          <div class="connected-contexts">
            <strong>Verbundene Konzepte:</strong>
            <ul>
              ${connectedNodesList || "<li>Keine verbundenen Konzepte</li>"}
            </ul>
          </div>
        </div>
      </div>
    `;

    // Info-Panel sichtbar machen
    infoPanel.classList.add("visible");
  }
}
