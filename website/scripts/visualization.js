// Network Visualization using D3.js

document.addEventListener("DOMContentLoaded", function () {
  // Globale Variablen initialisieren und an window-Objekt binden
  window.nodes = [];
  window.links = [];
  window.simulation = null;
  window.nodeElements = null;
  window.linkElements = null;
  window.textElements = null;
  window.svg = null;
  window.width = 0;
  window.height = 0;
  window.selectedNode = null;
  window.colorScheme = "category";

  // Define attribute types
  window.attributeTypes = [
    "Taste",     // Geschmack
    "Appearance",// Aussehen
    "Size",      // Größe
    "Function",  // Funktion
    "Age",       // Alter
    "Origin",    // Herkunft
    "Material",  // Material
  ];

  // Color scale
  window.categoryColors = d3.scaleOrdinal(d3.schemeCategory10);

  // Delay to ensure DOM is fully loaded
  setTimeout(() => {
    // Check if overlay exists
    const loadingOverlay = document.querySelector(".loading-overlay");
    if (loadingOverlay) {
      loadingOverlay.style.display = "none";
    }

    // Initialize network if container element is present
    const networkContainer = document.getElementById("network");
    if (networkContainer) {
      try {
        initNetworkVisualization();
        console.log("Network visualization initialized successfully");
      } catch (error) {
        console.error(
          "Error during network visualization initialization:",
          error
        );
        // Display error message
        networkContainer.innerHTML = `
          <div class="error-message">
            <p><i class="fas fa-exclamation-triangle"></i> Error loading visualization</p>
            <small>Please refresh the page or contact the administrator.</small>
          </div>
        `;
      }
    } else {
      console.warn("Network container not found");
    }

    // Set up event listeners
    setupEventListeners();
  }, 1000);
});

// Event-Listener einrichten
function setupEventListeners() {
  // Netzwerk-Steuerung
  const addRandomNodeButton = document.getElementById("addRandomNode");
  if (addRandomNodeButton) {
    addRandomNodeButton.addEventListener("click", addRandomNode);
  }

  const resetNetworkButton = document.getElementById("resetNetwork");
  if (resetNetworkButton) {
    resetNetworkButton.addEventListener("click", resetNetwork);
  }
  if (document.getElementById("nodeCharge")) {
    document
      .getElementById("nodeCharge")
      .addEventListener("input", updateCharge);
  }
  if (document.getElementById("linkDistance")) {
    document
      .getElementById("linkDistance")
      .addEventListener("input", updateLinkDistance);
  }

  // Darstellungs-Optionen
  if (document.getElementById("showLabels")) {
    document
      .getElementById("showLabels")
      .addEventListener("change", toggleLabels);
  }
  if (document.getElementById("showAttributes")) {
    document
      .getElementById("showAttributes")
      .addEventListener("change", toggleAttributes);
  }
  if (document.getElementById("highlightConnections")) {
    document
      .getElementById("highlightConnections")
      .addEventListener("change", toggleHighlights);
  }
  if (document.getElementById("nodeColorScheme")) {
    document
      .getElementById("nodeColorScheme")
      .addEventListener("change", updateColorScheme);
  }

  // Simulations-Bereich
  if (document.getElementById("addContext")) {
    document
      .getElementById("addContext")
      .addEventListener("click", addUserContext);
  }
}

// Initialize network visualization
function initNetworkVisualization() {
  const networkContainer = document.getElementById("network");
  if (!networkContainer) return;

  width = networkContainer.clientWidth;
  height = networkContainer.clientHeight;

  // SVG-Element erstellen
  svg = d3
    .select("#network")
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("overflow", "visible"); // Wichtig für Klickbarkeit

  // Container für Links und Knoten
  const container = svg.append("g");

  // Zoom-Funktion
  const zoom = d3
    .zoom()
    .scaleExtent([0.1, 4])
    .on("zoom", (event) => {
      container.attr("transform", event.transform);
    });

  svg.call(zoom);

  // Kraft-Simulation erstellen mit verbesserten Parametern für Interaktivität
  simulation = d3
    .forceSimulation()
    .force(
      "link",
      d3
        .forceLink()
        .id((d) => d.id)
        .distance(100)
    )
    .force("charge", d3.forceManyBody().strength(-300))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force(
      "collision",
      d3.forceCollide().radius((d) => d.size + 10)
    );

  // Selektionen für Elemente
  linkElements = container.append("g").attr("class", "links").selectAll("line");

  nodeElements = container
    .append("g")
    .attr("class", "nodes")
    .selectAll("circle");

  textElements = container.append("g").attr("class", "texts").selectAll("text");

  // Beispieldaten erstellen
  createSampleData();

  // Visualisierung aktualisieren
  updateSimulation();

  // Statistiken aktualisieren
  updateStats();

  // Laden-Overlay ausblenden
  if (document.querySelector(".loading-overlay")) {
    document.querySelector(".loading-overlay").style.display = "none";
  }

  // Knoten nach dem Start kurz hervorheben, um Klickbarkeit anzuzeigen
  setTimeout(highlightNodesSequentially, 1000);

  logProcessingStep("Netzwerk initialisiert.", "success");
}

