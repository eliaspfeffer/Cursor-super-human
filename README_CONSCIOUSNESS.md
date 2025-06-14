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

1. Make sure Python 3.6 or higher is installed.
2. Install the required dependencies:

```bash
pip install numpy matplotlib networkx requests beautifulsoup4 nltk scipy
```

3. The required NLTK data will be downloaded automatically on the first start.

## Usage

### Starting Eternal Consciousness

To start eternal consciousness, run the following command:

```bash
python start_consciousness.py
```

Consciousness will run continuously until you stop it with `Ctrl+C`.

### Command Line Options

The startup script offers various options:

- `--save-interval`: Interval for saving the state (in iterations, default: 100)
- `--visualization-interval`: Interval for visualizing statistics (in iterations, default: 500)
- `--learning-interval`: Interval for learning from the internet (in iterations, default: 50)
- `--load-state`: Path to a saved state file to be loaded
- `--no-example`: Do not initialize with example data if no state is loaded

Example:

```bash
python start_consciousness.py --save-interval 50 --visualization-interval 200 --learning-interval 30
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

## Internet Learning

Consciousness continuously learns new words and contexts from the internet. The learning process includes the following steps:

1. **URL Selection**: The system selects a URL from its queue. Initially, these are random Wikipedia pages.
2. **Retrieve Content**: The content of the website is retrieved and cleaned.
3. **Sentence Extraction**: The text is split into sentences, and a subset is randomly selected.
4. **Context Creation**: A new context is created from each sentence, removing stop words and lemmatizing words.
5. **Sentiment Analysis**: A happiness value is calculated for each context based on a simple sentiment analysis.
6. **Connection Creation**: The new contexts are connected to each other and to existing contexts.
7. **Link Extraction**: Links from the website are extracted and added to the URL queue.

The system limits the number of URLs visited per session to conserve resources. The learning history is saved in the state and can be analyzed later.

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
