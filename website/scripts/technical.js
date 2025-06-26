// Technical Page Specific JavaScript

// Global variables
let networkData = null;
let networkSvg = null;
let nodeElements = null;
let linkElements = null;
let selectedHoneypot = "Food"; // Translated from "Essen"
let showAllNodes = false;
let highlightFocus = true;

// Global variables for word visualization
let wordsVisible = {};
let expandedNode = null;
let wordsSimulation = null;

// Global variables for dynamic network visualization
let dynamicNetworkData = null;
let dynamicSimulation = null;
let dynamicSvg = null;
let dynamicNodes = null;
let dynamicLinks = null;
let currentFocusNode = null;
let focusAnimationInterval = null;
let currentEnergyLevel = 75; // Current energy level (globally available)
let selectedHoneypotType = "Food"; // Translated from "Nahrung"
let showAllConnections = true;
let enableAutoFocusTransition = true;
let isUpdatingSlider = false; // Flag to prevent infinite loops during slider updates

document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM fully loaded and parsed");

  // Check if D3.js is available
  if (typeof d3 === "undefined") {
    console.error(
      "ERROR: D3.js is not available! Visualizations cannot be initialized."
    );
    return;
  } else {
    console.log("D3.js Version:", d3.version, "found");
  }

  // Debug function to check if all containers exist
  function debugContainers() {
    console.log("Debugging containers...");

    const containers = [
      { id: "focusNetwork", name: "Focus Network" },
      { id: "dynamic-network", name: "Dynamic Network" },
      { id: "energyWave", name: "Energy Wave" },
      { id: "honeypotWave", name: "Honeypot Wave" },
      { id: "focusRadar", name: "Focus Radar" },
    ];

    containers.forEach((container) => {
      const element = document.getElementById(container.id);
      if (element) {
        console.log(`${container.name} (${container.id}) found:`, {
          width: element.clientWidth,
          height: element.clientHeight,
          display: window.getComputedStyle(element).display,
          visibility: window.getComputedStyle(element).visibility,
        });
      } else {
        console.error(`${container.name} (${container.id}) NOT found!`);
      }
    });
  }

  // Debug output
  debugContainers();

  // This function is a placeholder and will be implemented later
  function initArchitectureDiagrams() {
    console.log(
      "Architecture diagrams are not initialized (not yet implemented)"
    );
  }

  // This function is a placeholder for Focus Radar initialization
  function initFocusRadar() {
    console.log(
      "Focus Radar is not initialized (not yet implemented)"
    );
    // The radar canvas exists but is not yet implemented
    const focusRadarCanvas = document.getElementById("focusRadar");
    if (focusRadarCanvas) {
      console.log(
        "Focus Radar canvas found, but initialization skipped"
      );
    }
  }

  // Initialization of architecture diagrams
  initArchitectureDiagrams();

  // Initialization of energy charts
  initEnergyCharts();

  // Initialization of process steps
  initProcessSteps();

  // Initialization of Focus Radar
  initFocusRadar();

  // Check if containers for visualizations exist
  const focusNetworkContainer = document.getElementById("focusNetwork");
  if (focusNetworkContainer) {
    console.log(
      "Focus Network container found, initializing Focus Network"
    );
    initFocusNetwork();
  }

  // Initialize dynamic network visualization if the container exists
  const dynamicNetworkContainer = document.getElementById("dynamic-network");
  if (dynamicNetworkContainer) {
    console.log(
      "Dynamic Network container found, initializing Dynamic Network"
    );
    initDynamicNetwork();
  }

  // Start/stop auto-fluctuation for energy waves
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

  // Event-Listener für den Energieschieberegler
  const energyLevelControl = document.getElementById(
    "networkEnergyLevelControl"
  ); // Diese ID ändern
  const networkEnergyValue = document.getElementById("networkEnergyValue");
  const dynamicEnergySlider = document.getElementById("dynamic-energy-slider");
  const energyValueDisplay = document.getElementById("energy-value");

  if (energyLevelControl) {
    console.log("Verbinde Energieschieberegler mit Netzwerkvisualisierung");

    // Update the displayed value on load
    networkEnergyValue.textContent = `${energyLevelControl.value}%`;

    // Update the displayed value and visualization on changes
    energyLevelControl.addEventListener("input", function () {
      const value = this.value;
      networkEnergyValue.textContent = `${value}%`;

      // Update the network visualization with the new energy value
      currentEnergyLevel = parseInt(value);

      // Synchronize the dynamic slider
      if (dynamicEnergySlider && !isUpdatingSlider) {
        isUpdatingSlider = true;
        dynamicEnergySlider.value = value;
        if (energyValueDisplay) {
          energyValueDisplay.textContent = value;
        }
        isUpdatingSlider = false;
      }

      // If we have a dynamic network, update it
      if (typeof updateDynamicNetwork === "function") {
        updateDynamicNetwork(currentEnergyLevel);
      }
    });
  }

  // Event listener for the dynamic energy slider
  if (dynamicEnergySlider) {
    console.log(
      "Adding event listener for dynamic energy slider"
    );

    // Update on initialization
    if (energyValueDisplay) {
      energyValueDisplay.textContent = dynamicEnergySlider.value;
    }

    // Event listener for slider movement
    dynamicEnergySlider.addEventListener("input", function () {
      const newEnergyLevel = parseInt(this.value);

      // Update display
      if (energyValueDisplay) {
        energyValueDisplay.textContent = newEnergyLevel;
      }

      // Synchronize the main slider
      if (energyLevelControl && !isUpdatingSlider) {
        isUpdatingSlider = true;
        energyLevelControl.value = newEnergyLevel; // This updates the slider's position
        if (networkEnergyValue) {
          networkEnergyValue.textContent = `${newEnergyLevel}%`;
        }
        isUpdatingSlider = false;
      }

      // Update global variable
      currentEnergyLevel = newEnergyLevel;

      // Update network visualization
      if (typeof updateDynamicNetwork === "function") {
        updateDynamicNetwork(newEnergyLevel);
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

// Energy Charts Animation with Waveform
function initEnergyCharts() {
  console.log("Initializing Energy Charts");

  // Select elements
  const energyWaveCanvas = document.getElementById("energyWave");
  const honeypotWaveCanvas = document.getElementById("honeypotWave");
  const energyLevelControl = document.getElementById("mainEnergyLevelControl");
  const energyLevelDisplay = document.getElementById("energyLevelDisplay");
  const autoFluctuateControl = document.getElementById("autoFluctuateControl");
  const focusRadarCanvas = document.getElementById("focusRadar");

  // Debug output to check if elements were found
  console.log("Canvas elements:", {
    energyWaveCanvas,
    honeypotWaveCanvas,
    energyLevelDisplay,
    focusRadarCanvas,
  });

  // Check if elements exist
  if (!energyWaveCanvas || !honeypotWaveCanvas) {
    console.error("Canvas elements for wave animation not found!");
    return;
  }

  // Canvas contexts for drawing waveforms
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
      console.error("Canvas context could not be initialized");
      return;
    }

    console.log("Canvas contexts initialized successfully");
  } catch (error) {
    console.error("Error initializing canvas contexts:", error);
    return;
  }

  // Animation parameters
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
      phase: Math.PI, // 180° Phasenverschiebung (PI) im Vergleich zur Energiewelle
      speed: 0.05, // Gleiche Geschwindigkeit wie Energiewelle
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
    // Hole aktuelle Werte
    const energyLevel = currentEnergyLevel;

    // Berechne Honeypot-Intensität basierend auf dem Energielevel
    // Je niedriger die Energie, desto intensiver die Honeypot-Suche
    const honeypotIntensity = Math.max(5, Math.round(100 - energyLevel * 1.2));

    // Energielevel-Anzeige aktualisieren
    const energyLevelDisplay = document.getElementById("energyLevelDisplay");
    if (energyLevelDisplay) {
      energyLevelDisplay.textContent = energyLevel + "%";

      // Klassen für Styling entfernen und basierend auf dem Wert neu setzen
      energyLevelDisplay.classList.remove("low", "medium", "high");
      if (energyLevel < 40) {
        energyLevelDisplay.classList.add("low");
      } else if (energyLevel < 70) {
        energyLevelDisplay.classList.add("medium");
      } else {
        energyLevelDisplay.classList.add("high");
      }
    }

    // Honeypot-Intensitätsanzeige aktualisieren
    const honeypotIntensityDisplay = document.getElementById(
      "honeypotIntensityDisplay"
    );
    if (honeypotIntensityDisplay) {
      honeypotIntensityDisplay.textContent = honeypotIntensity + "%";
    }

    // Aktualisiere Slider-Positionen
    const mainEnergySlider = document.getElementById("mainEnergyLevelControl");
    if (mainEnergySlider) {
      mainEnergySlider.value = energyLevel;
    }

    const networkEnergySlider = document.getElementById(
      "networkEnergyLevelControl"
    );
    if (networkEnergySlider) {
      networkEnergySlider.value = energyLevel;
    }

    // Aktualisiere auch den dynamischen Energieschieberegler in der Simulationssektion
    const dynamicEnergySlider = document.getElementById(
      "dynamic-energy-slider"
    );
    if (dynamicEnergySlider) {
      dynamicEnergySlider.value = energyLevel;

      // Aktualisiere auch die entsprechende Anzeige
      const energyValue = document.getElementById("energy-value");
      if (energyValue) {
        energyValue.textContent = energyLevel;
      }
    }

    // Network Energy Value aktualisieren
    const networkEnergyValue = document.getElementById("networkEnergyValue");
    if (networkEnergyValue) {
      networkEnergyValue.textContent = energyLevel + "%";

      // Klassen für Styling entfernen und basierend auf dem Wert neu setzen
      networkEnergyValue.classList.remove("low", "medium", "high");
      if (energyLevel < 40) {
        networkEnergyValue.classList.add("low");
      } else if (energyLevel < 70) {
        networkEnergyValue.classList.add("medium");
      } else {
        networkEnergyValue.classList.add("high");
      }
    }

    // Wellen-Amplitude basierend auf Energielevel und Suchintensität anpassen
    if (typeof waveParams !== "undefined") {
      waveParams.energy.amplitude = 10 + (energyLevel / 100) * 20;
      waveParams.honeypot.amplitude = 5 + (honeypotIntensity / 100) * 25;
    }

    // Fokus-Radar aktualisieren, wenn vorhanden
    if (
      typeof radarCtx !== "undefined" &&
      typeof focusRadarCanvas !== "undefined" &&
      typeof frameCounter !== "undefined"
    ) {
      // Nur alle 10 Frames die Kontexte aktualisieren (Verlangsamung auf 1/10)
      const shouldUpdatePositions = frameCounter % 10 === 0;

      if (typeof drawFocusRadar === "function") {
        drawFocusRadar(
          radarCtx,
          energyLevel,
          honeypotIntensity,
          shouldUpdatePositions
        );
      }
    }

    return {
      energyLevel,
      honeypotIntensity,
    };
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
        `Energy Level: ${Math.round(energyValue)}%`,
        width / 2,
        barY - 5
      );
    } catch (error) {
      console.error("Error drawing Focus Radar:", error);
    }
  }

  // Function to animate waves
  function animateWaves() {
    try {
      // Increment frame counter
      frameCounter++;

      // Update canvas dimensions
      const energyWidth = energyWaveCanvas.offsetWidth || 600;
      const energyHeight = energyWaveCanvas.offsetHeight || 100;
      const honeypotWidth = honeypotWaveCanvas.offsetWidth || 600;
      const honeypotHeight = honeypotWaveCanvas.offsetHeight || 100;

      // Set canvas sizes
      energyWaveCanvas.width = energyWidth;
      energyWaveCanvas.height = energyHeight;
      honeypotWaveCanvas.width = honeypotWidth;
      honeypotWaveCanvas.height = honeypotHeight;

      // Update radar canvas size if present
      if (focusRadarCanvas) {
        focusRadarCanvas.width = focusRadarCanvas.offsetWidth || 500;
        focusRadarCanvas.height = focusRadarCanvas.offsetHeight || 300;
      }

      // Draw energy wave
      drawWave(
        energyCtx,
        waveParams.energy,
        energyValue,
        energyWaveCanvas.width,
        energyWaveCanvas.height
      );

      // Calculate honeypot search intensity
      let searchIntensity;
      if (energyValue < 40) {
        searchIntensity = 80 - energyValue; // Higher intensity at lower energy
      } else {
        searchIntensity = 10 + (70 - energyValue) / 3; // Lower base value at higher energy
      }
      searchIntensity = Math.max(5, Math.min(80, searchIntensity));

      // Draw honeypot wave
      drawWave(
        honeypotCtx,
        waveParams.honeypot,
        searchIntensity,
        honeypotWaveCanvas.width,
        honeypotWaveCanvas.height
      );

      // Update Focus Radar if present
      if (radarCtx && focusRadarCanvas) {
        // Only update contexts every 10 frames (slow down to 1/10th)
        const shouldUpdatePositions = frameCounter % 10 === 0;
        drawFocusRadar(
          radarCtx,
          energyValue,
          searchIntensity,
          shouldUpdatePositions
        );
      }

      // Continue animation
      animationFrameId = requestAnimationFrame(animateWaves);
    } catch (error) {
      console.error("Error in wave animation:", error);
    }
  }

  // Start automatic fluctuation
  function startAutoFluctuate() {
    if (autoFluctuateInterval) clearInterval(autoFluctuateInterval);

    isAutoFluctuate = true;

    autoFluctuateInterval = setInterval(() => {
      // Occasionally change direction randomly
      if (Math.random() < 0.3) {
        direction *= -1;
      }

      // Update energy with small random changes
      energyValue += direction * (Math.random() * 2);

      // Keep within bounds
      if (energyValue > 90) {
        energyValue = 90;
        direction = -1;
      } else if (energyValue < 30) {
        energyValue = 30;
        direction = 1;
      }

      // Update displays
      updateDisplays();
    }, 1000); // More frequent updates for better visibility of changes
  }

  // Stop automatic fluctuation
  function stopAutoFluctuate() {
    clearInterval(autoFluctuateInterval);
    isAutoFluctuate = false;
  }

  // If energy slider is present, add event listeners
  if (energyLevelControl) {
    // On interaction start
    energyLevelControl.addEventListener("mousedown", function () {
      this.classList.add("user-adjusting");
      // Stop automatic fluctuation
      stopAutoFluctuate();

      // Disable checkbox
      if (autoFluctuateControl) {
        autoFluctuateControl.checked = false;
      }
    });

    // For touch devices
    energyLevelControl.addEventListener("touchstart", function () {
      this.classList.add("user-adjusting");
      stopAutoFluctuate();

      if (autoFluctuateControl) {
        autoFluctuateControl.checked = false;
      }
    });

    // On value change
    energyLevelControl.addEventListener("input", function () {
      const newEnergyLevel = parseFloat(this.value);
      energyValue = newEnergyLevel; // Update current energy value
      updateDisplays();
    });

    // After interaction ends
    energyLevelControl.addEventListener("mouseup", function () {
      this.classList.remove("user-adjusting");
    });

    // For touch devices
    energyLevelControl.addEventListener("touchend", function () {
      this.classList.remove("user-adjusting");
    });
  }

  // If auto-fluctuation checkbox is present, add event listener
  if (autoFluctuateControl) {
    // This event listener is already set in DOMContentLoaded,
    // so here just check if checkbox is active
    if (autoFluctuateControl.checked) {
      startAutoFluctuate(); // Start auto-fluctuation
    } else {
      stopAutoFluctuate();
    }
  }

  // Handle window resize
  window.addEventListener("resize", () => {
    // Briefly stop and restart animation for correct canvas size
    cancelAnimationFrame(animationFrameId);
    console.log(
      "Window resize detected, canvas sizes will be recalculated"
    );
    animateWaves();
  });

  // Initially update displays
  updateDisplays();

  // Start animation
  console.log("Starting wave animation...");
  animateWaves();

  // Connect the updateFocusNetwork function to the dynamic energy slider
  const networkEnergySlider = document.getElementById(
    "networkEnergyLevelControl"
  );
  if (networkEnergySlider) {
    networkEnergySlider.addEventListener("input", function () {
      if (isUpdatingSlider) return; // Wenn bereits ein Update läuft, abbrechen

      isUpdatingSlider = true; // Flag setzen
      const newValue = parseInt(this.value);

      // Globale Variable aktualisieren
      currentEnergyLevel = newValue;

      // Aktualisiere auch den Haupt-Energieschieberegler
      const mainEnergySlider = document.getElementById(
        "mainEnergyLevelControl"
      );
      if (mainEnergySlider) {
        mainEnergySlider.value = newValue;

        // Aktualisiere die Anzeige des Energiewertes für den Hauptschieberegler
        const energyValueDisplay =
          document.getElementById("energyLevelDisplay");
        if (energyValueDisplay) {
          energyValueDisplay.textContent = newValue + "%";
        }
      }

      // Aktualisiere die Netzwerkanzeige des Energiewertes
      const networkEnergyValue = document.getElementById("networkEnergyValue");
      if (networkEnergyValue) {
        networkEnergyValue.textContent = newValue + "%";

        // Energieklasse aktualisieren (für farbliche Markierung)
        networkEnergyValue.className = "";
        if (newValue < 40) {
          networkEnergyValue.classList.add("low");
        } else if (newValue < 70) {
          networkEnergyValue.classList.add("medium");
        } else {
          networkEnergyValue.classList.add("high");
        }
      }

      // Aktualisiere auch den dynamischen Energieschieberegler in der Simulationssektion
      const dynamicEnergySlider = document.getElementById(
        "dynamic-energy-slider"
      );
      if (dynamicEnergySlider) {
        dynamicEnergySlider.value = newValue;

        // Aktualisiere auch die entsprechende Anzeige
        const energyValue = document.getElementById("energy-value");
        if (energyValue) {
          energyValue.textContent = newValue;
        }
      }

      // Aktualisiere die Netzwerke mit dem neuen Energielevel
      if (window.updateFocusNetwork) {
        window.updateFocusNetwork(newValue);
      }

      // Aktualisiere auch das dynamische Netzwerk, falls die Funktion existiert
      if (typeof updateDynamicNetwork === "function") {
        updateDynamicNetwork(newValue);
      }

      isUpdatingSlider = false; // Flag zurücksetzen
    });
  }

  // Auch den Haupt-Energieschieberegler mit der Fokus-Funktion verbinden
  const mainEnergySlider = document.getElementById("mainEnergyLevelControl");
  if (mainEnergySlider) {
    mainEnergySlider.addEventListener("input", function () {
      if (isUpdatingSlider) return; // Wenn bereits ein Update läuft, abbrechen

      isUpdatingSlider = true; // Flag setzen
      const newValue = parseInt(this.value);

      // Globale Variable aktualisieren
      currentEnergyLevel = newValue;

      // Aktualisiere auch den dynamischen Energieschieberegler
      const networkEnergySlider = document.getElementById(
        "networkEnergyLevelControl"
      );
      if (networkEnergySlider) {
        networkEnergySlider.value = newValue;
      }

      // Aktualisiere auch den dynamischen Energieschieberegler in der Simulationssektion
      const dynamicEnergySlider = document.getElementById(
        "dynamic-energy-slider"
      );
      if (dynamicEnergySlider) {
        dynamicEnergySlider.value = newValue;

        // Aktualisiere auch die entsprechende Anzeige
        const energyValue = document.getElementById("energy-value");
        if (energyValue) {
          energyValue.textContent = newValue;
        }
      }

      // Aktualisiere die Anzeige des Energiewertes für den Hauptschieberegler
      const energyValueDisplay = document.getElementById("energyLevelDisplay");
      if (energyValueDisplay) {
        energyValueDisplay.textContent = newValue + "%";
      }

      // Aktualisiere die Netzwerke mit dem neuen Energielevel
      if (window.updateFocusNetwork) {
        window.updateFocusNetwork(newValue);
      }

      // Aktualisiere auch das dynamische Netzwerk, falls die Funktion existiert
      if (typeof updateDynamicNetwork === "function") {
        updateDynamicNetwork(newValue);
      }

      isUpdatingSlider = false; // Flag zurücksetzen
    });
  }

  // Auch den dritten Energieschieberegler in der Simulationssektion verbinden
  const dynamicEnergySlider = document.getElementById("dynamic-energy-slider");
  if (dynamicEnergySlider) {
    dynamicEnergySlider.addEventListener("input", function () {
      if (isUpdatingSlider) return; // Wenn bereits ein Update läuft, abbrechen

      isUpdatingSlider = true; // Flag setzen
      const newValue = parseInt(this.value);

      // Globale Variable aktualisieren
      currentEnergyLevel = newValue;

      // Aktualisiere die Anzeige des Energiewerts
      const energyValue = document.getElementById("energy-value");
      if (energyValue) {
        energyValue.textContent = newValue;
      }

      // Aktualisiere auch den Haupt-Energieschieberegler
      const mainEnergySlider = document.getElementById(
        "mainEnergyLevelControl"
      );
      if (mainEnergySlider) {
        mainEnergySlider.value = newValue;

        // Aktualisiere die Anzeige des Energiewertes für den Hauptschieberegler
        const energyValueDisplay =
          document.getElementById("energyLevelDisplay");
        if (energyValueDisplay) {
          energyValueDisplay.textContent = newValue + "%";
        }
      }

      // Aktualisiere auch den Netzwerk-Energieschieberegler
      const networkEnergySlider = document.getElementById(
        "networkEnergyLevelControl"
      );
      if (networkEnergySlider) {
        networkEnergySlider.value = newValue;

        // Aktualisiere die Anzeige des Energiewertes für den Netzwerk-Schieberegler
        const networkEnergyValue =
          document.getElementById("networkEnergyValue");
        if (networkEnergyValue) {
          networkEnergyValue.textContent = newValue + "%";

          // Energieklasse aktualisieren (für farbliche Markierung)
          networkEnergyValue.className = "";
          if (newValue < 40) {
            networkEnergyValue.classList.add("low");
          } else if (newValue < 70) {
            networkEnergyValue.classList.add("medium");
          } else {
            networkEnergyValue.classList.add("high");
          }
        }
      }

      // Aktualisiere die Netzwerke mit dem neuen Energielevel
      if (window.updateFocusNetwork) {
        window.updateFocusNetwork(newValue);
      }

      // Aktualisiere auch das dynamische Netzwerk, falls die Funktion existiert
      if (typeof updateDynamicNetwork === "function") {
        updateDynamicNetwork(newValue);
      }

      isUpdatingSlider = false; // Flag zurücksetzen
    });
  }
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

