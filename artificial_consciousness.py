"""
Künstliches Bewusstsein basierend auf dem Reasoning for AGI-Modell.

Dieses Modul implementiert ein künstliches Bewusstsein, das auf der Verbindung von Wörtern
und Kontexten basiert, mit einem Fokus-Mechanismus und einer Glücksbewertung.
"""

import numpy as np
from typing import List, Dict, Set, Tuple, Optional
import math
import heapq
import time


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
    """Erweiterte Kontext-Klasse mit Reasoning-Fähigkeiten."""
    def __init__(self, words: List[Word], label: str = None, happiness: float = 0.0):
        super().__init__(words, label, happiness)
        self.truth_value = 0.5
        self.source_type = None
        self.references = []
        self.contradictions = []
        self.consistency_cache = {}
        self.connections = {}  # Dict von Context zu ConnectionInfo

    def calculate_truth_value(self, all_contexts: Dict[str, 'ReasoningContext']) -> float:
        """Berechnet den Wahrhaftigkeitswert basierend auf Konsistenz und Verbindungen."""
        # Grundwert basierend auf Quelle
        if self.source_type == 'wikipedia':
            base_truth = 0.7  # Wikipedia starts with higher base truth
            # Erhöhe für Artikel mit vielen Referenzen
            if len(self.references) > 5:
                base_truth += 0.1
        else:
            base_truth = 0.5  # Chat input starts neutral

        # Konsistenzprüfung
        consistency_score = 0.0
        contradiction_penalty = 0.0
        
        # Prüfe Konsistenz mit verbundenen Kontexten
        connected_contexts = [all_contexts[label] for label in self.connections 
                            if label in all_contexts]
        
        if connected_contexts:
            for other in connected_contexts:
                # Berechne Übereinstimmung der Wörter
                common_words = set(w.content for w in self.words) & set(w.content for w in other.words)
                if common_words:
                    # Wenn gemeinsame Wörter gefunden wurden, prüfe auf Widersprüche
                    if other in self.contradictions:
                        contradiction_penalty += 0.1
                    else:
                        consistency_score += len(common_words) / len(self.words)

            consistency_score /= len(connected_contexts)
        
        # Verbindungsdichte-Bonus
        connection_density = len(self.connections) / max(1, len(all_contexts))
        density_bonus = min(0.2, connection_density)
        
        # Mehrsprachiger Bonus (wenn der gleiche Inhalt in verschiedenen Sprachen existiert)
        multilingual_bonus = 0.0
        if self.source_type == 'wikipedia':
            # Implementierung vereinfacht - würde normalerweise Sprachversionen prüfen
            multilingual_bonus = 0.1 if len(self.references) > 3 else 0.0
        
        # Kombiniere alle Faktoren
        final_truth = base_truth + \
                     (consistency_score * 0.3) - \
                     contradiction_penalty + \
                     density_bonus + \
                     multilingual_bonus
        
        # Begrenzen auf [0.0, 1.0]
        self.truth_value = max(0.0, min(1.0, final_truth))
        return self.truth_value

    def add_reference(self, reference_context: 'ReasoningContext'):
        """Fügt einen unterstützenden Referenzkontext hinzu."""
        if reference_context not in self.references:
            self.references.append(reference_context)
    
    def add_contradiction(self, contradicting_context: 'ReasoningContext'):
        """Fügt einen widersprechenden Kontext hinzu."""
        if contradicting_context not in self.contradictions:
            self.contradictions.append(contradicting_context)
            # Wenn ein Widerspruch gefunden wird, aktualisiere den Wahrhaftigkeitswert
            self.truth_value *= 0.8  # Reduziere den Wahrhaftigkeitswert
    
    def calculate_consistency(self, other_context: 'ReasoningContext') -> float:
        """Berechnet die semantische Konsistenz zwischen zwei Kontexten."""
        # Cache-Check
        cache_key = (self.label, other_context.label)
        if cache_key in self.consistency_cache:
            return self.consistency_cache[cache_key]
        
        # Wenn eine direkte Verbindung existiert, nutze deren Stärke
        if other_context in self.connections:
            consistency = self.connections[other_context].strength
        else:
            # Berechne Wort-basierte Konsistenz
            words1 = set(w.content for w in self.words)
            words2 = set(w.content for w in other_context.words)
            
            # Jaccard-Index für Wortüberlappung
            intersection = len(words1 & words2)
            union = len(words1 | words2)
            consistency = intersection / union if union > 0 else 0.0
        
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
            if path[i+1] in path[i].connections:
                relation_score += path[i].connections[path[i+1]].strength
        
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
        """Findet den besten Reasoning-Pfad zwischen diesem und dem Zielkontext mit optimierter Suche."""
        if self == target_context:
            return [self], 1.0

        # Initialisiere bidirektionale Suche
        forward_frontier = [(0, [self])]  # Von Start zum Ziel
        backward_frontier = [(0, [target_context])]  # Von Ziel zum Start
        forward_visited = {self.label: 0}  # Label -> Pfadlänge
        backward_visited = {target_context.label: 0}
        best_path = None
        best_score = float('-inf')
        
        # Cache für Nachbarschaftsfilterung
        neighbor_cache = {}
        
        def filter_neighbors(context: ReasoningContext, direction: str) -> List[Tuple[ReasoningContext, float]]:
            """Filtert und sortiert Nachbarn nach Relevanz."""
            cache_key = (context.label, direction)
            if cache_key in neighbor_cache:
                return neighbor_cache[cache_key]
            
            neighbors = []
            for next_context in context.connections:
                if not isinstance(next_context, ReasoningContext):
                    continue
                
                # Berechne einen schnellen Relevanz-Score
                connection_info = context.connections[next_context]
                relevance = connection_info.strength
                
                # Berücksichtige Richtung der Suche
                if direction == 'forward':
                    heuristic = next_context.calculate_consistency(target_context)
                else:
                    heuristic = next_context.calculate_consistency(self)
                
                combined_score = relevance * 0.7 + heuristic * 0.3
                neighbors.append((next_context, combined_score))
            
            # Sortiere nach Score und behalte nur die Top-K
            neighbors.sort(key=lambda x: x[1], reverse=True)
            top_k = neighbors[:min(10, len(neighbors))]  # Maximale Verzweigung begrenzen
            
            neighbor_cache[cache_key] = top_k
            return top_k
        
        def try_connect_paths(forward_path: List[ReasoningContext], backward_path: List[ReasoningContext]) -> Tuple[List[ReasoningContext], float]:
            """Versucht, zwei Teilpfade zu verbinden."""
            # Prüfe direkte Verbindung zwischen Endpunkten
            forward_end = forward_path[-1]
            backward_start = backward_path[0]
            
            if backward_start in forward_end.connections:
                # Verbinde die Pfade
                complete_path = forward_path + backward_path[1:]
                return complete_path, self.calculate_path_score(complete_path)
            
            return None, float('-inf')
        
        while forward_frontier and backward_frontier:
            # Expandiere vorwärts
            if forward_frontier:
                current_score, current_path = heapq.heappop(forward_frontier)
                current_node = current_path[-1]
                current_depth = forward_visited[current_node.label]
                
                if current_depth < max_depth:
                    # Expandiere gefilterte Nachbarn
                    for next_node, relevance in filter_neighbors(current_node, 'forward'):
                        if next_node.label in forward_visited:
                            continue
                        
                        new_path = current_path + [next_node]
                        path_score = self.calculate_path_score(new_path)
                        forward_visited[next_node.label] = current_depth + 1
                        
                        # Versuche Verbindung mit rückwärts-Pfaden
                        if next_node.label in backward_visited:
                            for _, back_path in backward_frontier:
                                if back_path[0].label == next_node.label:
                                    connected_path, connected_score = try_connect_paths(new_path, back_path)
                                    if connected_path and connected_score > best_score:
                                        best_path = connected_path
                                        best_score = connected_score
                        
                        heapq.heappush(forward_frontier, (-path_score, new_path))
            
            # Expandiere rückwärts
            if backward_frontier:
                current_score, current_path = heapq.heappop(backward_frontier)
                current_node = current_path[0]
                current_depth = backward_visited[current_node.label]
                
                if current_depth < max_depth:
                    # Expandiere gefilterte Nachbarn
                    for next_node, relevance in filter_neighbors(current_node, 'backward'):
                        if next_node.label in backward_visited:
                            continue
                        
                        new_path = [next_node] + current_path
                        path_score = self.calculate_path_score(new_path)
                        backward_visited[next_node.label] = current_depth + 1
                        
                        # Versuche Verbindung mit vorwärts-Pfaden
                        if next_node.label in forward_visited:
                            for _, forward_path in forward_frontier:
                                if forward_path[-1].label == next_node.label:
                                    connected_path, connected_score = try_connect_paths(forward_path, new_path)
                                    if connected_path and connected_score > best_score:
                                        best_path = connected_path
                                        best_score = connected_score
                        
                        heapq.heappush(backward_frontier, (-path_score, new_path))
            
            # Früher Abbruch, wenn ein guter Pfad gefunden wurde
            if best_score > 0.8:  # Schwellenwert für "guten" Pfad
                break
        
        if best_path:
            return best_path, best_score
        return [], 0.0


