#!/usr/bin/env python3
"""
Interaktion mit dem künstlichen Bewusstsein.

Dieses Skript ermöglicht die Interaktion mit dem künstlichen Bewusstsein durch
Texteingaben. Das Bewusstsein verarbeitet die Eingaben und generiert Antworten
basierend auf seinem aktuellen Zustand und Wissen.
"""

import os
import sys
import time
import argparse
import json
import random
import datetime
from typing import List, Dict, Any, Optional
import networkx as nx

# Versuche, die Bewusstseinsmodule zu importieren
try:
    from eternal_consciousness import EternalConsciousnessEngine, Context
except ImportError:
    print("Fehler: Die Bewusstseinsmodule konnten nicht importiert werden.")
    print("Stellen Sie sicher, dass Sie sich im richtigen Verzeichnis befinden.")
    sys.exit(1)

def parse_arguments():
    """Parst die Kommandozeilenargumente."""
    parser = argparse.ArgumentParser(description="Interagiere mit dem künstlichen Bewusstsein")
    
    parser.add_argument(
        "--state-file", 
        type=str, 
        help="Pfad zur Zustandsdatei, die geladen werden soll. Wenn nicht angegeben, wird die neueste Datei verwendet."
    )
    
    parser.add_argument(
        "--max-response-length", 
        type=int, 
        default=100, 
        help="Maximale Länge der Antwort in Wörtern"
    )
    
    parser.add_argument(
        "--creativity", 
        type=float, 
        default=0.3, 
        help="Kreativitätsfaktor für die Antwortgenerierung (0.0-1.0)"
    )
    
    parser.add_argument(
        "--coherence", 
        type=float, 
        default=0.7, 
        help="Kohärenzfaktor für die Antwortgenerierung (0.0-1.0)"
    )
    
    return parser.parse_args()

def load_consciousness(state_file=None):
    """Lädt das Bewusstsein aus einer Zustandsdatei."""
    consciousness = EternalConsciousnessEngine(
        save_interval=1000,  # Hoher Wert, damit es nicht während der Interaktion speichert
        visualization_interval=10000,  # Hoher Wert, damit es nicht während der Interaktion visualisiert
        learning_interval=500  # Mittlerer Wert, damit es gelegentlich lernt
    )
    
    # Wenn keine Zustandsdatei angegeben wurde, versuche die neueste zu laden
    if not state_file:
        if os.path.exists(consciousness.save_dir):
            state_files = [
                f for f in os.listdir(consciousness.save_dir) 
                if f.startswith("consciousness_state_") and f.endswith(".json")
            ]
            if state_files:
                # Sortiere nach Zeitstempel (neueste zuerst)
                state_files.sort(reverse=True)
                state_file = os.path.join(consciousness.save_dir, state_files[0])
                print(f"Lade neuesten Zustand: {state_file}")
    
    # Lade den Zustand, falls vorhanden
    if state_file and os.path.exists(state_file):
        success = consciousness.load_state(state_file)
        if not success:
            print("Fehler beim Laden des Zustands. Initialisiere mit Beispieldaten...")
            consciousness.initialize_example()
            consciousness.initialize_example_environment()
    else:
        if not state_file:
            print("Kein gespeicherter Zustand gefunden.")
        else:
            print(f"Zustandsdatei nicht gefunden: {state_file}")
        print("Initialisiere mit Beispieldaten...")
        consciousness.initialize_example()
        consciousness.initialize_example_environment()
    
    return consciousness

def create_input_context(consciousness, user_input):
    """Erstellt einen Kontext aus der Benutzereingabe."""
    # Bereinige die Eingabe
    cleaned_input = user_input.strip()
    
    # Erstelle einen neuen Kontext mit der Eingabe
    label = f"UserInput_{int(time.time())}"
    
    # Berechne einen Glückswert basierend auf dem Text
    # Dies ist eine einfache Implementierung und könnte durch eine bessere Sentiment-Analyse ersetzt werden
    happiness = consciousness.calculate_sentiment(cleaned_input.split())
    
    # Erstelle den Kontext mit der vorhandenen Methode
    input_context_id = consciousness.create_context(cleaned_input, label, happiness)
    
    # Gib den tatsächlichen Kontext zurück, nicht nur die ID
    return consciousness.contexts[input_context_id]