// Function to initialize the Focus Network
function initFocusNetwork() {
  console.log("Initializing Focus Network with semantic sentences");

  // Check for valid container
  const container = document.getElementById("focusNetwork");
  if (!container) {
    console.error("Container #focusNetwork not found!");
    // Add fallback content if visualization cannot be loaded
    container.innerHTML = `
      <div class="fallback-content">
        <div class="fallback-icon"><i class="fas fa-project-diagram"></i></div>
        <h3>Network Visualization</h3>
        <p>The visualization could not be loaded. Please refresh the page.</p>
      </div>
    `;
    return;
  }

  // Check D3.js availability
  if (!window.d3) {
    console.error("D3.js is not available!");
    container.innerHTML = `
      <div class="fallback-content">
        <div class="fallback-icon"><i class="fas fa-exclamation-triangle"></i></div>
        <h3>D3.js Missing</h3>
        <p>The required D3.js library was not loaded.</p>
      </div>
    `;
    return;
  } else {
    console.log("D3.js Version:", d3.version);
  }

  console.log("Container found:", container);

  // Set size to a reasonable value
  const width = Math.max(container.clientWidth, 300);
  const height = Math.max(container.clientHeight, 300);

  console.log("Container size:", width, "x", height);

  // Remove existing SVG elements, if any
  d3.select(container).selectAll("svg").remove();
  console.log("Existing SVG elements removed");

  try {
    // Create SVG element
    const svg = d3
      .select(container)
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto;");

    // Main group for zooming and panning
    const g = svg.append("g");

    // Add zoom behavior
    const zoom = d3
      .zoom()
      .scaleExtent([0.1, 4])
      .on("zoom", (event) => {
        g.attr("transform", event.transform);
      });

    // Apply zoom behavior to SVG
    svg.call(zoom);

    // Zoom to center by default
    svg.call(
      zoom.transform,
      d3.zoomIdentity.translate(width / 4, height / 4).scale(0.8)
    );

    // Define semantic sentence nodes
    const nodes = [
      // Key concepts (Translated labels)
      { id: "a_art", group: "article", label: "a" }, // "ein"
      { id: "Apple", group: "object", label: "🍎 Apple" }, // "Apfel"
      { id: "tastes", group: "verb", label: "tastes" }, // "schmeckt"
      { id: "Color", group: "property", label: "Color" }, // "Farbe"
      { id: "red_adj", group: "property", label: "red" }, // "rote"
      { id: "has", group: "verb", label: "has" }, // "hat"
      { id: "I_pron", group: "pronoun", label: "I" }, // "ich"
      { id: "me_pron", group: "pronoun", label: "me" }, // "mir"
      { id: "what_pron", group: "pronoun", label: "what" }, // "was"
      { id: "eat_act", group: "action", label: "eat" }, // "esse"
      { id: "delicious_adj", group: "property", label: "delicious" }, // "lecker"
      { id: "an_art", group: "article", label: "an" }, // "eine" - using "an" as "a" is already used. Or consider "one" if it means number.

      // Category and Honeypot (Translated labels)
      { id: "Food_cat", group: "category", label: "🍽️ Food" }, // "Essen"
      { id: "BasicNeed_hp", group: "honeypot", label: "🍯 Basic Need" }, // "Grundbedürfnis"
    ];

    // Object to track node sizes
    const nodeRadii = {};
    nodes.forEach((node) => {
      if (node.group === "honeypot") nodeRadii[node.id] = 30;
      else if (node.group === "category") nodeRadii[node.id] = 25;
      else if (node.group === "sentence") nodeRadii[node.id] = 20;
      else nodeRadii[node.id] = 15;
    });

    const links = [
      // Connections between words and sentences (using new translated IDs)
      { source: "a_art", target: "Apple", value: 2, type: "part_of" },
      {
        source: "Apple",
        target: "tastes",
        value: 2,
        type: "part_of",
      },
      {
        source: "tastes",
        target: "delicious_adj",
        value: 2,
        type: "part_of",
      },

      {
        source: "Apple",
        target: "has",
        value: 2,
        type: "part_of",
      },
      {
        source: "has",
        target: "an_art", // Assuming "eine" translates to "an" or "a" depending on context
        value: 2,
        type: "part_of",
      },
      {
        source: "an_art",
        target: "red_adj",
        value: 2,
        type: "part_of",
      },
      {
        source: "red_adj",
        target: "Color",
        value: 2,
        type: "part_of",
      },

      {
        source: "me_pron",
        target: "tastes",
        value: 2,
        type: "part_of",
      },
      {
        source: "tastes",
        target: "Apple", // "schmeckt Apfel" -> "tastes Apple"
        value: 2,
        type: "part_of",
      },

      {
        source: "I_pron",
        target: "eat_act",
        value: 2,
        type: "part_of",
      },
      {
        source: "eat_act",
        target: "what_pron",
        value: 2,
        type: "part_of",
      },
      {
        source: "what_pron",
        target: "me_pron",
        value: 2,
        type: "part_of",
      },
      // This connection "mir schmeckt" is already covered by "me_pron" -> "tastes"
      // {
      //   source: "me_pron",
      //   target: "tastes",
      //   value: 2,
      //   type: "part_of",
      // },

      // Connections to Food and Honeypot
      { source: "eat_act", target: "Food_cat", value: 3, type: "category" },
      // { source: "Apple", target: "Food_cat", value: 2, type: "category" }, // Example, if Apple is food
      { source: "Food_cat", target: "BasicNeed_hp", value: 4, type: "honeypot" },
    ];

    // Create force simulation
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
        "Mouse: Drag to pan, Wheel to zoom, Shift+Wheel for node size"
      );

    // Start simulation and update on each tick
    simulation.on("tick", () => {
      link
        .attr("x1", (d) => d.source.x)
        .attr("y1", (d) => d.source.y)
        .attr("x2", (d) => d.target.x)
        .attr("y2", (d) => d.target.y);

      node.attr("transform", (d) => {
        // Restrict position to visible area
        d.x = Math.max(20, Math.min(width - 20, d.x));
        d.y = Math.max(20, Math.min(height - 20, d.y));
        return `translate(${d.x}, ${d.y})`;
      });
    });

    // Store references for later use
    networkData = {
      simulation: simulation,
      nodes: nodes,
      links: links,
      nodeElements: node,
      linkElements: link,
      svg: svg,
      container: container,
    };

    // New function: Updates the focus network based on energy level
    window.updateFocusNetwork = function (energyLevel) {
      console.log("Updating Focus Network with energy level:", energyLevel);

      // Remove all previous focus markings
      node.classed("focus", false);
      link.classed("focus", false);

      // Identify existing sentence groups in the network
      // A sentence consists of several connected words (using new translated IDs)
      const sentences = [
        // Sentence 1: "a Apple tastes delicious"
        ["a_art", "Apple", "tastes", "delicious_adj"],
        // Sentence 2: "a Apple has an red Color" (or "a Apple has a red color")
        ["a_art", "Apple", "has", "an_art", "red_adj", "Color"],
        // Sentence 3: "I eat what"
        ["I_pron", "eat_act", "what_pron"],
        // Sentence 4: "me tastes a Apple" (grammatically a bit off, but reflects original structure)
        ["me_pron", "tastes", "a_art", "Apple"],
      ];

      // Identify honeypot node
      const honeypotNode = nodes.find((n) => n.group === "honeypot");
      if (!honeypotNode) {
        console.error("No honeypot node found!");
        return;
      }

      // Priority for sentences based on their "distance" to the honeypot
      // This is a simplified logic, as we don't calculate actual graph distance
      const sentencePriorities = [
        { sentence: sentences[0], priority: 2 }, // Contains "Apple", linked to Food
        { sentence: sentences[1], priority: 3 }, // Describes properties
        { sentence: sentences[2], priority: 1 }, // Direct relation to eating
        { sentence: sentences[3], priority: 2 }, // Contains "Apple"
      ];

      // Sort sentences by priority (lower number = closer to honeypot/more important)
      const sortedSentences = sentencePriorities.sort(
        (a, b) => a.priority - b.priority
      );

      // Select sentence based on energy level
      let selectedSentence;

      if (energyLevel < 40) {
        // At low energy level: focus on sentence near honeypot (highest priority)
        selectedSentence = sortedSentences[0].sentence;
        console.log(
          "Low energy level, focus on sentence with highest priority"
        );
      } else if (energyLevel < 70) {
        // At medium energy level: focus on sentence with medium priority
        const middleIndex = Math.min(1, sortedSentences.length - 1);
        selectedSentence = sortedSentences[middleIndex].sentence;
        console.log(
          "Medium energy level, focus on sentence with medium priority"
        );
      } else {
        // At high energy level: focus on sentence far from honeypot (lowest priority)
        selectedSentence = sortedSentences[sortedSentences.length - 1].sentence;
        console.log(
          "High energy level, focus on sentence with lowest priority"
        );
      }

      // Mark all nodes in the selected sentence as focused
      node
        .filter((d) => selectedSentence.includes(d.id))
        .classed("focus", true);

      // Mark all connections between words in the sentence
      link
        .filter((l) => {
          return (
            selectedSentence.includes(l.source.id) &&
            selectedSentence.includes(l.target.id)
          );
        })
        .classed("focus", true);

      // Find a representative node for displaying sentence information
      const mainNode =
        nodes.find((n) => n.id === selectedSentence[0]) || nodes[0];

      // If an information panel exists, update it
      const infoPanel = document.getElementById("contextInfo");
      if (infoPanel) {
        // Create a human-readable sentence version by concatenating words
        const readableSentence = selectedSentence
          .map((wordId) => {
            const node = nodes.find((n) => n.id === wordId);
            // Remove emoji/icon prefix for readable sentence
            return node ? (node.label.includes(" ") ? node.label.split(" ")[1] : node.label) : wordId;
          })
          .join(" ")
          .replace(/\s([,.!?])/g, "$1"); // Remove spaces before punctuation

        infoPanel.innerHTML = `
          <div class="context-details">
            <div class="context-header">
              <div class="context-emoji">📝</div>
              <h4>Focused Sentence</h4>
              <span class="context-type sentence">Sentence</span>
            </div>
            <div class="context-body">
              <p><strong>"${readableSentence}"</strong></p>
              <p>Focused due to current energy level of <span class="energy-value ${
                energyLevel < 40 ? "low" : energyLevel < 70 ? "medium" : "high"
              }">${energyLevel}%</span></p>
              <div class="context-energy">
                <strong>Distance to Honeypot:</strong>
                ${
                  sortedSentences.findIndex(
                    (s) => s.sentence === selectedSentence
                  ) === 0
                    ? "Low (high priority)"
                    : sortedSentences.findIndex(
                        (s) => s.sentence === selectedSentence
                      ) ===
                      sortedSentences.length - 1
                    ? "High (low priority)"
                    : "Medium"
                }
              </div>
            </div>
          </div>
        `;
      }
    };

    // Set initial focus based on current energy level
    if (typeof currentEnergyLevel !== "undefined") {
      window.updateFocusNetwork(currentEnergyLevel);
    } else {
      // Default value if global variable is not defined
      window.updateFocusNetwork(50);
    }

    // Display user help information in the info panel
    const infoPanel = document.getElementById("contextInfo");
    if (infoPanel) {
      infoPanel.innerHTML = `
        <div class="network-help">
          <h3>Interactive Network</h3>
          <p>• Drag with the mouse to pan the entire network</p>
          <p>• Mouse wheel to zoom the network</p>
          <p>• Drag nodes to move them</p>
          <p>• Click nodes for details</p>
          <p>• Shift + Mouse wheel to change node size</p>
        </div>
      `;
    }

    console.log("Focus Network initialized successfully");
  } catch (error) {
    console.error("Error initializing Focus Network:", error);
    container.innerHTML = `
      <div class="fallback-content">
        <div class="fallback-icon"><i class="fas fa-bug"></i></div>
        <h3>Visualization Failed</h3>
        <p>Error: ${error.message}</p>
      </div>
    `;
  }
}

