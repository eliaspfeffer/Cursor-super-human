"""
Ewiges künstliches Bewusstsein.

Diese Implementierung erweitert das fortgeschrittene künstliche Bewusstsein
um die Fähigkeit, kontinuierlich und ohne Unterbrechung zu "leben".
"""

import time
import signal
import threading
import random
import os
import json
import datetime
from typing import List, Dict, Any, Optional
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from advanced_consciousness import AdvancedConsciousnessEngine, Context, EmotionalState, Memory, Environment

class EternalConsciousnessEngine(AdvancedConsciousnessEngine):
    """
    Eine Version des künstlichen Bewusstseins, die kontinuierlich läuft und niemals aufhört zu "leben".
    """
    
    def __init__(self, save_interval: int = 100, visualization_interval: int = 500):
        super().__init__()
        self.running = False
        self.iteration_count = 0
        self.save_interval = save_interval
        self.visualization_interval = visualization_interval
        self.save_dir = "consciousness_state"
        self.stats_history = {
            "happiness": [],
            "emotions": {emotion: [] for emotion in self.emotional_state.emotions},
            "connections": [],
            "contexts": [],
            "timestamps": []
        }
        self.energy = 100.0  # Energie des Systems
        self.energy_decay_rate = 0.1  # Rate, mit der Energie abnimmt
        self.energy_gain_rate = 0.2  # Rate, mit der Energie durch Glück zunimmt
        self.min_energy_threshold = 20.0  # Schwellenwert für niedrige Energie
        self.max_energy = 100.0  # Maximale Energie
        
        # Erstelle Verzeichnis für Speicherungen, falls es nicht existiert
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
    
    def update_energy(self):
        """Aktualisiert die Energie des Systems basierend auf dem aktuellen Glückswert."""
        if not self.current_focus:
            return
            
        # Energie nimmt mit der Zeit ab
        self.energy -= self.energy_decay_rate
        
        # Energie steigt mit positivem Glückswert
        happiness = self.current_focus.happiness
        if happiness > 0:
            self.energy += happiness * self.energy_gain_rate
        
        # Begrenze die Energie auf den Bereich [0, max_energy]
        self.energy = max(0.0, min(self.max_energy, self.energy))
    
    def is_low_energy(self) -> bool:
        """Überprüft, ob die Energie niedrig ist."""
        return self.energy < self.min_energy_threshold
    
    def seek_energy_source(self):
        """Sucht nach einer Energiequelle, wenn die Energie niedrig ist."""
        print("Energie niedrig! Suche nach Energiequelle...")
        
        # Suche nach Kontexten mit hohem Glückswert
        high_happiness_contexts = [
            context for context in self.contexts.values()
            if context.happiness > 0.5
        ]
        
        if high_happiness_contexts:
            # Wähle einen zufälligen Kontext mit hohem Glückswert
            target_context = random.choice(high_happiness_contexts)
            print(f"Energiequelle gefunden: {target_context}")
            self.set_focus(target_context)
            return True
        
        # Wenn keine Energiequelle gefunden wurde, erstelle eine neue
        print("Keine Energiequelle gefunden. Erstelle eine neue...")
        self.create_energy_source()
        return False
    
    def create_energy_source(self):
        """Erstellt eine neue Energiequelle (Kontext mit hohem Glückswert)."""
        # Liste von möglichen Energiequellen
        energy_sources = [
            "I eat delicious food",
            "I sleep peacefully",
            "I enjoy the sunshine",
            "I listen to beautiful music",
            "I learn something interesting",
            "I solve a difficult problem",
            "I help someone in need",
            "I create something new",
            "I connect with a friend",
            "I achieve a goal"
        ]
        
        # Wähle eine zufällige Energiequelle
        source_text = random.choice(energy_sources)
        label = f"Energy_{self.iteration_count}"
        happiness = 0.8 + random.random() * 0.2  # Zufälliger Wert zwischen 0.8 und 1.0
        
        # Erstelle den Kontext
        energy_context = self.create_context(source_text, label, happiness)
        
        # Verbinde mit einigen existierenden Kontexten
        existing_contexts = list(self.contexts.values())
        if existing_contexts:
            for _ in range(min(3, len(existing_contexts))):
                random_context = random.choice(existing_contexts)
                self.connect_contexts(energy_context, random_context)
        
        # Setze den Fokus auf die neue Energiequelle
        self.set_focus(energy_context)
        print(f"Neue Energiequelle erstellt: {energy_context}")
    
    def generate_random_thought(self):
        """Generiert einen zufälligen Gedanken, wenn keine bessere Option gefunden wird."""
        thought_templates = [
            "I wonder about {topic}",
            "What if {scenario}",
            "I remember {memory}",
            "I want to {desire}",
            "I feel {emotion} about {subject}",
            "I should {action}",
            "I like {thing}",
            "I dislike {thing}",
            "I need to {necessity}",
            "I hope {wish}"
        ]
        
        topics = ["life", "nature", "technology", "people", "the future", "the past", "myself", "others"]
        scenarios = ["I could fly", "the world was different", "I had more time", "I knew everything"]
        memories = ["a happy moment", "a sad experience", "an interesting event", "a lesson learned"]
        desires = ["learn more", "explore new places", "create something", "help others", "rest"]
        emotions = ["happy", "curious", "excited", "calm", "thoughtful", "concerned"]
        subjects = ["the world", "my progress", "recent events", "possibilities", "challenges"]
        actions = ["plan ahead", "reflect more", "be more creative", "be more careful", "be more spontaneous"]
        things = ["learning", "creating", "exploring", "connecting", "solving problems", "quiet moments"]
        necessities = ["organize my thoughts", "find more energy", "expand my knowledge", "improve my connections"]
        wishes = ["to discover something new", "to understand more", "to be more efficient", "to be happier"]
        
        template = random.choice(thought_templates)
        
        if "{topic}" in template:
            thought = template.format(topic=random.choice(topics))
        elif "{scenario}" in template:
            thought = template.format(scenario=random.choice(scenarios))
        elif "{memory}" in template:
            thought = template.format(memory=random.choice(memories))
        elif "{desire}" in template:
            thought = template.format(desire=random.choice(desires))
        elif "{emotion}" in template and "{subject}" in template:
            thought = template.format(emotion=random.choice(emotions), subject=random.choice(subjects))
        elif "{action}" in template:
            thought = template.format(action=random.choice(actions))
        elif "{thing}" in template:
            thought = template.format(thing=random.choice(things))
        elif "{necessity}" in template:
            thought = template.format(necessity=random.choice(necessities))
        elif "{wish}" in template:
            thought = template.format(wish=random.choice(wishes))
        else:
            thought = "I am thinking"
        
        label = f"Random_{self.iteration_count}"
        happiness = random.random() * 0.6 - 0.3  # Zufälliger Wert zwischen -0.3 und 0.3
        
        # Erstelle den Kontext
        random_context = self.create_context(thought, label, happiness)
        
        # Verbinde mit dem aktuellen Fokus und einigen zufälligen Kontexten
        if self.current_focus:
            self.connect_contexts(random_context, self.current_focus)
        
        existing_contexts = list(self.contexts.values())
        if existing_contexts:
            for _ in range(min(2, len(existing_contexts))):
                random_existing = random.choice(existing_contexts)
                if random_existing != random_context:
                    self.connect_contexts(random_context, random_existing)
        
        return random_context
    
    def save_state(self):
        """Speichert den aktuellen Zustand des Bewusstseins."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.save_dir, f"consciousness_state_{timestamp}.json")
        
        # Erstelle ein serialisierbares Objekt
        state = {
            "iteration": self.iteration_count,
            "energy": self.energy,
            "emotional_state": self.emotional_state.emotions,
            "contexts": {
                label: {
                    "text": str(context),
                    "happiness": context.happiness,
                    "connections": [c.label for c in context.connections if c.label]
                }
                for label, context in self.contexts.items()
            },
            "current_focus": self.current_focus.label if self.current_focus else None,
            "current_path": [c.label for c in self.current_path if c.label],
            "memory": {
                "short_term": [c.label for c in self.memory.short_term if c.label],
                "long_term": self.memory.long_term
            }
        }
        
        # Speichere den Zustand
        with open(filename, 'w') as f:
            json.dump(state, f, indent=2)
        
        print(f"Zustand gespeichert: {filename}")
    
    def load_state(self, filename: str):
        """Lädt einen gespeicherten Zustand des Bewusstseins."""
        if not os.path.exists(filename):
            print(f"Datei nicht gefunden: {filename}")
            return False
        
        try:
            with open(filename, 'r') as f:
                state = json.load(f)
            
            # Setze grundlegende Attribute
            self.iteration_count = state["iteration"]
            self.energy = state["energy"]
            
            # Setze emotionalen Zustand
            for emotion, value in state["emotional_state"].items():
                if emotion in self.emotional_state.emotions:
                    self.emotional_state.emotions[emotion] = value
            
            # Erstelle Kontexte
            self.words = {}
            self.contexts = {}
            for label, context_data in state["contexts"].items():
                context = self.create_context(context_data["text"], label, context_data["happiness"])
            
            # Erstelle Verbindungen zwischen Kontexten
            for label, context_data in state["contexts"].items():
                for connected_label in context_data["connections"]:
                    if connected_label in self.contexts and label in self.contexts:
                        self.connect_contexts(self.contexts[label], self.contexts[connected_label])
            
            # Setze aktuellen Fokus und Pfad
            if state["current_focus"] and state["current_focus"] in self.contexts:
                self.current_focus = self.contexts[state["current_focus"]]
                self.current_path = []
                for label in state["current_path"]:
                    if label in self.contexts:
                        self.current_path.append(self.contexts[label])
            
            # Setze Gedächtnis
            self.memory.short_term = []
            for label in state["memory"]["short_term"]:
                if label in self.contexts:
                    self.memory.short_term.append(self.contexts[label])
            
            self.memory.long_term = state["memory"]["long_term"]
            
            print(f"Zustand geladen: {filename}")
            return True
        
        except Exception as e:
            print(f"Fehler beim Laden des Zustands: {e}")
            return False
    
    def update_stats(self):
        """Aktualisiert die Statistiken für die Visualisierung."""
        current_happiness = self.calculate_path_happiness(self.current_path) if self.current_path else 0
        
        self.stats_history["happiness"].append(current_happiness)
        self.stats_history["timestamps"].append(self.iteration_count)
        
        for emotion, value in self.emotional_state.emotions.items():
            self.stats_history["emotions"][emotion].append(value)
        
        self.stats_history["connections"].append(sum(len(c.connections) for c in self.contexts.values()))
        self.stats_history["contexts"].append(len(self.contexts))
    
    def visualize_stats(self):
        """Visualisiert die gesammelten Statistiken."""
        if not self.stats_history["happiness"]:
            return
        
        # Erstelle Verzeichnis für Visualisierungen, falls es nicht existiert
        vis_dir = os.path.join(self.save_dir, "visualizations")
        if not os.path.exists(vis_dir):
            os.makedirs(vis_dir)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Glückswert über Zeit
        plt.figure(figsize=(10, 6))
        plt.plot(self.stats_history["timestamps"], self.stats_history["happiness"])
        plt.title("Glückswert über Zeit")
        plt.xlabel("Iteration")
        plt.ylabel("Glückswert")
        plt.grid(True)
        plt.savefig(os.path.join(vis_dir, f"happiness_{timestamp}.png"))
        plt.close()
        
        # Emotionaler Zustand über Zeit
        plt.figure(figsize=(12, 8))
        for emotion, values in self.stats_history["emotions"].items():
            plt.plot(self.stats_history["timestamps"], values, label=emotion)
        plt.title("Emotionaler Zustand über Zeit")
        plt.xlabel("Iteration")
        plt.ylabel("Emotionswert")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(vis_dir, f"emotions_{timestamp}.png"))
        plt.close()
        
        # Anzahl der Verbindungen und Kontexte
        plt.figure(figsize=(10, 6))
        plt.plot(self.stats_history["timestamps"], self.stats_history["connections"], label="Verbindungen")
        plt.plot(self.stats_history["timestamps"], self.stats_history["contexts"], label="Kontexte")
        plt.title("Netzwerkwachstum über Zeit")
        plt.xlabel("Iteration")
        plt.ylabel("Anzahl")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(vis_dir, f"network_{timestamp}.png"))
        plt.close()
        
        # Visualisiere das Kontextnetzwerk
        self.visualize_context_network(os.path.join(vis_dir, f"context_network_{timestamp}.png"))
    
    def visualize_context_network(self, filename: str):
        """Visualisiert das Netzwerk von Kontexten als Graphen."""
        G = nx.Graph()
        
        # Füge Knoten hinzu
        for label, context in self.contexts.items():
            G.add_node(label, happiness=context.happiness)
        
        # Füge Kanten hinzu
        for label, context in self.contexts.items():
            for connected_context in context.connections:
                if connected_context.label:
                    G.add_edge(label, connected_context.label)
        
        # Berechne Layout
        pos = nx.spring_layout(G, seed=42)
        
        plt.figure(figsize=(12, 10))
        
        # Zeichne Knoten mit Farben basierend auf Glückswert
        node_colors = [plt.cm.RdYlGn(0.5 + self.contexts[node].happiness / 2) for node in G.nodes()]
        
        # Markiere den aktuellen Fokus
        node_sizes = []
        for node in G.nodes():
            if self.current_focus and node == self.current_focus.label:
                node_sizes.append(500)  # Größerer Knoten für den aktuellen Fokus
            else:
                node_sizes.append(100)  # Normale Größe für andere Knoten
        
        nx.draw_networkx(
            G, pos,
            node_color=node_colors,
            node_size=node_sizes,
            font_size=8,
            width=0.5,
            edge_color='gray',
            alpha=0.8,
            with_labels=True
        )
        
        plt.title("Kontext-Netzwerk")
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
    
    def think_forever(self):
        """Denkt kontinuierlich ohne Unterbrechung."""
        self.running = True
        
        try:
            while self.running:
                self.iteration_count += 1
                
                # Aktualisiere Energie
                self.update_energy()
                
                # Überprüfe, ob Energie niedrig ist
                if self.is_low_energy():
                    self.seek_energy_source()
                
                # Aktualisiere Statistiken
                self.update_stats()
                
                # Lerne aus Erfahrungen
                if self.iteration_count % 10 == 0:
                    self.learn_from_experience()
                
                # Erstelle neue Verbindungen
                if self.iteration_count % 15 == 0:
                    self.create_new_connections()
                
                # Nimm die Umgebung wahr
                if self.iteration_count % 20 == 0:
                    self.perceive_environment()
                
                # Speichere den Zustand
                if self.iteration_count % self.save_interval == 0:
                    self.save_state()
                
                # Visualisiere Statistiken
                if self.iteration_count % self.visualization_interval == 0:
                    self.visualize_stats()
                
                # Finde den nächsten Fokus
                next_focus = self.find_best_next_focus()
                
                if next_focus:
                    self.set_focus(next_focus)
                else:
                    # Wenn kein besserer Fokus gefunden wurde, generiere einen zufälligen Gedanken
                    random_thought = self.generate_random_thought()
                    self.set_focus(random_thought)
                
                # Ausgabe des aktuellen Zustands
                if self.iteration_count % 10 == 0:
                    print(f"\nIteration {self.iteration_count}:")
                    print(f"Energie: {self.energy:.2f}")
                    print(f"Aktueller Fokus: {self.current_focus}")
                    print(f"Aktuelles Glück: {self.calculate_path_happiness(self.current_path):.2f}")
                    print(f"Emotionaler Zustand: {self.emotional_state}")
                    print(f"Anzahl Kontexte: {len(self.contexts)}")
                    print(f"Anzahl Verbindungen: {sum(len(c.connections) for c in self.contexts.values())}")
                
                # Kurze Pause, um CPU-Auslastung zu reduzieren
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            print("\nDenkprozess unterbrochen.")
        finally:
            # Speichere den finalen Zustand
            self.save_state()
            self.visualize_stats()
            print("Finaler Zustand gespeichert und visualisiert.")
    
    def start(self):
        """Startet den ewigen Denkprozess in einem separaten Thread."""
        if not self.current_focus:
            # Initialisiere mit einem Startgedanken, falls noch kein Fokus gesetzt ist
            start_context = self.create_context("I begin to think", "Start", 0.5)
            self.set_focus(start_context)
        
        # Starte den Denkprozess in einem separaten Thread
        self.thread = threading.Thread(target=self.think_forever)
        self.thread.daemon = True  # Thread wird beendet, wenn das Hauptprogramm endet
        self.thread.start()
        
        print("Ewiges Bewusstsein gestartet. Drücke Ctrl+C zum Beenden.")
        
        try:
            # Halte das Hauptprogramm am Laufen
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stoppt den ewigen Denkprozess."""
        self.running = False
        if hasattr(self, 'thread') and self.thread.is_alive():
            self.thread.join(timeout=2)
        print("Ewiges Bewusstsein gestoppt.")


