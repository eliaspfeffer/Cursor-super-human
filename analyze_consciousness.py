#!/usr/bin/env python3
"""
Analyse des künstlichen Bewusstseins.

Dieses Skript analysiert den aktuellen Zustand des künstlichen Bewusstseins
und zeigt, was es bisher gelernt hat.
"""

import os
import json
import argparse
import datetime
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter, defaultdict
import numpy as np
from wordcloud import WordCloud
import pandas as pd
from tabulate import tabulate

def parse_arguments():
    """Parst die Kommandozeilenargumente."""
    parser = argparse.ArgumentParser(description="Analysiere das künstliche Bewusstsein")
    
    parser.add_argument(
        "--state-file", 
        type=str, 
        help="Pfad zur Zustandsdatei, die analysiert werden soll. Wenn nicht angegeben, wird die neueste Datei verwendet."
    )
    
    parser.add_argument(
        "--output-dir", 
        type=str, 
        default="consciousness_analysis", 
        help="Verzeichnis für die Ausgabe der Analyse"
    )
    
    parser.add_argument(
        "--top-n", 
        type=int, 
        default=20, 
        help="Anzahl der Top-Elemente, die angezeigt werden sollen"
    )
    
    parser.add_argument(
        "--web-only", 
        action="store_true", 
        help="Nur aus dem Web gelernte Kontexte analysieren"
    )
    
    parser.add_argument(
        "--interactive", 
        action="store_true", 
        help="Interaktiven Modus aktivieren"
    )
    
    return parser.parse_args()

def load_state(state_file=None):
    """Lädt den Zustand des Bewusstseins."""
    if state_file is None:
        # Finde die neueste Zustandsdatei
        save_dir = "consciousness_state"
        if not os.path.exists(save_dir):
            print(f"Verzeichnis {save_dir} nicht gefunden.")
            return None
        
        state_files = [f for f in os.listdir(save_dir) if f.startswith("consciousness_state_") and f.endswith(".json")]
        if not state_files:
            print(f"Keine Zustandsdateien in {save_dir} gefunden.")
            return None
        
        # Sortiere nach Zeitstempel (neueste zuerst)
        state_files.sort(reverse=True)
        state_file = os.path.join(save_dir, state_files[0])
    
    try:
        with open(state_file, 'r') as f:
            state = json.load(f)
        print(f"Zustand geladen: {state_file}")
        return state
    except Exception as e:
        print(f"Fehler beim Laden des Zustands: {e}")
        return None