// Drag functions for interactive nodes
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

// Helper function to determine connection type name
function getConnectionTypeName(type) {
  switch (type) {
    case "part_of":
      return "Part of";
    case "semantic":
      return "Semantic Connection";
    case "category":
      return "Categorization";
    case "honeypot":
      return "Basic Need";
    case "color":
      return "Color Property";
    case "taste":
      return "Taste Property";
    case "property":
      return "Property";
    default:
      return type;
  }
}

// Function to generate network data (using translated node IDs and labels)
function generateNetworkData() {
  console.log("Generating network data...");

  // Define nodes
  const nodes = [
    // Honeypot and Category
    { id: "BasicNeed_hp", group: "honeypot", label: "🍯 Basic Need" },
    { id: "Food_cat", group: "category", label: "🍽️ Food" },

    // Words from "I eat what tastes good to me"
    { id: "I_pron", group: "pronoun", label: "I" },
    { id: "eat_act", group: "verb", label: "eat" },
    { id: "what_pron", group: "pronoun", label: "what" },
    { id: "me_pron", group: "pronoun", label: "me" },
    { id: "tastes", group: "verb", label: "tastes" },

    // Words from "An apple tastes delicious"
    { id: "a_art", group: "article", label: "a" }, // Changed from "an_art" to "a_art" for consistency if "ein" is "a"
    { id: "Apple", group: "object", label: "🍎 Apple" },
    { id: "delicious_adj", group: "property", label: "delicious" },

    // Words from "An apple has a red color"
    { id: "has", group: "verb", label: "has" },
    { id: "an_art", group: "article", label: "a" }, // Assuming "eine" as "a" here too for "a red color"
    { id: "red_adj", group: "property", label: "red" },
    { id: "Color", group: "object", label: "🎨 Color" }, // Changed from property to object as "Farbe" was
  ];

  // Define links
  const links = [
    // Connections to Honeypot
    { source: "BasicNeed_hp", target: "Food_cat", value: 3, type: "honeypot" },

    // Sequence 1: "I eat what tastes (good to) me"
    { source: "I_pron", target: "eat_act", value: 1, type: "part_of" },
    { source: "eat_act", target: "what_pron", value: 1, type: "part_of" },
    { source: "what_pron", target: "me_pron", value: 1, type: "part_of" }, // "what to me"
    { source: "me_pron", target: "tastes", value: 1, type: "part_of" }, // "me tastes" (original structure)

    // Sequence 2: "An apple tastes delicious"
    { source: "a_art", target: "Apple", value: 1, type: "part_of" },
    { source: "Apple", target: "tastes", value: 1, type: "part_of" },
    { source: "tastes", target: "delicious_adj", value: 1, type: "part_of" },

    // Sequence 3: "An apple has a red color"
    // { source: "a_art", target: "Apple", value: 1, type: "part_of" }, // Already defined
    { source: "Apple", target: "has", value: 1, type: "part_of" },
    { source: "has", target: "an_art", value: 1, type: "part_of" }, // "has a"
    { source: "an_art", target: "red_adj", value: 1, type: "part_of" }, // "a red"
    { source: "red_adj", target: "Color", value: 1, type: "part_of" }, // "red color"

    // Connections to Category
    { source: "Apple", target: "Food_cat", value: 2, type: "category" },
    { source: "eat_act", target: "Food_cat", value: 2, type: "category"} // Added: eat -> Food
  ];

  // Set node positions
  nodes.forEach((node, i) => {
    if (node.id === "BasicNeed_hp") { node.x = 400; node.y = 50; }
    else if (node.id === "Food_cat") { node.x = 400; node.y = 150; }
    else if (["I_pron", "eat_act", "what_pron", "me_pron", "tastes"].includes(node.id)) {
      node.x = 150 + ["I_pron", "eat_act", "what_pron", "me_pron", "tastes"].indexOf(node.id) * 100;
      node.y = 250;
    }
    else if (["a_art", "Apple", "delicious_adj"].includes(node.id)) {
      node.x = 250 + ["a_art", "Apple", "delicious_adj"].indexOf(node.id) * 120;
      node.y = 350;
    }
    else if (["has", "an_art", "red_adj", "Color"].includes(node.id)) {
      node.x = 200 + ["has", "an_art", "red_adj", "Color"].indexOf(node.id) * 100;
      node.y = 450;
    }
  });


  return { nodes, links };
}