// Funktion, um Knoten nacheinander kurz hervorzuheben
function highlightNodesSequentially() {
  const nodesArray = nodeElements.nodes();
  let index = 0;

  // Alle Knoten auf normale Darstellung zurücksetzen
  nodeElements.attr("stroke-width", 2).attr("stroke", "#fff");

  const interval = setInterval(() => {
    if (index >= nodesArray.length) {
      clearInterval(interval);
      return;
    }

    // Vorherigen Knoten zurücksetzen
    if (index > 0) {
      d3.select(nodesArray[index - 1])
        .attr("stroke-width", 2)
        .attr("stroke", "#fff");
    }

    // Aktuellen Knoten hervorheben
    d3.select(nodesArray[index])
      .attr("stroke-width", 3)
      .attr("stroke", "var(--primary-color)");

    index++;

    // Nach dem letzten Knoten alle zurücksetzen
    if (index >= nodesArray.length) {
      setTimeout(() => {
        nodeElements.attr("stroke-width", 2).attr("stroke", "#fff");
  // Display "Click me" hint
        logProcessingStep(
          "Tip: Click on a node to see details.",
          "info"
        );
      }, 500);
    }
  }, 200); // Switch to the next node every 200ms
}

// Create sample data
function createSampleData() {
  // Create nodes
  const sampleNodes = [
    {
      id: "Apple", // Apfel
      group: "food",
      attributes: { Taste: "sweet", Appearance: "red", Size: "medium" }, // Geschmack: süß, Aussehen: rot, Größe: mittel
      size: 20,
    },
    {
      id: "Banana", // Banane
      group: "food",
      attributes: { Taste: "sweet", Appearance: "yellow", Size: "medium" }, // Geschmack: süß, Aussehen: gelb, Größe: mittel
      size: 20,
    },
    { id: "sweet", group: "attribute", attributes: {}, size: 15 },
    { id: "red", group: "attribute", attributes: {}, size: 15 },
    { id: "yellow", group: "attribute", attributes: {}, size: 15 },
    { id: "medium", group: "attribute", attributes: {}, size: 10 },
    { id: "Taste", group: "category", label: "Taste", attributes: {}, size: 18 },
    { id: "Appearance", group: "category", label: "Appearance", attributes: {}, size: 18 },
    { id: "Size", group: "category", label: "Size", attributes: {}, size: 15 },
  ];

  // Create links
  const sampleLinks = [
    { source: "Apple", target: "sweet", weight: 3 },
    { source: "Apple", target: "red", weight: 3 },
    { source: "Apple", target: "medium", weight: 2 },
    { source: "Banana", target: "sweet", weight: 3 },
    { source: "Banana", target: "yellow", weight: 3 },
    { source: "Banana", target: "medium", weight: 2 },
    { source: "sweet", target: "Taste", weight: 5 },
    { source: "red", target: "Appearance", weight: 5 },
    { source: "yellow", target: "Appearance", weight: 5 },
    { source: "medium", target: "Size", weight: 5 },
  ];

  // Add to global arrays
  nodes = sampleNodes;
  links = sampleLinks;
}

