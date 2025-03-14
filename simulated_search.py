#!/usr/bin/env python3
"""
Simulierte Suche für das künstliche Bewusstsein.

Dieses Modul ermöglicht es, Google-Suchergebnisse zu simulieren und
dann die Logik aus dem Todo zu verwenden, um die richtige Antwort zu extrahieren.
"""

import re
import nltk
import json
import os
from collections import defaultdict

# Stelle sicher, dass die benötigten NLTK-Daten vorhanden sind
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class SimulatedSearch:
    def __init__(self, knowledge_file="simulated_knowledge.json"):
        """
        Initialisiert die simulierte Suche.
        
        Args:
            knowledge_file: Die Datei, in der das Wissen gespeichert wird
        """
        self.knowledge_file = knowledge_file
        self.knowledge = self.load_knowledge()
        
        # Definiere Attribute und ihre Synonyme
        self.attribute_synonyms = {
            "geschmack": ["schmeckt", "schmecken", "geschmack", "aroma", "süß", "sauer", "bitter", "salzig", "würzig", "scharf", "mild", "fruchtig", "herb"],
            "aussehen": ["sieht", "aussieht", "aussehen", "farbe", "form", "gestalt", "erscheinung"],
            "größe": ["groß", "größe", "dimension", "umfang", "ausdehnung", "höhe", "breite", "länge"],
            "alter": ["alt", "alter", "jahre", "jahrzehnte", "jahrhunderte", "entstehung", "geburt"],
            "funktion": ["funktioniert", "funktion", "arbeitet", "mechanismus", "prozess", "ablauf"]
        }
        
        # Erstelle ein invertiertes Wörterbuch für schnellere Suche
        self.word_to_attribute = {}
        for attr, synonyms in self.attribute_synonyms.items():
            for word in synonyms:
                self.word_to_attribute[word] = attr
    
    def load_knowledge(self):
        """Lädt das Wissen aus der Datei."""
        if os.path.exists(self.knowledge_file):
            try:
                with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Fehler beim Laden des Wissens: {e}")
                return {"contexts": []}
        else:
            return {"contexts": []}
    
    def save_knowledge(self):
        """Speichert das Wissen in der Datei."""
        try:
            with open(self.knowledge_file, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge, f, indent=2, ensure_ascii=False)
            print(f"Wissen gespeichert in {self.knowledge_file}")
        except Exception as e:
            print(f"Fehler beim Speichern des Wissens: {e}")
    
    def add_context(self, text):
        """
        Fügt einen neuen Kontext zum Wissen hinzu.
        
        Args:
            text: Der Text des Kontexts
        """
        # Erstelle eine eindeutige ID für den Kontext
        context_id = f"context_{len(self.knowledge['contexts'])}"
        
        # Extrahiere Attribute aus dem Text
        attributes = self.extract_attributes(text)
        
        # Erstelle den Kontext
        context = {
            "id": context_id,
            "text": text,
            "attributes": attributes,
            "connections": []
        }
        
        # Füge den Kontext zum Wissen hinzu
        self.knowledge["contexts"].append(context)
        
        # Erstelle Verbindungen zu anderen Kontexten
        self.create_connections(context)
        
        # Speichere das Wissen
        self.save_knowledge()
        
        return context_id
    
    def extract_attributes(self, text):
        """
        Extrahiert Attribute aus einem Text.
        
        Args:
            text: Der Text, aus dem Attribute extrahiert werden sollen
            
        Returns:
            Ein Dictionary mit Attributen und ihren Werten
        """
        attributes = {}
        
        # Normalisiere den Text
        text = text.lower()
        
        # Suche nach Attributen im Text
        for attr, synonyms in self.attribute_synonyms.items():
            for synonym in synonyms:
                if synonym in text:
                    # Extrahiere den Wert des Attributs
                    # Hier könnten wir komplexere NLP-Techniken verwenden
                    attributes[attr] = True
                    break
        
        return attributes
    
    def create_connections(self, context):
        """
        Erstellt Verbindungen zwischen dem neuen Kontext und bestehenden Kontexten.
        
        Args:
            context: Der neue Kontext
        """
        # Extrahiere Wörter aus dem Kontext
        context_words = set(re.findall(r'\b\w+\b', context["text"].lower()))
        
        # Für jeden bestehenden Kontext
        for other_context in self.knowledge["contexts"]:
            # Überspringe den Kontext selbst
            if other_context["id"] == context["id"]:
                continue
            
            # Extrahiere Wörter aus dem anderen Kontext
            other_words = set(re.findall(r'\b\w+\b', other_context["text"].lower()))
            
            # Berechne die Wortüberlappung
            overlap = context_words.intersection(other_words)
            
            # Wenn es eine Überlappung gibt, erstelle eine Verbindung
            if overlap:
                # Berechne die Stärke der Verbindung basierend auf der Überlappung
                strength = len(overlap) / max(len(context_words), len(other_words))
                
                # Berechne zusätzliche Stärke für Attribut-Verbindungen
                attribute_strength = 0
                
                # Prüfe, ob es gemeinsame Attribute gibt
                context_attrs = set(context.get("attributes", {}).keys())
                other_attrs = set(other_context.get("attributes", {}).keys())
                common_attrs = context_attrs.intersection(other_attrs)
                
                if common_attrs:
                    attribute_strength = len(common_attrs) * 0.2  # Bonus für gemeinsame Attribute
                
                # Berechne die Gesamtstärke
                total_strength = strength + attribute_strength
                
                # Erstelle die Verbindung
                connection = {
                    "target": other_context["id"],
                    "strength": total_strength
                }
                
                # Füge die Verbindung zum Kontext hinzu
                context["connections"].append(connection)
                
                # Füge auch eine Verbindung in die andere Richtung hinzu
                other_connection = {
                    "target": context["id"],
                    "strength": total_strength
                }
                
                other_context["connections"].append(other_connection)
    
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
            for word in words:
                if word in self.word_to_attribute:
                    attributes.append(self.word_to_attribute[word])
            
            # Wenn keine spezifischen Attribute gefunden wurden, verwende die allgemeine Beschaffenheit
            if not attributes:
                attributes.append('eigenschaft')
        
        # Ergebnis zusammenstellen
        result = {
            'type': question_type,
            'entities': entities,
            'attributes': attributes,
            'original_question': question
        }
        
        return result
    
    def find_relevant_contexts(self, question_analysis):
        """
        Findet relevante Kontexte basierend auf der Frageanalyse.
        
        Args:
            question_analysis: Die Analyse der Frage
            
        Returns:
            Eine Liste von relevanten Kontexten mit Scores
        """
        relevant_contexts = []
        
        # Extrahiere Entitäten und Attribute aus der Frageanalyse
        entities = question_analysis['entities']
        attributes = question_analysis['attributes']
        
        # Für jeden Kontext
        for context in self.knowledge["contexts"]:
            # Berechne den Score für den Kontext
            score = 0
            
            # Prüfe, ob der Kontext die gesuchten Entitäten enthält
            context_text = context["text"].lower()
            for entity in entities:
                if entity in context_text:
                    score += 1  # Bonus für jede gefundene Entität
            
            # Prüfe, ob der Kontext die gesuchten Attribute enthält
            context_attrs = context.get("attributes", {})
            for attr in attributes:
                if attr in context_attrs:
                    score += 2  # Bonus für jedes gefundene Attribut
            
            # Wenn der Score größer als 0 ist, füge den Kontext zur Liste hinzu
            if score > 0:
                relevant_contexts.append((context, score))
        
        # Sortiere die Kontexte nach Score (absteigend)
        relevant_contexts.sort(key=lambda x: x[1], reverse=True)
        
        return relevant_contexts
    
    def format_answer(self, question_analysis, relevant_contexts):
        """
        Formatiert eine Antwort basierend auf der Frageanalyse und den relevanten Kontexten.
        
        Args:
            question_analysis: Die Analyse der Frage
            relevant_contexts: Die relevanten Kontexte
            
        Returns:
            Eine formatierte Antwort
        """
        if not relevant_contexts:
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
        
        # Extrahiere den Text aus dem relevantesten Kontext
        best_context = relevant_contexts[0][0]
        answer_text = best_context["text"]
        
        # Füge die Einleitung hinzu
        formatted_answer = intro + answer_text
        
        return formatted_answer
    
    def get_answer(self, question):
        """
        Generiert eine Antwort auf eine Frage.
        
        Args:
            question: Die Frage
            
        Returns:
            Die Antwort
        """
        # Analysiere die Frage
        question_analysis = self.analyze_question(question)
        print(f"Frageanalyse: {question_analysis}")
        
        # Finde relevante Kontexte
        relevant_contexts = self.find_relevant_contexts(question_analysis)
        
        if not relevant_contexts:
            return "Ich konnte keine relevanten Informationen finden. Bitte gib mir mehr Wissen zu diesem Thema."
        
        # Formatiere die Antwort
        answer = self.format_answer(question_analysis, relevant_contexts)
        
        return answer

