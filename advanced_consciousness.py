"""
Erweiterte Version des künstlichen Bewusstseins.

Diese Version erweitert das Grundmodell um Lernfähigkeiten, emotionale Zustände
und die Fähigkeit, mit der Umgebung zu interagieren.
"""

from artificial_consciousness import Word, Context, ConsciousnessEngine
from typing import List, Dict, Set, Tuple, Optional, Any
import numpy as np
import random


class EmotionalState:
    """Repräsentiert den emotionalen Zustand des Bewusstseins."""
    
    def __init__(self):
        # Grundlegende Emotionen mit Werten zwischen -1 und 1
        self.emotions = {
            "happiness": 0.0,
            "sadness": 0.0,
            "fear": 0.0,
            "anger": 0.0,
            "surprise": 0.0,
            "disgust": 0.0,
            "trust": 0.0,
            "anticipation": 0.0
        }
        
        # Gewichtungen für die Emotionen bei der Entscheidungsfindung
        self.weights = {
            "happiness": 1.0,
            "sadness": -0.8,
            "fear": -0.6,
            "anger": -0.7,
            "surprise": 0.3,
            "disgust": -0.5,
            "trust": 0.7,
            "anticipation": 0.5
        }
    
    def update_from_context(self, context: Context):
        """Aktualisiert den emotionalen Zustand basierend auf einem Kontext."""
        # Einfache Implementierung: Glückswert beeinflusst Emotionen
        if context.happiness > 0:
            self.emotions["happiness"] += context.happiness * 0.2
            self.emotions["sadness"] -= context.happiness * 0.1
            self.emotions["trust"] += context.happiness * 0.1
        else:
            self.emotions["sadness"] -= context.happiness * 0.2
            self.emotions["happiness"] += context.happiness * 0.1
            self.emotions["disgust"] -= context.happiness * 0.1
        
        # Begrenze die Werte auf den Bereich [-1, 1]
        for emotion in self.emotions:
            self.emotions[emotion] = max(-1.0, min(1.0, self.emotions[emotion]))
    
    def get_weighted_emotional_value(self) -> float:
        """Berechnet einen gewichteten Wert für den emotionalen Zustand."""
        return sum(self.emotions[e] * self.weights[e] for e in self.emotions)
    
    def __str__(self):
        return ", ".join([f"{e}: {v:.2f}" for e, v in self.emotions.items()])


class Memory:
    """Repräsentiert das Gedächtnis des Bewusstseins."""
    
    def __init__(self, capacity: int = 100):
        self.short_term = []  # Kurzeitgedächtnis (Liste von Kontexten)
        self.long_term = {}   # Langzeitgedächtnis (Dict von Kontext-Label zu Häufigkeit)
        self.capacity = capacity
    
    def add_to_short_term(self, context: Context):
        """Fügt einen Kontext zum Kurzzeitgedächtnis hinzu."""
        self.short_term.append(context)
        if len(self.short_term) > self.capacity:
            # Entferne den ältesten Eintrag
            self.short_term.pop(0)
    
    def consolidate_to_long_term(self):
        """Konsolidiert Einträge aus dem Kurzzeitgedächtnis ins Langzeitgedächtnis."""
        for context in self.short_term:
            if context.label:
                if context.label in self.long_term:
                    self.long_term[context.label] += 1
                else:
                    self.long_term[context.label] = 1
    
    def get_most_frequent_contexts(self, n: int = 5) -> List[str]:
        """Gibt die n häufigsten Kontexte aus dem Langzeitgedächtnis zurück."""
        sorted_contexts = sorted(self.long_term.items(), key=lambda x: x[1], reverse=True)
        return [label for label, _ in sorted_contexts[:n]]


class Environment:
    """Repräsentiert die Umgebung, mit der das Bewusstsein interagieren kann."""
    
    def __init__(self):
        self.objects = {}  # Objekte in der Umgebung
        self.events = []   # Ereignisse, die in der Umgebung auftreten
    
    def add_object(self, name: str, properties: Dict[str, Any]):
        """Fügt ein Objekt zur Umgebung hinzu."""
        self.objects[name] = properties
    
    def add_event(self, event: Dict[str, Any]):
        """Fügt ein Ereignis zur Umgebung hinzu."""
        self.events.append(event)
    
    def get_perception(self) -> Dict[str, Any]:
        """Gibt die aktuelle Wahrnehmung der Umgebung zurück."""
        # Einfache Implementierung: Gibt alle Objekte und die letzten 3 Ereignisse zurück
        return {
            "objects": self.objects,
            "events": self.events[-3:] if self.events else []
        }


