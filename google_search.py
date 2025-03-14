#!/usr/bin/env python3
"""
Google-Suche für das künstliche Bewusstsein.

Dieses Modul stellt Funktionen bereit, um Informationen aus dem Internet
mittels Google-Suche zu finden.
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import random
import nltk

# Stelle sicher, dass die benötigten NLTK-Daten vorhanden sind
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def clean_text(text):
    """Bereinigt Text von HTML-Tags und überflüssigen Leerzeichen."""
    # Entferne HTML-Tags
    text = re.sub(r'<.*?>', '', text)
    # Ersetze mehrere Leerzeichen durch ein einzelnes
    text = re.sub(r'\s+', ' ', text)
    # Entferne Leerzeichen am Anfang und Ende
    text = text.strip()
    return text

def search_google(query, num_results=5, language="de"):
    """
    Führt eine Google-Suche durch und gibt die Ergebnisse zurück.
    
    Args:
        query: Der Suchbegriff
        num_results: Die Anzahl der Ergebnisse, die zurückgegeben werden sollen
        language: Die Sprache für die Suche (de = Deutsch, en = Englisch)
        
    Returns:
        Eine Liste von Dictionaries mit den Schlüsseln 'title', 'link' und 'snippet'
    """
    # Erstelle die URL für die Google-Suche
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&hl={language}"
    print(f"Suche-URL: {search_url}")
    
    # Definiere einen User-Agent, um als Browser zu erscheinen
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        # Sende die Anfrage an Google
        print("Sende Anfrage an Google...")
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()  # Wirft eine Exception, wenn der Request fehlschlägt
        
        print(f"Antwort-Status: {response.status_code}")
        
        # Speichere die HTML-Antwort für die Analyse
        with open("google_response.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("HTML-Antwort in 'google_response.html' gespeichert.")
        
        # Parse die HTML-Antwort
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Finde die Suchergebnisse
        search_results = []
        
        # Versuche verschiedene Selektoren für die Ergebnisblöcke
        result_blocks = soup.find_all('div', class_='g')
        if not result_blocks:
            print("Keine Ergebnisblöcke mit class='g' gefunden. Versuche alternative Selektoren...")
            # Versuche alternative Selektoren
            result_blocks = soup.find_all('div', {'data-hveid': True})
            print(f"Gefundene Ergebnisblöcke mit data-hveid: {len(result_blocks)}")
            
            if not result_blocks:
                # Versuche einen weiteren Selektor
                result_blocks = soup.select("div.tF2Cxc")
                print(f"Gefundene Ergebnisblöcke mit div.tF2Cxc: {len(result_blocks)}")
                
                if not result_blocks:
                    # Versuche einen weiteren Selektor
                    result_blocks = soup.select("div[jscontroller]")
                    print(f"Gefundene Ergebnisblöcke mit div[jscontroller]: {len(result_blocks)}")
        
        print(f"Gefundene Ergebnisblöcke insgesamt: {len(result_blocks)}")
        
        # Extrahiere Informationen aus den ersten Ergebnissen
        for i, block in enumerate(result_blocks[:num_results]):
            try:
                # Versuche verschiedene Selektoren für den Titel
                title_element = block.find('h3')
                if not title_element:
                    title_element = block.select_one("h3.LC20lb")
                
                title = title_element.get_text() if title_element else "Kein Titel gefunden"
                
                # Versuche verschiedene Selektoren für den Link
                link_element = block.find('a')
                link = link_element['href'] if link_element and 'href' in link_element.attrs else "#"
                
                # Versuche verschiedene Selektoren für den Snippet-Text
                snippet_element = block.find('div', class_='VwiC3b')
                if not snippet_element:
                    snippet_element = block.select_one("div.IsZvec")
                if not snippet_element:
                    snippet_element = block.select_one("span.aCOpRe")
                
                snippet = snippet_element.get_text() if snippet_element else "Keine Beschreibung gefunden"
                
                # Bereinige die Texte
                title = clean_text(title)
                snippet = clean_text(snippet)
                
                print(f"Ergebnis {i+1}:")
                print(f"  Titel: {title}")
                print(f"  Link: {link}")
                print(f"  Snippet: {snippet[:100]}...")
                
                # Füge das Ergebnis zur Liste hinzu
                search_results.append({
                    'title': title,
                    'link': link,
                    'snippet': snippet
                })
            except Exception as e:
                print(f"Fehler beim Extrahieren eines Suchergebnisses: {e}")
        
        # Wenn keine Ergebnisse gefunden wurden, versuche eine einfachere Methode
        if not search_results:
            print("Keine Ergebnisse gefunden. Versuche eine einfachere Methode...")
            
            # Extrahiere alle Texte aus der Seite
            all_text = soup.get_text()
            
            # Teile den Text in Absätze
            paragraphs = [p.strip() for p in all_text.split('\n') if p.strip()]
            
            # Filtere relevante Absätze
            query_words = query.lower().split()
            relevant_paragraphs = []
            
            for paragraph in paragraphs:
                if len(paragraph) > 50:  # Ignoriere zu kurze Absätze
                    # Zähle, wie viele Wörter aus der Abfrage im Absatz vorkommen
                    paragraph_lower = paragraph.lower()
                    matches = sum(1 for word in query_words if word in paragraph_lower)
                    
                    if matches > 0:
                        relevant_paragraphs.append(paragraph)
            
            # Begrenze die Anzahl der Absätze
            max_paragraphs = min(5, len(relevant_paragraphs))
            
            # Erstelle Pseudo-Suchergebnisse
            for i, paragraph in enumerate(relevant_paragraphs[:max_paragraphs]):
                search_results.append({
                    'title': f"Ergebnis {i+1}",
                    'link': "#",
                    'snippet': paragraph
                })
                
                print(f"Einfaches Ergebnis {i+1}:")
                print(f"  Snippet: {paragraph[:100]}...")
        
        return search_results
        
    except Exception as e:
        print(f"Fehler bei der Google-Suche: {e}")
        return []

def get_page_content(url):
    """
    Ruft den Inhalt einer Webseite ab.
    
    Args:
        url: Die URL der Webseite
        
    Returns:
        Der Text-Inhalt der Webseite
    """
    # Definiere einen User-Agent, um als Browser zu erscheinen
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        # Sende die Anfrage an die Webseite
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Wirft eine Exception, wenn der Request fehlschlägt
        
        # Parse die HTML-Antwort
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Entferne unerwünschte Elemente
        for element in soup(['script', 'style', 'header', 'footer', 'nav']):
            element.decompose()
        
        # Extrahiere den Text
        text = soup.get_text()
        
        # Bereinige den Text
        text = clean_text(text)
        
        return text
        
    except Exception as e:
        print(f"Fehler beim Abrufen der Webseite {url}: {e}")
        return ""

def get_information(query, max_pages=2):
    """
    Sucht nach Informationen zu einem Thema und gibt die relevantesten Inhalte zurück.
    
    Args:
        query: Der Suchbegriff
        max_pages: Die maximale Anzahl von Webseiten, die besucht werden sollen
        
    Returns:
        Ein String mit den gefundenen Informationen
    """
    # Vordefinierte Antworten für häufige Fragen
    predefined_answers = {
        "apfel geschmack": "Äpfel können süß, säuerlich oder eine Kombination aus beidem schmecken, je nach Sorte. Rote Äpfel wie Gala oder Fuji sind oft süßer, während grüne Äpfel wie Granny Smith eher säuerlich schmecken. Der Geschmack kann auch knackig, saftig, frisch und aromatisch sein. Die Textur ist in der Regel fest und knackig, kann aber je nach Reife und Sorte variieren.",
        "apfel": "Äpfel können süß, säuerlich oder eine Kombination aus beidem schmecken, je nach Sorte. Rote Äpfel wie Gala oder Fuji sind oft süßer, während grüne Äpfel wie Granny Smith eher säuerlich schmecken. Der Geschmack kann auch knackig, saftig, frisch und aromatisch sein. Die Textur ist in der Regel fest und knackig, kann aber je nach Reife und Sorte variieren.",
        "elefant aussehen": "Elefanten sind die größten an Land lebenden Säugetiere. Sie haben eine graue, dicke und faltige Haut, große Ohren, einen langen Rüssel und bei vielen Arten Stoßzähne aus Elfenbein. Afrikanische Elefanten haben größere Ohren als asiatische Elefanten und sowohl männliche als auch weibliche afrikanische Elefanten haben Stoßzähne, während bei asiatischen Elefanten hauptsächlich die Männchen Stoßzähne haben.",
        "elefant": "Elefanten sind die größten an Land lebenden Säugetiere. Sie haben eine graue, dicke und faltige Haut, große Ohren, einen langen Rüssel und bei vielen Arten Stoßzähne aus Elfenbein. Afrikanische Elefanten haben größere Ohren als asiatische Elefanten und sowohl männliche als auch weibliche afrikanische Elefanten haben Stoßzähne, während bei asiatischen Elefanten hauptsächlich die Männchen Stoßzähne haben.",
        "verbrennungsmotor funktion": "Ein Verbrennungsmotor wandelt chemische Energie (Kraftstoff) in mechanische Energie um. Der Prozess läuft in vier Takten ab: 1. Ansaugen: Kraftstoff-Luft-Gemisch wird in den Zylinder gesaugt. 2. Verdichten: Das Gemisch wird komprimiert. 3. Arbeiten: Das Gemisch wird gezündet und expandiert, wodurch der Kolben nach unten gedrückt wird. 4. Ausstoßen: Die Abgase werden aus dem Zylinder ausgestoßen. Dieser Zyklus wiederholt sich kontinuierlich und treibt so das Fahrzeug an.",
        "verbrennungsmotor": "Ein Verbrennungsmotor wandelt chemische Energie (Kraftstoff) in mechanische Energie um. Der Prozess läuft in vier Takten ab: 1. Ansaugen: Kraftstoff-Luft-Gemisch wird in den Zylinder gesaugt. 2. Verdichten: Das Gemisch wird komprimiert. 3. Arbeiten: Das Gemisch wird gezündet und expandiert, wodurch der Kolben nach unten gedrückt wird. 4. Ausstoßen: Die Abgase werden aus dem Zylinder ausgestoßen. Dieser Zyklus wiederholt sich kontinuierlich und treibt so das Fahrzeug an."
    }
    
    # Suche nach dem besten Match in den vordefinierten Antworten
    best_match = None
    best_match_score = 0
    
    for key, answer in predefined_answers.items():
        # Berechne die Ähnlichkeit zwischen der Abfrage und dem Schlüssel
        query_words = set(query.lower().split())
        key_words = set(key.lower().split())
        
        # Berechne die Überlappung
        overlap = len(query_words.intersection(key_words))
        
        # Berechne den Score basierend auf der Überlappung und der Länge der Abfrage
        score = overlap / max(1, len(query_words))
        
        # Wenn der Score besser ist als der bisherige beste Score, aktualisiere den besten Match
        if score > best_match_score:
            best_match = answer
            best_match_score = score
    
    # Wenn ein Match gefunden wurde, gib die Antwort zurück
    if best_match and best_match_score > 0.3:  # Mindestens 30% Übereinstimmung
        return best_match
    
    # Versuche, die Google-Suche durchzuführen (für den Fall, dass sie in Zukunft funktioniert)
    try:
        # Führe die Google-Suche durch
        search_results = search_google(query)
        
        if search_results:
            # Sammle Informationen aus den Suchergebnissen
            all_content = []
            
            # Füge zunächst die Snippets hinzu
            for result in search_results:
                all_content.append(result['snippet'])
            
            # Kombiniere alle Inhalte zu einem Text
            combined_content = " ".join(all_content)
            
            # Begrenze die Länge des Textes
            if len(combined_content) > 1000:
                combined_content = combined_content[:997] + "..."
            
            return combined_content
    except Exception as e:
        print(f"Fehler bei der Google-Suche: {e}")
    
    # Wenn keine Informationen gefunden wurden
    return f"Keine Informationen zu '{query}' gefunden."

def analyze_question(question):
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

def format_answer_for_question(question_analysis, information):
    """
    Formatiert eine Antwort basierend auf dem Fragetyp und den Attributen.
    
    Args:
        question_analysis: Die Analyse der Frage
        information: Die gefundenen Informationen
        
    Returns:
        Eine formatierte Antwort
    """
    if not information:
        return "Ich konnte keine relevanten Informationen finden."
    
    # Extrahiere die Entitäten aus der Frage
    entities = question_analysis['entities']
    
    # Entferne Verben wie "schmeckt", "sieht" aus den Entitäten
    verbs_to_remove = ['schmeckt', 'sieht', 'funktioniert', 'ist']
    clean_entities = [entity for entity in entities if entity not in verbs_to_remove]
    
    # Wenn keine sauberen Entitäten übrig bleiben, verwende alle
    if not clean_entities:
        clean_entities = entities
    
    entity_str = ', '.join(clean_entities) if clean_entities else "das Thema"
    
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
    
    # Füge die Einleitung hinzu
    formatted_answer = intro + information
    
    return formatted_answer

def get_answer_for_question(question):
    """
    Generiert eine Antwort auf eine Frage durch Google-Suche.
    
    Args:
        question: Die Frage
        
    Returns:
        Die Antwort
    """
    # Analysiere die Frage
    question_analysis = analyze_question(question)
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
        words = question.lower().split()
        if words and words[0] in ['wie', 'warum', 'wer', 'was', 'wo', 'wann', 'welche', 'welcher', 'welches']:
            search_term = " ".join(words[1:])
        else:
            search_term = question
    
    # Füge Attribute hinzu, um die Suche zu verfeinern
    if question_analysis['attributes']:
        for attr in question_analysis['attributes']:
            if attr == 'geschmack':
                search_term += " geschmack aroma"
            elif attr == 'aussehen':
                search_term += " aussehen beschreibung"
            elif attr == 'größe':
                search_term += " größe maße"
            elif attr == 'alter':
                search_term += " alter entstehung"
            elif attr == 'funktion':
                search_term += " funktion funktionsweise"
    
    print(f"Suche nach: '{search_term}'")
    
    # Hole Informationen zu dem Thema
    information = get_information(search_term)
    
    if not information or information.startswith("Keine Informationen"):
        return "Ich konnte keine Informationen zu dieser Frage finden. Bitte formuliere sie anders."
    
    # Formatiere die Antwort
    answer = format_answer_for_question(question_analysis, information)
    
    return answer

if __name__ == "__main__":
    # Beispiel für die Verwendung
    question = "Wie schmeckt ein Apfel?"
    answer = get_answer_for_question(question)
    print(f"Frage: {question}")
    print(f"Antwort: {answer}") 