def interactive_mode():
    """Startet den interaktiven Modus."""
    search = SimulatedSearch()
    
    print("\n" + "="*80)
    print("SIMULIERTE SUCHE")
    print("="*80)
    print("\nGib 'exit', 'quit' oder 'ende' ein, um die Interaktion zu beenden.")
    print("Gib 'add' ein, um Wissen hinzuzufügen.")
    print("Gib 'list' ein, um das vorhandene Wissen anzuzeigen.")
    print("Gib 'clear' ein, um das Wissen zu löschen.")
    print("\nDu kannst jetzt Fragen stellen oder Wissen hinzufügen:")
    
    while True:
        try:
            user_input = input("\nDu: ").strip()
            
            if user_input.lower() in ["exit", "quit", "ende"]:
                break
            
            if user_input.lower() == "add":
                # Füge Wissen hinzu
                print("Gib das Wissen ein (leere Zeile zum Beenden):")
                knowledge_text = ""
                while True:
                    line = input().strip()
                    if not line:
                        break
                    knowledge_text += line + " "
                
                if knowledge_text:
                    context_id = search.add_context(knowledge_text)
                    print(f"Wissen hinzugefügt mit ID: {context_id}")
                
                continue
            
            if user_input.lower() == "list":
                # Zeige das vorhandene Wissen an
                print("\nVorhandenes Wissen:")
                for i, context in enumerate(search.knowledge["contexts"]):
                    print(f"{i+1}. {context['text'][:100]}...")
                    print(f"   Attribute: {context.get('attributes', {})}")
                    print(f"   Verbindungen: {len(context.get('connections', []))}")
                    print()
                
                continue
            
            if user_input.lower() == "clear":
                # Lösche das Wissen
                search.knowledge["contexts"] = []
                search.save_knowledge()
                print("Wissen gelöscht.")
                
                continue
            
            if not user_input:
                continue
            
            # Verarbeite die Frage
            print("Verarbeite Frage...")
            answer = search.get_answer(user_input)
            
            # Gib die Antwort aus
            print(f"\nAntwort: {answer}")
            
        except KeyboardInterrupt:
            print("\nInteraktion beendet.")
            break
        except Exception as e:
            print(f"Fehler: {e}")
            import traceback
            traceback.print_exc()
    
    print("Auf Wiedersehen!")

if __name__ == "__main__":
    interactive_mode() 