class ConnectionInfo:
    """Repräsentiert eine Verbindung zwischen zwei Kontexten."""
    def __init__(self, target_context: ReasoningContext):
        self.target = target_context
        self.strength = 0.0  # Stärke der Verbindung (0.0 bis 1.0)
        self.type = "neutral"  # Art der Verbindung
        self.shared_words = set()  # Gemeinsame Wörter
        self.interaction_count = 0  # Wie oft wurde diese Verbindung genutzt
        self.last_interaction = None  # Zeitpunkt der letzten Interaktion
    
    def update_strength(self):
        """Aktualisiert die Verbindungsstärke basierend auf verschiedenen Faktoren."""
        # Basisstärke durch gemeinsame Wörter
        word_strength = len(self.shared_words) * 0.1
        
        # Bonus für häufige Interaktionen, aber mit Dämpfung
        interaction_bonus = min(0.3, self.interaction_count * 0.05)
        
        # Typ-basierte Modifikation
        type_modifier = {
            "supports": 0.2,      # Unterstützende Verbindung
            "contradicts": -0.3,  # Widersprechende Verbindung
            "implies": 0.15,      # Implikation
            "example": 0.1,       # Beispiel/Instanz
            "neutral": 0.0        # Neutrale Verbindung
        }.get(self.type, 0.0)
        
        # Kombiniere alle Faktoren
        self.strength = min(1.0, max(0.0,
            word_strength + interaction_bonus + type_modifier
        ))


