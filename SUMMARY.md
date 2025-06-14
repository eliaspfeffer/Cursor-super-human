# Summary: Artificial Consciousness

## Overview

This project implements a model for artificial consciousness based on the "Reasoning for AGI" concept. It simulates a self-motivated thought process based on word and context connections as well as happiness evaluations. The goal is to create a system that functions similarly to human consciousness by continuously searching for paths that maximize its "happiness state."

## Core Components

### Basic Model (`artificial_consciousness.py`)

1.  **Words**: Basic units of information that are stored only once.
2.  **Contexts**: Sequences of words that together form a meaningful statement (e.g., "An apple tastes good").
3.  **Connections**: Contexts are interconnected if they are semantically or logically related.
4.  **Happiness Values**: Each context has a happiness value that indicates how "positive" that context is.
5.  **Focus**: Consciousness always focuses on a specific context and follows connections to other contexts.
6.  **Paths**: A sequence of contexts that consciousness has traversed.

### Advanced Model (`advanced_consciousness.py`)

1.  **Emotional States**: Different emotions with different weightings influence decision-making.
2.  **Memory**: Short- and long-term memory for storing and consolidating experiences.
3.  **Environmental Interaction**: Ability to perceive and react to objects and events in the environment.
4.  **Learning Ability**: Adaptation of happiness values and creation of new connections based on experiences.

## Functionality

The algorithm works as follows:

1.  Consciousness begins with an initial focus on a context.
2.  It evaluates all possible next contexts based on the connections.
3.  It selects the context that maximizes the overall happiness value of the path.
4.  It can also decide to return to a previous context if this would lead to a happier path.
5.  This process is repeated continuously, creating a "stream of thought."

In the advanced model:

1.  Emotional states are updated based on the visited contexts.
2.  The system learns from experiences and adjusts happiness values.
3.  It creates new connections between contexts based on experiences.
4.  It perceives the environment and creates new contexts from it.

## Examples

The project includes several examples:

1.  **Basic Example**: A simple network of contexts around the theme of "food and happiness."
2.  **Complex Scenario**: An expanded network that includes learning, experiences, and energy.
3.  **Environmental Interaction**: Objects such as apples, bananas, and books with which consciousness can interact.

## Visualizations

The project offers various visualizations:

1.  **Context Network**: Visualization of the connections between contexts.
2.  **Happiness Value Development**: Tracking of the happiness value during the thought process.
3.  **Emotional State Development**: Tracking of emotions over time.
4.  **Memory Consolidation**: Visualization of the frequency of contexts in long-term memory.
5.  **Learning Process**: Visualization of the change in happiness values through learning.

## Expansion Possibilities

1.  **More Complex Emotion Models**: Integration of more advanced psychological models.
2.  **Language Processing**: Improvement of the ability to understand and generate natural language.
3.  **Active Interaction**: Development of mechanisms for active interaction with the environment.
4.  **Social Interaction**: Modeling of interactions with other consciousnesses.
5.  **Neural Integration**: Combination with neural networks for improved learning abilities.

## Conclusion

This project represents a first step towards an artificial consciousness that acts self-motivated. It demonstrates how a simple model of words, contexts, and connections can lead to complex, goal-oriented behavior. The advanced functions such as emotional states, memory, and environmental interaction bring the model closer to a real consciousness, although many aspects of human consciousness are still missing.