// Function to update the network
function updateNetwork() {
  // Check for valid container
  const container = document.getElementById("focusNetwork");
  if (!container) return;

  // Check existing SVG elements, create if not present
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

    // Define markers for arrowheads
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

    // Groups for links and nodes
    networkSvg.append("g").attr("class", "links");
    networkSvg.append("g").attr("class", "nodes");

    // Create simulation data
    networkData = generateNetworkData();

    // Create links
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

    // Create node groups
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

    // Circles for nodes
    nodeGroups
      .append("circle")
      .attr("r", (d) => {
        if (d.group === "fruit" || d.group === "object") return 30; // Adjusted for "Apple"
        if (d.group === "property") return 25;
        if (d.group === "color") return 20;
        if (d.group === "taste") return 20;
        return 15;
      })
      .attr("fill", (d) => {
        if (d.group === "fruit" || d.group === "object") return "#3b82f6"; // Blue for fruits/objects
        if (d.group === "property") return "#22c55e"; // Green for properties
        if (d.group === "color") return "#f97316"; // Orange for colors
        if (d.group === "taste") return "#f97316"; // Orange for taste
        return "#a855f7"; // Purple for others
      })
      .attr("stroke", "#fff")
      .attr("stroke-width", 1.5)
      .on("click", handleNodeClick);

    // Labels for nodes
    nodeGroups
      .append("text")
      .text((d) => d.label)
      .attr("x", 0)
      .attr("y", (d) => {
        if (d.group === "fruit" || d.group === "object") return 3;
        return 3;
      })
      .attr("text-anchor", "middle")
      .attr("dominant-baseline", "middle")
      .attr("font-size", (d) => {
        if (d.group === "fruit" || d.group === "object") return "12px";
        return "10px";
      })
      .attr("fill", "#fff")
      .attr("pointer-events", "none");

    // Create simulation
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

    // Initially position nodes at defined positions
    networkData.nodes.forEach((node) => {
      if (node.x && node.y) {
        node.fx = node.x;
        node.fy = node.y;
      }
    });

    // After a short delay, release fixed positions so nodes can move
    setTimeout(() => {
      networkData.nodes.forEach((node) => {
        node.fx = null;
        node.fy = null;
      });
      simulation.alpha(0.3).restart();
    }, 2000);

    // Tick function for simulation
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

    // Display help text
    const expandHint = document.createElement("div");
    expandHint.className = "expand-hint";
    expandHint.innerHTML =
      "<i class='fas fa-info-circle'></i> Click on a node to view details";
    container.appendChild(expandHint);

    nodeElements = nodeGroups;
  }
}