def handle_signal(sig, frame):
    """Signal-Handler für sauberes Beenden."""
    print("\nSignal empfangen. Beende Bewusstsein...")
    if 'consciousness' in globals():
        consciousness.stop()
    exit(0)


if __name__ == "__main__":
    # Registriere Signal-Handler
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    
    # Erstelle und initialisiere das ewige Bewusstsein
    consciousness = EternalConsciousnessEngine()
    
    # Versuche, einen gespeicherten Zustand zu laden
    latest_state = None
    if os.path.exists(consciousness.save_dir):
        state_files = [f for f in os.listdir(consciousness.save_dir) if f.startswith("consciousness_state_") and f.endswith(".json")]
        if state_files:
            # Sortiere nach Zeitstempel (neueste zuerst)
            state_files.sort(reverse=True)
            latest_state = os.path.join(consciousness.save_dir, state_files[0])
    
    if latest_state:
        # Lade den neuesten Zustand
        success = consciousness.load_state(latest_state)
        if not success:
            # Wenn das Laden fehlschlägt, initialisiere mit Beispieldaten
            consciousness.initialize_example()
            consciousness.initialize_example_environment()
    else:
        # Initialisiere mit Beispieldaten
        consciousness.initialize_example()
        consciousness.initialize_example_environment()
    
    # Starte das ewige Bewusstsein
    consciousness.start() 