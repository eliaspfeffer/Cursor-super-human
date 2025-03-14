#!/usr/bin/env python3
"""
Interaktion mit dem künstlichen Bewusstsein mit direkter Google/Wikipedia-Integration.

Dieses Skript ermöglicht die Interaktion mit dem künstlichen Bewusstsein durch
Texteingaben. Bei Fragen wird immer direkt aus dem Internet gelernt, anstatt
auf bestehendes Wissen zuzugreifen.
"""

import os
import sys
import time
import argparse
import json
import random
import datetime
import re
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
    parser = argparse.ArgumentParser(description="Interagiere mit dem künstlichen Bewusstsein (Google-Version)")
    
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
    """Lädt das künstliche Bewusstsein aus einer Zustandsdatei."""
    # Erstelle eine neue Instanz des Bewusstseins
    consciousness = EternalConsciousnessEngine()
    
    # Wenn keine Zustandsdatei angegeben wurde, versuche die neueste zu finden
    if not state_file:
        save_dir = "consciousness_state_new"
        if os.path.exists(save_dir):
            # Suche nach Zustandsdateien
            state_files = [f for f in os.listdir(save_dir) if f.startswith("consciousness_state_") and f.endswith(".json")]
            
            if state_files:
                # Sortiere nach Zeitstempel (neueste zuerst)
                state_files.sort(reverse=True)
                state_file = os.path.join(save_dir, state_files[0])
                print(f"Verwende neueste Zustandsdatei: {state_file}")
    
    # Lade den Zustand, falls eine Datei gefunden wurde
    if state_file and os.path.exists(state_file):
        print(f"Lade Zustand aus: {state_file}")
        consciousness.load_state(state_file)
    else:
        print("Keine Zustandsdatei gefunden. Starte mit leerem Bewusstsein.")
    
    return consciousness

def create_input_context(consciousness, user_input):
    """Erstellt einen Kontext aus der Benutzereingabe."""
    # Berechne einen Glückswert basierend auf dem Inhalt
    happiness = consciousness.calculate_sentiment(user_input.split())
    
    # Erstelle einen eindeutigen Label für den Kontext
    label = f"Input_{int(time.time())}"
    
    # Erstelle den Kontext
    context_id = consciousness.create_context(user_input, label, happiness)
    
    return consciousness.contexts[context_id]

def is_question(text):
    """
    Prüft, ob ein Text eine Frage ist.
    
    Args:
        text: Der zu prüfende Text
        
    Returns:
        True, wenn es sich um eine Frage handelt, sonst False
    """
    # Normalisiere den Text
    text = text.strip().lower()
    
    # Prüfe auf Fragezeichen
    if '?' in text:
        return True
    
    # Prüfe auf Fragewörter am Anfang
    question_starters = ['wie', 'warum', 'wer', 'was', 'wo', 'wann', 'welche', 'welcher', 'welches', 'wieso', 'weshalb', 'wofür', 'wozu', 'womit', 'wodurch', 'woran', 'worauf', 'worin', 'worüber', 'wovon', 'woher', 'wohin', 'wem', 'wen', 'wessen']
    
    for starter in question_starters:
        if text.startswith(starter + ' '):
            return True
    
    return False