// Function to initialize dynamic network visualization
function initDynamicNetwork() {
  console.log(
    "Initializing dynamic network with simplified implementation"
  );

  // Check for valid container
  const container = document.getElementById("dynamic-network");
  if (!container) {
    console.error("Container #dynamic-network not found!");
    return;
  }

  console.log("Container found:", container);
  console.log(
    "Container size:",
    container.clientWidth,
    "x",
    container.clientHeight
  );

  // Set size to a reasonable value if too small
  const width = container.clientWidth || 600;
  const height = container.clientHeight || 400;

  if (width < 100 || height < 100) {
    console.warn("Container size is too small:", width, "x", height);
    console.warn("Using default size: 600 x 400");
  }

  try {
    // Remove existing SVG elements, if any
    d3.select(container).selectAll("svg").remove();
    console.log("Existing SVG elements removed");

    // Create SVG element
    const svg = d3
      .select(container)
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: 100%;");

    // Main group for zooming and panning
    const g = svg.append("g");

    // Add zoom behavior
    const zoom = d3
      .zoom()
      .scaleExtent([0.1, 4])
      .on("zoom", (event) => {
        g.attr("transform", event.transform);
      });

    // Apply zoom behavior to SVG
    svg.call(zoom);

    // Zoom to center by default
    svg.call(
      zoom.transform,
      d3.zoomIdentity.translate(width / 4, height / 4).scale(0.8)
    );

    console.log("SVG element created:", svg.node());

    // Simple test data - just a few honeypots and contexts
    const nodes = [
      {
        id: "honeypot1",
        type: "honeypot",
        label: "Food", // Translated from "Essen"
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
        label: "Nourishment", // Translated from "Nahrung"
        x: width / 2 + 120,
        y: height / 2 - 80,
      },
      {
        id: "context3",
        type: "related",
        label: "Cooking", // Translated from "Kochen"
        x: width / 2 - 80,
        y: height / 2 + 100,
      },
      {
        id: "context4",
        type: "related",
        label: "Health", // Translated from "Gesundheit"
        x: width / 2 + 80,
        y: height / 2 + 100,
      },
      {
        id: "context5",
        type: "distant",
        label: "Culture", // Translated from "Kultur"
        x: width / 2 - 200,
        y: height / 2 + 20,
      },
    ];

    // Object to track node sizes
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

    // Create force simulation for interactive movement
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

    // Create links
    const link = g
      .append("g")
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("class", (d) => `dynamic-link ${d.type}`);

    // Create nodes
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

    // Circles for nodes
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

    // Labels for nodes
    node
      .append("text")
      .attr("text-anchor", "middle")
      .attr("dy", (d) => (d.type === "honeypot" ? 35 : 25))
      .text((d) => d.label)
      .attr("font-size", (d) => (d.type === "honeypot" ? 12 : 10))
      .attr("font-weight", "bold")
      .attr("fill", "#333")
      .attr("pointer-events", "none");

    console.log("Dynamic network created");

    // Mark a node as focused
    svg
      .selectAll(".dynamic-node")
      .filter((d, i) => i === 1)
      .classed("focused", true);

    // Mark corresponding links as focused
    svg
      .selectAll(".dynamic-link")
      .filter((d, i) => i === 0)
      .classed("focused", true);

    // Set initial focus based on current energy level
    updateDynamicNetwork(currentEnergyLevel);
  } catch (error) {
    console.error("Error creating dynamic network:", error);
  }
}