def find_relevant_contexts(consciousness, input_context, max_contexts=10, min_score=0.1):
    """Findet Kontexte, die für die Eingabe relevant sind."""
    relevant_contexts = []
    
    # Extrahiere wichtige Wörter aus der Eingabe
    input_words = [word.content.lower() for word in input_context.words]
    
    # Entferne sehr häufige Wörter (Stopwörter)
    stopwords = {'der', 'die', 'das', 'ein', 'eine', 'und', 'oder', 'aber', 'wenn', 'ist', 'sind', 'war', 'waren',
                'the', 'a', 'an', 'and', 'or', 'but', 'if', 'is', 'are', 'was', 'were', 'in', 'on', 'at', 'to', 'from'}
    filtered_input_words = [word for word in input_words if word not in stopwords and len(word) > 2]
    
    # Wenn nach dem Filtern keine Wörter übrig bleiben, verwende die ursprünglichen Wörter
    if not filtered_input_words:
        filtered_input_words = input_words
    
    # Bewerte alle Kontexte nach Relevanz
    context_scores = {}
    for label, context in consciousness.contexts.items():
        # Überspringe den Eingabekontext selbst
        if label == input_context.label:
            continue
        
        # Extrahiere Wörter aus dem Kontext
        context_words = [word.content.lower() for word in context.words]
        filtered_context_words = [word for word in context_words if word not in stopwords and len(word) > 2]
        
        # Wenn nach dem Filtern keine Wörter übrig bleiben, verwende die ursprünglichen Wörter
        if not filtered_context_words:
            filtered_context_words = context_words
        
        # Berechne Überlappung der Wörter
        common_words = set(filtered_input_words).intersection(set(filtered_context_words))
        
        # Wenn es gemeinsame Wörter gibt, berechne den Score
        if common_words:
            # Gewichte wichtigere Wörter stärker (längere Wörter sind oft wichtiger)
            weighted_common = sum(len(word) for word in common_words)
            weighted_input = sum(len(word) for word in filtered_input_words)
            weighted_context = sum(len(word) for word in filtered_context_words)
            
            # Berechne den Wort-Score basierend auf der gewichteten Überlappung
            word_score = weighted_common / max(weighted_input, weighted_context, 1)
            
            # Berücksichtige auch den Glückswert (ähnliche Emotionen sind relevanter)
            happiness_diff = abs(input_context.happiness - context.happiness)
            happiness_score = 1.0 - (happiness_diff / 2.0)  # Normalisiere auf [0, 1]
            
            # Kombiniere die Scores, mit stärkerer Gewichtung der Wortüberlappung
            combined_score = (word_score * 0.8) + (happiness_score * 0.2)
        else:
            # Wenn keine gemeinsamen Wörter gefunden wurden, setze einen niedrigen Score
            combined_score = 0.05
        
        # Speichere den Score
        context_scores[label] = combined_score
    
    # Sortiere Kontexte nach Relevanz und wähle die besten aus, die über dem Mindestscore liegen
    sorted_contexts = sorted(context_scores.items(), key=lambda x: x[1], reverse=True)
    for label, score in sorted_contexts:
        if score >= min_score and len(relevant_contexts) < max_contexts:
            relevant_contexts.append((label, consciousness.contexts[label], score))
    
    # Wenn keine relevanten Kontexte gefunden wurden, versuche es mit einem niedrigeren Mindestscore
    if not relevant_contexts and min_score > 0.01:
        return find_relevant_contexts(consciousness, input_context, max_contexts, min_score=0.01)
    
    return relevant_contexts