class ConsciousnessEngine:
    """Basis-Engine für künstliches Bewusstsein."""
    def __init__(self):
        self.words = {}  # Dict von Wort-Inhalt zu Word-Objekt
        self.contexts = {}  # Dict von Kontext-Label zu Context-Objekt
        self.current_focus = None  # Aktueller Fokus-Kontext
        self.energy = 1.0  # Energie des Bewusstseins
        self.honeypots = []  # Liste von Honeypot-Kontexten
        self.truth_threshold = 0.6  # Schwellenwert für Wahrhaftigkeit
        self.conversation_path = []  # Explizite Speicherung des Konversationspfades
        self.current_topic = []  # Aktuelles Gesprächsthema (Liste von Schlüsselwörtern)
    
    def get_or_create_word(self, content: str) -> Word:
        """Holt ein existierendes Wort oder erstellt ein neues."""
        if content not in self.words:
            word = Word(content)
            self.words[content] = word
        return self.words[content]
    
    def create_context(self, text: str, label: str = None, happiness: float = 0.0, source_type: str = 'chat') -> ReasoningContext:
        """Erstellt einen neuen Kontext aus einem Text."""
        words = [self.get_or_create_word(word) for word in text.split()]
        context = ReasoningContext(words, label, happiness)
        context.source_type = source_type
        
        if label:
            self.contexts[label] = context
            # Berechne initialen Wahrhaftigkeitswert basierend auf allen existierenden Kontexten
            context.calculate_truth_value(self.contexts)
        
        return context
    
    def connect_contexts(self, context1: ReasoningContext, context2: ReasoningContext, connection_type: str = "neutral"):
        """Verbindet zwei Kontexte mit verfeinertem Scoring."""
        if not isinstance(context1, ReasoningContext) or not isinstance(context2, ReasoningContext):
            raise TypeError("Beide Kontexte müssen ReasoningContext-Instanzen sein")
        
        # Finde gemeinsame Wörter
        words1 = set(w.content for w in context1.words)
        words2 = set(w.content for w in context2.words)
        shared_words = words1 & words2
        
        # Erstelle Verbindungsinformationen in beide Richtungen
        if context2 not in context1.connections:
            connection1 = ConnectionInfo(context2)
            context1.connections[context2] = connection1
        else:
            connection1 = context1.connections[context2]
        
        if context1 not in context2.connections:
            connection2 = ConnectionInfo(context1)
            context2.connections[context1] = connection2
        else:
            connection2 = context2.connections[context1]
        
        # Aktualisiere Verbindungsinformationen
        for connection in [connection1, connection2]:
            connection.type = connection_type
            connection.shared_words = shared_words
            connection.interaction_count += 1
            connection.last_interaction = time.time()
            connection.update_strength()
        
        # Wenn es sich um einen Widerspruch handelt
        if connection_type == "contradicts":
            context1.add_contradiction(context2)
            context2.add_contradiction(context1)
        
        # Wenn es sich um eine unterstützende Verbindung handelt
        elif connection_type == "supports":
            context1.add_reference(context2)
            context2.add_reference(context1)
    
    def set_focus(self, context: Context):
        """Setzt den Fokus auf einen bestimmten Kontext."""
        self.current_focus = context
        if isinstance(context, ReasoningContext):
            self.add_to_conversation(context)
    
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
        
        best_happiness = self.calculate_path_happiness(self.conversation_path)
        best_next_context = None
        
        # Für jede mögliche nächste Verbindung
        for next_context in connections:
            # Wenn wir bereits auf diesem Pfad sind, überspringen
            if next_context in self.conversation_path:
                continue
                
            # Simuliere das Hinzufügen dieses Kontexts zum Pfad
            simulated_path = self.conversation_path + [next_context]
            
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
        if len(self.conversation_path) > 1:
            previous_context = self.conversation_path[-2]
            alternative_paths = []
            
            # Finde alternative Pfade vom vorherigen Kontext
            for alt_next in previous_context.connections:
                if alt_next != self.current_focus and alt_next not in self.conversation_path:
                    alt_path = self.conversation_path[:-1] + [alt_next]
                    alternative_paths.append((alt_next, self.calculate_path_happiness(alt_path)))
            
            # Wenn es bessere alternative Pfade gibt
            if alternative_paths:
                best_alt_context, best_alt_happiness = max(alternative_paths, key=lambda x: x[1])
                if best_alt_happiness > best_happiness:
                    # Es ist besser, zurückzugehen und einen anderen Pfad zu nehmen
                    self.conversation_path.pop()  # Entferne den aktuellen Fokus
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
            print(f"Aktueller Pfad: {' -> '.join([str(c) for c in self.conversation_path])}")
            print(f"Aktuelles Glück: {self.calculate_path_happiness(self.conversation_path)}")
            
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
        """Führt einen Denkschritt mit Reasoning durch, unter Berücksichtigung der Konversationshistorie."""
        if not self.current_focus or not isinstance(self.current_focus, ReasoningContext):
            return None
        
        # Hole die Konversationshistorie
        conversation_history = self.conversation_path[-10:]  # Betrachte bis zu 10 Kontexte
        
        best_next_context = None
        best_path_score = -float('inf')
        
        # Sammle potenzielle nächste Kontexte
        potential_next_contexts = set()
        
        # Füge direkt verbundene Kontexte hinzu
        for next_context in self.current_focus.connections:
            if isinstance(next_context, ReasoningContext):
                potential_next_contexts.add(next_context)
        
        # Füge Kontexte hinzu, die mit der Historie verbunden sind
        for i, hist_context in enumerate(conversation_history):
            if isinstance(hist_context, ReasoningContext):
                # Zeitliche Gewichtung: Neuere Kontexte haben mehr Einfluss
                recency_weight = 0.7 ** (len(conversation_history) - 1 - i)
                
                for connected in hist_context.connections:
                    if isinstance(connected, ReasoningContext):
                        potential_next_contexts.add(connected)
        
        # Bewerte jeden potenziellen nächsten Kontext
        for next_context in potential_next_contexts:
            # Finde den besten Pfad zum nächsten Kontext
            path, base_score = self.find_reasoning_path(self.current_focus, next_context)
            
            if not self.validate_reasoning_path(path):
                continue
            
            # Berechne zusätzliche Scores
            history_score = 0.0
            relevance_to_history = 0.0
            topic_relevance = 0.0
            
            # Gewichtete Historien-Scores
            total_weight = 0
            for i, hist_context in enumerate(conversation_history):
                if isinstance(hist_context, ReasoningContext):
                    # Zeitliche Gewichtung
                    recency_weight = 0.7 ** (len(conversation_history) - 1 - i)
                    total_weight += recency_weight
                    
                    # Konsistenz mit historischen Kontexten
                    consistency = next_context.calculate_consistency(hist_context)
                    history_score += consistency * recency_weight
                    
                    # Relevanz zur Historie
                    if next_context in hist_context.connections:
                        connection_info = hist_context.connections[next_context]
                        relevance_to_history += connection_info.strength * recency_weight
            
            # Normalisiere die Scores
            if total_weight > 0:
                history_score /= total_weight
                relevance_to_history /= total_weight
            
            # Thematische Relevanz
            if self.current_topic:
                topic_words = set(self.current_topic)
                context_words = set(w.content for w in next_context.words)
                topic_overlap = len(topic_words & context_words) / len(topic_words) if topic_words else 0
                topic_relevance = topic_overlap
            
            # Kombiniere die Scores
            combined_score = (
                base_score * 0.35 +                # Basis-Pfad-Score
                history_score * 0.25 +             # Historien-Konsistenz
                relevance_to_history * 0.15 +      # Relevanz zur Historie
                topic_relevance * 0.15 +           # Thematische Relevanz
                (1.0 - (len(self.conversation_path) / max(100, len(self.contexts)))) * 0.1  # Aktualität
            )
            
            if combined_score > best_path_score:
                best_path_score = combined_score
                best_next_context = next_context
        
        # Füge den ausgewählten Kontext zum Konversationspfad hinzu
        if best_next_context:
            self.add_to_conversation(best_next_context)
        
        return best_next_context

    def add_to_conversation(self, context: ReasoningContext):
        """Fügt einen Kontext zum Konversationspfad hinzu."""
        self.conversation_path.append(context)
        # Begrenze die Länge des Pfades
        if len(self.conversation_path) > 20:  # Längere Historie für Themenanalyse
            self.conversation_path.pop(0)
        self.update_current_topic()

    def update_current_topic(self):
        """Aktualisiert das aktuelle Gesprächsthema basierend auf der Historie."""
        if not self.conversation_path:
            return
        
        # Extrahiere häufige Wörter aus den letzten Kontexten
        word_counts = {}
        for context in self.conversation_path[-5:]:  # Betrachte die letzten 5 Kontexte
            for word in context.words:
                word_counts[word.content] = word_counts.get(word.content, 0) + 1
        
        # Einfache Stoppwortliste
        stopwords = {'der', 'die', 'das', 'und', 'ist', 'in', 'mit', 'für', 'von', 'zu', 'ein', 'eine', 'einen', 'auf', 'bei', 'es', 'an', 'als', 'am', 'um', 'aus', 'wie', 'im', 'so', 'zum', 'zur', 'oder', 'aber', 'auch', 'sich', 'dem', 'den', 'des', 'dass', 'daß', 'wenn', 'weil', 'doch', 'noch', 'nur', 'schon', 'sehr', 'hier', 'da', 'dort', 'dann', 'nach', 'über', 'vor', 'durch', 'bis', 'gegen', 'ohne', 'unter', 'was', 'wer', 'wo', 'wie', 'wann', 'warum', 'wieso', 'weshalb', 'welche', 'welcher', 'welches', 'werden', 'wurde', 'wurden', 'sein', 'seine', 'seinen', 'seiner', 'seines', 'ihr', 'ihre', 'ihren', 'ihrer', 'ihres', 'mein', 'meine', 'meinen', 'meiner', 'meines', 'dein', 'deine', 'deinen', 'deiner', 'deines', 'unser', 'unsere', 'unseren', 'unserer', 'unseres', 'euer', 'eure', 'euren', 'eurer', 'eures', 'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'to', 'of', 'for', 'with', 'by', 'at', 'in', 'on', 'from', 'this', 'that', 'these', 'those', 'it', 'its', 'they', 'them', 'their', 'he', 'him', 'his', 'she', 'her', 'hers', 'we', 'us', 'our', 'you', 'your', 'yours', 'i', 'me', 'my', 'mine', 'who', 'whom', 'whose', 'which', 'what', 'when', 'where', 'why', 'how'}
        
        # Filtere Stoppwörter und finde die häufigsten Wörter
        filtered_words = {word: count for word, count in word_counts.items() if word.lower() not in stopwords and len(word) > 2}
        top_words = sorted(filtered_words.items(), key=lambda x: x[1], reverse=True)[:5]
        self.current_topic = [word for word, _ in top_words]




# Beispiel für die Verwendung
if __name__ == "__main__":
    engine = ConsciousnessEngine()
    engine.initialize_example()
    
    print("Initialer Zustand:")
    print(f"Fokus: {engine.current_focus}")
    print(f"Pfad: {engine.conversation_path}")
    
    # Führe den Denkprozess durch
    engine.think(10) 