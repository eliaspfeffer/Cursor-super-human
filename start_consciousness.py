#!/usr/bin/env python3
"""
Startskript für das ewige künstliche Bewusstsein.

Dieses Skript startet das ewige künstliche Bewusstsein und bietet eine einfache
Benutzeroberfläche zur Interaktion mit dem Bewusstsein.
"""

import os
import sys
import time
import argparse
from eternal_consciousness import EternalConsciousnessEngine

def parse_arguments():
    """Parst die Kommandozeilenargumente."""
    parser = argparse.ArgumentParser(description="Starte das ewige künstliche Bewusstsein")
    
    parser.add_argument(
        "--save-interval", 
        type=int, 
        default=100, 
        help="Intervall für das Speichern des Zustands (in Iterationen)"
    )
    
    parser.add_argument(
        "--visualization-interval", 
        type=int, 
        default=500, 
        help="Intervall für die Visualisierung der Statistiken (in Iterationen)"
    )
    
    parser.add_argument(
        "--learning-interval", 
        type=int, 
        default=50, 
        help="Intervall für das Lernen aus dem Internet (in Iterationen)"
    )
    
    parser.add_argument(
        "--load-state", 
        type=str, 
        help="Pfad zu einer gespeicherten Zustandsdatei, die geladen werden soll"
    )
    
    parser.add_argument(
        "--no-example", 
        action="store_true", 
        help="Nicht mit Beispieldaten initialisieren, wenn kein Zustand geladen wird"
    )
    
    return parser.parse_args()

def main():
    """Hauptfunktion zum Starten des ewigen Bewusstseins."""
    args = parse_arguments()
    
    print("Starte ewiges künstliches Bewusstsein...")
    print("Drücke Ctrl+C zum Beenden.")
    
    # Erstelle das ewige Bewusstsein
    consciousness = EternalConsciousnessEngine(
        save_interval=args.save_interval,
        visualization_interval=args.visualization_interval,
        learning_interval=args.learning_interval
    )
    
    # Lade einen gespeicherten Zustand, falls angegeben
    if args.load_state:
        if os.path.exists(args.load_state):
            print(f"Lade Zustand aus: {args.load_state}")
            success = consciousness.load_state(args.load_state)
            if not success:
                print("Fehler beim Laden des Zustands.")
                if not args.no_example:
                    print("Initialisiere mit Beispieldaten...")
                    consciousness.initialize_example()
                    consciousness.initialize_example_environment()
        else:
            print(f"Zustandsdatei nicht gefunden: {args.load_state}")
            if not args.no_example:
                print("Initialisiere mit Beispieldaten...")
                consciousness.initialize_example()
                consciousness.initialize_example_environment()
    else:
        # Versuche, den neuesten Zustand zu laden
        latest_state = None
        if os.path.exists(consciousness.save_dir):
            state_files = [
                f for f in os.listdir(consciousness.save_dir) 
                if f.startswith("consciousness_state_") and f.endswith(".json")
            ]
            if state_files:
                # Sortiere nach Zeitstempel (neueste zuerst)
                state_files.sort(reverse=True)
                latest_state = os.path.join(consciousness.save_dir, state_files[0])
        
        if latest_state:
            print(f"Lade neuesten Zustand: {latest_state}")
            success = consciousness.load_state(latest_state)
            if not success and not args.no_example:
                print("Initialisiere mit Beispieldaten...")
                consciousness.initialize_example()
                consciousness.initialize_example_environment()
        elif not args.no_example:
            print("Kein gespeicherter Zustand gefunden. Initialisiere mit Beispieldaten...")
            consciousness.initialize_example()
            consciousness.initialize_example_environment()
    
    # Starte das ewige Bewusstsein
    try:
        consciousness.start()
    except KeyboardInterrupt:
        print("\nBeende das Bewusstsein...")
        consciousness.stop()
        print("Bewusstsein beendet.")

if __name__ == "__main__":
    main() 