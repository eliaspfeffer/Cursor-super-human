"""
Testskript für die erweiterte Version des künstlichen Bewusstseins.

Dieses Skript demonstriert die erweiterten Funktionen wie emotionale Zustände,
Gedächtnis und Umgebungsinteraktion.
"""

from advanced_consciousness import AdvancedConsciousnessEngine, EmotionalState, Memory, Environment
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from typing import List, Dict, Tuple


def visualize_emotional_state_over_time(engine: AdvancedConsciousnessEngine, iterations: int = 15):
    """Visualisiert die Entwicklung des emotionalen Zustands über die Zeit."""
    # Initialisiere Datenstrukturen für die Verfolgung
    emotion_history = {emotion: [] for emotion in engine.emotional_state.emotions}
    path_labels = []
    
    # Speichere den Ausgangszustand
    for emotion, value in engine.emotional_state.emotions.items():
        emotion_history[emotion].append(value)
    path_labels.append([context.label for context in engine.current_path])
    
    # Führe den Denkprozess durch und verfolge die Werte
    for i in range(iterations):
        # Führe Lern- und Wahrnehmungsprozesse durch
        if i % 3 == 0:
            engine.learn_from_experience()
        if i % 4 == 0:
            engine.perceive_environment()
        if i % 5 == 0:
            engine.create_new_connections()
        
        # Finde den nächsten Fokus
        next_focus = engine.find_best_next_focus()
        if next_focus:
            engine.set_focus(next_focus)
        
        # Speichere den emotionalen Zustand
        for emotion, value in engine.emotional_state.emotions.items():
            emotion_history[emotion].append(value)
        
        path_labels.append([context.label for context in engine.current_path])
    
    # Visualisiere die Ergebnisse
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Zeichne die Emotionen
    for emotion, values in emotion_history.items():
        ax.plot(values, marker='o', linestyle='-', linewidth=2, label=emotion)
    
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Emotionswert')
    ax.set_title('Entwicklung des emotionalen Zustands während des Denkprozesses')
    ax.legend()
    
    # Füge Beschriftungen für die Pfade hinzu
    for i, path in enumerate(path_labels):
        ax.annotate(' → '.join(path), 
                    (i, 0.9),
                    textcoords="data",
                    ha='center',
                    fontsize=8,
                    rotation=90)
    
    plt.tight_layout()
    plt.savefig('emotional_state_over_time.png')
    plt.close()
    
    print("Emotionale Zustandsentwicklung wurde als 'emotional_state_over_time.png' gespeichert.")


def visualize_memory_consolidation(engine: AdvancedConsciousnessEngine):
    """Visualisiert die Konsolidierung des Gedächtnisses."""
    # Konsolidiere das Gedächtnis
    engine.memory.consolidate_to_long_term()
    
    # Hole die Daten aus dem Langzeitgedächtnis
    memory_data = engine.memory.long_term
    
    if not memory_data:
        print("Keine Daten im Langzeitgedächtnis.")
        return
    
    # Sortiere die Daten nach Häufigkeit
    sorted_data = sorted(memory_data.items(), key=lambda x: x[1], reverse=True)
    labels, frequencies = zip(*sorted_data)
    
    # Erstelle ein Balkendiagramm
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(labels, frequencies, color='skyblue')
    
    # Füge Werte über den Balken hinzu
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height:.0f}',
                ha='center', va='bottom', fontsize=9)
    
    ax.set_xlabel('Kontext')
    ax.set_ylabel('Häufigkeit')
    ax.set_title('Langzeitgedächtnis: Häufigkeit der Kontexte')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('memory_consolidation.png')
    plt.close()
    
    print("Gedächtniskonsolidierung wurde als 'memory_consolidation.png' gespeichert.")


