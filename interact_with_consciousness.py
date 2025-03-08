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
            print("Fehler beim Laden des Zustands. Starte mit leerem Bewusstsein...")
            # Keine Beispieldaten laden, da dies zu Fehlern führt
    else:
        if not state_file:
            print("Kein gespeicherter Zustand gefunden.")
        else:
            print(f"Zustandsdatei nicht gefunden: {state_file}")
        print("Starte mit leerem Bewusstsein...")
        # Keine Beispieldaten laden, da dies zu Fehlern führt
    
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
    input_words = [word.content.lower() for word in input_context.words]
    
    # Ignoriere sehr kurze Wörter (Stoppwörter)
    filtered_input_words = [w for w in input_words if len(w) > 2]
    
    # Wenn keine sinnvollen Wörter übrig bleiben, verwende die ursprünglichen
    if not filtered_input_words:
        filtered_input_words = input_words
    
    # Verschiedene Relevanzmetriken berechnen
    context_scores = []
    
    for context_id, context in consciousness.contexts.items():
        # Ignoriere den Eingabekontext selbst
        if context_id == input_context.label:
            continue
        
        context_words = [word.content.lower() for word in context.words]
        
        # 1. Wortüberlappung (Jaccard-Ähnlichkeit)
        input_word_set = set(filtered_input_words)
        context_word_set = set(context_words)
        
        if input_word_set and context_word_set:
            intersection = input_word_set.intersection(context_word_set)
            union = input_word_set.union(context_word_set)
            jaccard_similarity = len(intersection) / len(union)
        else:
            jaccard_similarity = 0
            
        # 2. Wichtige Wörter (längere Wörter haben mehr Gewicht)
        important_word_score = 0
        for word in filtered_input_words:
            if len(word) >= 4 and word in context_word_set:  # Längere Wörter sind wichtiger
                important_word_score += (len(word) / 10)  # Normalisiere auf 0-1 Skala
                
        # Normalisiere den Score
        if filtered_input_words:
            important_word_score /= len(filtered_input_words)
        
        # 3. Sequenzielle Übereinstimmung (Wortpaare oder -tripel)
        sequence_score = 0
        for i in range(len(filtered_input_words) - 1):
            word_pair = (filtered_input_words[i], filtered_input_words[i+1])
            
            # Suche nach dem Wortpaar im Kontext
            for j in range(len(context_words) - 1):
                context_pair = (context_words[j], context_words[j+1])
                if word_pair == context_pair:
                    sequence_score += 0.5  # Bonus für aufeinanderfolgende Wörter
        
        # Normalisiere den Score
        if len(filtered_input_words) > 1:
            sequence_score /= (len(filtered_input_words) - 1)
            
        # 4. Emotionale Ähnlichkeit
        emotional_similarity = 1.0 - abs(input_context.happiness - context.happiness)
        
        # 5. Netzwerkverbindungen (Transitivität)
        network_score = 0
        
        # Prüfe, ob der Kontext mit Kontexten verbunden ist, die ähnliche Wörter enthalten
        if hasattr(context, 'connections'):
            for connected_id in context.connections:
                if connected_id in consciousness.contexts:
                    connected_context = consciousness.contexts[connected_id]
                    connected_words = [word.content.lower() for word in connected_context.words]
                    connected_word_set = set(connected_words)
                    
                    # Berechne Überlappung mit der Eingabe
                    connected_intersection = input_word_set.intersection(connected_word_set)
                    if connected_intersection:
                        network_score += len(connected_intersection) / len(input_word_set)
            
            # Normalisiere den Score
            if context.connections:
                network_score /= len(context.connections)
        
        # Gewichtete Gesamtbewertung
        total_score = (
            jaccard_similarity * 0.3 +
            important_word_score * 0.3 +
            sequence_score * 0.2 +
            emotional_similarity * 0.1 +
            network_score * 0.1
        )
        
        # Speichere den Score, wenn er über dem Schwellenwert liegt
        if total_score >= min_score:
            context_scores.append((context_id, context, total_score))
    
    # Sortiere nach Relevanz
    context_scores.sort(key=lambda x: x[2], reverse=True)
    
    # Begrenze die Anzahl der zurückgegebenen Kontexte
    return context_scores[:max_contexts]

