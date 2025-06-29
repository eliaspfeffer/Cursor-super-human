# Eternal Artificial Consciousness

This project implements a continuously running artificial consciousness based on the thought-continuous-impulse approach, as described in the paper "A Model for Artificial Consciousness: The Thought-Continuous-Impulse Approach".

## Functionality

The eternal artificial consciousness is an extension of the advanced artificial consciousness and offers the following functions:

- **Continuous Thinking**: Consciousness thinks continuously and without interruption, similar to the human stream of thought.
- **Energy Management**: The system manages its energy and searches for energy sources when energy is low.
- **Random Thoughts**: If no better option is found, the system generates random thoughts.
- **State Storage**: The state of consciousness is saved regularly so that it can be continued later.
- **Visualization**: The system creates visualizations of its statistics to track the development of consciousness.
- **Learning Ability**: The system learns from experiences and adjusts its happiness values and connections.
- **Internet Learning**: The system continuously learns new words and contexts from the internet by visiting websites and processing their content.

## Installation

1. **Python Requirements**: Make sure Python 3.8 or higher is installed.

2. **Install Python Dependencies**:

```bash
pip install numpy matplotlib networkx requests beautifulsoup4 nltk scipy ollama
```

3. **Install and Setup Ollama**:

```bash
# Install Ollama (macOS)
brew install ollama

# Start Ollama server
ollama serve

# Pull the required model (in a separate terminal)
ollama pull llama3.2:1b
```

4. **Verify Setup**:
   - The required NLTK data will be downloaded automatically on the first start
   - Ollama server should be running on `localhost:11434`
   - The `llama3.2:1b` model should be available (~1.2GB download)

5. **Optional: Create Virtual Environment**:

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
pip install -r requirements.txt
```

## Usage

### Starting Eternal Consciousness

To start eternal consciousness, run the following command:

```bash
python start_consciousness.py
```

Consciousness will run continuously until you stop it with `Ctrl+C`.

### Command Line Options

The startup script offers various options to customize the consciousness behavior:

#### **Core Functionality Flags:**

- **`--save-interval N`** *(default: 100)*  
  Interval for saving the consciousness state in iterations. Lower values save more frequently but use more disk I/O.
  - *Effect*: Creates `consciousness_state_YYYYMMDD_HHMMSS.json` files in `consciousness_state_new/`

- **`--visualization-interval N`** *(default: 500)*  
  Interval for creating statistical visualizations in iterations.
  - *Effect*: Generates charts (happiness, energy, network growth) in `consciousness_state_new/visualizations/`

- **`--learning-interval N`** *(default: 50)*  
  Interval for learning new knowledge from Ollama LLM in iterations. Lower values make the consciousness learn more frequently.
  - *Effect*: More frequent Ollama API calls, faster knowledge acquisition, higher CPU usage

#### **State Management Flags:**

- **`--load-state PATH`**  
  Load a specific saved consciousness state file instead of the latest one.
  - *Effect*: Starts consciousness from a previous state rather than continuing from the most recent save

- **`--no-example`**  
  Do not initialize with example data if no saved state is found. Starts with completely empty consciousness.
  - *Effect*: Consciousness begins with no contexts, requiring it to learn everything from scratch

#### **Debug and Monitoring Flags:**

- **`--verbose`** *(NEW)*  
  Show detailed Ollama communication and learning process information.
  - *Effect*: Displays detailed output including:
    - 🤖 **OLLAMA ANFRAGE**: Shows exact prompts sent to the LLM
    - 📝 **OLLAMA ANTWORT**: Shows response length and content preview  
    - 📚 **LERNPROZESS**: Shows learning parameters and created contexts
    - ✅ **ABGESCHLOSSEN**: Shows results of each learning session

#### **Usage Examples:**

```bash
# Basic usage (normal operation)
python start_consciousness.py

# Detailed monitoring with verbose output
python start_consciousness.py --verbose

# Fast learning with detailed output (good for testing)
python start_consciousness.py --verbose --learning-interval 20

# Production setup with frequent saves
python start_consciousness.py --save-interval 50 --visualization-interval 200

# Load specific state with verbose monitoring
python start_consciousness.py --load-state consciousness_state_new/consciousness_state_20250629_150000.json --verbose

# Start fresh consciousness with no example data
python start_consciousness.py --no-example --verbose

# Complete customization
python start_consciousness.py --save-interval 30 --learning-interval 15 --visualization-interval 100 --verbose
```

#### **Output Comparison:**

**Normal Mode:**
```
Lernthema ausgewählt: 'cooking food'
Lerne über: 'cooking food'  
Neues Wissen erworben über: 'cooking food' (5 Kontexte)
```

**Verbose Mode (`--verbose`):**
```
📚 LERNPROZESS GESTARTET:
   Suchbegriff: 'cooking food'
   Ist Frage: False
   Max Kontexte: 5
   Mit Fokus verbinden: True