class AdvancedConsciousnessEngine(ConsciousnessEngine):
    """Erweiterte Version des künstlichen Bewusstseins."""
    
    def __init__(self):
        super().__init__()
        self.emotional_state = EmotionalState()
        self.memory = Memory()
        self.environment = Environment()
        self.learning_rate = 0.1
    
    def set_focus(self, context: Context):
        """Überschreibt die set_focus-Methode, um emotionale Zustände zu aktualisieren."""
        super().set_focus(context)
        self.emotional_state.update_from_context(context)
        self.memory.add_to_short_term(context)
    
    def calculate_path_happiness(self, path: List[Context]) -> float:
        """Überschreibt die calculate_path_happiness-Methode, um emotionale Zustände einzubeziehen."""
        base_happiness = super().calculate_path_happiness(path)
        emotional_factor = self.emotional_state.get_weighted_emotional_value()
        
        # Kombiniere Glückswert und emotionalen Faktor
        return base_happiness * (1.0 + 0.2 * emotional_factor)
    
    def learn_from_experience(self):
        """Lernt aus Erfahrungen und passt Glückswerte an."""
        if len(self.current_path) < 2:
            return
        
        # Konsolidiere Gedächtnis
        self.memory.consolidate_to_long_term()
        
        # Passe Glückswerte basierend auf der Häufigkeit im Langzeitgedächtnis an
        for label, frequency in self.memory.long_term.items():
            if label in self.contexts:
                context = self.contexts[label]
                # Häufig besuchte Kontexte werden leicht positiver bewertet
                context.happiness += self.learning_rate * (frequency / 10) * 0.01
                # Begrenze den Glückswert
                context.happiness = max(-1.0, min(1.0, context.happiness))
    
    def create_new_connections(self):
        """Erstellt neue Verbindungen zwischen Kontexten basierend auf Erfahrungen."""
        if len(self.current_path) < 3:
            return
        
        # Verbinde nicht-benachbarte Kontexte im aktuellen Pfad mit geringer Wahrscheinlichkeit
        for i in range(len(self.current_path) - 2):
            for j in range(i + 2, len(self.current_path)):
                if random.random() < 0.1:  # 10% Chance
                    self.connect_contexts(self.current_path[i], self.current_path[j])
    
    def perceive_environment(self):
        """Nimmt die Umgebung wahr und erstellt daraus neue Kontexte."""
        perception = self.environment.get_perception()
        
        # Erstelle neue Kontexte aus wahrgenommenen Objekten
        for obj_name, properties in perception["objects"].items():
            if "edible" in properties and properties["edible"]:
                text = f"I can eat {obj_name}"
                happiness = 0.5 if properties.get("tasty", False) else 0.1
                context = self.create_context(text, f"Obj_{obj_name}", happiness)
                
                # Verbinde mit relevanten existierenden Kontexten
                for existing in self.contexts.values():
                    if "eat" in str(existing) and random.random() < 0.3:
                        self.connect_contexts(context, existing)
    
    def think_advanced(self, iterations: int = 10):
        """Erweiterte Denkfunktion mit Lernen und Umgebungswahrnehmung."""
        for i in range(iterations):
            print(f"\nIteration {i+1}:")
            print(f"Aktueller Fokus: {self.current_focus}")
            print(f"Aktueller Pfad: {' -> '.join([str(c) for c in self.current_path])}")
            print(f"Aktuelles Glück: {self.calculate_path_happiness(self.current_path)}")
            print(f"Emotionaler Zustand: {self.emotional_state}")
            
            # Lerne aus Erfahrungen
            if i % 3 == 0:  # Alle 3 Iterationen
                self.learn_from_experience()
                print("Lerne aus Erfahrungen...")
            
            # Erstelle neue Verbindungen
            if i % 5 == 0:  # Alle 5 Iterationen
                self.create_new_connections()
                print("Erstelle neue Verbindungen...")
            
            # Nimm die Umgebung wahr
            if i % 4 == 0:  # Alle 4 Iterationen
                self.perceive_environment()
                print("Nehme Umgebung wahr...")
            
            # Finde den nächsten Fokus
            next_focus = self.find_best_next_focus()
            
            if next_focus:
                print(f"Neuer Fokus: {next_focus}")
                self.set_focus(next_focus)
            else:
                print("Kein besserer Fokus gefunden. Bleibe beim aktuellen.")
    
    def initialize_example_environment(self):
        """Initialisiert eine Beispielumgebung."""
        # Füge Objekte hinzu
        self.environment.add_object("apple", {
            "edible": True,
            "tasty": True,
            "color": "red",
            "nutrition": 0.7
        })
        
        self.environment.add_object("banana", {
            "edible": True,
            "tasty": False,
            "color": "yellow",
            "nutrition": 0.8
        })
        
        self.environment.add_object("book", {
            "edible": False,
            "readable": True,
            "knowledge": 0.9
        })
        
        # Füge Ereignisse hinzu
        self.environment.add_event({
            "type": "found",
            "object": "apple",
            "time": "now"
        })
        
        self.environment.add_event({
            "type": "read",
            "object": "book",
            "time": "yesterday"
        })


# Beispiel für die Verwendung
if __name__ == "__main__":
    engine = AdvancedConsciousnessEngine()
    engine.initialize_example()  # Grundlegende Kontexte
    engine.initialize_example_environment()  # Umgebung
    
    print("Initialer Zustand:")
    print(f"Fokus: {engine.current_focus}")
    print(f"Pfad: {engine.current_path}")
    print(f"Emotionaler Zustand: {engine.emotional_state}")
    
    # Führe den erweiterten Denkprozess durch
    engine.think_advanced(15) 