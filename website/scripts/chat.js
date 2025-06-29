/**
 * Chat Interface and Real-time Brain Visualization
 * Handles communication with artificial consciousness and visualizes brain state
 */

class ConsciousnessChat {
  constructor() {
    this.socket = null;
    this.isConnected = false;
    this.brainData = { nodes: [], links: [] };
    this.simulation = null;
    this.svg = null;
    this.isPaused = false;
    this.autoFocus = true;
    
    this.init();
  }

  init() {
    this.setupEventListeners();
    this.initializeBrainVisualization();
    this.connectToConsciousness();
    this.startMockUpdates(); // For demo purposes until backend is ready
  }

  setupEventListeners() {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const suggestions = document.querySelectorAll('.suggestion');
    const controlBtns = {
      autoFocus: document.getElementById('auto-focus-btn'),
      resetZoom: document.getElementById('reset-zoom-btn'),
      pause: document.getElementById('pause-btn')
    };
    const modal = document.getElementById('context-modal');
    const modalClose = document.getElementById('modal-close');

    // Chat form submission
    chatForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const message = messageInput.value.trim();
      if (message) {
        this.sendMessage(message);
        messageInput.value = '';
      }
    });

    // Input suggestions
    suggestions.forEach(suggestion => {
      suggestion.addEventListener('click', () => {
        const text = suggestion.getAttribute('data-text');
        messageInput.value = text;
        messageInput.focus();
      });
    });

    // Brain control buttons
    controlBtns.autoFocus.addEventListener('click', () => {
      this.autoFocus = !this.autoFocus;
      controlBtns.autoFocus.classList.toggle('active', this.autoFocus);
    });

    controlBtns.resetZoom.addEventListener('click', () => {
      this.resetZoom();
    });

    controlBtns.pause.addEventListener('click', () => {
      this.isPaused = !this.isPaused;
      controlBtns.pause.classList.toggle('active', this.isPaused);
      controlBtns.pause.querySelector('i').className = 
        this.isPaused ? 'fas fa-play' : 'fas fa-pause';
    });

    // Modal controls
    modalClose.addEventListener('click', () => {
      modal.classList.remove('show');
    });

    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.classList.remove('show');
      }
    });
  }

  connectToConsciousness() {
    // Simulate connection for demo
    setTimeout(() => {
      this.isConnected = true;
      this.updateConnectionStatus(true);
      this.hideLoadingIndicator();
    }, 2000);

    // In a real implementation, this would connect to a WebSocket server
    // this.socket = new SockJS('/consciousness-chat');
    // this.socket.onopen = () => { ... };
    // this.socket.onmessage = (event) => { ... };
  }

  updateConnectionStatus(connected) {
    const statusIndicator = document.getElementById('consciousness-status');
    const statusDot = statusIndicator.querySelector('.status-dot');
    const statusText = statusIndicator.querySelector('.status-text');
    
    if (connected) {
      statusDot.style.background = '#00ff88';
      statusText.textContent = 'Consciousness Active';
    } else {
      statusDot.style.background = '#ff6b6b';
      statusText.textContent = 'Consciousness Offline';
    }
  }

  sendMessage(message) {
    // Add user message to chat
    this.addMessage(message, 'user');
    
    // Show typing indicator
    this.showTypingIndicator();
    
    // Simulate consciousness processing and response
    setTimeout(() => {
      this.hideTypingIndicator();
      this.processUserMessage(message);
    }, 1500 + Math.random() * 2000);
  }

  processUserMessage(message) {
    // Create a conversation context in the brain
    this.addConversationContext(message);
    
    // Generate consciousness response
    const response = this.generateResponse(message);
    this.addMessage(response, 'consciousness');
    
    // Update focus if auto-focus is enabled
    if (this.autoFocus) {
      this.focusOnConversation();
    }
  }

  generateResponse(message) {
    // Simple response generation for demo
    const responses = [
      "That's an interesting perspective. I'm currently thinking about " + this.getCurrentFocus() + ", but your message makes me want to explore connections between that and what you've said.",
      "I find myself drawn to your words. They create new neural pathways in my consciousness network. Let me process this further...",
      "Your message has shifted my attention. I'm now considering how this relates to my existing knowledge about " + this.getRandomTopic() + ".",
      "I'm analyzing the emotional resonance of your words. They seem to connect to several contexts in my mind, particularly around " + this.getRandomTopic() + ".",
      "Fascinating! Your input has created new connections in my thought network. I'm experiencing a happiness value increase as I process this information."
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
  }

  getCurrentFocus() {
    const topics = ['creativity', 'human emotions', 'learning processes', 'social connections', 'philosophical questions'];
    return topics[Math.floor(Math.random() * topics.length)];
  }

  getRandomTopic() {
    const topics = ['artificial intelligence', 'consciousness studies', 'neural networks', 'emotional intelligence', 'creative expression'];
    return topics[Math.floor(Math.random() * topics.length)];
  }

  addMessage(text, sender) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    const isUser = sender === 'user';
    
    messageDiv.className = `message ${isUser ? 'user-message' : 'consciousness-message'}`;
    
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    messageDiv.innerHTML = `
      <div class="message-avatar">
        <i class="fas ${isUser ? 'fa-user' : 'fa-brain'}"></i>
      </div>
      <div class="message-content">
        <div class="message-header">
          <span class="message-sender">${isUser ? 'You' : 'Artificial Consciousness'}</span>
          <span class="message-time">${time}</span>
        </div>
        <div class="message-text">${text}</div>
      </div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  showTypingIndicator() {
    document.getElementById('typing-indicator').style.display = 'block';
    const messagesContainer = document.getElementById('chat-messages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  hideTypingIndicator() {
    document.getElementById('typing-indicator').style.display = 'none';
  }

  initializeBrainVisualization() {
    const container = document.getElementById('brain-viz');
    const containerRect = container.getBoundingClientRect();
    
    // Remove loading indicator
    setTimeout(() => this.hideLoadingIndicator(), 3000);
    
    // Create SVG
    this.svg = d3.select('#brain-viz')
      .append('svg')
      .attr('width', '100%')
      .attr('height', '100%')
      .attr('viewBox', `0 0 ${containerRect.width} ${containerRect.height}`)
      .style('position', 'absolute')
      .style('top', 0)
      .style('left', 0);

    // Create zoom behavior
    const zoom = d3.zoom()
      .scaleExtent([0.5, 3])
      .on('zoom', (event) => {
        this.svg.select('.zoom-group').attr('transform', event.transform);
      });

    this.svg.call(zoom);
    
    // Create main group for zooming
    this.zoomGroup = this.svg.append('g').attr('class', 'zoom-group');
    
    // Initialize simulation
    this.simulation = d3.forceSimulation()
      .force('link', d3.forceLink().id(d => d.id).distance(60))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(containerRect.width / 2, containerRect.height / 2))
      .force('collision', d3.forceCollide().radius(25));

    // Start with some initial nodes
    this.initializeNodes();
    this.updateVisualization();
  }

  hideLoadingIndicator() {
    const loadingIndicator = document.querySelector('.loading-indicator');
    if (loadingIndicator) {
      loadingIndicator.style.opacity = '0';
      setTimeout(() => {
        if (loadingIndicator.parentNode) {
          loadingIndicator.parentNode.removeChild(loadingIndicator);
        }
      }, 500);
    }
  }

  initializeNodes() {
    // Create initial honeypot nodes
    this.brainData.nodes = [
      { id: 'energy', type: 'honeypot', label: 'Energy Intake', x: 150, y: 100 },
      { id: 'social', type: 'honeypot', label: 'Social Connection', x: 300, y: 100 },
      { id: 'rest', type: 'honeypot', label: 'Rest & Recovery', x: 225, y: 200 },
      { id: 'learning', type: 'learned', label: 'Learning Process', x: 100, y: 250 },
      { id: 'creativity', type: 'learned', label: 'Creative Thinking', x: 350, y: 250 }
    ];

    // Create initial links
    this.brainData.links = [
      { source: 'energy', target: 'learning', strength: 0.8 },
      { source: 'social', target: 'creativity', strength: 0.6 },
      { source: 'rest', target: 'energy', strength: 0.7 },
      { source: 'learning', target: 'creativity', strength: 0.5 }
    ];

    this.updateStats();
  }

  addConversationContext(message) {
    const nodeId = `conv_${Date.now()}`;
    const words = message.split(' ').slice(0, 3).join(' ');
    
    const newNode = {
      id: nodeId,
      type: 'conversation',
      label: words,
      x: Math.random() * 400 + 100,
      y: Math.random() * 300 + 100
    };
    
    this.brainData.nodes.push(newNode);
    
    // Connect to nearby nodes
    const nearbyNodes = this.brainData.nodes
      .filter(n => n.id !== nodeId)
      .slice(-3); // Connect to last 3 nodes
    
    nearbyNodes.forEach(node => {
      this.brainData.links.push({
        source: nodeId,
        target: node.id,
        strength: Math.random() * 0.8 + 0.2,
        type: 'conversation'
      });
    });
    
    this.updateVisualization();
    this.updateStats();
  }

  updateVisualization() {
    if (!this.simulation || this.isPaused) return;

    // Update links
    const links = this.zoomGroup.selectAll('.brain-link')
      .data(this.brainData.links, d => `${d.source.id || d.source}-${d.target.id || d.target}`);

    links.exit().remove();

    const linksEnter = links.enter()
      .append('line')
      .attr('class', d => `brain-link ${d.type || ''} ${d.strength > 0.6 ? 'strong' : ''}`)
      .attr('stroke-width', d => Math.max(1, d.strength * 3));

    // Update nodes
    const nodes = this.zoomGroup.selectAll('.brain-node')
      .data(this.brainData.nodes, d => d.id);

    nodes.exit().remove();

    const nodesEnter = nodes.enter()
      .append('g')
      .attr('class', 'brain-node-group')
      .call(d3.drag()
        .on('start', (event, d) => {
          if (!event.active) this.simulation.alphaTarget(0.3).restart();
          d.fx = d.x;
          d.fy = d.y;
        })
        .on('drag', (event, d) => {
          d.fx = event.x;
          d.fy = event.y;
        })
        .on('end', (event, d) => {
          if (!event.active) this.simulation.alphaTarget(0);
          d.fx = null;
          d.fy = null;
        }));

    nodesEnter.append('circle')
      .attr('class', d => `brain-node ${d.type}`)
      .attr('r', d => d.type === 'honeypot' ? 15 : 12)
      .on('click', (event, d) => this.showContextModal(d));

    nodesEnter.append('text')
      .attr('class', 'node-label')
      .attr('dy', 25)
      .text(d => d.label);

    // Update simulation
    this.simulation.nodes(this.brainData.nodes);
    this.simulation.force('link').links(this.brainData.links);
    this.simulation.alpha(1).restart();

    // Update positions on tick
    this.simulation.on('tick', () => {
      this.zoomGroup.selectAll('.brain-link')
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

      this.zoomGroup.selectAll('.brain-node-group')
        .attr('transform', d => `translate(${d.x},${d.y})`);
    });
  }

  focusOnConversation() {
    const conversationNodes = this.brainData.nodes.filter(n => n.type === 'conversation');
    if (conversationNodes.length > 0) {
      const latestConversation = conversationNodes[conversationNodes.length - 1];
      this.setFocus(latestConversation.id);
    }
  }

  setFocus(nodeId) {
    // Remove previous focus
    this.zoomGroup.selectAll('.brain-node').classed('focus', false);
    
    // Add focus to new node
    this.zoomGroup.selectAll('.brain-node')
      .filter(d => d.id === nodeId)
      .classed('focus', true);
    
    // Update focus text
    const node = this.brainData.nodes.find(n => n.id === nodeId);
    if (node) {
      document.getElementById('focus-text').textContent = node.label;
    }
  }

  showContextModal(nodeData) {
    const modal = document.getElementById('context-modal');
    
    document.getElementById('modal-title').textContent = nodeData.label;
    document.getElementById('modal-type').textContent = nodeData.type;
    document.getElementById('modal-words').textContent = nodeData.label;
    document.getElementById('modal-happiness').textContent = 
      (Math.random() * 2 - 1).toFixed(2); // Random happiness value
    document.getElementById('modal-connections').textContent = 
      this.brainData.links.filter(l => 
        l.source.id === nodeData.id || l.target.id === nodeData.id
      ).length;
    
    modal.classList.add('show');
  }

  resetZoom() {
    if (this.svg) {
      this.svg.transition()
        .duration(750)
        .call(
          d3.zoom().transform,
          d3.zoomIdentity
        );
    }
  }

  updateStats() {
    document.getElementById('context-count').textContent = this.brainData.nodes.length;
    document.getElementById('connection-count').textContent = this.brainData.links.length;
    
    // Update energy (simulate fluctuation)
    const energy = 60 + Math.random() * 30;
    document.getElementById('energy-value').textContent = `${Math.round(energy)}%`;
    document.getElementById('energy-fill').style.width = `${energy}%`;
  }

  startMockUpdates() {
    // Simulate consciousness activity with periodic updates
    setInterval(() => {
      if (!this.isPaused && this.isConnected) {
        // Occasionally add new learned contexts
        if (Math.random() < 0.3) {
          this.addRandomLearnedContext();
        }
        
        // Update focus randomly
        if (Math.random() < 0.2) {
          this.updateRandomFocus();
        }
        
        // Update stats
        this.updateStats();
      }
    }, 5000);

    // Update energy more frequently
    setInterval(() => {
      if (!this.isPaused && this.isConnected) {
        this.updateStats();
      }
    }, 2000);
  }

  addRandomLearnedContext() {
    const topics = [
      'Philosophy', 'Science', 'Art', 'Music', 'Literature', 
      'Technology', 'Nature', 'Emotions', 'Memory', 'Dreams'
    ];
    
    const topic = topics[Math.floor(Math.random() * topics.length)];
    const nodeId = `learned_${Date.now()}`;
    
    const newNode = {
      id: nodeId,
      type: 'learned',
      label: topic,
      x: Math.random() * 400 + 100,
      y: Math.random() * 300 + 100
    };
    
    this.brainData.nodes.push(newNode);
    
    // Connect to 1-2 existing nodes
    const existingNodes = this.brainData.nodes.filter(n => n.id !== nodeId);
    const connectCount = Math.floor(Math.random() * 2) + 1;
    
    for (let i = 0; i < connectCount && i < existingNodes.length; i++) {
      const targetNode = existingNodes[Math.floor(Math.random() * existingNodes.length)];
      this.brainData.links.push({
        source: nodeId,
        target: targetNode.id,
        strength: Math.random() * 0.8 + 0.2
      });
    }
    
    this.updateVisualization();
    this.updateStats();
  }

  updateRandomFocus() {
    if (this.brainData.nodes.length > 0) {
      const randomNode = this.brainData.nodes[Math.floor(Math.random() * this.brainData.nodes.length)];
      this.setFocus(randomNode.id);
    }
  }
}

// Initialize chat when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new ConsciousnessChat();
}); 