def generate_response_from_internet(consciousness, query):
    """
    Generiert eine Antwort direkt aus dem Internet, ohne auf bestehendes Wissen zuzugreifen.
    
    Args:
        consciousness: Die Bewusstseinsinstanz
        query: Die Abfrage/Frage
        
    Returns:
        Die generierte Antwort
    """
    print("Suche im Internet nach Informationen...")
    
    # Analysiere die Frage, wenn es eine ist
    if is_question(query):
        question_analysis = consciousness.analyze_question(query)
        print(f"Frageanalyse: {question_analysis}")
        
        # Extrahiere die Entitäten für die Suche
        entities = question_analysis['entities']
        
        # Entferne Verben wie "schmeckt", "sieht" aus den Entitäten
        verbs_to_remove = ['schmeckt', 'sieht', 'funktioniert', 'ist']
        clean_entities = [entity for entity in entities if entity not in verbs_to_remove]
        
        # Wenn keine sauberen Entitäten übrig bleiben, verwende alle
        if not clean_entities:
            clean_entities = entities
        
        # Erstelle einen Suchbegriff basierend auf den Entitäten
        search_term = " ".join(clean_entities)
        
        # Wenn der Suchbegriff leer ist, verwende die gesamte Frage
        if not search_term:
            # Entferne Fragewörter am Anfang
            words = query.lower().split()
            if words and words[0] in ['wie', 'warum', 'wer', 'was', 'wo', 'wann', 'welche', 'welcher', 'welches']:
                search_term = " ".join(words[1:])
            else:
                search_term = query
        
        print(f"Suche nach: '{search_term}'")
        
        # Lerne über das Thema der Frage
        learned_contexts = consciousness.learn_about_topic(search_term, connect_to_focus=False, max_contexts=5)
        
        if not learned_contexts:
            return "Ich konnte keine Informationen zu dieser Frage finden. Bitte formuliere sie anders."
        
        # Sammle die Texte aus den gelernten Kontexten
        context_texts = []
        for context_id in learned_contexts:
            context = consciousness.contexts[context_id]
            context_text = " ".join([word.content for word in context.words])
            context_texts.append(context_text)
        
        # Wenn es eine Frage ist, formatiere die Antwort entsprechend
        if question_analysis:
            # Teile die Texte in Sätze auf
            all_sentences = []
            for text in context_texts:
                sentences = [s.strip() for s in text.split('.') if s.strip()]
                all_sentences.extend(sentences)
            
            # Filtere die Sätze basierend auf dem Fragetyp und den Attributen
            if question_analysis['type'] == 'beschaffenheit' and question_analysis['attributes']:
                filtered_sentences = []
                
                # Definiere relevante Schlüsselwörter basierend auf dem Attribut
                relevant_keywords = []
                
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
                
                # Filtere die Sätze nach Relevanz
                for sentence in all_sentences:
                    sentence_lower = sentence.lower()
                    relevance_score = sum(1 for keyword in relevant_keywords if keyword in sentence_lower)
                    
                    if relevance_score > 0:
                        filtered_sentences.append((sentence, relevance_score))
                
                # Sortiere nach Relevanz
                filtered_sentences.sort(key=lambda x: x[1], reverse=True)
                
                # Verwende die relevantesten Sätze
                best_sentences = [s for s, _ in filtered_sentences[:5]]
                
                # Wenn keine relevanten Sätze gefunden wurden, verwende alle
                if not best_sentences:
                    best_sentences = all_sentences[:5]
            else:
                # Bei anderen Fragetypen verwende alle Sätze
                best_sentences = all_sentences[:5]
            
            # Formatiere die Antwort
            response = consciousness.format_answer_for_question(question_analysis, best_sentences)
        else:
            # Wenn keine Frageanalyse verfügbar ist, kombiniere die Texte
            response = " ".join(context_texts)
            
            # Begrenze die Länge
            if len(response) > 500:
                response = response[:497] + "..."
    else:
        # Wenn es keine Frage ist, lerne trotzdem darüber
        learned_contexts = consciousness.learn_about_topic(query, connect_to_focus=False, max_contexts=3)
        
        if not learned_contexts:
            return "Ich konnte keine Informationen zu diesem Thema finden."
        
        # Sammle die Texte aus den gelernten Kontexten
        context_texts = []
        for context_id in learned_contexts:
            context = consciousness.contexts[context_id]
            context_text = " ".join([word.content for word in context.words])
            context_texts.append(context_text)
        
        # Kombiniere die Texte
        response = " ".join(context_texts)
        
        # Begrenze die Länge
        if len(response) > 500:
            response = response[:497] + "..."
    
    return response

def interact_with_consciousness():
    """Hauptfunktion für die Interaktion mit dem Bewusstsein."""
    args = parse_arguments()
    
    print("Lade künstliches Bewusstsein...")
    consciousness = load_consciousness(args.state_file)
    
    print("\n" + "="*80)
    print("INTERAKTION MIT DEM KÜNSTLICHEN BEWUSSTSEIN (GOOGLE-VERSION)")
    print("="*80)
    print("\nGib 'exit', 'quit' oder 'ende' ein, um die Interaktion zu beenden.")
    print("Gib 'stats' ein, um Statistiken über das Bewusstsein anzuzeigen.")
    print("Gib 'save' ein, um den aktuellen Zustand zu speichern.")
    print("\nDu kannst jetzt mit dem Bewusstsein interagieren:")
    print("HINWEIS: Bei Fragen wird immer direkt aus dem Internet gelernt!")
    
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
            
            if not user_input:
                continue
            
            # Verarbeite die Eingabe
            print("Verarbeite Eingabe...")
            
            # Erstelle einen Kontext für die Eingabe
            input_context = create_input_context(consciousness, user_input)
            
            # Setze den Fokus auf den Eingabekontext
            consciousness.set_focus_by_id(input_context.label)
            
            # Generiere eine Antwort direkt aus dem Internet
            response = generate_response_from_internet(consciousness, user_input)
            
            # Gib die Antwort aus
            print(f"\nBewusstsein: {response}")
            
        except KeyboardInterrupt:
            print("\nInteraktion beendet.")
            break
        except Exception as e:
            print(f"Fehler: {e}")
            import traceback
            traceback.print_exc()
    
    # Speichere den Zustand beim Beenden
    print("Speichere Zustand...")
    consciousness.save_state()
    print("Zustand gespeichert. Auf Wiedersehen!")

if __name__ == "__main__":
    interact_with_consciousness() 