def generate_response(consciousness, input_context, relevant_contexts, max_length=50, creativity=0.3, coherence=0.7):
    """Generiert eine Antwort basierend auf der Eingabe und relevanten Kontexten."""
    # Extrahiere die Eingabewörter für die Antwortgenerierung
    input_words = [word.content.lower() for word in input_context.words]
    
    if not relevant_contexts:
        # Wenn keine relevanten Kontexte gefunden wurden, suche nach Kontexten mit ähnlichen Wörtern
        all_contexts = list(consciousness.contexts.values())
        word_based_contexts = []
        
        for word in input_words:
            for context in all_contexts:
                context_words = [w.content.lower() for w in context.words]
                if word in context_words and context not in [c[1] for c in word_based_contexts]:
                    # Berechne Relevanz basierend auf Wortüberlappung
                    overlap = sum(1 for w in input_words if w in context_words)
                    score = overlap / len(input_words) if input_words else 0
                    if score > 0.1:  # Mindestens 10% Überlappung
                        word_based_contexts.append((context.label, context, score))
        
        if word_based_contexts:
            # Sortiere nach Relevanz
            word_based_contexts.sort(key=lambda x: x[2], reverse=True)
            relevant_contexts = word_based_contexts[:5]  # Verwende die 5 relevantesten
        else:
            # Wenn immer noch keine Kontexte gefunden wurden, verwende die Eingabewörter
            response_text = " ".join(input_words[:min(5, len(input_words))])
            response_label = f"Response_{int(time.time())}"
            response_happiness = 0.0  # Neutral
            
            # Erstelle den Antwortkontext
            response_context_id = consciousness.create_context(response_text, response_label, response_happiness)
            response_context = consciousness.contexts[response_context_id]
            
            # Verbinde den Antwortkontext mit dem Eingabekontext
            consciousness.connect_contexts(response_context, input_context)
            
            return response_text
    
    # Erstelle einen Graphen aus den relevanten Kontexten
    G = nx.Graph()
    
    # Füge Knoten hinzu
    for label, context, score in relevant_contexts:
        # Konvertiere die Wörter in Text
        context_text = " ".join([word.content for word in context.words])
        G.add_node(label, text=context_text, happiness=context.happiness, score=score)
    
    # Füge Kanten hinzu - verbesserte Verbindungslogik
    for label1, context1, _ in relevant_contexts:
        for label2, context2, _ in relevant_contexts:
            if label1 != label2:
                # Prüfe direkte Verbindungen
                if label2 in context1.connections:
                    G.add_edge(label1, label2, weight=1.0)
                else:
                    # Prüfe Wortüberlappung für indirekte Verbindungen
                    words1 = [w.content.lower() for w in context1.words]
                    words2 = [w.content.lower() for w in context2.words]
                    overlap = sum(1 for w in words1 if w in words2)
                    if overlap > 0:
                        similarity = overlap / (len(words1) + len(words2) - overlap)  # Jaccard-Ähnlichkeit
                        if similarity > 0.1:  # Mindestens 10% Ähnlichkeit
                            G.add_edge(label1, label2, weight=similarity)
    
    # Finde den am besten bewerteten Kontext als Startpunkt
    start_node = relevant_contexts[0][0]
    
    # Verbesserte Pfadgenerierung mit semantischer Kohärenz
    # Verwende PageRank, um wichtige Knoten zu identifizieren
    pagerank = nx.pagerank(G, weight='weight')
    
    # Sortiere Knoten nach PageRank
    sorted_nodes = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)
    
    # Wähle die Top-N Knoten basierend auf PageRank
    top_n = min(5, len(sorted_nodes))
    important_nodes = [node for node, _ in sorted_nodes[:top_n]]
    
    # Generiere einen Pfad, der die wichtigsten Knoten verbindet
    path = []
    current_node = start_node
    path.append(current_node)
    
    # Versuche, einen zusammenhängenden Pfad durch die wichtigsten Knoten zu finden
    for node in important_nodes:
        if node not in path:
            # Finde den kürzesten Pfad vom aktuellen Knoten zum Zielknoten
            try:
                shortest_path = nx.shortest_path(G, current_node, node, weight='weight')
                # Füge den Pfad hinzu, überspringe den ersten Knoten (ist bereits im Pfad)
                path.extend(shortest_path[1:])
                current_node = node
            except nx.NetworkXNoPath:
                # Wenn kein Pfad existiert, füge den Knoten direkt hinzu
                path.append(node)
                current_node = node
    
    # Extrahiere Texte aus dem Pfad und entferne Duplikate
    response_parts = []
    seen_texts = set()
    
    for node in path:
        node_text = G.nodes[node]["text"]
        
        # Vermeide Duplikate und sehr ähnliche Texte
        if node_text not in seen_texts and not any(similar(node_text, part) for part in response_parts):
            response_parts.append(node_text)
            seen_texts.add(node_text)
    
    # Verbesserte Textgenerierung mit Kohärenz
    if len(response_parts) > 1:
        # Verwende NLP-Techniken, um die Teile besser zu verbinden
        conjunctions = ["und", "aber", "denn", "weil", "obwohl", "jedoch", "außerdem", "zudem", "dadurch", "folglich"]
        transitions = ["Interessanterweise", "Darüber hinaus", "Wichtig ist auch", "Bemerkenswert ist", "Dabei gilt"]
        
        raw_response = response_parts[0]
        
        for i, part in enumerate(response_parts[1:]):
            # Wähle eine passende Überleitung basierend auf Kontext
            if random.random() < 0.3:
                # Verwende eine Überleitung
                raw_response += f". {random.choice(transitions)} {part}"
            elif random.random() < 0.7:
                # Verwende eine Konjunktion
                raw_response += f". {part.capitalize()}"
            else:
                # Verbinde mit einer Konjunktion
                raw_response += f" {random.choice(conjunctions)} {part}"
    else:
        raw_response = " ".join(response_parts)
    
    # Begrenze die Länge der Antwort
    words = raw_response.split()
    if len(words) > max_length:
        # Intelligentere Kürzung: Versuche, Sätze zu erhalten
        sentences = raw_response.split('.')
        shortened_response = ""
        word_count = 0
        
        for sentence in sentences:
            sentence_words = sentence.split()
            if word_count + len(sentence_words) <= max_length:
                shortened_response += sentence + "."
                word_count += len(sentence_words)
            else:
                remaining_words = max_length - word_count
                if remaining_words > 3:  # Nur hinzufügen, wenn genug Wörter übrig sind
                    shortened_response += " ".join(sentence_words[:remaining_words]) + "..."
                break
        
        raw_response = shortened_response
    
    # Füge die Antwort als neuen Kontext zum Bewusstsein hinzu
    response_text = raw_response.strip()
    
    # Stelle sicher, dass die Antwort sinnvoll ist
    if len(response_text.split()) < 3:
        # Wenn die Antwort zu kurz ist, verwende die relevantesten Kontexte direkt
        best_context = relevant_contexts[0][1]
        response_text = " ".join([word.content for word in best_context.words])
    
    response_label = f"Response_{int(time.time())}"
    response_happiness = consciousness.calculate_sentiment(response_text.split())
    
    # Erstelle den Antwortkontext mit der vorhandenen Methode
    response_context_id = consciousness.create_context(response_text, response_label, response_happiness)
    response_context = consciousness.contexts[response_context_id]
    
    # Verbinde den Antwortkontext mit dem Eingabekontext und relevanten Kontexten
    consciousness.connect_contexts(response_context, input_context)
    
    # Verbinde auch mit den relevantesten Kontexten für bessere Netzwerkbildung
    for _, context, _ in relevant_contexts[:3]:
        consciousness.connect_contexts(response_context, context)
    
    return response_text

# Hilfsfunktion zur Bestimmung der Textähnlichkeit
def similar(text1, text2, threshold=0.7):
    """Prüft, ob zwei Texte ähnlich sind basierend auf Wortüberlappung."""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 or not words2:
        return False
    
    # Jaccard-Ähnlichkeit
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    similarity = len(intersection) / len(union)
    
    return similarity > threshold

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
    print("Gib 'learn' ein, um das Bewusstsein basierend auf seinem aktuellen Fokus aus dem Internet lernen zu lassen.")
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
                print("Lerne aus dem Internet basierend auf dem aktuellen Fokus...")
                if consciousness.current_focus:
                    focus_text = consciousness.contexts[consciousness.current_focus].text
                    print(f"Aktueller Fokus: '{focus_text}'")
                    consciousness.learn_from_internet()
                    print("Lernen abgeschlossen.")
                else:
                    print("Kein aktueller Fokus vorhanden. Setze zuerst einen Fokus, bevor du lernst.")
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
            
            # Setze den Fokus auf den Eingabekontext
            consciousness.set_focus_by_id(input_context.label)
            
            # Verwende die neue generate_response-Methode direkt aus dem Bewusstsein
            response = consciousness.generate_response(user_input)
            
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