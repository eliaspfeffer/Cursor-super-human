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

from advanced_consciousness import AdvancedConsciousnessEngine, Context, EmotionalState, Memory, Environment

class EternalConsciousnessEngine(AdvancedConsciousnessEngine):
    """
    Eine Version des künstlichen Bewusstseins, die kontinuierlich läuft und niemals aufhört zu "leben".
    """
    
    def __init__(self, save_interval: int = 100, visualization_interval: int = 500, learning_interval: int = 50):
        super().__init__()
        self.running = False
        self.iteration_count = 0
        self.save_interval = save_interval
        self.visualization_interval = visualization_interval
        self.learning_interval = learning_interval
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
            },
            "visited_urls": list(self.visited_urls),
            "url_queue": self.url_queue,
            "learning_history": self.learning_history
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
            
            # Setze Internet-Lernparameter
            if "visited_urls" in state:
                self.visited_urls = set(state["visited_urls"])
            
            if "url_queue" in state:
                self.url_queue = state["url_queue"]
            
            if "learning_history" in state:
                self.learning_history = state["learning_history"]
            
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
        
        try:
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
                
                # Lerne aus dem Internet
                if self.iteration_count % self.learning_interval == 0:
                    self.learn_from_internet()
                
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

    def learn_from_internet(self):
        """Lernt neue Worte und Kontexte aus dem Internet."""
        if not self.url_queue:
            self.add_random_urls()
        
        if self.current_url_count >= self.max_urls_per_session:
            print("Maximale Anzahl an URLs für diese Sitzung erreicht. Warte auf nächste Sitzung.")
            return
        
        # Hole die nächste URL aus der Warteschlange
        url = self.url_queue.pop(0)
        
        try:
            print(f"Lerne von URL: {url}")
            
            # Hole den Inhalt der Webseite
            headers = {
                'User-Agent': 'EternalConsciousness/1.0 (Learning AI; Educational Purpose)'
            }
            response = requests.get(url, headers=headers, timeout=10)
            
            # Überprüfe, ob die Anfrage erfolgreich war
            if response.status_code != 200:
                print(f"Fehler beim Abrufen der URL: {response.status_code}")
                return
            
            # Parse den HTML-Inhalt
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Entferne JavaScript und CSS
            for script in soup(["script", "style"]):
                script.extract()
            
            # Hole den Text
            text = soup.get_text()
            
            # Bereinige den Text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Teile den Text in Sätze mit einfacher Methode, falls NLTK fehlschlägt
            try:
                sentences = sent_tokenize(text)
            except Exception as e:
                print(f"Fehler bei NLTK sent_tokenize: {e}")
                # Fallback: Einfache Satztrennung
                sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
            
            # Wähle zufällig einige Sätze aus (maximal max_contexts_per_page)
            if len(sentences) > self.max_contexts_per_page:
                selected_sentences = random.sample(sentences, self.max_contexts_per_page)
            else:
                selected_sentences = sentences
            
            # Erstelle neue Kontexte aus den Sätzen
            new_contexts = []
            for i, sentence in enumerate(selected_sentences):
                # Bereinige den Satz
                clean_sentence = re.sub(r'[^\w\s]', '', sentence)
                
                # Tokenisiere den Satz mit einfacher Methode, falls NLTK fehlschlägt
                try:
                    words = word_tokenize(clean_sentence)
                except Exception as e:
                    print(f"Fehler bei NLTK word_tokenize: {e}")
                    # Fallback: Einfache Worttrennung
                    words = [w.strip() for w in clean_sentence.split() if w.strip()]
                
                # Entferne Stopwörter und lemmatisiere
                try:
                    filtered_words = [self.lemmatizer.lemmatize(word.lower()) for word in words 
                                     if word.lower() not in self.stop_words and len(word) > 1]
                except Exception as e:
                    print(f"Fehler bei Lemmatisierung: {e}")
                    # Fallback: Nur Stopwörter entfernen ohne Lemmatisierung
                    filtered_words = [word.lower() for word in words 
                                     if word.lower() not in self.stop_words and len(word) > 1]
                
                # Wenn nach der Filterung noch genug Wörter übrig sind
                if len(filtered_words) >= 3:
                    # Erstelle einen neuen Kontext
                    context_text = " ".join(filtered_words)
                    label = f"Web_{self.iteration_count}_{i}"
                    
                    # Berechne einen Glückswert basierend auf dem emotionalen Zustand
                    sentiment_score = self.calculate_sentiment(filtered_words)
                    happiness = sentiment_score * 0.5  # Skaliere auf [-0.5, 0.5]
                    
                    context = self.create_context(context_text, label, happiness)
                    new_contexts.append(context)
                    
                    print(f"Neuer Kontext gelernt: {context_text} (Glück: {happiness:.2f})")
            
            # Verbinde die neuen Kontexte miteinander und mit existierenden Kontexten
            self.connect_new_contexts(new_contexts)
            
            # Füge die Seite zu den besuchten URLs hinzu
            self.visited_urls.add(url)
            self.current_url_count += 1
            
            # Extrahiere Links für die nächste Runde
            self.extract_links(soup, url)
            
            # Speichere Lernhistorie
            self.learning_history.append({
                "url": url,
                "timestamp": datetime.datetime.now().isoformat(),
                "contexts_learned": len(new_contexts)
            })
            
            print(f"Lernen von {url} abgeschlossen. {len(new_contexts)} neue Kontexte erstellt.")
            
        except Exception as e:
            print(f"Fehler beim Lernen von {url}: {str(e)}")
            # Füge die URL wieder zur Warteschlange hinzu, wenn es sich um einen temporären Fehler handeln könnte
            if "timeout" in str(e).lower() or "connection" in str(e).lower():
                self.url_queue.append(url)
    
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