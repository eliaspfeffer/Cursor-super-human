"""
Künstliches Bewusstsein basierend auf dem Reasoning for AGI-Modell.

Dieses Modul implementiert ein künstliches Bewusstsein, das auf der Verbindung von Wörtern
und Kontexten basiert, mit einem Fokus-Mechanismus und einer Glücksbewertung.
"""

import numpy as np
from typing import List, Dict, Set, Tuple, Optional


class Word:
    """Repräsentiert ein einzelnes Wort oder eine Information."""
    
    def __init__(self, content: str):
        self.content = content
        self.id = None  # Wird später gesetzt
    
    def __str__(self):
        return self.content
    
    def __repr__(self):
        return f"Word({self.content})"
    
    def __eq__(self, other):
        if isinstance(other, Word):
            return self.content == other.content
        return False
    
    def __hash__(self):
        return hash(self.content)


class Context:
    """Repräsentiert einen Kontext, der aus einer Sequenz von Wörtern besteht."""
    
    def __init__(self, words: List[Word], label: str = None, happiness: float = 0.0):
        self.words = words
        self.label = label
        self.happiness = happiness
        self.connections = set()  # Andere Kontexte, mit denen dieser verbunden ist
    
    def add_connection(self, context: 'Context'):
        """Fügt eine Verbindung zu einem anderen Kontext hinzu."""
        self.connections.add(context)
    
    def __str__(self):
        return " ".join([word.content for word in self.words])
    
    def __repr__(self):
        return f"Context({self.label}: {str(self)})"