// Update the visualization with current data
function updateSimulation() {
  // Apply the nodes to the force simulation
  simulation.nodes(nodes);
  simulation.force("link").links(links);

  // Update links
  linkElements = linkElements
    .data(links, (d) => `${d.source.id}-${d.target.id}`)
    .join("line")
    .attr("class", "link")
    .attr("stroke-width", (d) => Math.sqrt(d.weight));

  // Update nodes with improved click area
  nodeElements = nodeElements
    .data(nodes, (d) => d.id)
    .join("circle")
    .attr("class", "node")
    .attr("r", (d) => d.size)
    .attr("fill", getNodeColor)
    .style("cursor", "pointer") // Add pointer cursor
    .attr("pointer-events", "all") // Ensure clickability
    .call(
      d3
        .drag()
        .on("start", dragStarted)
        .on("drag", dragging)
        .on("end", dragEnded)
    )
    .on("click", selectNode);

  // Update text labels with click events too
  textElements = textElements
    .data(nodes, (d) => d.id)
    .join("text")
    .text((d) => d.id)
    .attr("font-size", (d) => d.size * 0.7)
    .attr("dx", (d) => d.size + 5)
    .attr("dy", 4)
    .style("cursor", "pointer") // Add pointer cursor to labels
    .style("pointer-events", "none"); // Prevent text from intercepting clicks

  // Define tick function
  simulation.on("tick", () => {
    linkElements
      .attr("x1", (d) => d.source.x)
      .attr("y1", (d) => d.source.y)
      .attr("x2", (d) => d.target.x)
      .attr("y2", (d) => d.target.y);

    nodeElements.attr("cx", (d) => d.x).attr("cy", (d) => d.y);

    textElements.attr("x", (d) => d.x).attr("y", (d) => d.y);
  });

  // Restart simulation
  simulation.alpha(1).restart();

  // For debugging - print out all nodes to console
  console.log(
    "Nodes in visualization:",
    nodes.map((n) => n.id)
  );
}

// Get node color based on current color scheme
function getNodeColor(node) {
  switch (colorScheme) {
    case "weight":
      const connectedLinks = links.filter(
        (link) => link.source.id === node.id || link.target.id === node.id
      );
      const totalWeight = connectedLinks.reduce(
        (sum, link) => sum + link.weight,
        0
      );
      return d3.interpolateViridis(Math.min(totalWeight / 20, 1));

    case "age":
      return node.createdAt
        ? d3.interpolateBlues(
            1 - Math.min((Date.now() - node.createdAt) / 50000, 1)
          )
        : d3.interpolateBlues(0.5);

    case "category":
    default:
      return categoryColors(node.group);
  }
}

