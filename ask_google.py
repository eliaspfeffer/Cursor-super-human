#!/usr/bin/env python3
"""
Interaktion mit der Google-Suche.

Dieses Skript ermöglicht die Interaktion mit der Google-Suche durch
Texteingaben. Es stellt Fragen an Google und gibt die Antworten zurück.
"""

import argparse
import sys
from google_search import get_answer_for_question

def parse_arguments():
    """Parst die Kommandozeilenargumente."""
    parser = argparse.ArgumentParser(description="Stelle Fragen an Google")
    
    parser.add_argument(
        "--question", 
        type=str, 
        help="Die Frage, die gestellt werden soll. Wenn nicht angegeben, wird der interaktive Modus gestartet."
    )
    
    return parser.parse_args()

def interactive_mode():
    """Startet den interaktiven Modus, in dem Fragen gestellt werden können."""
    print("\n" + "="*80)
    print("GOOGLE-FRAGE-ASSISTENT")
    print("="*80)
    print("\nGib 'exit', 'quit' oder 'ende' ein, um die Interaktion zu beenden.")
    print("Du kannst jetzt Fragen stellen:")
    
    while True:
        try:
            user_input = input("\nDu: ").strip()
            
            if user_input.lower() in ["exit", "quit", "ende"]:
                break
            
            if not user_input:
                continue
            
            # Verarbeite die Frage
            print("Verarbeite Frage...")
            answer = get_answer_for_question(user_input)
            
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

def main():
    """Hauptfunktion."""
    args = parse_arguments()
    
    # Überprüfe, ob eine Frage als Argument übergeben wurde
    if args.question:
        # Verarbeite die Frage
        print(f"Frage: {args.question}")
        print("Verarbeite Frage...")
        answer = get_answer_for_question(args.question)
        
        # Gib die Antwort aus
        print(f"\nAntwort: {answer}")
    else:
        # Starte den interaktiven Modus
        interactive_mode()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Fehler: {e}")
        sys.exit(1)