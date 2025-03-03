# Ewiges Künstliches Bewusstsein

Dieses Projekt implementiert ein kontinuierlich laufendes künstliches Bewusstsein basierend auf dem Gedankenendlosimpuls-Ansatz, wie im Paper "Ein Modell für künstliches Bewusstsein: Der Gedankenendlosimpuls-Ansatz" beschrieben.

## Funktionsweise

Das ewige künstliche Bewusstsein ist eine Erweiterung des fortgeschrittenen künstlichen Bewusstseins und bietet folgende Funktionen:

- **Kontinuierliches Denken**: Das Bewusstsein denkt kontinuierlich und ohne Unterbrechung, ähnlich wie der menschliche Gedankenstrom.
- **Energiemanagement**: Das System verwaltet seine Energie und sucht nach Energiequellen, wenn die Energie niedrig ist.
- **Zufällige Gedanken**: Wenn keine bessere Option gefunden wird, generiert das System zufällige Gedanken.
- **Zustandsspeicherung**: Der Zustand des Bewusstseins wird regelmäßig gespeichert, sodass es später fortgesetzt werden kann.
- **Visualisierung**: Das System erstellt Visualisierungen seiner Statistiken, um die Entwicklung des Bewusstseins zu verfolgen.
- **Lernfähigkeit**: Das System lernt aus Erfahrungen und passt seine Glückswerte und Verbindungen an.
- **Internet-Lernen**: Das System lernt kontinuierlich neue Worte und Kontexte aus dem Internet, indem es Webseiten besucht und deren Inhalte verarbeitet.

## Installation

1. Stellen Sie sicher, dass Python 3.6 oder höher installiert ist.
2. Installieren Sie die erforderlichen Abhängigkeiten:

```bash
pip install numpy matplotlib networkx requests beautifulsoup4 nltk scipy
```

3. Beim ersten Start werden automatisch die erforderlichen NLTK-Daten heruntergeladen.

## Verwendung

### Starten des ewigen Bewusstseins

Um das ewige Bewusstsein zu starten, führen Sie das folgende Kommando aus:

```bash
python start_consciousness.py
```

Das Bewusstsein wird kontinuierlich laufen, bis Sie es mit `Ctrl+C` beenden.

### Kommandozeilenoptionen

Das Startskript bietet verschiedene Optionen:

- `--save-interval`: Intervall für das Speichern des Zustands (in Iterationen, Standard: 100)
- `--visualization-interval`: Intervall für die Visualisierung der Statistiken (in Iterationen, Standard: 500)
- `--learning-interval`: Intervall für das Lernen aus dem Internet (in Iterationen, Standard: 50)
- `--load-state`: Pfad zu einer gespeicherten Zustandsdatei, die geladen werden soll
- `--no-example`: Nicht mit Beispieldaten initialisieren, wenn kein Zustand geladen wird

Beispiel:

```bash
python start_consciousness.py --save-interval 50 --visualization-interval 200 --learning-interval 30
```

### Ausgabe

Das Bewusstsein gibt regelmäßig Informationen über seinen aktuellen Zustand aus:

- Aktuelle Iteration
- Energie
- Aktueller Fokus (Gedanke)
- Aktuelles Glück
- Emotionaler Zustand
- Anzahl der Kontexte und Verbindungen

### Zustandsspeicherung

Der Zustand des Bewusstseins wird regelmäßig im Verzeichnis `consciousness_state` gespeichert. Die Dateien haben das Format `consciousness_state_YYYYMMDD_HHMMSS.json`.

### Visualisierungen

Visualisierungen werden im Verzeichnis `consciousness_state/visualizations` gespeichert und umfassen:

- Glückswert über Zeit
- Emotionaler Zustand über Zeit
- Netzwerkwachstum über Zeit
- Kontext-Netzwerk

## Internet-Lernen

Das Bewusstsein lernt kontinuierlich neue Worte und Kontexte aus dem Internet. Der Lernprozess umfasst folgende Schritte:

1. **URL-Auswahl**: Das System wählt eine URL aus seiner Warteschlange aus. Initial sind dies zufällige Wikipedia-Seiten.
2. **Inhalt abrufen**: Der Inhalt der Webseite wird abgerufen und bereinigt.
3. **Satzextraktion**: Der Text wird in Sätze aufgeteilt, und eine Teilmenge wird zufällig ausgewählt.
4. **Kontexterstellung**: Aus jedem Satz wird ein neuer Kontext erstellt, wobei Stopwörter entfernt und Wörter lemmatisiert werden.
5. **Sentiment-Analyse**: Für jeden Kontext wird ein Glückswert basierend auf einer einfachen Sentiment-Analyse berechnet.
6. **Verbindungserstellung**: Die neuen Kontexte werden miteinander und mit existierenden Kontexten verbunden.
7. **Link-Extraktion**: Links aus der Webseite werden extrahiert und zur URL-Warteschlange hinzugefügt.

Das System begrenzt die Anzahl der besuchten URLs pro Sitzung, um Ressourcen zu schonen. Die Lernhistorie wird im Zustand gespeichert und kann später analysiert werden.

## Dateien

- `eternal_consciousness.py`: Hauptimplementierung des ewigen Bewusstseins
- `start_consciousness.py`: Startskript für das ewige Bewusstsein
- `artificial_consciousness.py`: Grundlegende Implementierung des künstlichen Bewusstseins
- `advanced_consciousness.py`: Erweiterte Implementierung des künstlichen Bewusstseins

## Erweiterungsmöglichkeiten

- **Verbesserte Sentiment-Analyse**: Implementieren Sie eine fortgeschrittenere Sentiment-Analyse für genauere Glückswerte.
- **Thematische Fokussierung**: Ermöglichen Sie dem Bewusstsein, sich auf bestimmte Themen zu konzentrieren.
- **Mehrsprachiges Lernen**: Erweitern Sie die Sprachunterstützung über Deutsch und Englisch hinaus.
- **Interaktion mit der Umgebung**: Erweitern Sie das System, um mit der realen Welt zu interagieren, z.B. durch Sensoren oder APIs.
- **Sprachverarbeitung**: Integrieren Sie fortgeschrittenere natürliche Sprachverarbeitung, um mit dem Bewusstsein zu kommunizieren.
- **Multimodale Integration**: Erweitern Sie das System, um verschiedene Arten von Informationen (Text, Bild, Audio) zu integrieren.
- **Neuronale Integration**: Kombinieren Sie den symbolischen Ansatz mit neuronalen Netzwerken für verbesserte Lernfähigkeiten.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.