// Drag functions
function dragStarted(event, d) {
  if (!event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragging(event, d) {
  d.fx = event.x;
  d.fy = event.y;
}

function dragEnded(event, d) {
  if (!event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}

// Select a node to show details
function selectNode(event, selectedNode) {
  event.stopPropagation(); // Prevent event bubbling

  console.log("Node clicked:", selectedNode.id); // Debug info

  // Reset previous selections
  nodeElements.attr("stroke-width", 2);
  linkElements
    .attr("stroke-opacity", 0.6)
    .attr("stroke-width", (d) => Math.sqrt(d.weight));

  if (selectedNode) {
    // Highlight selected node
    d3.select(this).attr("stroke-width", 3);

    // Highlight connected links and nodes
    if (
      document.getElementById("highlightConnections") &&
      document.getElementById("highlightConnections").checked
    ) {
      linkElements
        .attr("stroke-opacity", (d) =>
          d.source.id === selectedNode.id || d.target.id === selectedNode.id
            ? 0.9
            : 0.2
        )
        .attr("stroke-width", (d) =>
          d.source.id === selectedNode.id || d.target.id === selectedNode.id
            ? Math.sqrt(d.weight) * 2
            : Math.sqrt(d.weight)
        );
    }

    // Update info panel
    updateNodeInfo(selectedNode);
  }
}

// Update the node information panel
function updateNodeInfo(node) {
  const nodeInfo = document.getElementById("nodeInfo");

  // Create info HTML
  let infoHTML = `
        <div class="node-details">
            <h4>${node.id}</h4>
            <p><strong>Group:</strong> ${node.group}</p>
            <p><strong>Connections:</strong> ${ // Verbindungen
              getNodeConnections(node).length
            }</p>
            ${getAttributesHTML(node)}
            ${getConnectionsHTML(node)}
        </div>
    `;

  nodeInfo.innerHTML = infoHTML;
}

// Generate HTML for node attributes
function getAttributesHTML(node) {
  if (!node.attributes || Object.keys(node.attributes).length === 0) {
    return "";
  }

  let html = '<div class="attribute-list"><h5>Attributes:</h5><ul>'; // Attribute

  for (const [key, value] of Object.entries(node.attributes)) {
    html += `<li><strong>${key}:</strong> ${value}</li>`;
  }

  html += "</ul></div>";
  return html;
}

// Generate HTML for node connections
function getConnectionsHTML(node) {
  const connections = getNodeConnections(node);

  if (connections.length === 0) {
    return "";
  }

  let html = '<div class="connections-list"><h5>Connections:</h5><ul>'; // Verbindungen

  connections.forEach((link) => {
    const isSource = link.source.id === node.id;
    const connectedNode = isSource ? link.target : link.source;
    html += `<li><strong>${connectedNode.id}</strong> (Weight: ${link.weight})</li>`; // Gewichtung
  });

  html += "</ul></div>";
  return html;
}

// Get all connections for a node
function getNodeConnections(node) {
  return links.filter(
    (link) => link.source.id === node.id || link.target.id === node.id
  );
}

// Add a random node to the network
function addRandomNode() {
  // Generate random data
  const groups = ["food", "object", "attribute", "action", "abstract"];
  const randomGroup = groups[Math.floor(Math.random() * groups.length)];

  // Random node ID with timestamp to ensure uniqueness
  const timestamp = new Date().getTime().toString().substr(-4);
  const nodeId = `Node_${timestamp}`;

  // Create random attributes
  const attributes = {};
  if (Math.random() > 0.5) {
    const numAttributes = Math.floor(Math.random() * 3) + 1;
    for (let i = 0; i < numAttributes; i++) {
      const attrType =
        attributeTypes[Math.floor(Math.random() * attributeTypes.length)];
      attributes[attrType] = `Value_${Math.floor(Math.random() * 100)}`;
    }
  }

  // Create the new node
  const newNode = {
    id: nodeId,
    group: randomGroup,
    attributes: attributes,
    size: 10 + Math.random() * 15,
    createdAt: Date.now(),
  };

  // Add random connections to existing nodes
  const numConnections = Math.floor(Math.random() * 3) + 1;
  const potentialTargets = [...nodes]; // Copy existing nodes

  for (let i = 0; i < numConnections && potentialTargets.length > 0; i++) {
    // Pick a random target node
    const targetIndex = Math.floor(Math.random() * potentialTargets.length);
    const targetNode = potentialTargets[targetIndex];

    // Create link with random weight
    const newLink = {
      source: newNode.id,
      target: targetNode.id,
      weight: Math.floor(Math.random() * 5) + 1,
    };

    // Add link to links array
    links.push(newLink);

    // Remove target from potential targets to avoid duplicate links
    potentialTargets.splice(targetIndex, 1);
  }

  // Add node to nodes array
  nodes.push(newNode);

  // Update network visualization
  updateSimulation();

  // Update statistics
  updateStats();

  // Log to processing steps
  logProcessingStep(
    `Node "${nodeId}" (${randomGroup}) added with ${numConnections} connections.`, // Knoten ... hinzugefügt mit ... Verbindungen
    "success"
  );
}

// Add user-defined context
function addUserContext() {
  const contextInput = document.getElementById("newContext");
  const categorySelect = document.getElementById("contextCategory");

  const contextText = contextInput.value.trim();
  const category = categorySelect.value;

  if (!contextText) {
    logProcessingStep("Please enter a context.", "error"); // Bitte geben Sie einen Kontext ein.
    return;
  }

  // Process the input text
  logProcessingStep(`Processing input: "${contextText}"`, "info"); // Verarbeite Eingabe

  // Simple NLP: Split into words and analyze
  const words = contextText.split(/\s+/);
  logProcessingStep(`${words.length} words identified.`, "info"); // ... Wörter identifiziert.

  // Extract main entity and attributes
  const mainEntity = words[0]; // Simplified approach

  // Create or find the main entity node
  let entityNode = nodes.find(
    (n) => n.id.toLowerCase() === mainEntity.toLowerCase()
  );

  if (!entityNode) {
    entityNode = {
      id: mainEntity,
      group: category,
      attributes: {},
      size: 20,
      createdAt: Date.now(),
    };
    nodes.push(entityNode);
    logProcessingStep(`New entity created: "${mainEntity}"`, "success"); // Neue Entität erstellt
  } else {
    logProcessingStep(`Existing entity found: "${mainEntity}"`, "info"); // Bestehende Entität gefunden
  }

  // Process words after the first one for potential attributes
  const attributesFound = [];

  for (let i = 1; i < words.length; i++) {
    const word = words[i];

    // Skip common English words (and some German ones that might have been missed if input is mixed)
    if (
      ["is", "and", "or", "the", "a", "an", "to", "of",
       "ist", "und", "oder", "der", "die", "das", "ein", "eine"].includes(
        word.toLowerCase()
      )
    ) {
      continue;
    }

    // Check if this word is already a node
    let attributeNode = nodes.find(
      (n) => n.id.toLowerCase() === word.toLowerCase()
    );

    if (!attributeNode) {
      // Create a new attribute node
      attributeNode = {
        id: word,
        group: "attribute",
        attributes: {},
        size: 15,
        createdAt: Date.now(),
      };
      nodes.push(attributeNode);
      logProcessingStep(`New attribute created: "${word}"`, "success"); // Neues Attribut erstellt
    } else {
      logProcessingStep(`Existing attribute found: "${word}"`, "info"); // Bestehendes Attribut gefunden
    }

    // Create a link between entity and attribute
    const existingLink = links.find(
      (l) =>
        (l.source.id === entityNode.id && l.target.id === attributeNode.id) ||
        (l.source.id === attributeNode.id && l.target.id === entityNode.id)
    );

    if (existingLink) {
      // Strengthen existing connection
      existingLink.weight += 1;
      logProcessingStep(
        `Existing connection strengthened: ${entityNode.id} - ${attributeNode.id}`, // Bestehende Verbindung gestärkt
        "info"
      );
    } else {
      // Create new connection
      links.push({
        source: entityNode.id,
        target: attributeNode.id,
        weight: 2,
      });
      logProcessingStep(
        `New connection created: ${entityNode.id} - ${attributeNode.id}`, // Neue Verbindung erstellt
        "success"
      );
    }

    attributesFound.push(word);
  }

  // Update visualization and stats
  updateSimulation();
  updateStats();

  // Clear input
  contextInput.value = "";

  logProcessingStep(
    `Context processed successfully: "${mainEntity}" with ${attributesFound.length} attributes.`, // Kontext erfolgreich verarbeitet ... mit ... Attributen.
    "success"
  );
}

// Reset the network to initial state
function resetNetwork() {
  // Clear arrays
  nodes = [];
  links = [];

  // Create new sample data
  createSampleData();

  // Update visualization
  updateSimulation();
  updateStats();

  // Clear node info panel
  document.getElementById("nodeInfo").innerHTML =
    '<p class="empty-state">Select a node to view details</p>'; // Wählen Sie einen Knoten aus, um Details anzuzeigen

  // Log to processing steps
  logProcessingStep("Network reset.", "info"); // Netzwerk zurückgesetzt.
}

// Update charge force
function updateCharge() {
  const chargeValue = document.getElementById("nodeCharge").value;
  simulation.force("charge").strength(chargeValue);
  simulation.alpha(0.3).restart();
}

// Update link distance
function updateLinkDistance() {
  const distance = document.getElementById("linkDistance").value;
  simulation.force("link").distance(distance);
  simulation.alpha(0.3).restart();
}

// Toggle node labels
function toggleLabels() {
  const showLabels = document.getElementById("showLabels").checked;
  textElements.style("display", showLabels ? "block" : "none");
}

// Toggle attribute display
function toggleAttributes() {
  const showAttributes = document.getElementById("showAttributes").checked;
  // This would typically update node rendering to show attribute indicators
  // For this demo, we'll just adjust node colors slightly
  nodeElements.attr("fill-opacity", showAttributes ? 1 : 0.7);
}

// Toggle connection highlights
function toggleHighlights() {
  const showHighlights = document.getElementById(
    "highlightConnections"
  ).checked;
  const links = d3.selectAll(".link");

  if (showHighlights) {
    links
      .style("stroke-width", "2px")
      .style("stroke", "#6366f1")
      .style("opacity", "0.8")
      .style("filter", "drop-shadow(0 2px 4px rgba(99, 102, 241, 0.3))");
  } else {
    links
      .style("stroke-width", "1px")
      .style("stroke", "#444")
      .style("opacity", "0.4")
      .style("filter", "none");
  }
}

// Update color scheme
function updateColorScheme() {
  colorScheme = document.getElementById("nodeColorScheme").value;
  nodeElements.attr("fill", getNodeColor);
}

// Update statistics display
function updateStats() {
  document.getElementById("nodeCount").textContent = nodes.length;
  document.getElementById("linkCount").textContent = links.length;

  // Calculate central nodes (simplified: nodes with most connections)
  const nodeDegrees = nodes.map((node) => {
    const degree = links.filter(
      (link) => link.source.id === node.id || link.target.id === node.id
    ).length;
    return { id: node.id, degree };
  });

  nodeDegrees.sort((a, b) => b.degree - a.degree);

  // Count nodes with more than 2 connections as "central"
  const centralCount = nodeDegrees.filter((n) => n.degree > 2).length;
  document.getElementById("centralNodes").textContent = centralCount;

  // Simple cluster detection (very simplified)
  // In a real application, you would use a proper community detection algorithm
  const uniqueGroups = new Set(nodes.map((n) => n.group));
  document.getElementById("clusterCount").textContent = uniqueGroups.size;
}

// Log processing steps to the UI
function logProcessingStep(message, type = "info") {
  const processingLog = document.getElementById("processingSteps");
  const logEntry = document.createElement("p");
  logEntry.className = `log-entry ${type}`;
  logEntry.textContent = message;
  processingLog.appendChild(logEntry);

  // Scroll to bottom
  processingLog.scrollTop = processingLog.scrollHeight;
}
