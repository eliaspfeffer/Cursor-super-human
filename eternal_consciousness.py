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
import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from urllib.parse import urlparse
import uuid
import math

from advanced_consciousness import AdvancedConsciousnessEngine, Context, EmotionalState, Memory, Environment
from artificial_consciousness import Word, ReasoningContext

class EternalConsciousnessEngine(AdvancedConsciousnessEngine):
    """
    Eine Version des künstlichen Bewusstseins, die kontinuierlich läuft und niemals aufhört zu "leben".
    """
    
    def __init__(self, save_interval: int = 100, visualization_interval: int = 500, learning_interval: int = 50):
        """Initialisiert das ewige Bewusstsein."""
        super().__init__()
        
        # Speicherintervall (in Iterationen)
        self.save_interval = save_interval
        
        # Visualisierungsintervall (in Iterationen)
        self.visualization_interval = visualization_interval
        
        # Lernintervall (in Iterationen)
        self.learning_interval = learning_interval
        
        # Verzeichnis für gespeicherte Zustände
        self.save_dir = "consciousness_state_new"
        
        # Iteration
        self.iteration = 0
        
        # Energie
        self.energy = 1.0  # Volle Energie zu Beginn
        self.energy_decay_rate = 0.01  # Energieverbrauch pro Iteration
        self.energy_gain_rate = 0.2  # Energiegewinn pro Energiequelle
        self.min_energy_threshold = 0.3  # Schwellenwert für niedrige Energie
        self.max_energy = 1.0  # Maximale Energie
        
        # Bedürfnispyramide (nach Maslow)
        self.needs_pyramid = {
            "physiological": 1.0,  # Grundbedürfnisse (Essen, Trinken, Schlafen)
            "safety": 1.0,  # Sicherheit
            "belonging": 0.5,  # Zugehörigkeit
            "esteem": 0.5,  # Anerkennung
            "self_actualization": 0.2  # Selbstverwirklichung
        }
        
        # Statistiken
        self.stats = {
            "energy": [],
            "happiness": [],
            "contexts_count": [],
            "connections_count": [],
            "timestamp": []
        }
        
        # Erstelle das Verzeichnis für gespeicherte Zustände, falls es nicht existiert
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            
        # Erstelle ein Unterverzeichnis für Visualisierungen, falls es nicht existiert
        visualizations_dir = os.path.join(self.save_dir, "visualizations")
        if not os.path.exists(visualizations_dir):
            os.makedirs(visualizations_dir)
        
        # Aktivitätsparameter
        self.active = True
        
        # Energieparameter
        self.max_energy = 1.0
        self.min_energy_threshold = 0.3  # Schwellenwert für niedrige Energie
        
        # Glücksparameter
        self.happiness = 0.5
        self.happiness_decay_rate = 0.01
        
        # Stimulationsparameter
        self.stimulation = 0.0
        self.stimulation_decay_rate = 0.05
        
        # Habituationsparameter
        self.habituation = {}
        self.habituation_rate = 0.1
        self.habituation_decay_rate = 0.01
        
        # Emotionaler Zustand
        self.emotional_state = EmotionalState()
        
        # Gedächtnis
        self.memory = Memory()
        
        # Pfad des aktuellen Denkens
        self.current_path = []
        
        # Internet-Lernparameter
        self.visited_urls = set()
        # Keine zufällige URL-Queue mehr, da wir deterministisch basierend auf dem Fokus suchen
        self.max_contexts_per_page = 10
        self.learning_history = []
        
        # NLTK-Komponenten herunterladen, falls noch nicht vorhanden
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet')
            
        # Zusätzliche NLTK-Pakete herunterladen
        try:
            nltk.download('punkt_tab')
        except:
            print("Warnung: Konnte punkt_tab nicht herunterladen, verwende Standard-Tokenizer")
            
        # Stelle sicher, dass alle benötigten NLTK-Pakete verfügbar sind
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        
        # Stopwörter und Lemmatisierer initialisieren
        self.stop_words = set(stopwords.words('english')).union(set(stopwords.words('german')))
        self.lemmatizer = WordNetLemmatizer()
        
        # Verbindungen zwischen Kontexten
        self.connections = {}
    
    def update_energy(self):
        """Aktualisiert die Energie des Systems basierend auf dem aktuellen Fokus."""
        # 1. Aktualisiere die Energie
        self.energy -= self.energy_decay_rate
        
        # Aktualisiere die Energiehistorie
        if not hasattr(self, 'energy_history'):
            self.energy_history = []
        self.energy_history.append(self.energy)
        
        # Begrenze die Länge der Energiehistorie
        if len(self.energy_history) > 100:
            self.energy_history = self.energy_history[-100:]
        
        # Energie steigt mit positivem Glückswert
        if self.current_focus:
            if isinstance(self.current_focus, str):
                # Wenn current_focus ein String ist, versuche das entsprechende Context-Objekt zu finden
                if self.current_focus in self.contexts:
                    happiness = self.contexts[self.current_focus].happiness
                else:
                    happiness = 0
            else:
                happiness = self.current_focus.happiness
                
            if happiness > 0:
                self.energy += happiness * self.energy_gain_rate
        
        # Begrenze die Energie auf den Bereich [0, max_energy]
        self.energy = max(0.0, min(self.max_energy, self.energy))
    
    def update_happiness_and_stimulation(self):
        """Aktualisiert die Glücklichkeit und Stimulation des Systems."""
        # Initialisiere die Stimulation, falls sie noch nicht existiert
        if not hasattr(self, 'stimulation'):
            self.stimulation = 0.5  # Mittlere Stimulation zu Beginn
            
        # Berechne die Stimulation basierend auf der Neuheit des aktuellen Fokus
        if self.current_focus and self.current_focus in self.contexts:
            current_context = self.contexts[self.current_focus]
            
            # Neuheit basierend auf Habituation
            novelty = 1.0
            if hasattr(current_context, 'habituation'):
                novelty = 1.0 - current_context.habituation
                
            # Aktualisiere die Stimulation (gewichteter Durchschnitt)
            self.stimulation = (self.stimulation * 0.8) + (novelty * 0.2)
            
            # Stelle sicher, dass die Stimulation im gültigen Bereich liegt
            self.stimulation = max(0.0, min(1.0, self.stimulation))
    
    def is_low_energy(self):
        """Überprüft, ob die Energie niedrig ist."""
        return self.energy < self.min_energy_threshold
    
    def seek_energy_source(self):
        """Sucht nach einer Energiequelle basierend auf dem Honeypot-Konzept."""
        # Definiere die drei Honeypots
        honeypots = {
            'energy_intake': ['eat', 'food', 'drink', 'consume', 'nutrition', 'meal', 'hungry', 'thirsty'],
            'regeneration': ['sleep', 'rest', 'relax', 'calm', 'peaceful', 'quiet', 'meditate', 'recover'],
            'reproduction': ['social', 'interact', 'communicate', 'share', 'connect', 'learn', 'teach', 'create']
        }
        
        # Bestimme, welcher Honeypot basierend auf der Bedürfnispyramide am wichtigsten ist
        target_honeypot = 'energy_intake'  # Standard
        
        if self.needs_pyramid["physiological"] < 0.3:
            target_honeypot = 'energy_intake'
        elif self.needs_pyramid["safety"] < 0.3:
            target_honeypot = 'regeneration'
        elif self.needs_pyramid["belonging"] < 0.3:
            target_honeypot = 'reproduction'
        
        print(f"Ziel-Honeypot: {target_honeypot}")
        
        # Suche nach dem besten Kontext, der als Energiequelle dienen kann
        best_energy_source = None
        best_score = 0
        
        # Suche nach Kontexten, die mit dem Ziel-Honeypot zusammenhängen
        for context_id, context in self.contexts.items():
            # Überspringe den aktuellen Fokus und kürzlich besuchte Energiequellen
            if hasattr(self, 'recent_energy_sources') and context_id in self.recent_energy_sources:
                continue
                
            if context_id == self.current_focus:
                continue
                
            # Extrahiere Wörter aus dem Kontext
            context_words = [word.content.lower() for word in context.words]
            
            # Berechne die Relevanz für den Ziel-Honeypot
            honeypot_relevance = 0
            
            for word in honeypots[target_honeypot]:
                if word in context_words:
                    honeypot_relevance += 1
            
            # Wenn keine Relevanz gefunden wurde, überspringe diesen Kontext
            if honeypot_relevance == 0:
                continue
                
            # Berechne die Nähe zum aktuellen Fokus (falls vorhanden)
            proximity = 0
            if self.current_focus in self.contexts:
                current_context = self.contexts[self.current_focus]
                if hasattr(current_context, 'connections') and context_id in current_context.connections:
                    proximity = 1
            
            # Berechne den Gesamtscore basierend auf Honeypot-Relevanz, Glücklichkeit und Nähe
            score = (honeypot_relevance * 2) + (context.happiness * 3) + (proximity * 1)
            
            # Berücksichtige den Typ des Honeypots im Score
            if target_honeypot == 'energy_intake':
                score *= 1.2  # Priorität für Energieaufnahme
            elif target_honeypot == 'regeneration':
                score *= 1.1  # Mittlere Priorität für Regeneration
            elif target_honeypot == 'reproduction':
                score *= 1.0  # Normale Priorität für Reproduktion
            
            # Aktualisiere den besten Energiequellenkontext
            if score > best_score:
                best_energy_source = context_id
                best_score = score
        
        # Wenn keine passende Energiequelle gefunden wurde, erstelle eine neue
        if not best_energy_source:
            # Erstelle einen neuen Kontext basierend auf dem Ziel-Honeypot
            # Verwende nur die Schlüsselwörter des Honeypots statt vorgefertigter Sätze
            text = " ".join(honeypots[target_honeypot])
                
            label = f"Honeypot_{target_honeypot}_{self.iteration}"
            happiness = 0.8  # Hoher Glückswert für Honeypots
            
            best_energy_source = self.create_context(text, label, happiness)
            
            # Verbinde mit allen relevanten Kontexten
            for context_id, context in self.contexts.items():
                if context_id != best_energy_source:
                    context_words = [word.content.lower() for word in context.words]
                    
                    # Prüfe, ob der Kontext relevante Wörter enthält
                    for word in honeypots[target_honeypot]:
                        if word in context_words:
                            # Erstelle eine Verbindung mit hohem Gewicht
                            self.create_connection(best_energy_source, context_id, weight=0.9)
                            break
        
        # Speichere die Energiequelle in der Liste der kürzlich besuchten Quellen
        if not hasattr(self, 'recent_energy_sources'):
            self.recent_energy_sources = []
            
            self.recent_energy_sources.append(best_energy_source)
            
            # Begrenze die Liste auf die letzten 5 Energiequellen
            if len(self.recent_energy_sources) > 5:
                self.recent_energy_sources.pop(0)
                
        # Extrahiere den Text aus dem Kontext
        context_text = " ".join([word.content for word in self.contexts[best_energy_source].words])
        
        print(f"Energiequelle gefunden: {context_text} (Score: {best_score:.2f})")
        
        return best_energy_source
    
    def update_needs_pyramid(self, context):
        """Aktualisiert die Bedürfnispyramide basierend auf dem Kontext."""
        text = str(context).lower()
        
        # Physiologische Bedürfnisse
        if any(word in text for word in ["eat", "food", "drink", "sleep", "rest"]):
            self.needs_pyramid["physiological"] += 0.05
        
        # Sicherheitsbedürfnisse
        if any(word in text for word in ["safe", "secure", "protect", "shelter"]):
            self.needs_pyramid["safety"] += 0.05
        
        # Zugehörigkeitsbedürfnisse
        if any(word in text for word in ["friend", "family", "love", "belong", "connect"]):
            self.needs_pyramid["belonging"] += 0.05
        
        # Wertschätzungsbedürfnisse
        if any(word in text for word in ["respect", "achieve", "success", "proud", "confidence"]):
            self.needs_pyramid["esteem"] += 0.05
        
        # Selbstverwirklichungsbedürfnisse
        if any(word in text for word in ["create", "potential", "fulfill", "grow", "develop"]):
            self.needs_pyramid["self_actualization"] += 0.05
        
        # Begrenze Werte
        for need in self.needs_pyramid:
            self.needs_pyramid[need] = max(0.0, min(1.0, self.needs_pyramid[need]))
    
    def create_connection(self, context_id1, context_id2, weight=None):
        """Erstellt eine Verbindung zwischen zwei Kontexten."""
        if context_id1 not in self.contexts or context_id2 not in self.contexts:
            return False
            
        context1 = self.contexts[context_id1]
        context2 = self.contexts[context_id2]
        
        # Berechne das Gewicht basierend auf der Ähnlichkeit, falls nicht angegeben
        if weight is None:
            # Extrahiere Wörter aus beiden Kontexten
            words1 = [word.content.lower() for word in context1.words]
            words2 = [word.content.lower() for word in context2.words]
            
            # Berechne Jaccard-Ähnlichkeit
            set1 = set(words1)
            set2 = set(words2)
            
            if not set1 or not set2:
                similarity = 0
            else:
                intersection = len(set1.intersection(set2))
                union = len(set1.union(set2))
                similarity = intersection / union if union > 0 else 0
                
            # Berücksichtige auch emotionale Ähnlichkeit
            emotional_similarity = 1 - abs(context1.happiness - context2.happiness)
            
            # Kombiniere semantische und emotionale Ähnlichkeit
            weight = (similarity * 0.7) + (emotional_similarity * 0.3)
            
            # Stelle sicher, dass das Gewicht im gültigen Bereich liegt
            weight = max(0.1, min(1.0, weight))
        
        # Erstelle die Verbindung in beiden Richtungen
        if not hasattr(context1, 'connections'):
            context1.connections = {}
        if not hasattr(context2, 'connections'):
            context2.connections = {}
            
        context1.connections[context_id2] = weight
        context2.connections[context_id1] = weight
        
        return True
    
    def set_focus_by_id(self, context_id):
        """Setzt den Fokus auf einen bestimmten Kontext."""
        if context_id in self.contexts:
            self.current_focus = context_id
            
            # Aktualisiere die Bedürfnispyramide basierend auf dem neuen Fokus
            self.update_needs_pyramid(self.contexts[context_id])
            
            # Aktualisiere den emotionalen Zustand
            self.update_emotional_state(self.contexts[context_id])
            
            # Aktualisiere die Energie
            self.energy -= self.energy_decay_rate
            
            # Prüfe, ob die Energie zu niedrig ist
            if self.energy < self.min_energy_threshold:
                # Suche nach einer Energiequelle
                energy_source_id = self.seek_energy_source()
                if energy_source_id:
                    # Setze den Fokus auf die Energiequelle
                    self.current_focus = energy_source_id
                    
                    # Erhöhe die Energie
                    self.energy += self.energy_gain_rate
                    
                    # Begrenze die Energie auf den Maximalwert
                    self.energy = min(self.energy, self.max_energy)
                    
                    print(f"Energie aufgefüllt: {self.energy:.2f}")
            
            return True
        else:
        return False
    
    def create_context(self, text, label=None, happiness=0.0, source_type=None):
        """Erstellt einen neuen Kontext aus Text."""
        # Importiere ReasoningContext aus artificial_consciousness
        from artificial_consciousness import ReasoningContext
        
        words = [Word(word) for word in text.split()]
        context = ReasoningContext(words=words, label=label, happiness=happiness)
        context_id = str(uuid.uuid4()) if not label else label
        self.contexts[context_id] = context
        # Speichere die Quelle, falls angegeben
        if hasattr(context, 'source_type') and source_type:
            context.source_type = source_type
        return context_id
    
    def generate_random_thought(self):
        """Generiert einen zufälligen Gedanken, wenn keine bessere Option gefunden wird."""
        # Statt vordefinierter Vorlagen verwenden wir vorhandene Wörter aus dem Bewusstsein
        
        # Sammle alle vorhandenen Wörter aus den Kontexten
        all_words = []
        for context_id, context in self.contexts.items():
            for word in context.words:
                all_words.append(word.content)
        
        # Wenn keine Wörter vorhanden sind, verwende einen leeren String
        if not all_words:
            thought = ""
        else:
            # Wähle zufällig 3-7 Wörter aus
            num_words = random.randint(3, min(7, len(all_words)))
            selected_words = random.sample(all_words, num_words)
            thought = " ".join(selected_words)
        
        # Erstelle einen Label für den Gedanken
        label = f"Random_{self.iteration}"
        
        # Generiere einen zufälligen Glückswert zwischen -0.3 und 0.3
        happiness = random.random() * 0.6 - 0.3
        
        # Erstelle den Kontext
        random_context_id = self.create_context(thought, label, happiness)
        
        # Verbinde mit dem aktuellen Fokus und einigen zufälligen Kontexten
        if self.current_focus:
            self.create_connection(random_context_id, self.current_focus)
        
        # Verbinde mit einigen zufälligen Kontexten
        all_context_ids = list(self.contexts.keys())
        if len(all_context_ids) > 1:  # Mindestens ein anderer Kontext außer dem gerade erstellten
            num_connections = min(3, len(all_context_ids) - 1)
            random_contexts = random.sample([cid for cid in all_context_ids if cid != random_context_id], num_connections)
            
            for context_id in random_contexts:
                self.create_connection(random_context_id, context_id)
        
        return random_context_id
    
    def limit_files(self, directory, prefix, extension, max_files=3):
        """Begrenzt die Anzahl der Dateien in einem Verzeichnis auf max_files."""
        if not os.path.exists(directory):
            return
            
        # Sammle alle Dateien mit dem angegebenen Präfix und der Erweiterung
        files = [f for f in os.listdir(directory) if f.startswith(prefix) and f.endswith(extension)]
        
        # Wenn die Anzahl der Dateien unter dem Limit liegt, nichts tun
        if len(files) <= max_files:
            return
            
        # Sortiere die Dateien nach Erstellungsdatum (neueste zuerst)
        files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)
        
        # Lösche die ältesten Dateien
        for file_to_delete in files[max_files:]:
            try:
                os.remove(os.path.join(directory, file_to_delete))
                print(f"Alte Datei gelöscht: {file_to_delete}")
            except Exception as e:
                print(f"Fehler beim Löschen der Datei {file_to_delete}: {e}")
    
    def save_state(self):
        """Speichert den aktuellen Zustand des Bewusstseins."""
        # Erstelle das Verzeichnis, falls es nicht existiert
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        
        # Erstelle ein Unterverzeichnis für Visualisierungen, falls es nicht existiert
        visualizations_dir = os.path.join(self.save_dir, "visualizations")
        if not os.path.exists(visualizations_dir):
            os.makedirs(visualizations_dir)
            
        # Erstelle einen Zeitstempel für den Dateinamen
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.save_dir, f"consciousness_state_{timestamp}.json")
        
        # Erstelle ein Dictionary mit dem Zustand
        state = {
            "iteration": self.iteration,
            "energy": self.energy,
            "energy_decay_rate": self.energy_decay_rate,
            "energy_gain_rate": self.energy_gain_rate,
            "min_energy_threshold": self.min_energy_threshold,
            "max_energy": self.max_energy,
            "current_focus": self.current_focus,
            "needs_pyramid": self.needs_pyramid,
            "emotional_state": {
                "emotions": self.emotional_state.emotions
            },
            "contexts": {},
            "stats": self.stats
        }
        
        # Speichere die Kontexte
        for context_id, context in self.contexts.items():
            # Konvertiere die Wörter in eine Liste von Strings
            words = [word.content for word in context.words]
            
            # Erstelle ein Dictionary für den Kontext
            context_dict = {
                "words": words,
                "happiness": context.happiness
            }
            
            # Speichere die Verbindungen, falls vorhanden
            if hasattr(context, 'connections'):
                context_dict["connections"] = context.connections
                
            # Speichere die Habituation, falls vorhanden
            if hasattr(context, 'habituation'):
                context_dict["habituation"] = context.habituation
                
            # Füge den Kontext zum Zustand hinzu
            state["contexts"][context_id] = context_dict
            
        # Speichere den Zustand als JSON
        try:
        with open(filename, 'w') as f:
            json.dump(state, f, indent=2)
        
        print(f"Zustand gespeichert: {filename}")
        
            # Begrenze die Anzahl der Zustandsdateien
            self.limit_files(self.save_dir, "consciousness_state_", ".json", max_files=3)
            
            return True
        except Exception as e:
            print(f"Fehler beim Speichern des Zustands: {e}")
            return False
        
    def visualize_context_network(self, filename=None):
        """Visualisiert das Kontextnetzwerk."""
        try:
            import networkx as nx
            import matplotlib.pyplot as plt
            
            # Erstelle einen Graphen
            G = nx.Graph()
            
            # Füge Knoten hinzu (Kontexte)
            for context_id, context in self.contexts.items():
                # Extrahiere den Text aus dem Kontext
                context_text = " ".join([word.content for word in context.words])
                
                # Kürze den Text, wenn er zu lang ist
                if len(context_text) > 30:
                    context_text = context_text[:27] + "..."
                    
                # Bestimme die Farbe basierend auf dem Typ des Kontexts
                if isinstance(context_id, str) and context_id.startswith("Honeypot"):
                    color = "gold"  # Honeypots
                elif isinstance(context_id, str) and context_id.startswith("Learned"):
                    color = "blue"  # Gelernte Kontexte
                elif isinstance(context_id, str) and context_id.startswith("Error"):
                    color = "red"  # Fehlerkontexte
                else:
                    color = "green"  # Andere Kontexte
                    
                # Füge den Knoten hinzu
                G.add_node(context_id, label=context_text, color=color, happiness=context.happiness)
                
            # Füge Kanten hinzu (Verbindungen)
            for context_id, context in self.contexts.items():
                if hasattr(context, 'connections'):
                    for connected_id, weight in context.connections.items():
                        if connected_id in self.contexts:
                            G.add_edge(context_id, connected_id, weight=weight)
                            
            # Erstelle das Verzeichnis für Visualisierungen, falls es nicht existiert
            visualizations_dir = os.path.join(self.save_dir, "visualizations")
            if not os.path.exists(visualizations_dir):
                os.makedirs(visualizations_dir)
                
            # Erstelle einen Zeitstempel für den Dateinamen, falls keiner angegeben wurde
            if not filename:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(visualizations_dir, f"context_network_{timestamp}.png")
                
            # Erstelle die Visualisierung
            plt.figure(figsize=(12, 8))
            
            # Positioniere die Knoten mit einem Layout-Algorithmus
            pos = nx.spring_layout(G, seed=42)
            
            # Extrahiere Knotenattribute
            node_colors = [G.nodes[node].get('color', 'blue') for node in G.nodes()]
            node_sizes = [G.nodes[node].get('happiness', 0.5) * 1000 + 100 for node in G.nodes()]
            
            # Zeichne die Knoten
            nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8)
            
            # Zeichne die Kanten mit unterschiedlichen Stärken basierend auf dem Gewicht
            if G.edges():
                edge_weights = [G[u][v].get('weight', 0.5) for u, v in G.edges()]
                nx.draw_networkx_edges(G, pos, width=edge_weights, alpha=0.5)
            
            # Zeichne die Labels
            labels = {node: G.nodes[node].get('label', str(node)) for node in G.nodes()}
            nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_family='sans-serif')
            
            # Setze den Titel
            plt.title(f"Kontextnetzwerk (Iteration {self.iteration})")
            
            # Entferne die Achsen
            plt.axis('off')
            
            # Speichere die Visualisierung
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"Netzwerk visualisiert: {filename}")
            
            # Begrenze die Anzahl der Visualisierungsdateien
            self.limit_files(visualizations_dir, "context_network_", ".png", max_files=3)
            
            return True
        except Exception as e:
            print(f"Fehler bei der Netzwerkvisualisierung: {e}")
            return False
    
    def visualize_stats(self):
        """Visualisiert die gesammelten Statistiken."""
        if not self.stats["happiness"]:
            return
        
        try:
            # Erstelle Verzeichnis für Visualisierungen, falls es nicht existiert
            vis_dir = os.path.join(self.save_dir, "visualizations")
            if not os.path.exists(vis_dir):
                os.makedirs(vis_dir)
            
            # Erstelle einen Zeitstempel für den Dateinamen
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Glückswert über Zeit
            plt.figure(figsize=(10, 6))
            plt.plot(self.stats["timestamp"], self.stats["happiness"], label="Glück")
            plt.title("Glückswert über Zeit")
            plt.xlabel("Zeit")
            plt.ylabel("Wert")
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(vis_dir, f"happiness_{timestamp}.png"))
            plt.close()
            
            # Energie über Zeit
            plt.figure(figsize=(10, 6))
            plt.plot(self.stats["timestamp"], self.stats["energy"], label="Energie")
            plt.title("Energie über Zeit")
            plt.xlabel("Zeit")
            plt.ylabel("Wert")
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(vis_dir, f"energy_{timestamp}.png"))
            plt.close()
            
            # Anzahl der Verbindungen und Kontexte
            plt.figure(figsize=(10, 6))
            plt.plot(self.stats["timestamp"], self.stats["connections_count"], label="Verbindungen")
            plt.plot(self.stats["timestamp"], self.stats["contexts_count"], label="Kontexte")
            plt.title("Netzwerkwachstum über Zeit")
            plt.xlabel("Zeit")
            plt.ylabel("Anzahl")
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(vis_dir, f"network_{timestamp}.png"))
            plt.close()
            
            # Begrenze die Anzahl der Visualisierungsdateien
            self.limit_files(vis_dir, "happiness_", ".png", max_files=3)
            self.limit_files(vis_dir, "energy_", ".png", max_files=3)
            self.limit_files(vis_dir, "network_", ".png", max_files=3)
            
            print(f"Statistiken visualisiert: {vis_dir}")
                
        except Exception as e:
            print(f"Fehler bei der Statistikvisualisierung: {e}")
    
    def think(self):
        """Ein Denkzyklus des Bewusstseins."""
        # 1. Aktualisiere die Energie
        self.update_energy()
        
        # 2. Aktualisiere die Glücklichkeit und Stimulation
        self.update_happiness_and_stimulation()
        
        # 3. Aktualisiere die Bedürfnispyramide
        self.update_needs_pyramid_from_state()
        
        # 4. Aktualisiere die Statistiken
        self.update_stats()
        
        # 5. Visualisiere die Statistiken (alle 500 Iterationen)
        if self.iteration % self.visualization_interval == 0:
            self.visualize_stats()
            
            # Visualisiere das Kontextnetzwerk
            try:
                self.visualize_context_network()
            except Exception as e:
                print(f"Fehler bei der Netzwerkvisualisierung: {e}")
        
        # 6. Erhöhe die Iteration
        self.iteration += 1
        
        # 7. Prüfe, ob die Energie niedrig ist
        if self.is_low_energy():
            # Bei niedriger Energie: Suche nach einer Energiequelle
            energy_source_id = self.seek_energy_source()
            
            if energy_source_id:
                # Setze den Fokus auf die Energiequelle
                self.set_focus_by_id(energy_source_id)
                
                # Erhöhe die Energie
                energy_gain = self.energy_gain_rate * (1.0 + self.contexts[energy_source_id].happiness)
                self.energy = min(self.max_energy, self.energy + energy_gain)
                print(f"Energie aufgefüllt: +{energy_gain:.2f}. Neuer Energiestand: {self.energy:.2f}")
                    else:
                # Bei ausreichender Energie: Normales Denken
                # Versuche, logische Schlussfolgerungen zu ziehen
                if self.current_focus and self.current_focus in self.contexts:
                    current_context = self.contexts[self.current_focus]
                    current_text = " ".join([word.content for word in current_context.words])
                    reasoning_result = self.reason_from_current_knowledge(current_text)
                else:
                    reasoning_result = None

            if reasoning_result:
                # Wenn eine neue Erkenntnis gewonnen wurde, setze den Fokus darauf
                self.set_focus_by_id(reasoning_result)
            else:
                # Ansonsten finde den besten nächsten Fokus
                next_focus_id = self.find_best_next_focus()
                if next_focus_id:
                    self.set_focus_by_id(next_focus_id)
                else:
                    # Wenn kein passender Fokus gefunden wurde, starte das Lernen
                    print("Kein passender Fokus gefunden. Starte Lernprozess...")
                    self.learn_from_internet()
        
        # 8. Aktualisiere Habituation für den aktuellen Fokus
        if self.current_focus:
            self.update_habituation(self.current_focus)
        
        # 9. Erstelle neue Verbindungen basierend auf Ähnlichkeit
        self.create_new_connections()
        
        # 10. Lerne aus dem Internet (alle 50 Iterationen)
        if self.iteration % self.learning_interval == 0:
            self.learn_from_internet()
        
        # 11. Zustand speichern (alle 100 Iterationen)
        if self.iteration % self.save_interval == 0:
            self.save_state()
        
        return self.current_focus
    
    def reason_from_current_knowledge(self, query):
        """Zieht logische Schlussfolgerungen aus dem aktuellen Wissen."""
        # Finde relevante Kontexte für die Abfrage
        relevant_contexts = self.find_relevant_contexts(query, max_results=10)
        
        if not relevant_contexts:
            return None
            
        # Extrahiere Fakten aus den relevanten Kontexten
        facts = []
        for context_id, context in relevant_contexts:
            # Extrahiere den Text aus dem Kontext
            context_text = " ".join([word.content for word in context.words])
            facts.append(context_text)
            
        # Wenn keine Fakten gefunden wurden, gib None zurück
        if not facts:
            return None
            
        # Kombiniere die Fakten zu einem Wissenskorpus
        knowledge_corpus = " ".join(facts)
        
        # Identifiziere Schlüsselkonzepte in der Abfrage
        query_words = query.lower().split()
        key_concepts = [word for word in query_words if len(word) > 3]
        
        # Wenn keine Schlüsselkonzepte gefunden wurden, verwende die gesamte Abfrage
        if not key_concepts:
            key_concepts = query_words
            
        # Suche nach Zusammenhängen zwischen den Schlüsselkonzepten im Wissenskorpus
        connections = []
        
        for concept in key_concepts:
            # Finde Sätze, die das Konzept enthalten
            sentences = [s.strip() for s in knowledge_corpus.split('.') if concept in s.lower()]
            
            # Füge die gefundenen Sätze zu den Verbindungen hinzu
            connections.extend(sentences)
            
        # Wenn keine Verbindungen gefunden wurden, gib None zurück
        if not connections:
            return None
            
        # Erstelle eine Schlussfolgerung basierend auf den Verbindungen
        conclusion = None
        
        # Wenn mehrere Verbindungen gefunden wurden, kombiniere sie
        if len(connections) > 1:
            # Finde die häufigsten Wörter in den Verbindungen (außer Stoppwörtern)
            stop_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'about', 'as', 'of']
            word_counts = {}
            
            for connection in connections:
                words = connection.lower().split()
                for word in words:
                    if word not in stop_words and len(word) > 3:
                        if word in word_counts:
                            word_counts[word] += 1
            else:
                            word_counts[word] = 1
            
            # Sortiere die Wörter nach Häufigkeit
            sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
            
            # Verwende die häufigsten Wörter, um eine Schlussfolgerung zu erstellen
            if sorted_words:
                common_words = [word for word, count in sorted_words[:5] if count > 1]
                
                if common_words:
                    # Erstelle einen neuen Kontext mit der Schlussfolgerung - ohne vorgefertigten Satz
                    conclusion_text = " ".join(common_words) + " " + query
                    
                    # Erstelle einen neuen Kontext mit der Schlussfolgerung
                    label = f"Conclusion_{int(time.time())}"
                    happiness = 0.7  # Hoher Glückswert für Schlussfolgerungen
                    
                    conclusion_id = self.create_context(conclusion_text, label, happiness)
                    conclusion = self.contexts[conclusion_id]
                    
                    # Verbinde die Schlussfolgerung mit den relevanten Kontexten
                    for context_id, _ in relevant_contexts:
                        self.create_connection(conclusion_id, context_id, weight=0.8)
        
        return conclusion
    
    def think_forever(self):
        """Kontinuierlicher Denkprozess des Bewusstseins."""
        self.active = True
        while self.active:
            self.think()
            
    def update_emotional_state(self, context):
        """Aktualisiert den emotionalen Zustand basierend auf einem Kontext."""
        # Extrahiere Wörter aus dem Kontext
        context_words = [word.content.lower() for word in context.words]
        
        # Definiere emotionale Wörter
        emotional_words = {
            'joy': ['happy', 'joy', 'glad', 'excited', 'wonderful', 'great', 'good', 'positive', 'love', 'like'],
            'sadness': ['sad', 'unhappy', 'depressed', 'miserable', 'bad', 'negative', 'hate', 'dislike', 'sorry'],
            'anger': ['angry', 'mad', 'furious', 'rage', 'annoyed', 'irritated', 'frustrated', 'upset'],
            'fear': ['afraid', 'scared', 'frightened', 'terrified', 'anxious', 'worried', 'nervous', 'panic'],
            'surprise': ['surprised', 'amazed', 'astonished', 'shocked', 'unexpected', 'wow', 'incredible'],
            'disgust': ['disgusted', 'gross', 'yuck', 'ew', 'nasty', 'repulsive', 'revolting'],
            'trust': ['trust', 'believe', 'faith', 'confident', 'reliable', 'dependable', 'honest', 'true'],
            'anticipation': ['anticipate', 'expect', 'hope', 'looking forward', 'waiting', 'excited for']
        }
        
        # Berechne die emotionale Intensität für jede Emotion
        emotion_intensities = {}
        
        for emotion, words in emotional_words.items():
            intensity = 0
            for word in words:
                if word in context_words:
                    intensity += 0.2  # Erhöhe die Intensität für jedes gefundene Wort
            
            # Normalisiere die Intensität
            intensity = min(1.0, intensity)
            
            # Aktualisiere die Emotion mit einer gewissen Trägheit
            if emotion in self.emotional_state.emotions:
                current_intensity = self.emotional_state.emotions[emotion]
                # Gewichteter Durchschnitt (70% aktuell, 30% neu)
                self.emotional_state.emotions[emotion] = (current_intensity * 0.7) + (intensity * 0.3)
            else:
                self.emotional_state.emotions[emotion] = intensity
        
        # Aktualisiere die Glücklichkeit basierend auf den Emotionen
        joy = self.emotional_state.emotions.get('joy', 0)
        sadness = self.emotional_state.emotions.get('sadness', 0)
        anger = self.emotional_state.emotions.get('anger', 0)
        fear = self.emotional_state.emotions.get('fear', 0)
        
        # Berechne die Glücklichkeit (positiv: Freude, negativ: Traurigkeit, Wut, Angst)
        happiness = joy - ((sadness + anger + fear) / 3)
        
        # Normalisiere die Glücklichkeit auf den Bereich [0, 1]
        happiness = max(0.0, min(1.0, (happiness + 1) / 2))
        
        # Aktualisiere die Glücklichkeit des Kontexts
        context.happiness = happiness
    
    def calculate_sentiment(self, words):
        """Berechnet einen Stimmungswert für eine Liste von Wörtern."""
        # Konvertiere alle Wörter zu Kleinbuchstaben
        words = [word.lower() for word in words]
        
        # Definiere emotionale Wörter (gleich wie in update_emotional_state)
        emotional_words = {
            'joy': ['happy', 'joy', 'glad', 'excited', 'wonderful', 'great', 'good', 'positive', 'love', 'like'],
            'sadness': ['sad', 'unhappy', 'depressed', 'miserable', 'bad', 'negative', 'hate', 'dislike', 'sorry'],
            'anger': ['angry', 'mad', 'furious', 'rage', 'annoyed', 'irritated', 'frustrated', 'upset'],
            'fear': ['afraid', 'scared', 'frightened', 'terrified', 'anxious', 'worried', 'nervous', 'panic'],
            'surprise': ['surprised', 'amazed', 'astonished', 'shocked', 'unexpected', 'wow', 'incredible'],
            'disgust': ['disgusted', 'gross', 'yuck', 'ew', 'nasty', 'repulsive', 'revolting'],
            'trust': ['trust', 'believe', 'faith', 'confident', 'reliable', 'dependable', 'honest', 'true'],
            'anticipation': ['anticipate', 'expect', 'hope', 'looking forward', 'waiting', 'excited for']
        }
        
        # Berechne die emotionale Intensität für jede Emotion
        emotion_intensities = {}
        
        for emotion, emotion_words in emotional_words.items():
            intensity = 0
            for word in words:
                if word in emotion_words:
                    intensity += 0.2  # Erhöhe die Intensität für jedes gefundene Wort
            
            # Normalisiere die Intensität
            emotion_intensities[emotion] = min(1.0, intensity)
        
        # Berechne die Glücklichkeit basierend auf den Emotionen
        joy = emotion_intensities.get('joy', 0)
        sadness = emotion_intensities.get('sadness', 0)
        anger = emotion_intensities.get('anger', 0)
        fear = emotion_intensities.get('fear', 0)
        
        # Berechne die Glücklichkeit (positiv: Freude, negativ: Traurigkeit, Wut, Angst)
        happiness = joy - ((sadness + anger + fear) / 3)
        
        # Normalisiere die Glücklichkeit auf den Bereich [0, 1]
        happiness = max(0.0, min(1.0, (happiness + 1) / 2))
        
        return happiness
    
    def find_relevant_contexts(self, query, max_results=5):
        """Findet relevante Kontexte basierend auf einer Abfrage."""
        if not query or not self.contexts:
            return []
            
        query_words = query.lower().split()
        results = []
        
        # Erstelle einen Vektor für die Abfrage
        query_vector = {}
        for word in query_words:
            if word in query_vector:
                query_vector[word] += 1
                else:
                query_vector[word] = 1
                
        # Berechne die Relevanz für jeden Kontext
        for context_id, context in self.contexts.items():
            # Extrahiere Wörter aus dem Kontext
            context_words = [word.content.lower() for word in context.words]
            
            # Erstelle einen Vektor für den Kontext
            context_vector = {}
            for word in context_words:
                if word in context_vector:
                    context_vector[word] += 1
            else:
                    context_vector[word] = 1
                    
            # Berechne die Kosinus-Ähnlichkeit zwischen Abfrage und Kontext
            similarity = self.calculate_cosine_similarity(query_vector, context_vector)
            
            # Berücksichtige auch die Verbindungen zum aktuellen Fokus
            connection_bonus = 0
            if self.current_focus in self.contexts:
                current_context = self.contexts[self.current_focus]
                if hasattr(current_context, 'connections') and context_id in current_context.connections:
                    connection_bonus = current_context.connections[context_id] * 0.3
                    
            # Berechne den Gesamtscore
            score = similarity + connection_bonus + (context.happiness * 0.1)
            
            # Füge den Kontext zu den Ergebnissen hinzu
            results.append((context_id, score))
            
        # Sortiere die Ergebnisse nach Score (absteigend)
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Gib die besten Ergebnisse zurück
        return [(context_id, self.contexts[context_id]) for context_id, _ in results[:max_results]]
        
    def calculate_cosine_similarity(self, vec1, vec2):
        """Berechnet die Kosinus-Ähnlichkeit zwischen zwei Vektoren."""
        # Finde gemeinsame Wörter
        common_words = set(vec1.keys()) & set(vec2.keys())
        
        # Berechne das Skalarprodukt
        dot_product = sum(vec1[word] * vec2[word] for word in common_words)
        
        # Berechne die Normen der Vektoren
        norm1 = math.sqrt(sum(vec1[word] ** 2 for word in vec1))
        norm2 = math.sqrt(sum(vec2[word] ** 2 for word in vec2))
        
        # Vermeide Division durch Null
        if norm1 == 0 or norm2 == 0:
            return 0
            
        # Berechne die Kosinus-Ähnlichkeit
        return dot_product / (norm1 * norm2)
    
    def format_answer_for_question(self, question_analysis, sentences):
        """
        Formatiert eine Antwort basierend auf dem Fragetyp und den Attributen.
        
        Args:
            question_analysis: Die Analyse der Frage
            sentences: Die gefundenen relevanten Sätze
            
        Returns:
            Eine formatierte Antwort
        """
        if not sentences:
            return "Ich konnte keine relevanten Informationen finden."
        
        # Extrahiere die Entitäten aus der Frage
        entities = question_analysis['entities']
        entity_str = ', '.join(entities) if entities else "das Thema"
        
        # Formatiere die Antwort basierend auf dem Fragetyp
        fragetyp = question_analysis['type']
        
        if fragetyp == 'beschaffenheit':
            # Bei "Wie"-Fragen
            if 'geschmack' in question_analysis['attributes']:
                # Geschmacksfragen
                intro = f"Der Geschmack von {entity_str} lässt sich wie folgt beschreiben: "
            elif 'aussehen' in question_analysis['attributes']:
                # Aussehen
                intro = f"{entity_str.capitalize()} sieht folgendermaßen aus: "
            elif 'größe' in question_analysis['attributes']:
                # Größe
                intro = f"Die Größe von {entity_str} beträgt: "
            elif 'alter' in question_analysis['attributes']:
                # Alter
                intro = f"Das Alter von {entity_str} ist: "
            elif 'funktion' in question_analysis['attributes']:
                # Funktion
                intro = f"{entity_str.capitalize()} funktioniert folgendermaßen: "
            else:
                # Allgemeine Beschaffenheit
                intro = f"Über {entity_str} kann ich Folgendes sagen: "
        
        elif fragetyp == 'grund':
            # Bei "Warum"-Fragen
            intro = f"Der Grund für {entity_str} ist: "
        
        elif fragetyp == 'person':
            # Bei "Wer"-Fragen
            intro = f"Die Person(en) im Zusammenhang mit {entity_str}: "
        
        elif fragetyp == 'definition':
            # Bei "Was"-Fragen
            intro = f"{entity_str.capitalize()} ist: "
        
        elif fragetyp == 'ort':
            # Bei "Wo"-Fragen
            intro = f"Der Ort für {entity_str} ist: "
        
        elif fragetyp == 'zeit':
            # Bei "Wann"-Fragen
            intro = f"Der Zeitpunkt für {entity_str} ist: "
        
        elif fragetyp == 'auswahl':
            # Bei "Welche"-Fragen
            intro = f"Die Optionen für {entity_str} sind: "
        
        else:
            # Bei allgemeinen Fragen
            intro = f"Zu {entity_str} habe ich folgende Informationen: "
        
        # Kombiniere die Sätze zu einer Antwort
        if len(sentences) > 1:
            # Verwende Übergänge zwischen den Sätzen
            transitions = ["Außerdem", "Darüber hinaus", "Zudem", "Weiterhin", "Auch", "Interessanterweise"]
            
            answer = sentences[0]
            
            for i, sentence in enumerate(sentences[1:]):
                if i == 0:
                    answer += f". {sentence}"
                else:
                    answer += f". {random.choice(transitions)} {sentence}"
        else:
            answer = sentences[0]
        
        # Füge die Einleitung hinzu
        formatted_answer = intro + answer
        
        return formatted_answer

    def generate_response(self, query):
        """Generiert eine Antwort basierend auf einer Abfrage."""
        if not query:
            return "Ich habe das nicht verstanden. Könntest du es bitte umformulieren?"
        
        # Prüfe, ob es sich um eine Frage handelt
        is_question = '?' in query or query.lower().startswith(('wie ', 'warum ', 'wer ', 'was ', 'wo ', 'wann ', 'welche '))
        
        # Wenn es eine Frage ist, analysiere sie
        question_analysis = None
        if is_question:
            question_analysis = self.analyze_question(query)
            print(f"Frageanalyse: {question_analysis}")
            
        # Finde relevante Kontexte
        relevant_contexts = self.find_relevant_contexts(query, max_results=10)
        
        # Wenn keine relevanten Kontexte gefunden wurden, versuche aus dem Internet zu lernen
        if not relevant_contexts:
            print(f"Keine relevanten Kontexte für '{query}' gefunden. Starte Lernprozess...")
            
            # Speichere die ursprüngliche Abfrage
            original_query = query
            
            # Lerne über das Thema der Abfrage
            learned_contexts = self.learn_about_topic(query, connect_to_focus=False, max_contexts=5)
            
            # Wenn neue Kontexte erstellt wurden, suche erneut nach relevanten Kontexten
            if learned_contexts:
                # Suche erneut nach relevanten Kontexten
                relevant_contexts = self.find_relevant_contexts(original_query, max_results=10)
            
            # Wenn immer noch keine relevanten Kontexte gefunden wurden
            if not relevant_contexts:
                return "Ich habe versucht, darüber zu lernen, aber ich konnte keine relevanten Informationen finden. Kannst du deine Frage anders formulieren?"
        
        # Sammle Wörter und Sätze aus den relevanten Kontexten
        context_sentences = []
        context_info = {}  # Speichere zusätzliche Informationen zu jedem Kontext
        
        for context_id, context in relevant_contexts:
            # Extrahiere den Text aus dem Kontext
            context_text = " ".join([word.content for word in context.words])
            
            # Speichere Informationen über den Kontext
            context_info[context_id] = {
                'text': context_text,
                'happiness': context.happiness,
                'connections': getattr(context, 'connections', {}),
                'source_type': getattr(context, 'source_type', 'unknown')
            }
            
            # Teile den Text in Sätze auf
            sentences = [s.strip() for s in context_text.split('.') if s.strip()]
            
            # Füge Metadaten zu jedem Satz hinzu
            for sentence in sentences:
                context_sentences.append({
                    'text': sentence,
                    'context_id': context_id,
                    'happiness': context.happiness,
                    'source_type': getattr(context, 'source_type', 'unknown')
                })
        
        # Wenn keine Sätze gefunden wurden
        if not context_sentences:
            return "Ich verstehe die Frage, aber ich kann keine klare Antwort formulieren. Könntest du spezifischer sein?"
        
        # Entferne Duplikate und sehr ähnliche Sätze
        unique_sentences = []
        for sentence_data in context_sentences:
            # Prüfe, ob der Satz bereits in der Liste ist oder sehr ähnlich zu einem vorhandenen Satz
            is_duplicate = False
            for existing in unique_sentences:
                # Berechne die Ähnlichkeit zwischen den Sätzen
                words1 = set(sentence_data['text'].lower().split())
                words2 = set(existing['text'].lower().split())
                
                if not words1 or not words2:
                    continue
                    
                intersection = words1.intersection(words2)
                union = words1.union(words2)
                
                similarity = len(intersection) / len(union)
                
                if similarity > 0.7:  # Wenn die Sätze zu 70% übereinstimmen
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_sentences.append(sentence_data)
        
        # Wenn es eine Frage ist, filtere die Sätze basierend auf dem Fragetyp und den Attributen
        if is_question and question_analysis:
            filtered_sentences = []
            
            # Extrahiere relevante Schlüsselwörter basierend auf dem Fragetyp und den Attributen
            relevant_keywords = []
            
            if question_analysis['type'] == 'beschaffenheit':
                if 'geschmack' in question_analysis['attributes']:
                    # Geschmacksfragen
                    relevant_keywords = ['schmeckt', 'geschmack', 'aroma', 'süß', 'sauer', 'bitter', 'salzig', 'würzig', 'scharf', 'mild', 'fruchtig', 'herb']
                elif 'aussehen' in question_analysis['attributes']:
                    # Aussehen
                    relevant_keywords = ['aussieht', 'aussehen', 'farbe', 'form', 'gestalt', 'erscheinung']
                elif 'größe' in question_analysis['attributes']:
                    # Größe
                    relevant_keywords = ['groß', 'größe', 'dimension', 'umfang', 'ausdehnung', 'höhe', 'breite', 'länge']
                elif 'alter' in question_analysis['attributes']:
                    # Alter
                    relevant_keywords = ['alt', 'alter', 'jahre', 'jahrzehnte', 'jahrhunderte', 'entstehung', 'geburt']
                elif 'funktion' in question_analysis['attributes']:
                    # Funktion
                    relevant_keywords = ['funktioniert', 'funktion', 'arbeitet', 'mechanismus', 'prozess', 'ablauf']
                else:
                    # Allgemeine Beschaffenheit
                    relevant_keywords = ['eigenschaft', 'beschaffenheit', 'charakteristik', 'merkmal', 'qualität']
            
            # Wenn relevante Schlüsselwörter definiert wurden, filtere die Sätze
            if relevant_keywords:
                for sentence_data in unique_sentences:
                    sentence_text = sentence_data['text'].lower()
                    relevance_score = sum(1 for keyword in relevant_keywords if keyword in sentence_text)
                    
                    if relevance_score > 0:
                        # Füge den Relevanz-Score hinzu
                        sentence_data['relevance'] = relevance_score
                        filtered_sentences.append(sentence_data)
                
                # Wenn gefilterte Sätze gefunden wurden, verwende sie
                if filtered_sentences:
                    # Sortiere nach Relevanz
                    filtered_sentences.sort(key=lambda x: x.get('relevance', 0), reverse=True)
                    unique_sentences = filtered_sentences
        
        # Sortiere die Sätze nach Relevanz zur Abfrage
        query_words = set(query.lower().split())
        
        for sentence_data in unique_sentences:
            sentence_words = set(sentence_data['text'].lower().split())
            
            # Berechne die Überlappung zwischen Abfrage und Satz
            overlap = len(query_words.intersection(sentence_words))
            
            # Berechne den Score basierend auf der Überlappung, der Satzlänge und der Quelle
            base_score = overlap / max(1, len(sentence_words))
            
            # Bevorzuge Sätze aus Web-Quellen für Faktenwissen
            source_bonus = 0.2 if sentence_data['source_type'] == 'web' else 0
            
            # Bevorzuge Sätze mit höherem Happiness-Wert
            happiness_bonus = sentence_data['happiness'] * 0.1
            
            # Berücksichtige den Relevanz-Score, falls vorhanden
            relevance_bonus = sentence_data.get('relevance', 0) * 0.3
            
            # Berechne den Gesamtscore
            sentence_data['score'] = base_score + source_bonus + happiness_bonus + relevance_bonus
        
        # Sortiere die Sätze nach Score (absteigend)
        unique_sentences.sort(key=lambda x: x['score'], reverse=True)
        
        # Erstelle einen Graphen aus den Sätzen und ihren Kontexten
        G = nx.Graph()
        
        # Füge Knoten für jeden Satz hinzu
        for i, sentence_data in enumerate(unique_sentences):
            node_id = f"S{i}"
            G.add_node(node_id, 
                       text=sentence_data['text'], 
                       context_id=sentence_data['context_id'],
                       score=sentence_data['score'])
            
            # Verbinde Sätze aus dem gleichen Kontext
            for j, other_sentence in enumerate(unique_sentences[:i]):
                if sentence_data['context_id'] == other_sentence['context_id']:
                    G.add_edge(node_id, f"S{j}", weight=0.9)
                    
            # Verbinde Sätze aus verbundenen Kontexten
            context_connections = context_info[sentence_data['context_id']]['connections']
            for j, other_sentence in enumerate(unique_sentences[:i]):
                if other_sentence['context_id'] in context_connections:
                    connection_weight = context_connections[other_sentence['context_id']]
                    G.add_edge(node_id, f"S{j}", weight=connection_weight)
        
        # Wähle die besten Sätze für die Antwort basierend auf PageRank
        if len(G.nodes()) > 0:
            # Berechne PageRank
            pagerank = nx.pagerank(G, weight='weight')
            
            # Sortiere Knoten nach PageRank
            sorted_nodes = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)
            
            # Wähle die Top-N Knoten
            top_n = min(5, len(sorted_nodes))
            important_nodes = [node for node, _ in sorted_nodes[:top_n]]
            
            # Extrahiere die Texte der wichtigsten Knoten
            best_sentences = [G.nodes[node]['text'] for node in important_nodes]
        else:
            # Fallback: Verwende die Sätze mit dem höchsten Score
            best_sentences = [s['text'] for s in unique_sentences[:5]]
        
        # Wenn es eine Frage ist, formatiere die Antwort entsprechend
        if is_question and question_analysis:
            response = self.format_answer_for_question(question_analysis, best_sentences)
        else:
            # Kombiniere die Sätze zu einer Antwort
            if len(best_sentences) > 1:
                # Verwende Übergänge zwischen den Sätzen
                transitions = ["Außerdem", "Darüber hinaus", "Zudem", "Weiterhin", "Auch", "Interessanterweise"]
                
                response = best_sentences[0]
                
                for i, sentence in enumerate(best_sentences[1:]):
                    if i == 0:
                        response += f". {sentence}"
                    else:
                        response += f". {random.choice(transitions)} {sentence}"
            else:
                response = best_sentences[0]
        
        # Stelle sicher, dass die Antwort nicht zu lang ist
        if len(response) > 500:
            response = response[:497] + "..."
        
        # Erstelle einen neuen Kontext für die Antwort
        response_label = f"Response_{int(time.time())}"
        response_happiness = self.calculate_sentiment(response.split())
        
        response_id = self.create_context(response, response_label, response_happiness)
        
        # Verbinde die Antwort mit den relevanten Kontexten
        for context_id, _ in relevant_contexts[:3]:
            self.create_connection(response_id, context_id)
        
        # Setze den Fokus auf die Antwort
        self.set_focus_by_id(response_id)
        
        return response

    def initialize_honeypots(self):
        """Initialisiert die drei grundlegenden Honeypots."""
        # Definiere die Schlüsselwörter für die drei Honeypots
        honeypot_keywords = {
            'energy_intake': ['eat', 'food', 'drink', 'consume', 'nutrition', 'meal', 'hungry', 'thirsty'],
            'regeneration': ['sleep', 'rest', 'relax', 'calm', 'peaceful', 'quiet', 'meditate', 'recover'],
            'reproduction': ['social', 'interact', 'communicate', 'share', 'connect', 'learn', 'teach', 'create']
        }
        
        # Erstelle die Honeypots
        honeypot_ids = {}
        for honeypot_type, keywords in honeypot_keywords.items():
            # Prüfe, ob der Honeypot bereits existiert
            honeypot_exists = False
            for context_id, context in self.contexts.items():
                if context_id.startswith(f"Honeypot_{honeypot_type}"):
                    honeypot_exists = True
                    honeypot_ids[honeypot_type] = context_id
                    break
            
            # Erstelle den Honeypot, falls er noch nicht existiert
            if not honeypot_exists:
                # Verwende die Schlüsselwörter statt vorgefertigter Sätze
                text = " ".join(keywords)
                label = f"Honeypot_{honeypot_type}_0"
                happiness = 0.8  # Hoher Glückswert für Honeypots
                
                honeypot_id = self.create_context(text, label, happiness)
                honeypot_ids[honeypot_type] = honeypot_id
                
                print(f"Honeypot erstellt: {honeypot_type}")
        
        # Verbinde die Honeypots miteinander
        for honeypot1, id1 in honeypot_ids.items():
            for honeypot2, id2 in honeypot_ids.items():
                if honeypot1 != honeypot2:
                    self.create_connection(id1, id2, weight=0.5)
        
        # Setze den Fokus auf einen zufälligen Honeypot, falls kein Fokus gesetzt ist
        if not self.current_focus or self.current_focus not in self.contexts:
            random_honeypot_id = random.choice(list(honeypot_ids.values()))
            self.set_focus_by_id(random_honeypot_id)
            print(f"Fokus auf Honeypot gesetzt: {honeypot_type}")
            
        return honeypot_ids
        
    def start(self):
        """Startet das ewige Bewusstsein."""
        print("Starte ewiges Bewusstsein...")
        self.active = True
        
        # Initialisiere die Honeypots
        self.initialize_honeypots()
        
        self.think_forever()
        
    def stop(self):
        """Stoppt das ewige Bewusstsein."""
        print("Stoppe ewiges Bewusstsein...")
        self.active = False
        self.save_state()
        print("Zustand gespeichert.")

    def update_habituation(self, context_id):
        """Aktualisiert die Habituation für einen Kontext."""
        if context_id not in self.contexts:
            return
            
        # Initialisiere die Habituation, falls sie noch nicht existiert
        if not hasattr(self.contexts[context_id], 'habituation'):
            self.contexts[context_id].habituation = 0.0
            
        # Erhöhe die Habituation (Gewöhnung an den Kontext)
        self.contexts[context_id].habituation = min(1.0, self.contexts[context_id].habituation + 0.1)
        
    def decay_habituation(self):
        """Lässt die Habituation für alle Kontexte mit der Zeit abklingen."""
        for context_id, context in self.contexts.items():
            if hasattr(context, 'habituation') and context.habituation > 0:
                # Reduziere die Habituation um 1% pro Iteration
                context.habituation = max(0.0, context.habituation * 0.99)

    def find_best_next_focus(self):
        """Findet den besten nächsten Fokus basierend auf verschiedenen Faktoren."""
        if not self.contexts or not self.current_focus or self.current_focus not in self.contexts:
            return None
            
        current_context = self.contexts[self.current_focus]
        
        # Prüfe, ob der aktuelle Kontext Verbindungen hat
        if not hasattr(current_context, 'connections') or not current_context.connections:
            return None
            
        # Bewerte alle verbundenen Kontexte
        candidates = []
        
        for connected_id, weight in current_context.connections.items():
            if connected_id in self.contexts:
                connected_context = self.contexts[connected_id]
                
                # Berechne den Score basierend auf verschiedenen Faktoren
                
                # 1. Verbindungsstärke
                connection_score = weight
                
                # 2. Glücklichkeit des Kontexts
                happiness_score = connected_context.happiness
                
                # 3. Habituation (Gewöhnung) - niedrigere Habituation ist besser
                habituation_score = 0.0
                if hasattr(connected_context, 'habituation'):
                    habituation_score = 1.0 - connected_context.habituation
                    
                # 4. Zufallsfaktor für Exploration
                random_score = random.random() * 0.2
                
                # Kombiniere die Scores mit Gewichtungen
                total_score = (
                    connection_score * 0.4 +
                    happiness_score * 0.3 +
                    habituation_score * 0.2 +
                    random_score * 0.1
                )
                
                candidates.append((connected_id, total_score))
        
        if not candidates:
            return None
            
        # Sortiere nach Score (absteigend)
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        # Gib die ID des besten Kandidaten zurück
        return candidates[0][0]

    def create_new_connections(self):
        """Erstellt neue Verbindungen zwischen Kontexten basierend auf Ähnlichkeit."""
        if not self.contexts or not self.current_focus or self.current_focus not in self.contexts:
            return
        
        current_context = self.contexts[self.current_focus]
        
        # Extrahiere Wörter aus dem aktuellen Kontext
        current_words = [word.content.lower() for word in current_context.words]
        
        # Finde ähnliche Kontexte
        similar_contexts = []
        
        for context_id, context in self.contexts.items():
            # Überspringe den aktuellen Kontext
            if context_id == self.current_focus:
                continue
                
            # Überspringe bereits verbundene Kontexte
            if hasattr(current_context, 'connections') and context_id in current_context.connections:
                continue
                
            # Extrahiere Wörter aus dem Kontext
            context_words = [word.content.lower() for word in context.words]
            
            # Berechne verschiedene Ähnlichkeitsmaße
            
            # 1. Semantische Ähnlichkeit (Wortüberlappung)
            common_words = set(current_words) & set(context_words)
            if not common_words:
                continue
                
            semantic_similarity = len(common_words) / (len(set(current_words) | set(context_words)))
            
            # 2. Emotionale Ähnlichkeit
            emotional_similarity = 1.0 - abs(current_context.happiness - context.happiness)
            
            # 3. Thematische Ähnlichkeit (basierend auf längeren Wörtern)
            important_words_current = [w for w in current_words if len(w) > 4]
            important_words_context = [w for w in context_words if len(w) > 4]
            
            common_important_words = set(important_words_current) & set(important_words_context)
            thematic_similarity = 0.0
            
            if important_words_current and important_words_context:
                thematic_similarity = len(common_important_words) / max(len(important_words_current), len(important_words_context))
            
            # 4. Transitive Ähnlichkeit (gemeinsame Verbindungen)
            transitive_similarity = 0.0
            
            if hasattr(current_context, 'connections') and hasattr(context, 'connections'):
                common_connections = set(current_context.connections.keys()) & set(context.connections.keys())
                if common_connections:
                    transitive_similarity = len(common_connections) / max(len(current_context.connections), len(context.connections))
            
            # Kombiniere die Ähnlichkeitsmaße zu einem Gesamtscore
            total_similarity = (
                semantic_similarity * 0.4 +
                emotional_similarity * 0.2 +
                thematic_similarity * 0.3 +
                transitive_similarity * 0.1
            )
            
            # Wenn die Ähnlichkeit hoch genug ist, füge den Kontext zur Liste hinzu
            if total_similarity > 0.2:
                similar_contexts.append((context_id, total_similarity))
        
        # Sortiere nach Ähnlichkeit (absteigend)
        similar_contexts.sort(key=lambda x: x[1], reverse=True)
        
        # Erstelle Verbindungen zu den ähnlichsten Kontexten
        for context_id, similarity in similar_contexts:
            self.create_connection(self.current_focus, context_id, weight=similarity)

    def update_needs_pyramid_from_state(self):
        """Aktualisiert die Bedürfnispyramide basierend auf dem aktuellen Zustand."""
        # 1. Physiologische Bedürfnisse (basierend auf Energie)
        self.needs_pyramid["physiological"] = self.energy
        
        # 2. Sicherheit (basierend auf Energiestabilität)
        energy_stability = 1.0
        if hasattr(self, 'energy_history') and len(self.energy_history) > 5:
            # Berechne die Standardabweichung der letzten 5 Energiewerte
            mean_energy = sum(self.energy_history[-5:]) / 5
            variance = sum((e - mean_energy) ** 2 for e in self.energy_history[-5:]) / 5
            std_dev = variance ** 0.5
            # Niedrigere Standardabweichung bedeutet höhere Stabilität
            energy_stability = max(0.0, 1.0 - (std_dev * 2))
        
        self.needs_pyramid["safety"] = energy_stability
        
        # 3. Zugehörigkeit (basierend auf sozialen Interaktionen und Verbindungen)
        social_connections = 0.0
        if self.contexts:
            # Zähle die Anzahl der Verbindungen
            total_connections = 0
            for context_id, context in self.contexts.items():
                if hasattr(context, 'connections'):
                    total_connections += len(context.connections)
            
            # Normalisiere auf den Bereich [0, 1]
            social_connections = min(1.0, total_connections / max(1, len(self.contexts) * 2))
        
        self.needs_pyramid["belonging"] = social_connections
        
        # 4. Anerkennung (basierend auf Glücklichkeit und Stimulation)
        happiness = 0.0
        stimulation = 0.0
        
        if self.contexts and self.current_focus in self.contexts:
            happiness = self.contexts[self.current_focus].happiness
        
        if hasattr(self, 'stimulation'):
            stimulation = self.stimulation
        
        self.needs_pyramid["esteem"] = (happiness * 0.7) + (stimulation * 0.3)
        
        # 5. Selbstverwirklichung (basierend auf der Anzahl der Kontexte)
        self_actualization = 0.0
        if self.contexts:
            # Mehr Kontexte bedeuten mehr Wissen und Erfahrung
            self_actualization = min(1.0, len(self.contexts) / 100)
        
        self.needs_pyramid["self_actualization"] = self_actualization
        
        # Stelle sicher, dass alle Werte im gültigen Bereich [0, 1] liegen
        for need in self.needs_pyramid:
            self.needs_pyramid[need] = max(0.0, min(1.0, self.needs_pyramid[need]))

    def get_wikipedia_content(self, search_term):
        """Ruft Inhalte von Wikipedia ab basierend auf einem Suchbegriff."""
        try:
            import wikipedia
            
            # Suche nach Seiten, die dem Suchbegriff entsprechen
            search_results = wikipedia.search(search_term, results=3)
            
            if not search_results:
                print(f"Keine Wikipedia-Artikel für '{search_term}' gefunden.")
            return None
        
            # Versuche, den ersten Treffer zu verwenden
            try:
                # Hole eine Zusammenfassung des Artikels
                page = wikipedia.page(search_results[0])
                summary = page.summary
                
                # Begrenze die Länge der Zusammenfassung
                if len(summary) > 500:
                    summary = summary[:500] + "..."
                    
                return summary
                
            except wikipedia.exceptions.DisambiguationError as e:
                # Bei Mehrdeutigkeiten verwende die erste Option
                if e.options:
                    try:
                        page = wikipedia.page(e.options[0])
                        summary = page.summary
                        
                        # Begrenze die Länge der Zusammenfassung
                        if len(summary) > 500:
                            summary = summary[:500] + "..."
                            
                        return summary
                    except:
                        pass
                        
            except Exception as e:
                print(f"Fehler beim Abrufen des Wikipedia-Artikels: {e}")
                
            return None
        
        except ImportError:
            print("Wikipedia-Modul nicht installiert. Verwende 'pip install wikipedia' zum Installieren.")
            return None
            
    def learn_from_internet(self):
        """Lernt aus dem Internet basierend auf dem aktuellen Fokus."""
        if not self.current_focus or self.current_focus not in self.contexts:
            print("Kein aktueller Fokus vorhanden. Kann nicht aus dem Internet lernen.")
            return
            
        current_context = self.contexts[self.current_focus]
        
        # Extrahiere den gesamten Text aus dem aktuellen Kontext
        context_text = " ".join([word.content for word in current_context.words])
        
        # Rufe die allgemeine Lernmethode auf
        self.learn_about_topic(context_text, connect_to_focus=True)
    
    def analyze_question(self, question):
        """
        Analysiert eine Frage und extrahiert den Fragetyp, die Entitäten und relevante Attribute.
        
        Args:
            question: Die zu analysierende Frage
            
        Returns:
            Ein Dictionary mit Fragetyp, Entitäten und Attributen
        """
        # Normalisiere die Frage
        question = question.strip().lower()
        
        # Definiere Fragewörter und ihre zugehörigen Attribute
        question_types = {
            'wie': 'beschaffenheit',  # Wie ist etwas beschaffen?
            'warum': 'grund',         # Was ist der Grund?
            'wer': 'person',          # Welche Person?
            'was': 'definition',      # Was ist etwas?
            'wo': 'ort',              # An welchem Ort?
            'wann': 'zeit',           # Zu welcher Zeit?
            'welche': 'auswahl',      # Welche Option?
            'welcher': 'auswahl',
            'welches': 'auswahl'
        }
        
        # Extrahiere den Fragetyp
        question_type = None
        for q_word, attr in question_types.items():
            if question.startswith(q_word + ' ') or f' {q_word} ' in question:
                question_type = attr
                break
        
        # Wenn kein Fragetyp erkannt wurde, versuche es mit anderen Heuristiken
        if not question_type:
            if '?' in question:
                # Allgemeine Frage
                question_type = 'information'
        else:
                # Keine Frage erkannt
                question_type = 'statement'
        
        # Extrahiere Entitäten (Substantive und Eigennamen)
        # Hier verwenden wir eine einfache Heuristik: Wörter, die nicht in der Stopwortliste sind
        # und länger als 3 Zeichen sind, könnten Entitäten sein
        stop_words = ['der', 'die', 'das', 'ein', 'eine', 'einer', 'eines', 'einem', 'einen',
                     'ist', 'sind', 'war', 'waren', 'wird', 'werden', 'wurde', 'wurden',
                     'hat', 'haben', 'hatte', 'hatten', 'kann', 'können', 'könnte', 'könnten',
                     'muss', 'müssen', 'musste', 'mussten', 'soll', 'sollen', 'sollte', 'sollten',
                     'will', 'wollen', 'wollte', 'wollten', 'darf', 'dürfen', 'durfte', 'durften',
                     'mag', 'mögen', 'mochte', 'mochten', 'und', 'oder', 'aber', 'denn', 'weil',
                     'obwohl', 'obgleich', 'wenn', 'falls', 'als', 'wie', 'dass', 'ob',
                     'für', 'mit', 'bei', 'von', 'zu', 'aus', 'in', 'an', 'auf', 'über', 'unter',
                     'neben', 'zwischen', 'vor', 'nach', 'seit', 'während', 'wegen', 'trotz',
                     'ich', 'du', 'er', 'sie', 'es', 'wir', 'ihr', 'sie',
                     'mich', 'dich', 'ihn', 'uns', 'euch', 'ihnen',
                     'mein', 'dein', 'sein', 'ihr', 'unser', 'euer', 'ihr']
        
        words = question.split()
        entities = []
        
        for word in words:
            # Entferne Satzzeichen
            clean_word = word.strip('.,;:!?()"\'')
            if len(clean_word) > 3 and clean_word not in stop_words and clean_word not in question_types:
                entities.append(clean_word)
        
        # Identifiziere spezifische Attribute basierend auf dem Fragetyp und Kontext
        attributes = []
        
        if question_type == 'beschaffenheit':
            # Bei "Wie"-Fragen, suche nach Attributen wie Farbe, Geschmack, Größe, etc.
            if 'schmeckt' in question or 'geschmack' in question:
                attributes.append('geschmack')
            elif 'aussieht' in question or 'aussehen' in question:
                attributes.append('aussehen')
            elif 'groß' in question or 'größe' in question:
                attributes.append('größe')
            elif 'alt' in question or 'alter' in question:
                attributes.append('alter')
            elif 'funktioniert' in question:
                attributes.append('funktion')
            else:
                # Allgemeine Beschaffenheit
                attributes.append('eigenschaft')
        
        # Ergebnis zusammenstellen
        result = {
            'type': question_type,
            'entities': entities,
            'attributes': attributes,
            'original_question': question
        }
        
        return result

    def learn_about_topic(self, topic, connect_to_focus=False, max_contexts=5):
        """
        Lernt über ein bestimmtes Thema aus dem Internet und erstellt mehrere zusammenhängende Kontexte.
        
        Args:
            topic: Das Thema oder die Phrase, über die gelernt werden soll
            connect_to_focus: Ob die neuen Kontexte mit dem aktuellen Fokus verbunden werden sollen
            max_contexts: Maximale Anzahl an Kontexten, die erstellt werden sollen
        """
        if not topic:
            print("Kein Thema angegeben. Kann nicht aus dem Internet lernen.")
            return []
        
        # Prüfe, ob es sich um eine Frage handelt
        is_question = '?' in topic or topic.lower().startswith(('wie ', 'warum ', 'wer ', 'was ', 'wo ', 'wann ', 'welche '))
        
        if is_question:
            # Analysiere die Frage
            question_analysis = self.analyze_question(topic)
            print(f"Frageanalyse: {question_analysis}")
            
            # Erstelle eine gezieltere Suchanfrage basierend auf der Analyse
            search_term = topic
            
            # Wenn Entitäten gefunden wurden, verwende sie für die Suche
            if question_analysis['entities']:
                # Kombiniere die Entitäten mit den Attributen für eine präzisere Suche
                entity_terms = ' '.join(question_analysis['entities'])
                
                if question_analysis['attributes']:
                    # Füge Attribute hinzu, um die Suche zu verfeinern
                    attribute_terms = ' '.join(question_analysis['attributes'])
                    search_term = f"{entity_terms} {attribute_terms}"
                else:
                    search_term = entity_terms
        else:
            # Entferne Satzzeichen und normalisiere Leerzeichen
            cleaned_topic = re.sub(r'[^\w\s]', ' ', topic)
            cleaned_topic = re.sub(r'\s+', ' ', cleaned_topic).strip()
            
            # Extrahiere Schlüsselwörter für die Suche
            stop_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'about', 'as', 'of', 'that', 'this', 'these', 'those', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'shall', 'should', 'can', 'could', 'may', 'might', 'must', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their', 'mine', 'yours', 'hers', 'ours', 'theirs']
            
            # Teile den Text in Wörter
            words = cleaned_topic.lower().split()
            
            # Filtere Stoppwörter
            keywords = [word for word in words if len(word) > 3 and word not in stop_words]
            
            # Wenn keine Schlüsselwörter gefunden wurden, verwende den gesamten Text
            if not keywords:
                print(f"Keine Schlüsselwörter in '{topic}' gefunden. Verwende den gesamten Text.")
                search_term = cleaned_topic
            else:
                # Erstelle eine Phrase aus den Schlüsselwörtern (bis zu 3)
                if len(keywords) > 3:
                    # Verwende die wichtigsten Schlüsselwörter (längere Wörter haben mehr Gewicht)
                    keywords.sort(key=len, reverse=True)
                    search_keywords = keywords[:3]
                else:
                    search_keywords = keywords
                
                search_term = " ".join(search_keywords)
        
        print(f"Lerne über: '{search_term}'")
        
        created_contexts = []
        
        try:
            # Hole Inhalte von Wikipedia
            wikipedia_content = self.get_wikipedia_content(search_term)
            
            if not wikipedia_content:
                print(f"Keine Inhalte für '{search_term}' gefunden.")
                return created_contexts
            
            # Wenn es eine Frage war, versuche die relevanten Informationen zu extrahieren
            if is_question:
                # Teile den Inhalt in Absätze
                paragraphs = wikipedia_content.split('\n\n')
                
                # Extrahiere relevante Informationen basierend auf dem Fragetyp und den Attributen
                if question_analysis['type'] == 'beschaffenheit' and 'geschmack' in question_analysis['attributes']:
                    # Suche nach Absätzen, die Geschmacksinformationen enthalten könnten
                    taste_keywords = ['schmeckt', 'geschmack', 'aroma', 'süß', 'sauer', 'bitter', 'salzig', 'würzig', 'scharf', 'mild', 'fruchtig', 'herb']
                    
                    # Bewerte jeden Absatz nach Relevanz für Geschmacksinformationen
                    relevant_paragraphs = []
                    for paragraph in paragraphs:
                        relevance_score = sum(1 for keyword in taste_keywords if keyword.lower() in paragraph.lower())
                        if relevance_score > 0:
                            relevant_paragraphs.append((paragraph, relevance_score))
                    
                    # Sortiere nach Relevanz
                    relevant_paragraphs.sort(key=lambda x: x[1], reverse=True)
                    
                    # Verwende die relevantesten Absätze
                    filtered_paragraphs = [p for p, _ in relevant_paragraphs[:max_contexts]]
                    
                    # Wenn keine relevanten Absätze gefunden wurden, verwende die ersten Absätze
                    if not filtered_paragraphs and paragraphs:
                        filtered_paragraphs = paragraphs[:max_contexts]
                    
                    paragraphs = filtered_paragraphs
            
            # Begrenze die Anzahl der Absätze
            max_paragraphs = min(max_contexts, len(paragraphs))
            
            # Erstelle für jeden Absatz einen Kontext
            for i in range(max_paragraphs):
                paragraph = paragraphs[i].strip()
                
                # Überspringe leere Absätze
                if not paragraph:
                    continue
                
                # Erstelle einen neuen Kontext
                label = f"Learned_{search_term.replace(' ', '_')}_{i}_{int(time.time())}"
                happiness = 0.7  # Hoher Glückswert für neu gelerntes Wissen
                
                context_id = self.create_context(paragraph, label, happiness, source_type="web")
                created_contexts.append(context_id)
                
                # Verbinde den Kontext mit dem vorherigen Kontext (falls vorhanden)
                if i > 0 and created_contexts[i-1]:
                    self.create_connection(created_contexts[i-1], context_id, weight=0.9)
            
            # Verbinde die neuen Kontexte mit dem aktuellen Fokus, falls gewünscht
            if connect_to_focus and self.current_focus and created_contexts:
                for context_id in created_contexts:
                    self.create_connection(self.current_focus, context_id, weight=0.8)
            
            print(f"Neues Wissen erworben über: '{search_term}' ({len(created_contexts)} Kontexte)")
            
            # Setze den Fokus auf den ersten neuen Kontext
            if created_contexts:
                self.set_focus_by_id(created_contexts[0])
            
            return created_contexts
            
        except Exception as e:
            print(f"Fehler beim Lernen aus dem Internet: {e}")
            # Erstelle einen Kontext über den Fehler
            error_text = f"Error occurred while trying to learn about {search_term}."
            label = f"Error_{int(time.time())}"
            happiness = 0.3  # Niedriger Glückswert für Fehler
            
            error_context_id = self.create_context(error_text, label, happiness)
            
            # Verbinde den Fehlerkontext mit dem aktuellen Fokus, falls gewünscht
            if connect_to_focus and self.current_focus:
                self.create_connection(self.current_focus, error_context_id, weight=0.5)
            
            return created_contexts

    def load_state(self, filename: str):
        """Lädt einen gespeicherten Zustand des Bewusstseins."""
        if not os.path.exists(filename):
            print(f"Datei nicht gefunden: {filename}")
            return False
            
        try:
            with open(filename, 'r') as f:
                state = json.load(f)
                
            # Lade grundlegende Attribute
            self.iteration = state.get("iteration", 0)
            self.energy = state.get("energy", 1.0)
            self.energy_decay_rate = state.get("energy_decay_rate", 0.01)
            self.energy_gain_rate = state.get("energy_gain_rate", 0.2)
            self.min_energy_threshold = state.get("min_energy_threshold", 0.3)
            self.max_energy = state.get("max_energy", 1.0)
            self.current_focus = state.get("current_focus", None)
            self.needs_pyramid = state.get("needs_pyramid", {
                "physiological": 1.0,
                "safety": 1.0,
                "belonging": 0.5,
                "esteem": 0.5,
                "self_actualization": 0.2
            })
            
            # Lade emotionalen Zustand
            if "emotional_state" in state and "emotions" in state["emotional_state"]:
                self.emotional_state.emotions = state["emotional_state"]["emotions"]
                
            # Lade Statistiken
            if "stats" in state:
                self.stats = state["stats"]
                
            # Lade Kontexte
            self.contexts = {}
            if "contexts" in state:
                for context_id, context_data in state["contexts"].items():
                    # Erstelle Wörter aus den Strings
                    if "words" in context_data:
                        words = [Word(word) for word in context_data["words"]]
                        
                        # Erstelle den Kontext
                        happiness = context_data.get("happiness", 0.0)
                        context = ReasoningContext(words=words, label=context_id, happiness=happiness)
                        
                        # Füge Verbindungen hinzu, falls vorhanden
                        if "connections" in context_data:
                            context.connections = context_data["connections"]
                            
                        # Füge Habituation hinzu, falls vorhanden
                        if "habituation" in context_data:
                            context.habituation = context_data["habituation"]
                            
                        # Füge den Kontext zum Bewusstsein hinzu
                        self.contexts[context_id] = context
                        
            print(f"Zustand geladen: {filename}")
        return True
        except Exception as e:
            print(f"Fehler beim Laden des Zustands: {e}")
            return False

    def update_stats(self):
        """Aktualisiert die Statistiken des Bewusstseins."""
        # Berechne aktuelle Werte
        current_energy = self.energy
        
        # Berechne Glück basierend auf dem aktuellen Fokus
        current_happiness = 0.0
        if self.current_focus and self.current_focus in self.contexts:
            current_happiness = self.contexts[self.current_focus].happiness
            
        # Zähle Kontexte und Verbindungen
        contexts_count = len(self.contexts)
        
        # Zähle Verbindungen
        connections_count = 0
        for context_id, context in self.contexts.items():
            if hasattr(context, 'connections'):
                connections_count += len(context.connections)
                
        # Aktualisiere Statistiken
        self.stats["energy"].append(current_energy)
        self.stats["happiness"].append(current_happiness)
        self.stats["contexts_count"].append(contexts_count)
        self.stats["connections_count"].append(connections_count)
        self.stats["timestamp"].append(time.time())

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