def generate_response(consciousness, input_context, relevant_contexts, max_length=50, creativity=0.3, coherence=0.7):
    """Generiert eine Antwort basierend auf der Eingabe und relevanten Kontexten."""
    if not relevant_contexts:
        # Wenn keine relevanten Kontexte gefunden wurden, generiere eine allgemeine Antwort
        default_responses = [
            "Ich verstehe nicht ganz, worüber du sprichst. Kannst du das näher erläutern?",
            "Darüber habe ich nicht genug Informationen. Magst du mir mehr darüber erzählen?",
            "Interessante Frage! Leider habe ich dazu noch keine Gedanken gesammelt.",
            "Das ist ein spannendes Thema, aber ich bin mir nicht sicher, was ich dazu sagen soll.",
            "Ich würde gerne mehr über dieses Thema lernen. Was denkst du darüber?"
        ]
        return random.choice(default_responses)
    
    # Extrahiere die Eingabewörter für die Antwortgenerierung
    input_words = [word.content.lower() for word in input_context.words]
    
    # Erstelle einen Graphen aus den relevanten Kontexten
    G = nx.Graph()
    
    # Füge Knoten hinzu
    for label, context, score in relevant_contexts:
        # Konvertiere die Wörter in Text
        context_text = " ".join([word.content for word in context.words])
        G.add_node(label, text=context_text, happiness=context.happiness, score=score)
    
    # Füge Kanten hinzu
    for label1, context1, _ in relevant_contexts:
        for label2, context2, _ in relevant_contexts:
            if label1 != label2 and label2 in context1.connections:
                G.add_edge(label1, label2)
    
    # Finde den am besten bewerteten Kontext als Startpunkt
    start_node = relevant_contexts[0][0]
    
    # Generiere einen Pfad durch den Graphen
    path = [start_node]
    current_node = start_node
    
    # Parameter für die Pfadgenerierung
    max_path_length = min(3, len(relevant_contexts))  # Begrenze die Pfadlänge für mehr Kohärenz
    
    # Generiere einen Pfad durch den Graphen mit mehr Kohärenz
    for _ in range(max_path_length - 1):
        neighbors = list(G.neighbors(current_node))
        if not neighbors:
            break
        
        # Wähle den nächsten Knoten basierend auf Kohärenz und Kreativität
        if random.random() < coherence and neighbors:
            # Kohärenter Pfad: Wähle einen verbundenen Knoten mit höherem Score
            neighbor_scores = [(neighbor, G.nodes[neighbor]['score']) for neighbor in neighbors]
            sorted_neighbors = sorted(neighbor_scores, key=lambda x: x[1], reverse=True)
            
            # Wähle einen der Top-Nachbarn (mit etwas Zufall)
            top_n = max(1, min(3, len(sorted_neighbors)))
            next_node = sorted_neighbors[random.randint(0, top_n-1)][0]
        else:
            # Kreativer Pfad: Wähle einen zufälligen Knoten mit höherem Score
            node_scores = [(node, G.nodes[node]['score']) for node in G.nodes() if node not in path]
            if node_scores:
                sorted_nodes = sorted(node_scores, key=lambda x: x[1], reverse=True)
                top_n = max(1, min(3, len(sorted_nodes)))
                next_node = sorted_nodes[random.randint(0, top_n-1)][0]
            else:
                # Wenn alle Knoten bereits im Pfad sind, breche ab
                break
        
        path.append(next_node)
        current_node = next_node
    
    # Extrahiere Texte aus dem Pfad
    response_parts = []
    for node in path:
        node_text = G.nodes[node]["text"]
        
        # Vermeide Wiederholungen im Text
        if not response_parts or not any(part in node_text or node_text in part for part in response_parts):
            response_parts.append(node_text)
    
    # Kombiniere die Teile zu einer Antwort
    if len(response_parts) > 1:
        # Versuche, die Antwort strukturierter zu gestalten
        conjunctions = ["und", "aber", "denn", "weil", "obwohl", "jedoch", "außerdem", "zudem"]
        raw_response = response_parts[0]
        
        for i, part in enumerate(response_parts[1:]):
            # Füge Konjunktionen hinzu, um die Antwort flüssiger zu gestalten
            if random.random() < 0.7 and i < len(conjunctions):
                raw_response += f". {part.capitalize()}"
            else:
                raw_response += f" {random.choice(conjunctions)} {part}"
    else:
        raw_response = " ".join(response_parts)
    
    # Begrenze die Länge der Antwort
    words = raw_response.split()
    if len(words) > max_length:
        words = words[:max_length]
        words.append("...")
    
    # Füge die Antwort als neuen Kontext zum Bewusstsein hinzu
    response_text = " ".join(words)
    
    # Stelle sicher, dass die Antwort sinnvoll ist
    if len(response_text.split()) < 3:
        # Wenn die Antwort zu kurz ist, verwende eine Standardantwort
        response_text = f"Ich denke über {' '.join(input_words[:3])} nach, aber ich bin mir nicht sicher, was ich dazu sagen soll."
    
    response_label = f"Response_{int(time.time())}"
    response_happiness = consciousness.calculate_sentiment(words)
    
    # Erstelle den Antwortkontext mit der vorhandenen Methode
    response_context_id = consciousness.create_context(response_text, response_label, response_happiness)
    response_context = consciousness.contexts[response_context_id]
    
    # Verbinde den Antwortkontext mit dem Eingabekontext
    consciousness.connect_contexts(response_context, input_context)
    
    return response_text

