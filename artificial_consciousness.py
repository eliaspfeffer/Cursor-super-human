"""
Künstliches Bewusstsein basierend auf dem Reasoning for AGI-Modell.

Dieses Modul implementiert ein künstliches Bewusstsein, das auf der Verbindung von Wörtern
und Kontexten basiert, mit einem Fokus-Mechanismus und einer Glücksbewertung.
"""

import numpy as np
from typing import List, Dict, Set, Tuple, Optional
import math
import heapq


class Word:
    """Repräsentiert ein einzelnes Wort oder eine Information."""
    
    def __init__(self, content: str):
        self.content = content
        self.id = None  # Wird später gesetzt
        self.attributes = {}  # Semantische Attribute des Wortes
        self.truth_value = 1.0  # Wahrhaftigkeitswert (0.0 bis 1.0)
    
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


class ReasoningContext(Context):
    """Erweiterte Kontext-Klasse mit Reasoning-Fähigkeiten basierend auf dem AGI-Paper."""
    def __init__(self, words: List[Word], label: str = None, happiness: float = 0.0):
        super().__init__(words, label, happiness)
        self.truth_value = 1.0  # Wahrhaftigkeitswert des Kontexts
        self.attributes = {}  # Extrahierte semantische Attribute
        self.relations = {}  # Beziehungen zu anderen Kontexten mit Gewichtungen
        self.consistency_cache = {}  # Cache für Konsistenzberechnungen
    
    def extract_attributes(self):
        """Extrahiert semantische Attribute aus den Wörtern des Kontexts."""
        # Attribute-Kategorien nach dem AGI-Paper
        self.attributes = {
            "subjects": [],  # Handelnde Entitäten
            "actions": [],   # Aktionen/Verben
            "objects": [],   # Objekte der Handlung
            "properties": [] # Eigenschaften/Adjektive
        }
        
        # Extrahiere Attribute aus Wörtern (vereinfachte Version)
        for word in self.words:
            # TODO: Hier sollte eine echte NLP-Analyse stehen
            # Aktuell nur simple Wortlängen-basierte Kategorisierung
            if len(word.content) > 6:
                self.attributes["subjects"].append(word.content)
            elif word.content.endswith("en"):
                self.attributes["actions"].append(word.content)
            elif word.content.startswith("ge"):
                self.attributes["objects"].append(word.content)
            else:
                self.attributes["properties"].append(word.content)
    
    def calculate_consistency(self, other_context: 'ReasoningContext') -> float:
        """Berechnet die semantische Konsistenz zwischen zwei Kontexten."""
        # Cache-Check
        cache_key = (self.label, other_context.label)
        if cache_key in self.consistency_cache:
            return self.consistency_cache[cache_key]
        
        # Berechne Jaccard-Index für jede Attribut-Kategorie
        consistency = 0.0
        weights = {"subjects": 0.3, "actions": 0.3, "objects": 0.2, "properties": 0.2}
        
        for category in self.attributes:
            set1 = set(self.attributes[category])
            set2 = set(other_context.attributes[category])
            if set1 or set2:  # Wenn mindestens eine Menge nicht leer ist
                intersection = len(set1 & set2)
                union = len(set1 | set2)
                category_consistency = intersection / union if union > 0 else 0
                consistency += category_consistency * weights[category]
        
        # Cache das Ergebnis
        self.consistency_cache[cache_key] = consistency
        return consistency
    
    def calculate_path_score(self, path: List['ReasoningContext']) -> float:
        """Berechnet den Score für einen Reasoning-Pfad."""
        if len(path) < 2:
            return 0.0
        
        # Komponenten des Scores nach dem AGI-Paper
        consistency_score = 0.0  # Semantische Konsistenz
        truth_score = 1.0       # Kombinierte Wahrhaftigkeit
        relation_score = 0.0    # Stärke der Relationen
        length_penalty = 1.0    # Bestrafung für lange Pfade
        
        # Berechne Konsistenz zwischen aufeinanderfolgenden Kontexten
        for i in range(len(path) - 1):
            consistency_score += path[i].calculate_consistency(path[i + 1])
            truth_score *= path[i].truth_value  # Multiplikative Kombination
            
            # Addiere Relationsstärke, falls vorhanden
            if path[i+1].label in path[i].relations:
                relation_score += path[i].relations[path[i+1].label]
        
        # Normalisiere Scores
        consistency_score /= (len(path) - 1)
        relation_score /= (len(path) - 1)
        
        # Längenbestrafung (mehr Schritte = höhere Bestrafung)
        length_penalty = 1.0 / (1.0 + math.log(len(path)))
        
        # Kombiniere alle Komponenten
        final_score = (
            consistency_score * 0.4 +  # Semantische Konsistenz
            truth_score * 0.3 +        # Wahrhaftigkeit
            relation_score * 0.2 +     # Relationsstärke
            length_penalty * 0.1       # Längenbestrafung
        )
        
        return final_score
    
    def find_best_reasoning_path(self, target_context: 'ReasoningContext', max_depth: int = 5) -> Tuple[List['ReasoningContext'], float]:
        """Findet den besten Reasoning-Pfad zwischen diesem und dem Zielkontext."""
        # Implementiere A*-Suche mit Reasoning-Scores
        start_node = self
        goal_node = target_context
        
        # Initialisiere Datenstrukturen für A*
        frontier = [(0, [start_node])]  # Priority Queue mit (score, path)
        visited = set()
        
        while frontier:
            current_score, current_path = heapq.heappop(frontier)
            current_node = current_path[-1]
            
            if current_node == goal_node:
                return current_path, -current_score  # Negiere Score, da heapq minimiert
            
            if len(current_path) >= max_depth:
                continue
                
            if current_node.label in visited:
                continue
                
            visited.add(current_node.label)
            
            # Expandiere Nachbarn
            for next_label, relation_strength in current_node.relations.items():
                if next_label not in visited:
                    next_node = self.contexts[next_label]
                    new_path = current_path + [next_node]
                    
                    # Berechne Score für den neuen Pfad
                    path_score = self.calculate_path_score(new_path)
                    
                    # Heuristik: Direkte Konsistenz zum Ziel
                    heuristic = next_node.calculate_consistency(goal_node)
                    
                    # Kombinierter Score für A*
                    priority = -(path_score + heuristic)  # Negativ für heapq
                    heapq.heappush(frontier, (priority, new_path))
        
        return [], 0.0  # Kein Pfad gefunden