def create_complex_scenario():
    """Erstellt ein komplexes Szenario mit verschiedenen Objekten und Ereignissen."""
    engine = AdvancedConsciousnessEngine()
    
    # Initialisiere die Grundkontexte
    c0 = engine.create_context("I want to be happy", "0", 0.5)
    cA = engine.create_context("I am happy when I learn", "A", 0.7)
    cB = engine.create_context("I learn by reading", "B", 0.6)
    cC = engine.create_context("I learn by experiencing", "C", 0.5)
    cD = engine.create_context("Reading books is enjoyable", "D", 0.8)
    cE = engine.create_context("Experiencing new things can be scary", "E", -0.2)
    cF = engine.create_context("I read books every day", "F", 0.7)
    cG = engine.create_context("I try new experiences occasionally", "G", 0.3)
    cH = engine.create_context("I need energy to learn", "H", 0.4)
    cI = engine.create_context("Food gives me energy", "I", 0.6)
    cJ = engine.create_context("Healthy food is better for energy", "J", 0.5)
    
    # Verbinde die Kontexte
    engine.connect_contexts(c0, cA)
    engine.connect_contexts(cA, cB)
    engine.connect_contexts(cA, cC)
    engine.connect_contexts(cB, cD)
    engine.connect_contexts(cC, cE)
    engine.connect_contexts(cD, cF)
    engine.connect_contexts(cE, cG)
    engine.connect_contexts(cA, cH)
    engine.connect_contexts(cH, cI)
    engine.connect_contexts(cI, cJ)
    
    # Initialisiere die Umgebung
    engine.environment.add_object("apple", {
        "edible": True,
        "tasty": True,
        "color": "red",
        "nutrition": 0.7,
        "healthy": True
    })
    
    engine.environment.add_object("chocolate", {
        "edible": True,
        "tasty": True,
        "color": "brown",
        "nutrition": 0.3,
        "healthy": False
    })
    
    engine.environment.add_object("book", {
        "edible": False,
        "readable": True,
        "knowledge": 0.9,
        "title": "Learning Python"
    })
    
    engine.environment.add_object("museum", {
        "edible": False,
        "visitable": True,
        "experience": 0.8,
        "knowledge": 0.7
    })
    
    # Füge Ereignisse hinzu
    engine.environment.add_event({
        "type": "found",
        "object": "book",
        "time": "today"
    })
    
    engine.environment.add_event({
        "type": "ate",
        "object": "apple",
        "time": "morning"
    })
    
    engine.environment.add_event({
        "type": "visited",
        "object": "museum",
        "time": "last week"
    })
    
    # Setze den initialen Fokus
    engine.set_focus(c0)
    
    return engine


def simulate_learning_process(engine: AdvancedConsciousnessEngine, iterations: int = 30):
    """Simuliert einen längeren Lernprozess und verfolgt die Veränderungen."""
    # Speichere die ursprünglichen Glückswerte
    original_happiness = {label: context.happiness for label, context in engine.contexts.items()}
    
    # Führe den Denkprozess für mehrere Iterationen durch
    for i in range(iterations):
        # Führe Lern- und Wahrnehmungsprozesse durch
        if i % 3 == 0:
            engine.learn_from_experience()
        if i % 4 == 0:
            engine.perceive_environment()
        if i % 5 == 0:
            engine.create_new_connections()
        
        # Finde den nächsten Fokus
        next_focus = engine.find_best_next_focus()
        if next_focus:
            engine.set_focus(next_focus)
    
    # Speichere die neuen Glückswerte
    new_happiness = {label: context.happiness for label, context in engine.contexts.items()}
    
    # Visualisiere die Veränderungen
    labels = list(original_happiness.keys())
    original_values = [original_happiness[label] for label in labels]
    new_values = [new_happiness[label] for label in labels]
    
    x = np.arange(len(labels))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.bar(x - width/2, original_values, width, label='Ursprüngliche Glückswerte')
    ax.bar(x + width/2, new_values, width, label='Neue Glückswerte')
    
    ax.set_xlabel('Kontext')
    ax.set_ylabel('Glückswert')
    ax.set_title('Veränderung der Glückswerte durch Lernen')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('learning_process.png')
    plt.close()
    
    print("Lernprozess wurde als 'learning_process.png' gespeichert.")
    
    # Zähle die neuen Verbindungen
    connection_count = {}
    for label, context in engine.contexts.items():
        connection_count[label] = len(context.connections)
    
    # Visualisiere die Verbindungen
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(connection_count.keys(), connection_count.values(), color='green')
    ax.set_xlabel('Kontext')
    ax.set_ylabel('Anzahl der Verbindungen')
    ax.set_title('Anzahl der Verbindungen pro Kontext nach dem Lernprozess')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('connection_count.png')
    plt.close()
    
    print("Verbindungsanzahl wurde als 'connection_count.png' gespeichert.")


def main():
    print("=== Test der erweiterten Version des künstlichen Bewusstseins ===\n")
    
    # Erstelle ein komplexes Szenario
    print("\n=== Komplexes Szenario ===")
    engine = create_complex_scenario()
    
    print("Initialer Zustand:")
    print(f"Fokus: {engine.current_focus}")
    print(f"Pfad: {' -> '.join([str(c) for c in engine.current_path])}")
    print(f"Emotionaler Zustand: {engine.emotional_state}")
    
    # Visualisiere den emotionalen Zustand über die Zeit
    print("\nVisualisierung des emotionalen Zustands über die Zeit:")
    visualize_emotional_state_over_time(engine, 15)
    
    # Simuliere einen längeren Lernprozess
    print("\nSimulation eines längeren Lernprozesses:")
    simulate_learning_process(engine, 30)
    
    # Visualisiere die Gedächtniskonsolidierung
    print("\nVisualisierung der Gedächtniskonsolidierung:")
    visualize_memory_consolidation(engine)
    
    print("\n=== Test abgeschlossen ===")


if __name__ == "__main__":
    main() 