def interact_with_consciousness():
    """Hauptfunktion für die Interaktion mit dem Bewusstsein."""
    args = parse_arguments()
    
    print("Lade künstliches Bewusstsein...")
    consciousness = load_consciousness(args.state_file)
    
    print("\n" + "="*80)
    print("INTERAKTION MIT DEM KÜNSTLICHEN BEWUSSTSEIN")
    print("="*80)
    print("\nGib 'exit', 'quit' oder 'ende' ein, um die Interaktion zu beenden.")
    print("Gib 'stats' ein, um Statistiken über das Bewusstsein anzuzeigen.")
    print("Gib 'save' ein, um den aktuellen Zustand zu speichern.")
    print("Gib 'learn' ein, um das Bewusstsein aus dem Internet lernen zu lassen.")
    print("Gib 'reset' ein, um die Antwortqualität zurückzusetzen.")
    print("\nDu kannst jetzt mit dem Bewusstsein interagieren:")
    
    # Parameter für die Antwortqualität
    coherence = args.coherence
    creativity = args.creativity
    max_response_length = args.max_response_length
    
    while True:
        try:
            user_input = input("\nDu: ").strip()
            
            if user_input.lower() in ["exit", "quit", "ende"]:
                break
            
            if user_input.lower() == "stats":
                # Zeige Statistiken an
                print("\nStatistiken des Bewusstseins:")
                print(f"  Anzahl Kontexte: {len(consciousness.contexts)}")
                print(f"  Anzahl Wörter: {len(consciousness.words)}")
                print(f"  Energie: {consciousness.energy:.2f}")
                print(f"  Emotionaler Zustand:")
                for emotion, value in consciousness.emotional_state.emotions.items():
                    print(f"    {emotion}: {value:.4f}")
                print(f"  Aktuelle Antwortparameter:")
                print(f"    Kohärenz: {coherence:.2f}")
                print(f"    Kreativität: {creativity:.2f}")
                print(f"    Max. Antwortlänge: {max_response_length}")
                continue
            
            if user_input.lower() == "save":
                # Speichere den aktuellen Zustand
                consciousness.save_state()
                print("Zustand gespeichert.")
                continue
            
            if user_input.lower() == "learn":
                # Lasse das Bewusstsein lernen
                print("Lerne aus dem Internet...")
                consciousness.learn_from_internet()
                print("Lernen abgeschlossen.")
                continue
            
            if user_input.lower() == "reset":
                # Setze die Antwortparameter zurück
                coherence = args.coherence
                creativity = args.creativity
                max_response_length = args.max_response_length
                print("Antwortparameter zurückgesetzt.")
                continue
            
            if user_input.lower().startswith("set coherence "):
                # Setze die Kohärenz
                try:
                    new_coherence = float(user_input.split()[2])
                    if 0.0 <= new_coherence <= 1.0:
                        coherence = new_coherence
                        print(f"Kohärenz auf {coherence:.2f} gesetzt.")
                    else:
                        print("Kohärenz muss zwischen 0.0 und 1.0 liegen.")
                except (IndexError, ValueError):
                    print("Ungültiges Format. Verwende 'set coherence 0.7'.")
                continue
            
            if user_input.lower().startswith("set creativity "):
                # Setze die Kreativität
                try:
                    new_creativity = float(user_input.split()[2])
                    if 0.0 <= new_creativity <= 1.0:
                        creativity = new_creativity
                        print(f"Kreativität auf {creativity:.2f} gesetzt.")
                    else:
                        print("Kreativität muss zwischen 0.0 und 1.0 liegen.")
                except (IndexError, ValueError):
                    print("Ungültiges Format. Verwende 'set creativity 0.3'.")
                continue
            
            if user_input.lower().startswith("set length "):
                # Setze die maximale Antwortlänge
                try:
                    new_length = int(user_input.split()[2])
                    if 10 <= new_length <= 200:
                        max_response_length = new_length
                        print(f"Max. Antwortlänge auf {max_response_length} gesetzt.")
                    else:
                        print("Max. Antwortlänge muss zwischen 10 und 200 liegen.")
                except (IndexError, ValueError):
                    print("Ungültiges Format. Verwende 'set length 50'.")
                continue
            
            if not user_input:
                continue
            
            # Verarbeite die Eingabe
            print("Verarbeite Eingabe...")
            input_context = create_input_context(consciousness, user_input)
            
            # Finde relevante Kontexte
            relevant_contexts = find_relevant_contexts(consciousness, input_context)
            
            # Generiere eine Antwort
            response = generate_response(
                consciousness, 
                input_context, 
                relevant_contexts, 
                max_length=max_response_length,
                creativity=creativity,
                coherence=coherence
            )
            
            # Gib die Antwort aus
            print(f"\nBewusstsein: {response}")
            
        except KeyboardInterrupt:
            print("\nInteraktion beendet.")
            break
        except Exception as e:
            print(f"Fehler: {e}")
    
    # Speichere den Zustand beim Beenden
    print("Speichere Zustand...")
    consciousness.save_state()
    print("Zustand gespeichert. Auf Wiedersehen!")

if __name__ == "__main__":
    interact_with_consciousness() 