// New function: Updates the dynamic network based on energy level
function updateDynamicNetwork(energyLevel) {
  console.log(
    "Updating dynamic network with energy level:",
    energyLevel
  );

  // Check if dynamic network is initialized
  if (!dynamicNodes || !dynamicSvg) {
    console.warn("Dynamic network is not yet initialized!");
    return;
  }

  // Try to find all nodes and sort them by distance to honeypot
  // (assuming a node of type "honeypot" exists)
  const allNodes = dynamicNodes.data();

  // Find the honeypot node
  const honeypotNode = allNodes.find((node) => node.type === "honeypot");
  if (!honeypotNode) {
    console.error("No honeypot node found!");
    return;
  }

  // Sort all nodes by distance to honeypot (excluding honeypot itself)
  // Assumption: Higher index means further from honeypot
  // (This is a simplification; a real implementation would likely use path lengths or other metrics)
  const sortedNodes = allNodes
    .filter((node) => node.type !== "honeypot") // Exclude honeypot itself
    .sort((a, b) => {
      // Sort by type (essential closer, distant further away)
      const typeOrder = { essential: 1, related: 2, default: 3 };
      const aOrder = typeOrder[a.type] || typeOrder.default;
      const bOrder = typeOrder[b.type] || typeOrder.default;
      return aOrder - bOrder;
    });

  if (sortedNodes.length === 0) {
    console.warn("No nodes found to focus!");
    return;
  }

  // Select node based on energy level
  let newFocusNode;

  if (energyLevel < 40) {
    // At low energy level: node near honeypot (start of list)
    newFocusNode = sortedNodes[0];
    console.log(
      "Low energy level, focus on node near honeypot:",
      newFocusNode.label
    );
  } else if (energyLevel < 70) {
    // At medium energy level: node in the middle
    const middleIndex = Math.floor(sortedNodes.length / 2);
    newFocusNode = sortedNodes[middleIndex];
    console.log(
      "Medium energy level, focus on node at medium distance:",
      newFocusNode.label
    );
  } else {
    // At high energy level: node far from honeypot (end of list)
    newFocusNode = sortedNodes[sortedNodes.length - 1];
    console.log(
      "High energy level, focus on node far from honeypot:",
      newFocusNode.label
    );
  }

  // Update current focus node
  currentFocusNode = newFocusNode;

  // Update visualization: Remove focus marking from all nodes
  dynamicSvg
    .selectAll(".node circle")
    .classed("focused", false)
    .attr("stroke-width", 1);

  // Set focus marking on the new focus node with a border
  dynamicSvg
    .selectAll(".node")
    .filter((d) => d === newFocusNode)
    .select("circle")
    .classed("focused", true)
    .attr("stroke", "#ff6b00")
    .attr("stroke-width", 3);

  // Update current focus display
  const focusNodeDisplay = document.getElementById("current-focus-node");
  if (focusNodeDisplay) {
    focusNodeDisplay.textContent = newFocusNode.label;
  }

  // Update honeypot distance display
  const focusDistanceDisplay = document.getElementById("focus-distance");
  if (focusDistanceDisplay) {
    // Use type as text for distance measure
    let distanceText = "unknown";
    if (newFocusNode.type === "essential") {
      distanceText = "low (essential)";
    } else if (newFocusNode.type === "related") {
      distanceText = "medium (related)";
    } else {
      distanceText = "high (distant)";
    }
    focusDistanceDisplay.textContent = distanceText;
  }
}