def analyze_contexts(state, top_n=20, web_only=False):
    """Analysiert die Kontexte des Bewusstseins."""
    if not state or "contexts" not in state:
        print("Keine Kontexte im Zustand gefunden.")
        return None
    
    contexts = state["contexts"]
    
    # Filtere Kontexte, wenn web_only aktiviert ist
    if web_only:
        contexts = {label: data for label, data in contexts.items() if label.startswith("Web_")}
        if not contexts:
            print("Keine aus dem Web gelernten Kontexte gefunden.")
            return None
    
    # Sammle Wörter aus allen Kontexten
    all_words = []
    for label, data in contexts.items():
        # Prüfe, ob "text" oder "words" vorhanden ist
        if "text" in data:
            words = data["text"].split()
        elif "words" in data:
            words = data["words"] if isinstance(data["words"], list) else " ".join(data["words"]).split()
        else:
            print(f"Warnung: Kontext {label} hat weder 'text' noch 'words' Attribute.")
            continue
        all_words.extend(words)
    
    # Zähle Häufigkeit der Wörter
    word_counts = Counter(all_words)
    
    # Finde die häufigsten Wörter
    top_words = word_counts.most_common(top_n)
    
    # Berechne durchschnittlichen Glückswert
    happiness_values = [data["happiness"] for data in contexts.values() if "happiness" in data]
    avg_happiness = sum(happiness_values) / len(happiness_values) if happiness_values else 0
    
    # Finde Kontexte mit höchstem und niedrigstem Glückswert
    if happiness_values:
        max_happiness_label = max(((label, data) for label, data in contexts.items() if "happiness" in data), key=lambda x: x[1]["happiness"])[0]
        min_happiness_label = min(((label, data) for label, data in contexts.items() if "happiness" in data), key=lambda x: x[1]["happiness"])[0]
        max_happiness_context = contexts[max_happiness_label]
        min_happiness_context = contexts[min_happiness_label]
    else:
        max_happiness_context = min_happiness_context = None
    
    # Analysiere Verbindungen
    connection_counts = {label: len(data.get("connections", [])) for label, data in contexts.items()}
    most_connected = sorted(connection_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    # Kategorisiere Kontexte nach Quelle
    context_sources = defaultdict(int)
    for label in contexts:
        if label.startswith("Web_"):
            context_sources["Web"] += 1
        elif label.startswith("Random_"):
            context_sources["Random"] += 1
        elif label.startswith("Energy_"):
            context_sources["Energy"] += 1
        elif label.startswith("Obj_"):
            context_sources["Object"] += 1
        else:
            context_sources["Other"] += 1
    
    return {
        "total_contexts": len(contexts),
        "top_words": top_words,
        "avg_happiness": avg_happiness,
        "max_happiness_context": max_happiness_context,
        "min_happiness_context": min_happiness_context,
        "most_connected": most_connected,
        "context_sources": dict(context_sources),
        "all_words": all_words,
        "contexts": contexts
    }

def analyze_learning_history(state, top_n=20):
    """Analysiert die Lernhistorie des Bewusstseins."""
    if not state or "learning_history" not in state:
        print("Keine Lernhistorie im Zustand gefunden.")
        return None
    
    learning_history = state["learning_history"]
    
    if not learning_history:
        print("Lernhistorie ist leer.")
        return None
    
    # Zähle Kontexte pro URL
    contexts_per_url = {entry["url"]: entry["contexts_learned"] for entry in learning_history}
    top_urls = sorted(contexts_per_url.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    # Analysiere Zeitstempel
    timestamps = [datetime.datetime.fromisoformat(entry["timestamp"]) for entry in learning_history]
    if timestamps:
        first_learning = min(timestamps)
        last_learning = max(timestamps)
        learning_duration = last_learning - first_learning
    else:
        first_learning = last_learning = learning_duration = None
    
    # Gesamtzahl der gelernten Kontexte
    total_learned = sum(entry["contexts_learned"] for entry in learning_history)
    
    return {
        "total_urls": len(learning_history),
        "total_learned": total_learned,
        "top_urls": top_urls,
        "first_learning": first_learning,
        "last_learning": last_learning,
        "learning_duration": learning_duration
    }

def analyze_emotional_state(state):
    """Analysiert den emotionalen Zustand des Bewusstseins."""
    if not state or "emotional_state" not in state:
        print("Kein emotionaler Zustand im Zustand gefunden.")
        return None
    
    emotional_state = state["emotional_state"]
    
    # Überprüfe die Struktur des emotionalen Zustands
    if isinstance(emotional_state, dict):
        # Wenn es ein einfaches Dictionary mit Emotion -> Wert ist
        if all(isinstance(v, (int, float)) for v in emotional_state.values()):
            sorted_emotions = sorted(emotional_state.items(), key=lambda x: abs(x[1]), reverse=True)
        else:
            # Wenn es ein komplexeres Dictionary ist, extrahiere die Werte
            print("Komplexe emotionale Zustandsstruktur erkannt.")
            simplified_state = {}
            for emotion, value in emotional_state.items():
                if isinstance(value, dict) and "value" in value:
                    simplified_state[emotion] = value["value"]
                elif isinstance(value, (int, float)):
                    simplified_state[emotion] = value
                else:
                    print(f"Unbekannte Struktur für Emotion {emotion}: {value}")
            
            sorted_emotions = sorted(simplified_state.items(), key=lambda x: abs(x[1]), reverse=True)
    else:
        print(f"Unerwarteter Typ des emotionalen Zustands: {type(emotional_state)}")
        sorted_emotions = []
    
    return {
        "emotional_state": emotional_state,
        "sorted_emotions": sorted_emotions
    }

def create_visualizations(analysis_results, output_dir, top_n=20):
    """Erstellt Visualisierungen der Analyseergebnisse."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Hilfsfunktion zum Abrufen des Glückswerts
    def get_happiness(data, default=0.0):
        return data.get("happiness", default)
    
    # Erstelle Wort-Cloud
    if "all_words" in analysis_results and analysis_results["all_words"]:
        try:
            wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(analysis_results["all_words"]))
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.title("Wort-Cloud der Kontexte")
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f"wordcloud_{timestamp}.png"))
            plt.close()
        except Exception as e:
            print(f"Fehler bei der Erstellung der Wort-Cloud: {e}")
    
    # Visualisiere Top-Wörter
    if "top_words" in analysis_results and analysis_results["top_words"]:
        try:
            words, counts = zip(*analysis_results["top_words"])
            plt.figure(figsize=(12, 6))
            plt.barh(range(len(words)), counts, align='center')
            plt.yticks(range(len(words)), words)
            plt.xlabel('Häufigkeit')
            plt.title(f'Top {len(words)} häufigste Wörter')
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f"top_words_{timestamp}.png"))
            plt.close()
        except Exception as e:
            print(f"Fehler bei der Visualisierung der Top-Wörter: {e}")
    
    # Visualisiere Kontextquellen
    if "context_sources" in analysis_results and analysis_results["context_sources"]:
        try:
            sources = list(analysis_results["context_sources"].keys())
            counts = list(analysis_results["context_sources"].values())
            plt.figure(figsize=(10, 6))
            plt.pie(counts, labels=sources, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')
            plt.title('Kontextquellen')
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f"context_sources_{timestamp}.png"))
            plt.close()
        except Exception as e:
            print(f"Fehler bei der Visualisierung der Kontextquellen: {e}")
    
    # Visualisiere emotionalen Zustand
    if "emotional_state" in analysis_results and analysis_results["emotional_state"]:
        try:
            emotions = list(analysis_results["emotional_state"].keys())
            values = list(analysis_results["emotional_state"].values())
            plt.figure(figsize=(10, 6))
            bars = plt.bar(emotions, values)
            
            # Färbe Balken basierend auf Wert (positiv=grün, negativ=rot)
            for i, v in enumerate(values):
                if v >= 0:
                    bars[i].set_color('green')
                else:
                    bars[i].set_color('red')
            
            plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
            plt.ylabel('Stärke')
            plt.title('Emotionaler Zustand')
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f"emotional_state_{timestamp}.png"))
            plt.close()
        except Exception as e:
            print(f"Fehler bei der Visualisierung des emotionalen Zustands: {e}")
    
    # Visualisiere Netzwerk der am stärksten verbundenen Kontexte
    if "most_connected" in analysis_results and analysis_results["most_connected"] and "contexts" in analysis_results:
        try:
            G = nx.Graph()
            
            # Füge die am stärksten verbundenen Kontexte als Knoten hinzu
            top_connected_labels = [label for label, _ in analysis_results["most_connected"][:min(10, len(analysis_results["most_connected"]))]]
            
            # Füge Knoten hinzu
            for label in top_connected_labels:
                if label in analysis_results["contexts"]:
                    G.add_node(label, happiness=get_happiness(analysis_results["contexts"][label]))
            
            # Füge Kanten hinzu
            for label in top_connected_labels:
                if label in analysis_results["contexts"]:
                    for connected_label in analysis_results["contexts"][label].get("connections", []):
                        if connected_label in top_connected_labels:
                            G.add_edge(label, connected_label)
            
            if G.nodes():
                plt.figure(figsize=(12, 10))
                
                # Berechne Layout
                try:
                    pos = nx.spring_layout(G, seed=42)
                except:
                    pos = nx.random_layout(G)
                
                # Zeichne Knoten mit Farben basierend auf Glückswert
                node_colors = [plt.cm.RdYlGn(0.5 + get_happiness(analysis_results["contexts"][node]) / 2) for node in G.nodes()]
                
                nx.draw_networkx(
                    G, pos,
                    node_color=node_colors,
                    node_size=300,
                    font_size=8,
                    width=0.5,
                    edge_color='gray',
                    alpha=0.8,
                    with_labels=True
                )
                
                plt.title("Netzwerk der am stärksten verbundenen Kontexte")
                plt.axis('off')
                plt.tight_layout()
                plt.savefig(os.path.join(output_dir, f"top_connected_network_{timestamp}.png"))
                plt.close()
        except Exception as e:
            print(f"Fehler bei der Visualisierung des Netzwerks: {e}")

def print_analysis_results(analysis_results, top_n=20):
    """Gibt die Analyseergebnisse aus."""
    print("\n" + "="*80)
    print("ANALYSE DES KÜNSTLICHEN BEWUSSTSEINS")
    print("="*80)
    
    # Allgemeine Informationen
    print(f"\nGesamtzahl der Kontexte: {analysis_results.get('total_contexts', 'N/A')}")
    print(f"Durchschnittlicher Glückswert: {analysis_results.get('avg_happiness', 'N/A'):.4f}")
    
    # Kontextquellen
    if "context_sources" in analysis_results:
        print("\nKontextquellen:")
        for source, count in sorted(analysis_results["context_sources"].items(), key=lambda x: x[1], reverse=True):
            print(f"  {source}: {count}")
    
    # Top-Wörter
    if "top_words" in analysis_results and analysis_results["top_words"]:
        print(f"\nTop {len(analysis_results['top_words'])} häufigste Wörter:")
        for word, count in analysis_results["top_words"]:
            print(f"  {word}: {count}")
    
    # Am stärksten verbundene Kontexte
    if "most_connected" in analysis_results and analysis_results["most_connected"]:
        print(f"\nTop {len(analysis_results['most_connected'])} am stärksten verbundene Kontexte:")
        for label, count in analysis_results["most_connected"]:
            print(f"  {label}: {count} Verbindungen")
    
    # Kontext mit höchstem Glückswert
    if "max_happiness_context" in analysis_results and analysis_results["max_happiness_context"]:
        print("\nKontext mit höchstem Glückswert:")
        if "text" in analysis_results["max_happiness_context"]:
            print(f"  Text: {analysis_results['max_happiness_context']['text']}")
        elif "words" in analysis_results["max_happiness_context"]:
            words = analysis_results["max_happiness_context"]["words"]
            text = " ".join(words) if isinstance(words, list) else words
            print(f"  Text: {text}")
        print(f"  Glückswert: {analysis_results['max_happiness_context']['happiness']:.4f}")
    
    # Kontext mit niedrigstem Glückswert
    if "min_happiness_context" in analysis_results and analysis_results["min_happiness_context"]:
        print("\nKontext mit niedrigstem Glückswert:")
        if "text" in analysis_results["min_happiness_context"]:
            print(f"  Text: {analysis_results['min_happiness_context']['text']}")
        elif "words" in analysis_results["min_happiness_context"]:
            words = analysis_results["min_happiness_context"]["words"]
            text = " ".join(words) if isinstance(words, list) else words
            print(f"  Text: {text}")
        print(f"  Glückswert: {analysis_results['min_happiness_context']['happiness']:.4f}")
    
    # Lernhistorie
    if "learning_history" in analysis_results and analysis_results["learning_history"]:
        print("\nLernhistorie:")
        learning_history = analysis_results["learning_history"]
        print(f"  Besuchte URLs: {learning_history.get('total_urls', 'N/A')}")
        print(f"  Gelernte Kontexte: {learning_history.get('total_learned', 'N/A')}")
        
        if "first_learning" in learning_history and learning_history["first_learning"]:
            print(f"  Erster Lernvorgang: {learning_history['first_learning']}")
            print(f"  Letzter Lernvorgang: {learning_history['last_learning']}")
            print(f"  Lerndauer: {learning_history['learning_duration']}")
        
        if "top_urls" in learning_history and learning_history["top_urls"]:
            print(f"\n  Top {len(learning_history['top_urls'])} URLs mit den meisten gelernten Kontexten:")
            for url, count in learning_history["top_urls"]:
                print(f"    {url}: {count} Kontexte")
    else:
        print("\nKeine Lernhistorie verfügbar.")
    
    # Emotionaler Zustand
    if "emotional_analysis" in analysis_results and analysis_results["emotional_analysis"] and "sorted_emotions" in analysis_results["emotional_analysis"]:
        print("\nEmotionaler Zustand:")
        for emotion, value in analysis_results["emotional_analysis"]["sorted_emotions"]:
            print(f"  {emotion}: {value:.4f}")
    
    print("\n" + "="*80)

def interactive_mode(analysis_results):
    """Startet den interaktiven Modus zur Erkundung der Analyseergebnisse."""
    if not analysis_results or "contexts" not in analysis_results:
        print("Keine Kontexte für den interaktiven Modus verfügbar.")
        return
    
    contexts = analysis_results["contexts"]
    
    # Hilfsfunktion zum Anzeigen des Textes eines Kontexts
    def get_context_text(data):
        if "text" in data:
            return data["text"]
        elif "words" in data:
            words = data["words"]
            return " ".join(words) if isinstance(words, list) else words
        else:
            return "[Kein Text verfügbar]"
    
    while True:
        print("\n" + "="*80)
        print("INTERAKTIVER MODUS")
        print("="*80)
        print("\nOptionen:")
        print("1. Kontext nach Label suchen")
        print("2. Kontexte nach Text durchsuchen")
        print("3. Verbindungen eines Kontexts anzeigen")
        print("4. Pfad zwischen zwei Kontexten finden")
        print("5. Zufälligen Kontext anzeigen")
        print("6. Beenden")
        
        choice = input("\nWähle eine Option (1-6): ")
        
        if choice == "1":
            label = input("Gib das Label des Kontexts ein: ")
            if label in contexts:
                print(f"\nKontext gefunden:")
                print(f"  Label: {label}")
                print(f"  Text: {get_context_text(contexts[label])}")
                print(f"  Glückswert: {contexts[label].get('happiness', 'N/A')}")
                print(f"  Anzahl Verbindungen: {len(contexts[label].get('connections', []))}")
            else:
                print(f"Kontext mit Label '{label}' nicht gefunden.")
        
        elif choice == "2":
            search_text = input("Gib den Suchtext ein: ").lower()
            found_contexts = []
            
            for label, data in contexts.items():
                context_text = get_context_text(data).lower()
                if search_text in context_text:
                    found_contexts.append((label, data))
            
            if found_contexts:
                print(f"\n{len(found_contexts)} Kontexte gefunden:")
                for i, (label, data) in enumerate(found_contexts[:10], 1):
                    print(f"  {i}. {label}: {get_context_text(data)}")
                
                if len(found_contexts) > 10:
                    print(f"  ... und {len(found_contexts) - 10} weitere")
            else:
                print(f"Keine Kontexte mit Text '{search_text}' gefunden.")
        
        elif choice == "3":
            label = input("Gib das Label des Kontexts ein: ")
            if label in contexts:
                connections = contexts[label].get("connections", [])
                if connections:
                    print(f"\n{len(connections)} Verbindungen gefunden:")
                    for i, connected_label in enumerate(connections[:20], 1):
                        if connected_label in contexts:
                            print(f"  {i}. {connected_label}: {get_context_text(contexts[connected_label])}")
                    
                    if len(connections) > 20:
                        print(f"  ... und {len(connections) - 20} weitere")
                else:
                    print("Keine Verbindungen gefunden.")
            else:
                print(f"Kontext mit Label '{label}' nicht gefunden.")
        
        elif choice == "4":
            start_label = input("Gib das Label des Startkontexts ein: ")
            end_label = input("Gib das Label des Zielkontexts ein: ")
            
            if start_label not in contexts:
                print(f"Startkontext mit Label '{start_label}' nicht gefunden.")
                continue
            
            if end_label not in contexts:
                print(f"Zielkontext mit Label '{end_label}' nicht gefunden.")
                continue
            
            # Erstelle einen Graphen aus den Kontexten
            G = nx.Graph()
            for label, data in contexts.items():
                G.add_node(label)
                for connected_label in data.get("connections", []):
                    if connected_label in contexts:
                        G.add_edge(label, connected_label)
            
            try:
                # Finde den kürzesten Pfad
                path = nx.shortest_path(G, start_label, end_label)
                
                print(f"\nPfad gefunden ({len(path)} Schritte):")
                for i, label in enumerate(path):
                    print(f"  {i+1}. {label}: {get_context_text(contexts[label])}")
            except nx.NetworkXNoPath:
                print("Kein Pfad zwischen den Kontexten gefunden.")
            except Exception as e:
                print(f"Fehler beim Finden des Pfads: {e}")
        
        elif choice == "5":
            import random
            random_label = random.choice(list(contexts.keys()))
            print(f"\nZufälliger Kontext:")
            print(f"  Label: {random_label}")
            print(f"  Text: {get_context_text(contexts[random_label])}")
            print(f"  Glückswert: {contexts[random_label].get('happiness', 'N/A')}")
            print(f"  Anzahl Verbindungen: {len(contexts[random_label].get('connections', []))}")
        
        elif choice == "6":
            print("Interaktiver Modus beendet.")
            break
        
        else:
            print("Ungültige Option. Bitte wähle eine Option zwischen 1 und 6.")

def main():
    """Hauptfunktion."""
    args = parse_arguments()
    
    # Lade den Zustand
    state = load_state(args.state_file)
    if not state:
        return
    
    # Erstelle Ausgabeverzeichnis
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    # Analysiere Kontexte
    context_analysis = analyze_contexts(state, args.top_n, args.web_only)
    
    # Analysiere Lernhistorie
    learning_history = analyze_learning_history(state, args.top_n)
    
    # Analysiere emotionalen Zustand
    emotional_analysis = analyze_emotional_state(state)
    
    # Kombiniere Analyseergebnisse
    analysis_results = {
        "iteration": state.get("iteration", "N/A"),
        "energy": state.get("energy", "N/A"),
        "current_focus": state.get("current_focus", "N/A"),
        **context_analysis,
        "learning_history": learning_history,
        "emotional_analysis": emotional_analysis
    }
    
    # Erstelle Visualisierungen
    create_visualizations(analysis_results, args.output_dir, args.top_n)
    
    # Gib Analyseergebnisse aus
    print_analysis_results(analysis_results, args.top_n)
    
    # Speichere Analyseergebnisse als JSON
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(os.path.join(args.output_dir, f"analysis_{timestamp}.json"), 'w') as f:
        # Konvertiere nicht-serialisierbare Objekte in Strings
        serializable_results = {}
        for key, value in analysis_results.items():
            if isinstance(value, dict):
                serializable_results[key] = value
            elif isinstance(value, (list, str, int, float, bool, type(None))):
                serializable_results[key] = value
            else:
                serializable_results[key] = str(value)
        
        json.dump(serializable_results, f, indent=2, default=str)
    
    print(f"\nAnalyseergebnisse gespeichert in: {os.path.join(args.output_dir, f'analysis_{timestamp}.json')}")
    
    # Starte interaktiven Modus, wenn gewünscht
    if args.interactive:
        interactive_mode(analysis_results)

if __name__ == "__main__":
    main() 