class ConsciousnessEngine:
    """Hauptklasse für das künstliche Bewusstsein."""
    
    def __init__(self):
        self.words = {}  # Dict von Wort-Inhalt zu Word-Objekt
        self.contexts = {}  # Dict von Label zu Context-Objekt
        self.current_focus = None  # Aktueller Fokus-Kontext
        self.current_path = []  # Aktueller Pfad von Kontexten
    
    def get_or_create_word(self, content: str) -> Word:
        """Holt ein existierendes Wort oder erstellt ein neues."""
        if content not in self.words:
            word = Word(content)
            self.words[content] = word
        return self.words[content]
    
    def create_context(self, text: str, label: str = None, happiness: float = 0.0) -> Context:
        """Erstellt einen neuen Kontext aus einem Text."""
        words = [self.get_or_create_word(word) for word in text.split()]
        context = Context(words, label, happiness)
        if label:
            self.contexts[label] = context
        return context
    
    def connect_contexts(self, context1: Context, context2: Context):
        """Verbindet zwei Kontexte miteinander."""
        context1.add_connection(context2)
        context2.add_connection(context1)
    
    def set_focus(self, context: Context):
        """Setzt den Fokus auf einen bestimmten Kontext."""
        self.current_focus = context
        if context not in self.current_path:
            self.current_path.append(context)
    
    def calculate_path_happiness(self, path: List[Context]) -> float:
        """Berechnet den Glückswert eines Pfades."""
        return sum(context.happiness for context in path)
    
    def find_best_next_focus(self, depth: int = 2) -> Optional[Context]:
        """
        Findet den besten nächsten Fokus basierend auf dem potenziellen Glück.
        
        Args:
            depth: Wie tief der Algorithmus in die Zukunft schauen soll
            
        Returns:
            Der beste nächste Kontext für den Fokus oder None, wenn kein besserer gefunden wurde
        """
        if not self.current_focus:
            return None
        
        # Aktuelle Verbindungen vom Fokus
        connections = self.current_focus.connections
        
        best_happiness = self.calculate_path_happiness(self.current_path)
        best_next_context = None
        
        # Für jede mögliche nächste Verbindung
        for next_context in connections:
            # Wenn wir bereits auf diesem Pfad sind, überspringen
            if next_context in self.current_path:
                continue
                
            # Simuliere das Hinzufügen dieses Kontexts zum Pfad
            simulated_path = self.current_path + [next_context]
            
            # Wenn wir tiefer schauen wollen
            if depth > 1:
                # Rekursiv weitere mögliche Pfade erkunden
                for future_context in next_context.connections:
                    if future_context not in simulated_path:
                        deeper_path = simulated_path + [future_context]
                        happiness = self.calculate_path_happiness(deeper_path)
                        
                        if happiness > best_happiness:
                            best_happiness = happiness
                            best_next_context = next_context
            else:
                # Einfach den direkten Pfad bewerten
                happiness = self.calculate_path_happiness(simulated_path)
                if happiness > best_happiness:
                    best_happiness = happiness
                    best_next_context = next_context
        
        # Überprüfe auch, ob es besser wäre, zurückzugehen
        if len(self.current_path) > 1:
            previous_context = self.current_path[-2]
            alternative_paths = []
            
            # Finde alternative Pfade vom vorherigen Kontext
            for alt_next in previous_context.connections:
                if alt_next != self.current_focus and alt_next not in self.current_path:
                    alt_path = self.current_path[:-1] + [alt_next]
                    alternative_paths.append((alt_next, self.calculate_path_happiness(alt_path)))
            
            # Wenn es bessere alternative Pfade gibt
            if alternative_paths:
                best_alt_context, best_alt_happiness = max(alternative_paths, key=lambda x: x[1])
                if best_alt_happiness > best_happiness:
                    # Es ist besser, zurückzugehen und einen anderen Pfad zu nehmen
                    self.current_path.pop()  # Entferne den aktuellen Fokus
                    return best_alt_context
        
        return best_next_context
    
    def think(self, iterations: int = 10):
        """
        Führt den Denkprozess für eine bestimmte Anzahl von Iterationen durch.
        
        Args:
            iterations: Anzahl der Denkschritte
        """
        for i in range(iterations):
            print(f"\nIteration {i+1}:")
            print(f"Aktueller Fokus: {self.current_focus}")
            print(f"Aktueller Pfad: {' -> '.join([str(c) for c in self.current_path])}")
            print(f"Aktuelles Glück: {self.calculate_path_happiness(self.current_path)}")
            
            next_focus = self.find_best_next_focus()
            
            if next_focus:
                print(f"Neuer Fokus: {next_focus}")
                self.set_focus(next_focus)
            else:
                print("Kein besserer Fokus gefunden. Bleibe beim aktuellen.")
    
    def initialize_example(self):
        """Initialisiert das Beispiel aus der Aufgabenstellung."""
        # Erstelle die Kontexte
        c0 = self.create_context("I want to be happy", "0", 0.5)
        cA = self.create_context("I am happy when I eat", "A", 0.7)
        cB = self.create_context("I eat what tastes good", "B", 0.6)
        cC = self.create_context("An apple tastes good", "C", 0.8)
        cD = self.create_context("A banana doesnt taste good", "D", -0.3)
        cE = self.create_context("I eat the apple", "E", 0.9)
        cF = self.create_context("I dont eat the apple", "F", -0.2)
        cG = self.create_context("I eat the banana", "G", -0.1)
        cH = self.create_context("I eat what is healthy", "H", 0.4)
        
        # Verbinde die Kontexte
        self.connect_contexts(c0, cA)
        self.connect_contexts(cA, cB)
        self.connect_contexts(cB, cC)
        self.connect_contexts(cB, cD)
        self.connect_contexts(cC, cE)
        self.connect_contexts(cC, cF)
        self.connect_contexts(cD, cG)
        self.connect_contexts(cB, cH)
        
        # Setze den initialen Fokus
        self.set_focus(c0)


# Beispiel für die Verwendung
if __name__ == "__main__":
    engine = ConsciousnessEngine()
    engine.initialize_example()
    
    print("Initialer Zustand:")
    print(f"Fokus: {engine.current_focus}")
    print(f"Pfad: {engine.current_path}")
    
    # Führe den Denkprozess durch
    engine.think(10) 