// This function is called when the page is fully loaded
window.onload = function () {
  console.log("Window.onload event triggered");

  // Direct call to visualization functions as fallback
  if (document.getElementById("focusNetwork")) {
    console.log("Direct call to initFocusNetwork");
    initFocusNetwork();
  }

  if (document.getElementById("dynamic-network")) {
    console.log("Direct call to initDynamicNetwork");
    initDynamicNetwork();
  }
};

// Helper function to generate a context description
function generateContextDescription(node) {
  if (!node)
    return {
      emoji: "❓",
      description: "No node selected",
      connectionType: "Unknown",
    };

  let emoji = "";
  let description = "";
  let connectionType = "";

  switch (node.group) {
    case "fruit":
      emoji = "🍎";
      description = `${node.label} is a fruit with specific properties like color and taste.`;
      connectionType = "Fruit";
      break;
    case "color":
      emoji = "🎨";
      description = `${node.label} is a color that can be assigned to specific objects.`;
      connectionType = "Color";
      break;
    case "taste":
      emoji = "👅";
      description = `${node.label} is a taste perceived from certain fruits or foods.`;
      connectionType = "Taste";
      break;
    case "sentence":
      emoji = "📝";
      description = `"${node.label}" is a complete sentence expressing a thought or relationship between concepts.`;
      connectionType = "Sentence";
      break;
    case "object":
      emoji = "🍎"; // Using apple emoji for generic object for now
      description = `${node.label} is a concrete object in our language model that can have properties and relationships with other concepts.`;
      connectionType = "Object";
      break;
    case "verb":
      emoji = "🏃";
      description = `${node.label} is a verb describing an action or state, connecting subjects with objects.`;
      connectionType = "Verb";
      break;
    case "pronoun":
      emoji = "👤";
      description = `${node.label} is a pronoun referring to a person or entity without naming it directly.`;
      connectionType = "Pronoun";
      break;
    case "property":
      emoji = "🏷️";
      description = `${node.label} is a property that describes objects or concepts in more detail.`;
      connectionType = "Property";
      break;
    case "action":
      emoji = "🔧";
      description = `${node.label} represents a concrete action that a subject can perform.`;
      connectionType = "Action";
      break;
    case "category":
      emoji = "🍽️";
      description = `${node.label} is a category that groups various concepts. It represents a basic need of the consciousness and is linked to a honeypot.`;
      connectionType = "Category";
      break;
    case "honeypot":
      emoji = "🍯";
      description = `${node.label} represents an elementary basic need of the artificial consciousness. Honeypots are central energy sources to which the consciousness returns when energy is low.`;
      connectionType = "Honeypot";
      break;
    default:
      emoji = "❓";
      description = `${node.label} is an unknown context type.`;
      connectionType = "Unknown";
  }

  return {
    emoji,
    description,
    connectionType,
  };
}

// Function to highlight connections of a node
function highlightConnections(node) {
  // Highlight links connected to this node
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

  // Also visually highlight connected nodes
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

// Function to display context information
function showContextInfo(node) {
  // Show info panel
  const infoPanel = document.querySelector(".node-info-panel");
  const contextInfo = document.getElementById("contextInfo");

  if (infoPanel && contextInfo) {
    // Generate context description
    const contextData = generateContextDescription(node);

    // Find connected nodes
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

    // Generate list of connected nodes with their types
    const connectedNodesList = connectedNodes
      .map((conn) => {
        const typeName = getConnectionTypeName(conn.type);
        return `<li><span class="context-type ${conn.node.group}">${conn.node.group}</span> ${conn.node.label} <small>(${typeName})</small></li>`;
      })
      .join("");

    // Create HTML for context information
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
            <strong>Connected Concepts:</strong>
            <ul>
              ${connectedNodesList || "<li>No connected concepts</li>"}
            </ul>
          </div>
        </div>
      </div>
    `;

    // Make info panel visible
    infoPanel.classList.add("visible");
  }
}