class ConsciousnessEngine:
    """Hauptklasse für das künstliche Bewusstsein."""
    
    def __init__(self):
        self.words = {}  # Dict von Wort-Inhalt zu Word-Objekt
        self.contexts = {}  # Dict von Label zu Context-Objekt
        self.current_focus = None  # Aktueller Fokus-Kontext
        self.current_path = []  # Aktueller Pfad von Kontexten
        self.energy = 100.0  # Anfängliche Energie
        self.honeypots = {}  # Dict von Honeypot-Label zu Honeypot-Objekt
        self.truth_threshold = 0.3  # Minimaler Wahrhaftigkeitswert für valide Pfade
    
    def get_or_create_word(self, content: str) -> Word:
        """Holt ein existierendes Wort oder erstellt ein neues."""
        if content not in self.words:
            word = Word(content)
            self.words[content] = word
        return self.words[content]
    
    def create_context(self, text: str, label: str = None, happiness: float = 0.0) -> ReasoningContext:
        """Erstellt einen neuen Kontext aus einem Text mit Reasoning-Fähigkeiten."""
        words = [self.get_or_create_word(word) for word in text.split()]
        context = ReasoningContext(words, label, happiness)
        
        # Extrahiere semantische Attribute
        context.extract_attributes()
        
        # Berechne initialen Wahrhaftigkeitswert
        # TODO: Hier sollte eine echte Wahrhaftigkeitsanalyse stehen
        # Aktuell: Einfache Heuristik basierend auf Wortlänge und Attribut-Verteilung
        num_attributes = sum(len(attrs) for attrs in context.attributes.values())
        if num_attributes > 0:
            context.truth_value = min(1.0, 0.5 + (num_attributes / 10))
        else:
            context.truth_value = 0.5
        
        if label:
            self.contexts[label] = context
        return context
    
    def connect_contexts(self, context1: ReasoningContext, context2: ReasoningContext, weight: float = None):
        """Verbindet zwei Kontexte mit Reasoning-basierter Gewichtung."""
        if not isinstance(context1, ReasoningContext) or not isinstance(context2, ReasoningContext):
            raise TypeError("Beide Kontexte müssen ReasoningContext-Instanzen sein")
        
        # Berechne Konsistenz zwischen den Kontexten
        consistency = context1.calculate_consistency(context2)
        
        # Wenn keine explizite Gewichtung angegeben wurde, nutze die Konsistenz
        if weight is None:
            weight = consistency
        
        # Speichere die Relation in beiden Kontexten
        context1.relations[context2.label] = weight
        context2.relations[context1.label] = weight
        
        # Füge auch zur traditionellen Verbindungsliste hinzu
        context1.connections.add(context2)
        context2.connections.add(context1)
    
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

    def find_reasoning_path(self, start_context: ReasoningContext, end_context: ReasoningContext) -> Tuple[List[ReasoningContext], float]:
        """Findet den besten Reasoning-Pfad zwischen zwei Kontexten."""
        return start_context.find_best_reasoning_path(end_context)
    
    def validate_reasoning_path(self, path: List[ReasoningContext]) -> bool:
        """Überprüft, ob ein Reasoning-Pfad valid ist."""
        if not path:
            return False
        
        # Prüfe Wahrhaftigkeitswerte
        for context in path:
            if context.truth_value < self.truth_threshold:
                return False
        
        # Berechne Gesamtscore des Pfades
        score = path[0].calculate_path_score(path)
        
        # Der Pfad ist valid, wenn der Score über einem Schwellenwert liegt
        return score > 0.5
    
    def think_with_reasoning(self) -> Optional[ReasoningContext]:
        """Führt einen Denkschritt mit Reasoning durch."""
        if not self.current_focus or not isinstance(self.current_focus, ReasoningContext):
            return None
        
        best_next_context = None
        best_path_score = -float('inf')
        
        # Durchsuche alle verbundenen Kontexte
        for next_context in self.current_focus.connections:
            if not isinstance(next_context, ReasoningContext):
                continue
            
            # Finde den besten Reasoning-Pfad zum nächsten Kontext
            path, score = self.find_reasoning_path(self.current_focus, next_context)
            
            # Wenn der Pfad valid ist und einen besseren Score hat
            if self.validate_reasoning_path(path) and score > best_path_score:
                best_path_score = score
                best_next_context = next_context
        
        return best_next_context


# Beispiel für die Verwendung
if __name__ == "__main__":
    engine = ConsciousnessEngine()
    engine.initialize_example()
    
    print("Initialer Zustand:")
    print(f"Fokus: {engine.current_focus}")
    print(f"Pfad: {engine.current_path}")
    
    # Führe den Denkprozess durch
    engine.think(10) 