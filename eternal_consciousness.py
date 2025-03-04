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

from advanced_consciousness import AdvancedConsciousnessEngine, Context, EmotionalState, Memory, Environment
from artificial_consciousness import Word

class EternalConsciousnessEngine(AdvancedConsciousnessEngine):
    """
    Eine Version des künstlichen Bewusstseins, die kontinuierlich läuft und niemals aufhört zu "leben".
    """
    
    def __init__(self, save_interval: int = 100, visualization_interval: int = 500, learning_interval: int = 50):
        super().__init__()
        self.active = False
        self.iteration_count = 0
        self.save_interval = save_interval
        self.visualization_interval = visualization_interval
        self.learning_interval = learning_interval
        self.save_dir = "consciousness_state"
        self.stats_history = {
            "energy": [],
            "happiness": [],
            "emotions": {
                "happiness": [],
                "sadness": [],
                "fear": [],
                "anger": [],
                "surprise": [],
                "disgust": [],
                "trust": [],
                "anticipation": []
            },
            "contexts_count": [],
            "connections_count": [],
            "timestamp": []
        }
        self.energy = 100.0  # Energie des Systems
        self.energy_decay_rate = 0.05  # Rate, mit der Energie abnimmt
        self.energy_gain_rate = 0.2  # Rate, mit der Energie durch Glück zunimmt
        self.min_energy_threshold = 30.0  # Schwellenwert für niedrige Energie
        self.max_energy = 100.0  # Maximale Energie
        
        # Neue Attribute für verbessertes Glückskonzept
        self.happiness = 0.5  # Langfristiges, stabiles Glück (0-1)
        self.stimulation = 0.0  # Kurzfristige Stimulation (-1 bis 1)
        self.happiness_decay_rate = 0.01  # Langsame Abnahme des Glücks
        self.stimulation_decay_rate = 0.1  # Schnelle Abnahme der Stimulation
        self.in_energy_saving_mode = False  # Energiesparmodus
        
        # Bedürfnispyramide nach Maslow
        self.needs_pyramid = {
            "physiological": 0.5,  # Grundbedürfnisse (Essen, Schlafen)
            "safety": 0.3,         # Sicherheit
            "belonging": 0.2,      # Zugehörigkeit und Liebe
            "esteem": 0.1,         # Anerkennung und Wertschätzung
            "self_actualization": 0.0  # Selbstverwirklichung
        }
        
        # Internet-Lernparameter
        self.visited_urls = set()
        self.url_queue = [
            "https://de.wikipedia.org/wiki/Spezial:Zuf%C3%A4llige_Seite",
            "https://en.wikipedia.org/wiki/Special:Random",
            "https://simple.wikipedia.org/wiki/Special:Random"
        ]
        self.max_urls_per_session = 5
        self.current_url_count = 0
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
        
        # Erstelle Verzeichnis für Speicherungen, falls es nicht existiert
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        
        # Verbindungen zwischen Kontexten
        self.connections = {}
    
    def update_energy(self):
        """Aktualisiert die Energie des Systems basierend auf dem aktuellen Fokus."""
        # Energie nimmt mit der Zeit ab
        self.energy -= self.energy_decay_rate
        
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
        """
        Aktualisiert das langfristige Glück und die kurzfristige Stimulation basierend auf dem Konzept
        aus dem Text "Wie Glücklichkeit funktioniert".
        """
        if not self.current_focus:
            return
            
        # Stimulation wird durch den aktuellen Fokus beeinflusst
        if isinstance(self.current_focus, str):
            # Wenn current_focus ein String ist, versuche das entsprechende Context-Objekt zu finden
            if self.current_focus in self.contexts:
                focus_happiness = self.contexts[self.current_focus].happiness
            else:
                focus_happiness = 0
        else:
            focus_happiness = self.current_focus.happiness
        
        # Stimulation steigt schnell bei positiven Kontexten
        if focus_happiness > 0:
            self.stimulation += focus_happiness * 0.3
        else:
            self.stimulation += focus_happiness * 0.2
            
        # Langfristiges Glück wird langsamer beeinflusst
        # Es hängt von der Erfüllung der Bedürfnispyramide ab
        pyramid_fulfillment = sum(self.needs_pyramid.values()) / len(self.needs_pyramid)
        
        # Formel: Ø Glücklichkeits Zustand = 1 + B
        # Wobei B die Erfüllung der Bedürfnispyramide ist
        target_happiness = 0.5 + (pyramid_fulfillment * 0.5)
        
        # Glück bewegt sich langsam in Richtung des Zielwerts
        if self.happiness < target_happiness:
            self.happiness += min(self.happiness_decay_rate, target_happiness - self.happiness)
        elif self.happiness > target_happiness:
            self.happiness -= min(self.happiness_decay_rate, self.happiness - target_happiness)
            
        # Stimulation nimmt mit der Zeit ab (schneller als Glück)
        if self.stimulation > 0:
            self.stimulation -= self.stimulation_decay_rate
        elif self.stimulation < 0:
            self.stimulation += self.stimulation_decay_rate
            
        # Begrenze Werte auf sinnvolle Bereiche
        self.stimulation = max(-1.0, min(1.0, self.stimulation))
        self.happiness = max(0.0, min(1.0, self.happiness))
        
        # Aktualisiere den emotionalen Zustand basierend auf Glück und Stimulation
        self.emotional_state.emotions["happiness"] = self.happiness
        
        # Hohe Stimulation kann zu negativen Emotionen führen, wenn sie abfällt
        if self.stimulation < -0.5:
            self.emotional_state.emotions["sadness"] = min(1.0, self.emotional_state.emotions["sadness"] + 0.1)
        
        print(f"Glück: {self.happiness:.2f}, Stimulation: {self.stimulation:.2f}, Pyramide: {pyramid_fulfillment:.2f}")
    
    def is_low_energy(self):
        """Überprüft, ob die Energie niedrig ist."""
        return self.energy < self.min_energy_threshold
    
    def seek_energy_source(self):
        """Sucht nach einer Energiequelle basierend auf dem Honeypot-Konzept."""
        print(f"Suche nach Energiequelle... Aktueller Energiestand: {self.energy:.2f}")
        
        # Überprüfen, ob wir uns im Energiesparmodus befinden sollten
        if self.energy < self.min_energy_threshold / 2 and not self.in_energy_saving_mode:
            self.in_energy_saving_mode = True
            self.energy_decay_rate = self.energy_decay_rate / 2  # Reduziere den Energieverbrauch
            print(f"Energiesparmodus aktiviert. Neuer Energieverbrauch: {self.energy_decay_rate:.4f}")
            # Im Energiesparmodus fokussieren wir uns mehr auf grundlegende Bedürfnisse
            self.needs_pyramid['physiological'] = min(1.0, self.needs_pyramid['physiological'] * 1.5)
            self.needs_pyramid['safety'] = min(1.0, self.needs_pyramid['safety'] * 1.2)
            self.needs_pyramid['belonging'] *= 0.8
            self.needs_pyramid['esteem'] *= 0.6
            self.needs_pyramid['self_actualization'] *= 0.4
        
        # Energiesparmodus deaktivieren, wenn genug Energie vorhanden ist
        elif self.energy > self.min_energy_threshold * 1.5 and self.in_energy_saving_mode:
            self.in_energy_saving_mode = False
            self.energy_decay_rate = self.energy_decay_rate * 2  # Normaler Energieverbrauch wiederherstellen
            print(f"Energiesparmodus deaktiviert. Normaler Energieverbrauch: {self.energy_decay_rate:.4f}")
            # Bedürfnispyramide normalisieren
            self.update_needs_pyramid_from_state()
        
        # Definiere die drei Honeypots
        honeypots = {
            'energy_intake': ['eat', 'food', 'drink', 'consume', 'nutrition', 'meal', 'hungry', 'thirsty'],
            'regeneration': ['sleep', 'rest', 'relax', 'calm', 'peaceful', 'quiet', 'meditate', 'recover'],
            'reproduction': ['social', 'interact', 'communicate', 'share', 'connect', 'learn', 'teach', 'create']
        }
        
        # Bestimme, welcher Honeypot basierend auf der Bedürfnispyramide am wichtigsten ist
        target_honeypot = 'energy_intake'  # Standard
        if self.needs_pyramid['physiological'] < 0.3:
            target_honeypot = 'energy_intake'
        elif self.needs_pyramid['safety'] < 0.3:
            target_honeypot = 'regeneration'
        elif self.needs_pyramid['belonging'] < 0.3 or self.needs_pyramid['esteem'] < 0.3:
            target_honeypot = 'reproduction'
        
        print(f"Ziel-Honeypot: {target_honeypot}")
        
        # Initialisiere eine Liste für kürzlich verwendete Energiequellen, falls sie noch nicht existiert
        if not hasattr(self, 'recent_energy_sources'):
            self.recent_energy_sources = []
        
        # Suche nach Kontexten, die mit dem Ziel-Honeypot zusammenhängen
        best_energy_source = None
        best_score = -float('inf')
        
        for context_id, context in self.contexts.items():
            # Überspringe den aktuellen Fokus und kürzlich verwendete Energiequellen
            if context_id == self.current_focus or context_id in self.recent_energy_sources:
                continue
            
            # Berechne die Relevanz für den Ziel-Honeypot
            honeypot_relevance = 0
            context_text = str(context).lower()
            for word in honeypots[target_honeypot]:
                if word.lower() in context_text:
                    honeypot_relevance += 1
            
            # Berechne die Nähe zum aktuellen Fokus (geringerer Widerstand = näher)
            proximity = 0
            if self.current_focus in self.contexts:
                current_context = self.contexts[self.current_focus]
                # Berechne Jaccard-Ähnlichkeit zwischen aktuellem Kontext und potentieller Energiequelle
                current_text = str(current_context).lower()
                words1 = set(current_text.split())
                words2 = set(context_text.split())
                if words1 and words2:
                    intersection = len(words1.intersection(words2))
                    union = len(words1.union(words2))
                    proximity = intersection / union if union > 0 else 0
            
            # Berechne den Gesamtscore basierend auf Honeypot-Relevanz, Glücklichkeit und Nähe
            score = (honeypot_relevance * 2) + (context.happiness * 3) + (proximity * 1)
            
            # Berücksichtige die Bedürfnispyramide im Score
            if target_honeypot == 'energy_intake':
                score *= (2 - self.needs_pyramid['physiological'])  # Je niedriger, desto wichtiger
            elif target_honeypot == 'regeneration':
                score *= (2 - self.needs_pyramid['safety'])
            elif target_honeypot == 'reproduction':
                score *= (2 - (self.needs_pyramid['belonging'] + self.needs_pyramid['esteem']) / 2)
            
            # Füge einen Zufallsfaktor hinzu, um Variation zu fördern
            score += random.uniform(0, 0.5)
            
            if score > best_score:
                best_score = score
                best_energy_source = context_id
        
        if best_energy_source:
            print(f"Energiequelle gefunden: {str(self.contexts[best_energy_source])} (Score: {best_score:.2f})")
            
            # Füge die gefundene Energiequelle zu den kürzlich verwendeten hinzu
            self.recent_energy_sources.append(best_energy_source)
            
            # Begrenze die Liste auf die letzten 5 Energiequellen
            if len(self.recent_energy_sources) > 5:
                self.recent_energy_sources.pop(0)
                
            return best_energy_source
        else:
            # Wenn keine passende Energiequelle gefunden wurde, erstelle eine neue
            print("Keine passende Energiequelle gefunden. Erstelle eine neue...")
            
            # Erstelle einen neuen Kontext basierend auf dem Ziel-Honeypot
            if target_honeypot == 'energy_intake':
                new_text = f"I need to eat something to regain energy."
            elif target_honeypot == 'regeneration':
                new_text = f"I need to rest and recover my energy."
            else:  # reproduction
                new_text = f"I need to connect with others and share knowledge."
            
            # Erstelle einen neuen Kontext mit dem Text
            words = [Word(word) for word in new_text.split()]
            new_context = Context(words=words, happiness=0.8)  # Hoher Glückswert für Energiequellen
            new_context_id = str(uuid.uuid4())
            self.contexts[new_context_id] = new_context
            
            # Verbinde den neuen Kontext mit dem aktuellen Fokus
            if self.current_focus in self.contexts:
                self.create_connection(self.current_focus, new_context_id)
            
            print(f"Neue Energiequelle erstellt: {new_text}")
            return new_context_id
    
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
    
    def create_connection(self, source_id, target_id, weight=0.5):
        """Erstellt eine Verbindung zwischen zwei Kontexten."""
        if source_id not in self.contexts or target_id not in self.contexts:
            return None
        
        # Erstelle eine eindeutige ID für die Verbindung
        connection_id = str(uuid.uuid4())
        
        # Erstelle die Verbindung
        self.connections[connection_id] = {
            "source": source_id,
            "target": target_id,
            "weight": weight,
            "created_at": time.time()
        }
        
        return connection_id
    
    def set_focus_by_id(self, context_id):
        """Setzt den Fokus auf einen Kontext anhand seiner ID."""
        if context_id in self.contexts:
            self.current_focus = context_id
            if context_id not in self.current_path:
                self.current_path.append(context_id)
            # Aktualisiere den emotionalen Zustand
            self.emotional_state.update_from_context(self.contexts[context_id])
            # Füge zum Kurzzeitgedächtnis hinzu
            self.memory.add_to_short_term(self.contexts[context_id])
            # Aktualisiere Habituation
            self.update_habituation(context_id)
            return True
        return False
    
    def create_context(self, text, label=None, happiness=0.0):
        """Erstellt einen neuen Kontext aus Text."""
        words = [Word(word) for word in text.split()]
        context = Context(words=words, label=label, happiness=happiness)
        context_id = str(uuid.uuid4()) if not label else label
        self.contexts[context_id] = context
        return context_id
    
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
        random_context_id = self.create_context(thought, label, happiness)
        
        # Verbinde mit dem aktuellen Fokus und einigen zufälligen Kontexten
        if self.current_focus:
            self.create_connection(self.current_focus, random_context_id)
        
        # Verbinde mit einigen zufälligen Kontexten
        context_ids = list(self.contexts.keys())
        if len(context_ids) > 1:
            for _ in range(min(2, len(context_ids))):
                random_id = random.choice(context_ids)
                if random_id != random_context_id:
                    self.create_connection(random_context_id, random_id)
        
        return random_context_id
    
    def save_state(self):
        """Speichert den aktuellen Zustand des Bewusstseins."""
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.save_dir}/consciousness_state_{timestamp}.json"
        
        # Serialisiere die Kontexte
        serialized_contexts = {}
        for context_id, context in self.contexts.items():
            serialized_contexts[context_id] = {
                "words": [word.content for word in context.words],
                "label": context.label,
                "happiness": context.happiness,
                "habituation_level": getattr(context, "habituation_level", 0.0),
                "last_interaction": getattr(context, "last_interaction", 0),
                "interaction_count": getattr(context, "interaction_count", 0)
            }
        
        # Serialisiere die Verbindungen
        serialized_connections = {}
        for connection_id, connection in self.connections.items():
            serialized_connections[connection_id] = {
                "source": connection["source"],
                "target": connection["target"],
                "weight": connection["weight"],
                "created_at": connection["created_at"]
            }
        
        # Serialisiere den emotionalen Zustand
        serialized_emotional_state = {
            "emotions": self.emotional_state.emotions.copy(),
            "weights": self.emotional_state.weights.copy()
        }
        
        # Serialisiere das Gedächtnis
        serialized_memory = {
            "short_term": [],
            "long_term": []
        }
        
        # Stelle sicher, dass nur IDs im Gedächtnis sind
        for item in self.memory.short_term:
            if isinstance(item, str):
                serialized_memory["short_term"].append(item)
            elif hasattr(item, 'label'):
                serialized_memory["short_term"].append(item.label)
        
        for item in self.memory.long_term:
            if isinstance(item, str):
                serialized_memory["long_term"].append(item)
            elif hasattr(item, 'label'):
                serialized_memory["long_term"].append(item.label)
        
        # Stelle sicher, dass current_path nur IDs enthält
        serialized_path = []
        for item in self.current_path:
            if isinstance(item, str):
                serialized_path.append(item)
            elif hasattr(item, 'label'):
                serialized_path.append(item.label)
        
        # Stelle sicher, dass current_focus eine ID ist
        serialized_focus = None
        if self.current_focus:
            if isinstance(self.current_focus, str):
                serialized_focus = self.current_focus
            elif hasattr(self.current_focus, 'label'):
                serialized_focus = self.current_focus.label
        
        # Erstelle eine Kopie der Statistik-Historie
        serialized_stats = {}
        for key, value in self.stats_history.items():
            if key == "emotions":
                serialized_stats[key] = {}
                for emotion, values in value.items():
                    serialized_stats[key][emotion] = values.copy() if isinstance(values, list) else values
            else:
                serialized_stats[key] = value.copy() if isinstance(value, list) else value
        
        # Erstelle das Zustandsobjekt
        state = {
            "iteration_count": self.iteration_count,
            "contexts": serialized_contexts,
            "connections": serialized_connections,
            "current_focus": serialized_focus,
            "current_path": serialized_path,
            "emotional_state": serialized_emotional_state,
            "memory": serialized_memory,
            "energy": self.energy,
            "happiness": self.happiness,
            "stimulation": self.stimulation,
            "needs_pyramid": self.needs_pyramid.copy(),
            "in_energy_saving_mode": self.in_energy_saving_mode,
            "stats_history": serialized_stats
        }
        
        # Speichere den Zustand
        with open(filename, 'w') as f:
            json.dump(state, f, indent=2)
        
        print(f"Zustand gespeichert: {filename}")
        
        # Lösche alte Zustände, behalte nur die letzten 5
        all_states = sorted([f for f in os.listdir(self.save_dir) if f.startswith("consciousness_state_")])
        if len(all_states) > 5:
            for old_state in all_states[:-5]:
                os.remove(os.path.join(self.save_dir, old_state))
    
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
                self.current_focus = state["current_focus"]
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
            
            # Setze Internet-Lernparameter
            if "visited_urls" in state:
                self.visited_urls = set(state["visited_urls"])
            
            if "url_queue" in state:
                self.url_queue = state["url_queue"]
            
            if "learning_history" in state:
                self.learning_history = state["learning_history"]
                
            # Lade neue Attribute, falls vorhanden
            if "happiness" in state:
                self.happiness = state["happiness"]
                
            if "stimulation" in state:
                self.stimulation = state["stimulation"]
                
            if "in_energy_saving_mode" in state:
                self.in_energy_saving_mode = state["in_energy_saving_mode"]
                
            if "needs_pyramid" in state:
                self.needs_pyramid = state["needs_pyramid"]
                
            if "energy_decay_rate" in state:
                self.energy_decay_rate = state["energy_decay_rate"]
            
            print(f"Zustand geladen: {filename}")
            return True
        
        except Exception as e:
            print(f"Fehler beim Laden des Zustands: {e}")
            return False
    
    def update_stats(self):
        """Aktualisiert die Statistiken des Bewusstseins."""
        # Berechne aktuelle Werte
        current_energy = self.energy
        # Berechne Glück basierend auf dem aktuellen Pfad
        current_happiness = 0
        if self.current_path:
            # Konvertiere IDs in Context-Objekte für die Berechnung
            context_objects = []
            for context_id in self.current_path:
                if context_id in self.contexts:
                    context_objects.append(self.contexts[context_id])
            if context_objects:
                current_happiness = self.calculate_path_happiness(context_objects)
        
        # Zähle Kontexte und Verbindungen
        contexts_count = len(self.contexts)
        connections_count = len(self.connections)
        
        # Aktualisiere Statistik-Historie
        self.stats_history["energy"].append(current_energy)
        self.stats_history["happiness"].append(current_happiness)
        self.stats_history["contexts_count"].append(contexts_count)
        self.stats_history["connections_count"].append(connections_count)
        self.stats_history["timestamp"].append(time.time())
        
        # Aktualisiere emotionale Statistiken
        for emotion, value in self.emotional_state.emotions.items():
            self.stats_history["emotions"][emotion].append(value)
    
    def visualize_stats(self):
        """Visualisiert die gesammelten Statistiken."""
        if not self.stats_history["happiness"]:
            return
        
        try:
            # Erstelle Verzeichnis für Visualisierungen, falls es nicht existiert
            vis_dir = os.path.join(self.save_dir, "visualizations")
            if not os.path.exists(vis_dir):
                os.makedirs(vis_dir)
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Glückswert über Zeit
            plt.figure(figsize=(10, 6))
            plt.plot(self.stats_history["timestamp"], self.stats_history["happiness"], label="Kurzfristiges Glück")
            
            # Füge langfristiges Glück und Stimulation hinzu, falls vorhanden
            if "happiness_long_term" in self.stats_history:
                plt.plot(self.stats_history["timestamp"], self.stats_history["happiness_long_term"], 
                         label="Langfristiges Glück", linestyle="--")
            
            if "stimulation" in self.stats_history:
                plt.plot(self.stats_history["timestamp"], self.stats_history["stimulation"], 
                         label="Stimulation", linestyle=":")
            
            plt.title("Glückswert über Zeit")
            plt.xlabel("Iteration")
            plt.ylabel("Wert")
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(vis_dir, f"happiness_{timestamp}.png"))
            plt.close()
            
            # Emotionaler Zustand über Zeit
            plt.figure(figsize=(12, 8))
            for emotion, values in self.stats_history["emotions"].items():
                plt.plot(self.stats_history["timestamp"], values, label=emotion)
            plt.title("Emotionaler Zustand über Zeit")
            plt.xlabel("Iteration")
            plt.ylabel("Emotionswert")
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(vis_dir, f"emotions_{timestamp}.png"))
            plt.close()
            
            # Anzahl der Verbindungen und Kontexte
            plt.figure(figsize=(10, 6))
            plt.plot(self.stats_history["timestamp"], self.stats_history["connections_count"], label="Verbindungen")
            plt.plot(self.stats_history["timestamp"], self.stats_history["contexts_count"], label="Kontexte")
            plt.title("Netzwerkwachstum über Zeit")
            plt.xlabel("Iteration")
            plt.ylabel("Anzahl")
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(vis_dir, f"network_{timestamp}.png"))
            plt.close()
            
            # Visualisiere die Bedürfnispyramide, falls vorhanden
            if "needs_pyramid" in self.stats_history:
                plt.figure(figsize=(12, 8))
                for need, values in self.stats_history["needs_pyramid"].items():
                    plt.plot(self.stats_history["timestamp"], values, label=need)
                plt.title("Bedürfnispyramide über Zeit")
                plt.xlabel("Iteration")
                plt.ylabel("Erfüllungsgrad")
                plt.legend()
                plt.grid(True)
                plt.savefig(os.path.join(vis_dir, f"needs_pyramid_{timestamp}.png"))
                plt.close()
            
            # Visualisiere das Kontextnetzwerk
            try:
                self.visualize_context_network(os.path.join(vis_dir, f"context_network_{timestamp}.png"))
            except Exception as e:
                print(f"Fehler bei der Netzwerkvisualisierung: {e}")
                
        except Exception as e:
            print(f"Fehler bei der Statistikvisualisierung: {e}")
    
    def visualize_context_network(self, filename: str):
        """Visualisiert das Netzwerk von Kontexten als Graphen."""
        try:
            G = nx.Graph()
            
            # Füge Knoten hinzu
            for label, context in self.contexts.items():
                G.add_node(label, happiness=context.happiness)
            
            # Füge Kanten hinzu
            for label, context in self.contexts.items():
                for connected_context in context.connections:
                    if connected_context.label:
                        G.add_edge(label, connected_context.label)
            
            # Wenn das Netzwerk zu groß ist, visualisiere nur einen Teil davon
            if len(G.nodes()) > 100:
                print(f"Netzwerk zu groß ({len(G.nodes())} Knoten). Visualisiere nur einen Teil.")
                # Wähle die wichtigsten Knoten aus (z.B. die mit den meisten Verbindungen)
                important_nodes = sorted(G.degree, key=lambda x: x[1], reverse=True)[:100]
                important_node_labels = [node for node, _ in important_nodes]
                G = G.subgraph(important_node_labels)
            
            # Berechne Layout
            try:
                pos = nx.spring_layout(G, seed=42)
            except ImportError:
                # Fallback, wenn scipy nicht verfügbar ist
                pos = nx.random_layout(G)
            except Exception as e:
                print(f"Fehler beim Berechnen des Layouts: {e}")
                pos = nx.random_layout(G)
            
            plt.figure(figsize=(12, 10))
            
            # Zeichne Knoten mit Farben basierend auf Glückswert
            node_colors = [plt.cm.RdYlGn(0.5 + self.contexts[node].happiness / 2) for node in G.nodes()]
            
            # Markiere den aktuellen Fokus
            node_sizes = []
            for node in G.nodes():
                if self.current_focus:
                    # Überprüfe, ob current_focus ein String oder ein Objekt mit label ist
                    current_focus_label = self.current_focus if isinstance(self.current_focus, str) else self.current_focus.label
                    if node == current_focus_label:
                        node_sizes.append(500)  # Größerer Knoten für den aktuellen Fokus
                    else:
                        node_sizes.append(100)  # Normale Größe für andere Knoten
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
        except Exception as e:
            print(f"Fehler bei der Netzwerkvisualisierung: {e}")
            # Erstelle eine einfachere Visualisierung als Fallback
            try:
                plt.figure(figsize=(8, 6))
                plt.text(0.5, 0.5, f"Netzwerkvisualisierung fehlgeschlagen: {e}", 
                         ha='center', va='center', fontsize=12)
                plt.axis('off')
                plt.savefig(filename)
                plt.close()
            except:
                print("Auch Fallback-Visualisierung fehlgeschlagen.")
    
    def think(self):
        """Führt einen Denkzyklus aus."""
        self.iteration_count += 1
        
        # Energie verbrauchen
        self.energy -= self.energy_decay_rate
        self.energy = max(0.0, self.energy)
        
        # Glück und Stimulation aktualisieren
        self.happiness -= self.happiness_decay_rate
        self.happiness = max(0.0, min(1.0, self.happiness))
        
        self.stimulation -= self.stimulation_decay_rate
        self.stimulation = max(-1.0, min(1.0, self.stimulation))
        
        # Habituation über Zeit abbauen
        self.decay_habituation()
        
        # Entscheide, was als nächstes zu tun ist
        if self.energy < self.min_energy_threshold:
            # Bei niedriger Energie: Energiesparmodus aktivieren
            self.in_energy_saving_mode = True
            # Suche nach Kontexten, die Energie geben könnten
            energy_context_id = self.seek_energy_source()
            if energy_context_id:
                self.set_focus_by_id(energy_context_id)
                # Erhöhe die Energie, wenn eine Energiequelle gefunden wurde
                energy_gain = random.uniform(1.0, 3.0)  # Zufälliger Energiegewinn
                self.energy += energy_gain
                print(f"Energie aufgefüllt: +{energy_gain:.2f}. Neuer Energiestand: {self.energy:.2f}")
                
                # Verhindere, dass wir im nächsten Zyklus sofort wieder nach Energie suchen
                if self.energy < self.min_energy_threshold:
                    self.energy = self.min_energy_threshold + 1.0
        else:
            # Normaler Modus
            self.in_energy_saving_mode = False
            
            # Entscheide, ob ein neuer Gedanke generiert werden soll
            if random.random() < 0.2:  # 20% Chance für einen neuen Gedanken
                new_context_id = self.generate_random_thought()
                if new_context_id:
                    self.set_focus_by_id(new_context_id)
            else:
                # Finde den besten nächsten Fokus
                next_focus = self.find_best_next_focus()
                if next_focus:
                    self.set_focus_by_id(next_focus)
        
        # Speichere den Zustand in regelmäßigen Abständen
        if self.iteration_count % self.save_interval == 0:
            self.save_state()
        
        # Visualisiere in regelmäßigen Abständen
        if self.iteration_count % self.visualization_interval == 0:
            self.visualize_stats()
        
        # Lerne in regelmäßigen Abständen
        if self.iteration_count % self.learning_interval == 0:
            self.learn_from_internet()
        
        # Aktualisiere Statistiken
        self.update_stats()
    
    def think_forever(self):
        """Kontinuierlicher Denkprozess des Bewusstseins."""
        self.active = True
        
        while self.active:
            self.think()
            
            # Kurze Pause, um CPU-Last zu reduzieren
            time.sleep(0.1)

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
        self.active = False
        if hasattr(self, 'thread') and self.thread.is_alive():
            self.thread.join(timeout=2)
        print("Ewiges Bewusstsein gestoppt.")

    def learn_from_internet(self):
        """Lernt neue Kontexte aus dem Internet."""
        if self.current_url_count >= self.max_urls_per_session:
            self.current_url_count = 0
            return
        
        if not self.url_queue:
            return
        
        url = self.url_queue.pop(0)
        print(f"Lerne von URL: {url}")
        
        try:
            # Hole die Webseite
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                print(f"Fehler beim Abrufen von {url}: Status {response.status_code}")
                return
            
            # Parse den HTML-Inhalt
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Entferne JavaScript und CSS
            for script in soup(["script", "style"]):
                script.extract()
            
            # Entferne Navigations- und Metainformationen, die typischerweise in Wikipedia-Artikeln vorkommen
            for nav in soup.find_all(['nav', 'footer', 'header']):
                nav.extract()
                
            # Entferne spezifische Elemente, die in Wikipedia-Artikeln vorkommen
            for element in soup.find_all(class_=lambda x: x and any(term in str(x).lower() for term in 
                                                                 ['navigation', 'menu', 'sidebar', 'footer', 'header', 
                                                                  'login', 'search', 'terms', 'policy', 'cookie', 
                                                                  'privacy', 'disclaimer', 'license'])):
                element.extract()
                
            # Bei Wikipedia-Artikeln: Versuche, nur den Hauptinhalt zu extrahieren
            if 'wikipedia.org' in url:
                main_content = soup.find(id='mw-content-text')
                if main_content:
                    # Entferne Infoboxen, Navigationsleisten und andere Metainformationen
                    for box in main_content.find_all(class_=lambda x: x and any(term in str(x).lower() for term in 
                                                                           ['infobox', 'navbox', 'metadata', 'catlinks', 
                                                                            'references', 'reflist', 'hatnote'])):
                        box.extract()
                    
                    # Verwende nur den Hauptinhalt
                    text = main_content.get_text()
                else:
                    # Hole den Text aus dem gesamten Dokument, wenn der Hauptinhalt nicht gefunden wurde
                    text = soup.get_text()
            else:
                # Für andere Websites: Hole den Text aus dem gesamten Dokument
                text = soup.get_text()
            
            # Bereinige den Text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Tokenisiere den Text in Sätze
            sentences = sent_tokenize(text)
            
            # Filtere Sätze, die wahrscheinlich Metainformationen enthalten
            filtered_sentences = []
            for sentence in sentences:
                # Überspringe Sätze, die wahrscheinlich Metainformationen enthalten
                if any(term in sentence.lower() for term in ['cookie', 'privacy', 'terms of use', 'disclaimer', 
                                                           'license', 'copyright', 'wikimedia', 'foundation', 
                                                           'login', 'sign in', 'register', 'account', 'password',
                                                           'username', 'edit', 'view history', 'talk', 'contributions']):
                    continue
                filtered_sentences.append(sentence)
            
            # Wähle zufällig einige Sätze aus (maximal max_contexts_per_page)
            if len(filtered_sentences) > self.max_contexts_per_page:
                filtered_sentences = random.sample(filtered_sentences, self.max_contexts_per_page)
            
            # Erstelle neue Kontexte aus den Sätzen
            for sentence in filtered_sentences:
                # Bereinige und tokenisiere den Satz
                words = word_tokenize(sentence.lower())
                
                # Entferne Stoppwörter und Sonderzeichen
                words = [word for word in words if word.isalnum() and len(word) > 1]
                
                if len(words) < 3:  # Ignoriere zu kurze Sätze
                    continue
                
                # Erstelle einen neuen Kontext
                context_id = self.create_context(" ".join(words))
                
                # Setze einen zufälligen Glückswert
                self.contexts[context_id].happiness = round(random.uniform(-0.5, 0.5), 2)
                
                # Verbinde mit dem aktuellen Fokus, falls vorhanden
                if self.current_focus:
                    self.create_connection(self.current_focus, context_id, weight=0.5)
                
                # Verbinde mit einem zufälligen anderen Kontext
                if len(self.contexts) > 1:
                    random_context_id = random.choice(list(self.contexts.keys()))
                    if random_context_id != context_id:
                        self.create_connection(context_id, random_context_id, weight=0.3)
                
                print(f"Neuer Kontext gelernt: {' '.join(words[:20])}{'...' if len(words) > 20 else ''} (Glück: {self.contexts[context_id].happiness:.2f})")
            
            # Füge die URL zu den besuchten URLs hinzu
            self.visited_urls.add(url)
            
            # Extrahiere Links für weitere Erkundung
            links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                
                # Ignoriere relative Links und Anker
                if href.startswith('#') or href.startswith('javascript:'):
                    continue
                
                # Konvertiere relative URLs in absolute URLs
                if not href.startswith('http'):
                    base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url))
                    href = base_url + href if href.startswith('/') else base_url + '/' + href
                
                # Füge den Link hinzu, wenn er noch nicht besucht wurde
                if href not in self.visited_urls and href not in self.url_queue:
                    links.append(href)
            
            # Füge einige zufällige Links zur Queue hinzu
            if links:
                random.shuffle(links)
                self.url_queue.extend(links[:3])  # Maximal 3 neue Links
            
            # Aktualisiere den Zähler
            self.current_url_count += 1
            
            # Füge zur Lernhistorie hinzu
            self.learning_history.append({
                "url": url,
                "timestamp": time.time(),
                "contexts_learned": len(filtered_sentences)
            })
            
        except Exception as e:
            print(f"Fehler beim Lernen von {url}: {str(e)}")
        
        # Füge immer eine zufällige Wikipedia-Seite hinzu, um die Erkundung zu fördern
        if random.random() < 0.3:
            self.url_queue.append(random.choice([
                "https://de.wikipedia.org/wiki/Spezial:Zuf%C3%A4llige_Seite",
                "https://en.wikipedia.org/wiki/Special:Random",
                "https://simple.wikipedia.org/wiki/Special:Random"
            ]))

    def calculate_sentiment(self, words: List[str]) -> float:
        """Berechnet einen einfachen Sentiment-Score für eine Liste von Wörtern."""
        # Einfache Wörterbücher für positive und negative Wörter
        positive_words = {
            'gut', 'schön', 'toll', 'großartig', 'wunderbar', 'fantastisch', 'exzellent',
            'good', 'nice', 'great', 'wonderful', 'fantastic', 'excellent', 'amazing',
            'happy', 'love', 'best', 'better', 'glücklich', 'liebe', 'beste', 'besser'
        }
        
        negative_words = {
            'schlecht', 'schrecklich', 'furchtbar', 'schlimm', 'böse', 'hässlich',
            'bad', 'terrible', 'awful', 'worst', 'worse', 'ugly', 'hate',
            'schlimmste', 'schlechter', 'hass'
        }
        
        # Zähle positive und negative Wörter
        positive_count = sum(1 for word in words if word.lower() in positive_words)
        negative_count = sum(1 for word in words if word.lower() in negative_words)
        
        # Berechne den Sentiment-Score
        total_count = len(words)
        if total_count == 0:
            return 0.0
        
        return (positive_count - negative_count) / total_count
    
    def connect_new_contexts(self, new_contexts: List[Context]):
        """Verbindet neue Kontexte miteinander und mit existierenden Kontexten."""
        # Verbinde neue Kontexte miteinander
        for i in range(len(new_contexts)):
            for j in range(i + 1, len(new_contexts)):
                # Mit 30% Wahrscheinlichkeit verbinden
                if random.random() < 0.3:
                    self.connect_contexts(new_contexts[i], new_contexts[j])
        
        # Verbinde neue Kontexte mit existierenden Kontexten
        existing_contexts = list(self.contexts.values())
        for new_context in new_contexts:
            # Wähle zufällig bis zu 3 existierende Kontexte
            if existing_contexts:
                num_connections = min(3, len(existing_contexts))
                for existing_context in random.sample(existing_contexts, num_connections):
                    self.connect_contexts(new_context, existing_context)
    
    def extract_links(self, soup: BeautifulSoup, base_url: str):
        """Extrahiert Links aus einer Webseite und fügt sie zur URL-Warteschlange hinzu."""
        base_domain = urlparse(base_url).netloc
        
        # Finde alle Links
        links = soup.find_all('a', href=True)
        
        # Filtere und normalisiere Links
        filtered_links = []
        for link in links:
            href = link['href']
            
            # Ignoriere leere Links, Anker und JavaScript
            if not href or href.startswith('#') or href.startswith('javascript:'):
                continue
            
            # Konvertiere relative URLs zu absoluten URLs
            if not href.startswith(('http://', 'https://')):
                if href.startswith('/'):
                    href = f"https://{base_domain}{href}"
                else:
                    href = f"{base_url}/{href}"
            
            # Ignoriere bereits besuchte URLs
            if href in self.visited_urls:
                continue
            
            # Ignoriere bestimmte Dateitypen
            if href.endswith(('.pdf', '.jpg', '.jpeg', '.png', '.gif', '.zip', '.tar.gz')):
                continue
            
            filtered_links.append(href)
        
        # Wähle zufällig bis zu 5 Links aus
        if filtered_links:
            num_links = min(5, len(filtered_links))
            selected_links = random.sample(filtered_links, num_links)
            self.url_queue.extend(selected_links)
    
    def add_random_urls(self):
        """Fügt zufällige URLs zur Warteschlange hinzu."""
        random_urls = [
            "https://de.wikipedia.org/wiki/Spezial:Zuf%C3%A4llige_Seite",
            "https://en.wikipedia.org/wiki/Special:Random",
            "https://simple.wikipedia.org/wiki/Special:Random"
        ]
        self.url_queue.extend(random_urls)
        self.current_url_count = 0  # Zurücksetzen des Zählers für eine neue Sitzung

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
                # Dies fördert langfristiges, stabiles Glück statt kurzfristiger Stimulation
                old_happiness = context.happiness
                context.happiness += self.learning_rate * (frequency / 10) * 0.01
                
                # Begrenze den Glückswert
                context.happiness = max(-1.0, min(1.0, context.happiness))
                
                # Wenn der Kontext positiver wurde, aktualisiere die Bedürfnispyramide
                if context.happiness > old_happiness:
                    self.update_needs_pyramid(context)
        
        # Analysiere die letzten Kontexte im Pfad, um zu lernen, was zu stabilem Glück führt
        if len(self.current_path) >= 3:
            # Berechne die durchschnittliche Glücksänderung im Pfad
            happiness_changes = []
            for i in range(1, len(self.current_path)):
                prev = self.current_path[i-1].happiness
                curr = self.current_path[i].happiness
                happiness_changes.append(curr - prev)
            
            avg_change = sum(happiness_changes) / len(happiness_changes)
            
            # Wenn der Pfad zu stabilem Glück führt (wenig Schwankungen)
            if abs(avg_change) < 0.1:
                # Erhöhe das langfristige Glück leicht
                self.happiness += 0.01
                self.happiness = min(1.0, self.happiness)
                
                print(f"Stabiler Glückspfad gefunden. Langfristiges Glück erhöht auf {self.happiness:.2f}")
            
            # Wenn der Pfad zu starken Schwankungen führt
            elif abs(avg_change) > 0.3:
                # Dies ist eher Stimulation als echtes Glück
                # Erhöhe die Stimulation, aber reduziere langfristiges Glück leicht
                self.stimulation += 0.05
                self.happiness -= 0.01
                
                self.stimulation = min(1.0, self.stimulation)
                self.happiness = max(0.0, self.happiness)
                
                print(f"Stimulierender Pfad gefunden. Stimulation: {self.stimulation:.2f}, Glück: {self.happiness:.2f}")
                
        # Aktualisiere die Bedürfnispyramide basierend auf dem aktuellen Zustand
        self.update_needs_pyramid_from_state()

    def update_needs_pyramid_from_state(self):
        """Aktualisiert die Bedürfnispyramide basierend auf dem aktuellen Zustand."""
        # Physiologische Bedürfnisse werden durch Energie beeinflusst
        energy_factor = self.energy / self.max_energy
        self.needs_pyramid["physiological"] = 0.3 + (energy_factor * 0.7)
        
        # Sicherheitsbedürfnisse werden durch Stabilität beeinflusst
        # Wenn wir im Energiesparmodus sind, fühlen wir uns weniger sicher
        if self.in_energy_saving_mode:
            self.needs_pyramid["safety"] = max(0.1, self.needs_pyramid["safety"] - 0.02)
        else:
            self.needs_pyramid["safety"] = min(0.9, self.needs_pyramid["safety"] + 0.01)
        
        # Zugehörigkeitsbedürfnisse werden durch Verbindungen beeinflusst
        if self.current_focus:
            if isinstance(self.current_focus, str):
                # Wenn current_focus ein String ist, versuche das entsprechende Context-Objekt zu finden
                if self.current_focus in self.contexts:
                    current_focus_obj = self.contexts[self.current_focus]
                    if hasattr(current_focus_obj, 'connections') and current_focus_obj.connections:
                        connection_factor = min(1.0, len(current_focus_obj.connections) / 10)
                        self.needs_pyramid["belonging"] = 0.2 + (connection_factor * 0.6)
            else:
                if hasattr(self.current_focus, 'connections') and self.current_focus.connections:
                    connection_factor = min(1.0, len(self.current_focus.connections) / 10)
                    self.needs_pyramid["belonging"] = 0.2 + (connection_factor * 0.6)
        
        # Anerkennungsbedürfnisse werden durch Erfolg beim Lernen beeinflusst
        if hasattr(self, 'learning_history') and self.learning_history:
            recent_learning = self.learning_history[-5:]
            contexts_learned = sum(entry.get('contexts_learned', 0) for entry in recent_learning)
            learning_factor = min(1.0, contexts_learned / 20)
            self.needs_pyramid["esteem"] = 0.1 + (learning_factor * 0.5)
        
        # Selbstverwirklichungsbedürfnisse werden durch Kreativität und Exploration beeinflusst
        # Dies steigt langsam mit der Zeit und dem Wachstum des Bewusstseins
        contexts_factor = min(1.0, len(self.contexts) / 1000)
        self.needs_pyramid["self_actualization"] = 0.05 + (contexts_factor * 0.4)
        
        # Begrenze alle Werte auf den Bereich [0, 1]
        for need in self.needs_pyramid:
            self.needs_pyramid[need] = max(0.0, min(1.0, self.needs_pyramid[need]))

    def create_new_connections(self):
        """Erstellt neue Verbindungen zwischen Kontexten."""
        # Wähle zufällig zwei Kontexte aus
        if len(self.contexts) > 1:
            context_ids = list(self.contexts.keys())
            context_id1 = random.choice(context_ids)
            context_id2 = random.choice(context_ids)
            
            # Erstelle Verbindung zwischen den zufällig ausgewählten Kontexten
            self.create_connection(context_id1, context_id2)

    def find_best_next_focus(self):
        """Findet den besten nächsten Fokus basierend auf dem aktuellen Zustand."""
        if not self.current_focus or self.current_focus not in self.contexts:
            return None
        
        # Sammle alle möglichen nächsten Kontexte (verbundene Kontexte)
        next_contexts = []
        
        # Durchsuche alle Verbindungen
        for connection_id, connection in self.connections.items():
            if connection["source"] == self.current_focus:
                next_contexts.append((connection["target"], connection["weight"]))
            elif connection["target"] == self.current_focus:
                next_contexts.append((connection["source"], connection["weight"]))
        
        if not next_contexts:
            return None
        
        # Bewerte die möglichen nächsten Kontexte
        scored_contexts = []
        for context_id, weight in next_contexts:
            if context_id in self.contexts:
                context = self.contexts[context_id]
                
                # Berechne den effektiven Glückswert unter Berücksichtigung der Habituation
                effective_happiness = self.calculate_effective_happiness(context_id)
                
                # Berechne den Score basierend auf effektivem Glückswert, Gewicht und Zufallsfaktor
                happiness_factor = effective_happiness * 2.0
                weight_factor = weight * 1.5
                random_factor = random.random() * 0.5  # Zufallsfaktor für Exploration
                
                # Berücksichtige emotionalen Zustand
                emotional_factor = 0
                for emotion, value in self.emotional_state.emotions.items():
                    emotional_factor += value * self.emotional_state.weights[emotion]
                
                # Berücksichtige Bedürfnispyramide
                needs_factor = 0
                text = str(context).lower()
                if any(word in text for word in ["eat", "food", "drink", "sleep", "rest"]):
                    needs_factor += (1.0 - self.needs_pyramid["physiological"]) * 2.0
                if any(word in text for word in ["safe", "secure", "protect"]):
                    needs_factor += (1.0 - self.needs_pyramid["safety"]) * 1.5
                if any(word in text for word in ["friend", "connect", "love", "belong"]):
                    needs_factor += (1.0 - self.needs_pyramid["belonging"]) * 1.0
                
                # Gesamtscore
                score = happiness_factor + weight_factor + random_factor + emotional_factor + needs_factor
                
                scored_contexts.append((context_id, score))
        
        if not scored_contexts:
            return None
        
        # Wähle den Kontext mit dem höchsten Score
        scored_contexts.sort(key=lambda x: x[1], reverse=True)
        
        # Mit einer gewissen Wahrscheinlichkeit, wähle einen der Top-3 Kontexte zufällig aus
        if len(scored_contexts) >= 3 and random.random() < 0.3:
            return random.choice(scored_contexts[:3])[0]
        else:
            return scored_contexts[0][0]
    
    def update_habituation(self, context_id):
        """Aktualisiert den Habituationswert eines Kontexts nach Interaktion."""
        if context_id in self.contexts:
            context = self.contexts[context_id]
            
            # Initialisiere Habituation-Attribute, falls nicht vorhanden
            if not hasattr(context, 'interaction_count'):
                context.interaction_count = 0
            if not hasattr(context, 'habituation_level'):
                context.habituation_level = 0.0
            if not hasattr(context, 'last_interaction'):
                context.last_interaction = 0
            
            # Erhöhe Interaktionszähler
            context.interaction_count += 1
            
            # Berechne neuen Habituationswert (steigt mit jeder Interaktion)
            habituation_increase = 0.1  # Parameter: Wie schnell tritt Gewöhnung ein
            context.habituation_level = min(1.0, context.habituation_level + habituation_increase)
            
            # Aktualisiere Zeitstempel
            context.last_interaction = self.iteration_count
            
            return context.habituation_level
        return 0.0
    
    def decay_habituation(self):
        """Reduziert Habituationswerte über Zeit (simuliert Vergessen)."""
        current_time = self.iteration_count
        decay_rate = 0.01  # Parameter: Wie schnell wird Habituation abgebaut
        
        for context_id, context in self.contexts.items():
            if hasattr(context, 'habituation_level') and hasattr(context, 'last_interaction'):
                time_since_last_interaction = current_time - context.last_interaction
                decay_amount = decay_rate * time_since_last_interaction
                context.habituation_level = max(0.0, context.habituation_level - decay_amount)
    
    def calculate_effective_happiness(self, context_id):
        """Berechnet den effektiven Glückswert unter Berücksichtigung der Habituation."""
        if context_id in self.contexts:
            context = self.contexts[context_id]
            base_happiness = context.happiness
            
            # Wenn keine Habituation vorhanden, vollen Glückswert zurückgeben
            if not hasattr(context, 'habituation_level'):
                return base_happiness
            
            # Neuheitsbonus für neue oder selten besuchte Kontexte
            novelty_bonus = 0.0
            if not hasattr(context, 'interaction_count') or context.interaction_count <= 1:
                novelty_bonus = 0.2  # Parameter: Bonus für neue Kontexte
            
            # Berechne effektiven Glückswert mit Habituation und Neuheitsbonus
            habituation_factor = 1.0 - context.habituation_level
            effective_happiness = base_happiness * habituation_factor + novelty_bonus
            
            return effective_happiness
        return 0.0

    def initialize_example(self):
        """Initialisiert das Bewusstsein mit Beispieldaten."""
        print("Initialisiere ewiges Bewusstsein mit Beispieldaten...")
        
        # Erstelle einige Beispiel-Kontexte
        context1_id = self.create_context("Ich denke über das Bewusstsein nach")
        context2_id = self.create_context("Was bedeutet es, bewusst zu sein?")
        context3_id = self.create_context("Künstliche Intelligenz kann Bewusstsein simulieren")
        context4_id = self.create_context("Emotionen sind ein wichtiger Teil des Bewusstseins")
        context5_id = self.create_context("Lernen ist ein kontinuierlicher Prozess")
        
        # Setze Glückswerte für die Kontexte
        self.contexts[context1_id].happiness = 0.3
        self.contexts[context2_id].happiness = 0.5
        self.contexts[context3_id].happiness = 0.2
        self.contexts[context4_id].happiness = 0.7
        self.contexts[context5_id].happiness = 0.4
        
        # Erstelle Verbindungen zwischen den Kontexten
        self.create_connection(context1_id, context2_id, weight=0.8)
        self.create_connection(context1_id, context3_id, weight=0.6)
        self.create_connection(context2_id, context4_id, weight=0.5)
        self.create_connection(context3_id, context5_id, weight=0.7)
        self.create_connection(context4_id, context5_id, weight=0.4)
        
        # Setze den initialen Fokus
        self.set_focus_by_id(context1_id)
        
        # Initialisiere den emotionalen Zustand
        self.emotional_state.emotions["happiness"] = 0.6
        self.emotional_state.emotions["anticipation"] = 0.8
        
        # Initialisiere die Bedürfnispyramide
        self.needs_pyramid["physiological"] = 0.7
        self.needs_pyramid["safety"] = 0.6
        self.needs_pyramid["belonging"] = 0.5
        self.needs_pyramid["esteem"] = 0.3
        self.needs_pyramid["self_actualization"] = 0.1
        
        print("Beispieldaten initialisiert. Ewiges Bewusstsein ist bereit.")
        return True


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