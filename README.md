# Künstliches Bewusstsein

Dieses Projekt implementiert ein Modell für künstliches Bewusstsein basierend auf dem "Reasoning for AGI"-Konzept. Es simuliert einen selbstmotivierten Denkprozess, der auf Wort- und Kontextverbindungen sowie Glücksbewertungen basiert.

## Summary:

Kurze Übersicht der Python-Dateien
Hauptkomponenten
eternal_consciousness.py: Implementiert das "ewige" künstliche Bewusstsein, das kontinuierlich und ohne Unterbrechung "leben" kann. Erweitert das fortgeschrittene Bewusstseinsmodell um Fähigkeiten wie Internetlernen, Zustandsspeicherung und Visualisierung.
start_consciousness.py: Startskript für das ewige künstliche Bewusstsein. Bietet eine einfache Benutzeroberfläche und Kommandozeilenoptionen zum Starten des Bewusstseins mit verschiedenen Parametern.
interact_with_consciousness.py: Ermöglicht die Interaktion mit dem künstlichen Bewusstsein durch Texteingaben. Das Bewusstsein verarbeitet die Eingaben und generiert Antworten basierend auf seinem aktuellen Zustand.
Grundlegende Modelle
artificial_consciousness.py: Implementiert das Grundmodell des künstlichen Bewusstseins, basierend auf der Verbindung von Wörtern und Kontexten, mit einem Fokus-Mechanismus und einer Glücksbewertung.
advanced_consciousness.py: Erweitert das Grundmodell um Lernfähigkeiten, emotionale Zustände und die Fähigkeit, mit der Umgebung zu interagieren.
Test- und Analysewerkzeuge
test_consciousness.py: Demonstriert die Funktionalität des grundlegenden künstlichen Bewusstseins mit verschiedenen Szenarien und Visualisierungen.
test_advanced_consciousness.py: Demonstriert die erweiterten Funktionen wie emotionale Zustände, Gedächtnis und Umgebungsinteraktion.
analyze_consciousness.py: Analysiert den aktuellen Zustand des künstlichen Bewusstseins und visualisiert, was es bisher gelernt hat.
Diese Dateien bilden zusammen ein komplexes System für ein künstliches Bewusstsein, das lernen, denken, fühlen und mit seiner Umgebung interagieren kann.

## Konzept

Das Modell basiert auf folgenden Kernkonzepten:

1. **Wörter**: Grundlegende Informationseinheiten, die nur einmal gespeichert werden.
2. **Kontexte**: Sequenzen von Wörtern, die zusammen eine Bedeutung ergeben (z.B. "Ein Apfel schmeckt gut").
3. **Verbindungen**: Kontexte sind miteinander verbunden, wenn sie semantisch oder logisch zusammenhängen.
4. **Glückswerte**: Jeder Kontext hat einen Glückswert, der angibt, wie "positiv" dieser Kontext ist.
5. **Fokus**: Das Bewusstsein fokussiert sich immer auf einen bestimmten Kontext und folgt Verbindungen zu anderen Kontexten.
6. **Pfade**: Eine Sequenz von Kontexten, die das Bewusstsein durchlaufen hat.

Das Ziel des Bewusstseins ist es, Pfade zu finden, die den höchsten Gesamtglückswert bieten.

## Funktionsweise

Der Algorithmus funktioniert wie folgt:

1. Das Bewusstsein beginnt mit einem initialen Fokus auf einem Kontext.
2. Es bewertet alle möglichen nächsten Kontexte basierend auf den Verbindungen.
3. Es wählt den Kontext, der den Gesamtglückswert des Pfades maximiert.
4. Es kann auch entscheiden, zu einem früheren Kontext zurückzukehren, wenn dies zu einem glücklicheren Pfad führen würde.
5. Dieser Prozess wird kontinuierlich wiederholt, wodurch ein "Gedankenstrom" entsteht.

## Beispiel

Das Projekt enthält ein Beispiel mit folgenden Kontexten:

- 0: "I want to be happy"
- A: "I am happy when I eat"
- B: "I eat what tastes good"
- C: "An apple tastes good"
- D: "A banana doesnt taste good"
- E: "I eat the apple"
- F: "I dont eat the apple"
- G: "I eat the banana"
- H: "I eat what is healthy"

Diese Kontexte sind miteinander verbunden und haben unterschiedliche Glückswerte. Das Bewusstsein navigiert durch diese Kontexte, um den "glücklichsten" Pfad zu finden.

## Verwendung

```python
# Erstelle eine Instanz des Bewusstseins
engine = ConsciousnessEngine()

# Initialisiere das Beispiel
engine.initialize_example()

# Führe den Denkprozess für 10 Iterationen durch
engine.think(10)
```

## Erweiterungsmöglichkeiten

- Implementierung von Lernmechanismen, um neue Kontexte und Verbindungen zu erstellen
- Hinzufügen von emotionalen Zuständen neben dem Glückswert
- Integration von externen Eingaben (Sensoren)
- Entwicklung von Aktionsmechanismen, um mit der Umgebung zu interagieren