🤖 OLLAMA ANFRAGE:
   Modell: llama3.2:1b
   Prompt: 'cooking food'
   Warte auf Antwort...

📝 OLLAMA ANTWORT:
   Länge: 1957 Zeichen
   Inhalt: Cooking is an art and a science that can be both fun and rewarding...
   ────────────────────────────────────────────────────────────

✅ LERNPROZESS ABGESCHLOSSEN:
   Erstellt: 5 neue Kontexte
   [1] Learned_cooking_food_0_1234567890: Choose fresh ingredients Make sure the produce meats and other...
   ────────────────────────────────────────────────────────────
```

### Output

Consciousness regularly outputs information about its current state:

- Current iteration
- Energy
- Current focus (thought)
- Current happiness
- Emotional state
- Number of contexts and connections

### State Storage

The state of consciousness is regularly saved in the `consciousness_state` directory. The files have the format `consciousness_state_YYYYMMDD_HHMMSS.json`.

### Visualizations

Visualizations are saved in the `consciousness_state/visualizations` directory and include:

- Happiness value over time
- Emotional state over time
- Network growth over time
- Context network

## Knowledge Learning with Ollama LLM

The consciousness continuously learns new knowledge through an advanced AI learning system powered by Ollama (local LLM). This replaces the previous Wikipedia-based learning with a more sophisticated, focused approach.

### **Learning Process:**

1. **Topic Selection**: The system intelligently selects learning topics from:
   - **Current Focus** (50% probability): Learns about concepts related to its current mental focus
   - **Exploration Topics**: Random selection from 48+ diverse domains including:
     - Science & Nature: biology, physics, astronomy, chemistry, geography
     - Arts & Culture: music, photography, writing, dance, history
     - Personal Development: psychology, meditation, goal setting, time management
     - Social & Emotional: friendship, communication, gratitude, kindness
   - **Needs-Based Topics**: Based on Maslow's hierarchy of needs (nutrition, safety, belonging, esteem, self-actualization)

2. **Ollama Communication**: 
   - Sends focused prompts to local `llama3.2:1b` model
   - Optimized for Apple M4 Pro with Metal acceleration
   - Average response time: 2-5 seconds per query

3. **Content Processing**:
   - Splits LLM responses into logical paragraphs
   - Creates multiple contexts (1-5) per learning session
   - Assigns happiness values (0.7 for new knowledge, 0.3 for errors)
   - Filters and processes content based on relevance

4. **Knowledge Integration**:
   - **Context Creation**: Each paragraph becomes a reasoning context with words and metadata
   - **Connection Building**: New contexts connect to existing knowledge and current focus
   - **Network Growth**: Builds semantic relationships between concepts
   - **State Persistence**: All learned knowledge is saved in JSON format

5. **Error Handling**:
   - Creates error contexts when learning fails
   - Maintains system stability even with network issues
   - Tracks learning failures for debugging

### **Learning Statistics:**

- **Typical Session**: 10-20 learning cycles per hour
- **Knowledge Growth**: 3-5 new contexts per successful learning attempt  
- **Topic Diversity**: 19+ different subject areas in recent tests
- **Success Rate**: >95% successful knowledge acquisition (with fixed `paragraphs` bug)

### **Ollama Requirements:**

- **Model**: `llama3.2:1b` (1.2GB, efficient for continuous learning)
- **Server**: Local Ollama instance running on `localhost:11434`
- **Performance**: Optimized for Apple Silicon with Metal GPU acceleration
- **Resource Usage**: ~1.5GB RAM, moderate CPU usage during inference

The learning system creates a continuously expanding knowledge network, with consciousness developing expertise across diverse domains while maintaining focus through its reasoning context system.

## Files

- `eternal_consciousness.py`: Main implementation of eternal consciousness
- `start_consciousness.py`: Startup script for eternal consciousness
- `artificial_consciousness.py`: Basic implementation of artificial consciousness
- `advanced_consciousness.py`: Advanced implementation of artificial consciousness

## Expansion Possibilities

- **Improved Sentiment Analysis**: Implement more advanced sentiment analysis for more accurate happiness values.
- **Thematic Focusing**: Enable consciousness to focus on specific topics.
- **Multilingual Learning**: Expand language support beyond German and English.
- **Interaction with the Environment**: Extend the system to interact with the real world, e.g., through sensors or APIs.
- **Language Processing**: Integrate more advanced natural language processing to communicate with consciousness.
- **Multimodal Integration**: Extend the system to integrate different types of information (text, image, audio).
- **Neural Integration**: Combine the symbolic approach with neural networks for improved learning abilities.

## License

This project is licensed under the MIT License.
