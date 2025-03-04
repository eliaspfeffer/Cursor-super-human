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

def find_relevant_contexts(consciousness, input_context, max_contexts=10):
    """Findet Kontexte, die für die Eingabe relevant sind."""
    relevant_contexts = []
    
    # Extrahiere wichtige Wörter aus der Eingabe
    input_words = [word.content.lower() for word in input_context.words]
    
    # Bewerte alle Kontexte nach Relevanz
    context_scores = {}
    for label, context in consciousness.contexts.items():
        # Überspringe den Eingabekontext selbst
        if label == input_context.label:
            continue
        
        # Extrahiere Wörter aus dem Kontext
        context_words = [word.content.lower() for word in context.words]
        
        # Berechne Überlappung der Wörter
        common_words = set(input_words).intersection(set(context_words))
        word_score = len(common_words) / max(len(input_words), 1)
        
        # Berücksichtige auch den Glückswert (ähnliche Emotionen sind relevanter)
        happiness_diff = abs(input_context.happiness - context.happiness)
        happiness_score = 1.0 - (happiness_diff / 2.0)  # Normalisiere auf [0, 1]
        
        # Kombiniere die Scores
        combined_score = (word_score * 0.7) + (happiness_score * 0.3)
        
        # Speichere den Score
        context_scores[label] = combined_score
    
    # Sortiere Kontexte nach Relevanz und wähle die besten aus
    sorted_contexts = sorted(context_scores.items(), key=lambda x: x[1], reverse=True)
    for label, score in sorted_contexts[:max_contexts]:
        relevant_contexts.append((label, consciousness.contexts[label], score))
    
    return relevant_contexts

def generate_response(consciousness, input_context, relevant_contexts, max_length=50, creativity=0.3, coherence=0.7):
    """Generiert eine Antwort basierend auf der Eingabe und relevanten Kontexten."""
    if not relevant_contexts:
        # Wenn keine relevanten Kontexte gefunden wurden, generiere eine allgemeine Antwort
        return "Ich verstehe nicht ganz, worüber du sprichst. Kannst du das näher erläutern?"
    
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
    max_path_length = min(max_length // 5, len(relevant_contexts))  # Begrenze die Pfadlänge
    
    # Generiere einen Pfad durch den Graphen
    for _ in range(max_path_length - 1):
        neighbors = list(G.neighbors(current_node))
        if not neighbors:
            break
        
        # Wähle den nächsten Knoten basierend auf Kohärenz und Kreativität
        if random.random() < coherence and neighbors:
            # Kohärenter Pfad: Wähle einen verbundenen Knoten
            next_node = random.choice(neighbors)
        else:
            # Kreativer Pfad: Wähle einen zufälligen Knoten
            next_node = random.choice(list(G.nodes()))
        
        path.append(next_node)
        current_node = next_node
    
    # Extrahiere Texte aus dem Pfad
    response_parts = []
    for node in path:
        response_parts.append(G.nodes[node]["text"])
    
    # Kombiniere die Teile zu einer Antwort
    raw_response = " ".join(response_parts)
    
    # Begrenze die Länge der Antwort
    words = raw_response.split()
    if len(words) > max_length:
        words = words[:max_length]
        words.append("...")
    
    # Füge die Antwort als neuen Kontext zum Bewusstsein hinzu
    response_text = " ".join(words)
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
    print("\nDu kannst jetzt mit dem Bewusstsein interagieren:")
    
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
                max_length=args.max_response_length,
                creativity=args.creativity,
                coherence=args.coherence
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