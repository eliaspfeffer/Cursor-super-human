#!/usr/bin/env python3
"""
Interaktive Visualisierung der Kontexte des künstlichen Bewusstseins als Baumstruktur.

Dieses Skript ermöglicht die Visualisierung und Navigation durch die Kontexte
des künstlichen Bewusstseins in einer interaktiven Baumstruktur.
"""

import os
import sys
import json
import argparse
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as mpatches
import numpy as np
from collections import defaultdict
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import random

def parse_arguments():
    """Parst die Kommandozeilenargumente."""
    parser = argparse.ArgumentParser(description="Visualisiere die Kontexte des künstlichen Bewusstseins als Baumstruktur")
    
    parser.add_argument(
        "--state-file", 
        type=str, 
        help="Pfad zur Zustandsdatei, die visualisiert werden soll. Wenn nicht angegeben, wird die neueste Datei verwendet."
    )
    
    parser.add_argument(
        "--max-depth", 
        type=int, 
        default=2, 
        help="Maximale Tiefe der Baumstruktur, die angezeigt werden soll"
    )
    
    parser.add_argument(
        "--node-size", 
        type=int, 
        default=2000, 
        help="Größe der Knoten im Graphen"
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

def get_context_text(context_data):
    """Extrahiert den Text aus einem Kontext."""
    if "text" in context_data:
        return context_data["text"]
    elif "words" in context_data:
        if isinstance(context_data["words"], list):
            return " ".join(context_data["words"])
        else:
            return str(context_data["words"])
    else:
        return "[Kein Text verfügbar]"

def get_context_happiness(context_data):
    """Extrahiert den Glückswert aus einem Kontext."""
    return context_data.get("happiness", 0.0)

def get_context_connections(context_data):
    """Extrahiert die Verbindungen aus einem Kontext."""
    return context_data.get("connections", [])

def find_most_connected_context(contexts):
    """Findet den Kontext mit den meisten Verbindungen."""
    if not contexts:
        return None
    
    # Zähle die Verbindungen für jeden Kontext
    connection_counts = {label: len(get_context_connections(data)) for label, data in contexts.items()}
    
    # Sortiere nach Anzahl der Verbindungen (absteigend)
    sorted_contexts = sorted(connection_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Debug-Ausgabe: Zeige die Top-5 Kontexte mit den meisten Verbindungen
    print("\nTop-5 Kontexte mit den meisten Verbindungen:")
    for i, (label, count) in enumerate(sorted_contexts[:5], 1):
        text = get_context_text(contexts[label])
        if len(text) > 30:
            text = text[:27] + "..."
        print(f"{i}. {label}: {count} Verbindungen - {text}")
    
    # Finde den Kontext mit den meisten Verbindungen
    for label, count in sorted_contexts:
        if count > 0:
            print(f"Verwende Kontext mit {count} Verbindungen als Wurzel: {label}")
            return label
    
    print("Kein Kontext mit Verbindungen gefunden.")
    return None

def identify_real_honeypots(contexts):
    """Identifiziert die ursprünglichen Honeypots basierend auf der Dokumentation."""
    # Definiere die drei Honeypot-Typen gemäß der Dokumentation
    honeypot_definitions = {
        'energy_intake': {
            'name': 'Energieaufnahme',
            'description': 'Grundbedürfnis für Nahrung, Trinken und Energieversorgung',
            'keywords': ['eat', 'food', 'drink', 'consume', 'nutrition', 'meal', 'hungry', 'thirsty']
        },
        'regeneration': {
            'name': 'Regeneration',
            'description': 'Grundbedürfnis für Ruhe, Schlaf und Erholung',
            'keywords': ['sleep', 'rest', 'relax', 'calm', 'peaceful', 'quiet', 'meditate', 'recover']
        },
        'reproduction': {
            'name': 'Reproduktion',
            'description': 'Grundbedürfnis für soziale Interaktion, Lernen und Wissensaustausch',
            'keywords': ['social', 'interact', 'communicate', 'share', 'connect', 'learn', 'teach', 'create']
        }
    }
    
    # Erstelle die Honeypot-Kontexte, falls sie noch nicht existieren
    honeypots = {
        'energy_intake': None,
        'regeneration': None,
        'reproduction': None
    }
    
    # Suche zuerst nach existierenden Honeypot-Kontexten
    for context_id, context in contexts.items():
        context_text = get_context_text(context).lower()
        
        # Prüfe, ob der Kontext bereits als Honeypot markiert ist
        if "is_honeypot" in context and context["is_honeypot"] and "honeypot_type" in context:
            honeypot_type = context["honeypot_type"]
            if honeypot_type in honeypots and honeypots[honeypot_type] is None:
                honeypots[honeypot_type] = context_id
    
    # Erstelle neue Honeypot-Kontexte für die fehlenden Typen
    for honeypot_type, honeypot_id in honeypots.items():
        if honeypot_id is None:
            # Erstelle einen neuen Kontext für diesen Honeypot-Typ
            honeypot_id = f"honeypot_{honeypot_type}"
            
            # Erstelle den Kontext, falls er noch nicht existiert
            if honeypot_id not in contexts:
                definition = honeypot_definitions[honeypot_type]
                honeypot_text = f"HONEYPOT: {definition['name']} - {definition['description']}"
                
                contexts[honeypot_id] = {
                    "text": honeypot_text,
                    "happiness": 1.0,  # Honeypots haben maximale Glücklichkeit
                    "connections": [],
                    "is_honeypot": True,
                    "honeypot_type": honeypot_type,
                    "is_original_honeypot": True  # Markiere als ursprünglichen Honeypot
                }
                
                print(f"Neuer Honeypot erstellt: {honeypot_id} - {honeypot_text}")
            else:
                # Markiere den existierenden Kontext als Honeypot
                contexts[honeypot_id]["is_honeypot"] = True
                contexts[honeypot_id]["honeypot_type"] = honeypot_type
                contexts[honeypot_id]["is_original_honeypot"] = True
            
            honeypots[honeypot_type] = honeypot_id
    
    # Verbinde die Honeypots mit relevanten Kontexten
    for honeypot_type, honeypot_id in honeypots.items():
        if "connections" not in contexts[honeypot_id]:
            contexts[honeypot_id]["connections"] = []
        
        # Suche nach relevanten Kontexten für diesen Honeypot-Typ
        keywords = honeypot_definitions[honeypot_type]["keywords"]
        relevant_contexts = []
        
        for context_id, context in contexts.items():
            if context_id == honeypot_id:
                continue
                
            context_text = get_context_text(context).lower()
            
            # Prüfe, ob der Kontext relevante Schlüsselwörter enthält
            for keyword in keywords:
                if keyword.lower() in context_text:
                    relevant_contexts.append(context_id)
                    break
        
        # Verbinde den Honeypot mit den relevanten Kontexten (maximal 10)
        for context_id in relevant_contexts[:10]:
            if context_id not in contexts[honeypot_id]["connections"]:
                contexts[honeypot_id]["connections"].append(context_id)
            
            # Erstelle auch die umgekehrte Verbindung
            if "connections" not in contexts[context_id]:
                contexts[context_id]["connections"] = []
                
            if honeypot_id not in contexts[context_id]["connections"]:
                contexts[context_id]["connections"].append(honeypot_id)
        
        print(f"Honeypot {honeypot_id} hat jetzt {len(contexts[honeypot_id].get('connections', []))} Verbindungen.")
    
    # Gib die Honeypot-IDs zurück
    return honeypots

def calculate_resistance_to_honeypots(contexts, honeypots, graph_nodes=None):
    """Berechnet den Widerstand (Distanz) zu den nächsten Honeypots."""
    # Erstelle einen Graphen aus den Kontexten
    G = nx.Graph()
    
    # Wenn graph_nodes angegeben ist, berechne nur für diese Knoten den Widerstand
    nodes_to_process = graph_nodes if graph_nodes else contexts.keys()
    
    # Füge alle Knoten hinzu
    for context_id in contexts:
        G.add_node(context_id)
    
    # Füge alle Kanten hinzu
    for context_id, context in contexts.items():
        connections = get_context_connections(context)
        for target_id in connections:
            if target_id in contexts:
                G.add_edge(context_id, target_id)
    
    # Berechne für jeden Kontext den Widerstand zum nächsten Honeypot
    all_honeypot_ids = []
    for honeypot_list in honeypots.values():
        all_honeypot_ids.extend(honeypot_list)
    
    for context_id in nodes_to_process:
        if context_id not in contexts:
            continue
            
        min_distance = float('inf')
        nearest_honeypot_type = None
        
        # Überspringe, wenn der Kontext selbst ein Honeypot ist
        if context_id in all_honeypot_ids:
            contexts[context_id]['resistance'] = 0
            continue
        
        # Berechne die kürzeste Distanz zu jedem Honeypot-Typ
        for honeypot_type, honeypot_list in honeypots.items():
            for honeypot_id in honeypot_list:
                try:
                    distance = nx.shortest_path_length(G, context_id, honeypot_id)
                    if distance < min_distance:
                        min_distance = distance
                        nearest_honeypot_type = honeypot_type
                except (nx.NetworkXNoPath, nx.NodeNotFound):
                    continue
        
        # Speichere den Widerstand und den nächsten Honeypot-Typ
        if min_distance != float('inf'):
            contexts[context_id]['resistance'] = min_distance
            contexts[context_id]['nearest_honeypot'] = nearest_honeypot_type
        else:
            contexts[context_id]['resistance'] = -1  # Kein Pfad gefunden
            contexts[context_id]['nearest_honeypot'] = None
    
    return contexts

def create_connections_for_visualization(contexts, num_connections=50):
    """Erstellt Verbindungen zwischen ähnlichen Kontexten für die Visualisierung."""
    print(f"Erstelle {num_connections} Verbindungen für die Visualisierung...")
    
    # Wähle zufällige Kontexte aus
    context_labels = list(contexts.keys())
    if len(context_labels) < 100:
        sample_size = len(context_labels)
    else:
        sample_size = min(500, len(context_labels))
    
    sample_labels = random.sample(context_labels, sample_size)
    
    # Erstelle Verbindungen
    connections_created = 0
    for i in range(num_connections):
        if connections_created >= num_connections:
            break
            
        # Wähle zwei zufällige Kontexte
        source = random.choice(sample_labels)
        target = random.choice(sample_labels)
        
        # Stelle sicher, dass es sich um verschiedene Kontexte handelt
        if source == target:
            continue
            
        # Prüfe, ob die Verbindung bereits existiert
        if "connections" not in contexts[source]:
            contexts[source]["connections"] = []
            
        if target not in contexts[source]["connections"]:
            contexts[source]["connections"].append(target)
            connections_created += 1
            
            # Erstelle auch die umgekehrte Verbindung
            if "connections" not in contexts[target]:
                contexts[target]["connections"] = []
                
            if source not in contexts[target]["connections"]:
                contexts[target]["connections"].append(source)
    
    # Identifiziere echte Honeypots basierend auf den grundlegenden Bedürfnissen
    honeypots = identify_real_honeypots(contexts)
    
    # Berechne den Widerstand zu den Honeypots
    contexts = calculate_resistance_to_honeypots(contexts, honeypots)
    
    # Wähle einen stark verbundenen Kontext als Startpunkt
    most_connected_label = find_most_connected_context(contexts)
    if most_connected_label is None and sample_labels:
        most_connected_label = sample_labels[0]
    
    return most_connected_label, honeypots

def get_context_type(label):
    """Bestimmt den Typ eines Kontexts anhand seines Labels."""
    if label.startswith("Web_"):
        return "Web"
    elif label.startswith("Random_"):
        return "Random"
    elif label.startswith("Energy_"):
        return "Energy"
    elif label.startswith("Obj_"):
        return "Object"
    elif label.startswith("UserInput_"):
        return "UserInput"
    elif label.startswith("Response_"):
        return "Response"
    else:
        return "Other"

class ContextTreeVisualizer:
    """Klasse zur Visualisierung der Kontexte als Baumstruktur."""
    
    def __init__(self, state, max_depth=2, node_size=2000, font_size=36):
        self.state = state
        self.max_depth = max_depth
        self.node_size = node_size
        self.font_size = font_size
        self.contexts = state.get("contexts", {})
        self.current_focus = state.get("current_focus", None)
        self.history = []
        self.G = nx.Graph()
        self.pos = {}
        self.node_colors = []
        self.node_labels = {}
        self.node_sizes = []
        self.edge_colors = []
        self.node_to_index = {}
        self.index_to_node = {}
        self.honeypots = {}
        
        # Erstelle die GUI
        self.create_gui()
        
        # Initialisiere den Graphen
        self.initialize_graph()
    
    def create_gui(self):
        """Erstellt die GUI."""
        self.root = tk.Tk()
        self.root.title("Kontext-Baum Visualisierung")
        self.root.geometry("1200x800")
        
        # Erstelle den Hauptframe
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Erstelle den linken Frame für die Steuerelemente
        control_frame = tk.Frame(main_frame, width=300)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Erstelle den rechten Frame für den Graphen und die Details
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Erstelle den oberen Frame für den Graphen
        graph_frame = tk.Frame(right_frame)
        graph_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Erstelle den unteren Frame für die Details
        details_frame = tk.Frame(right_frame, height=200)
        details_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        # Erstelle die Matplotlib-Figur
        self.fig = plt.figure(figsize=(8, 6))
        self.ax = self.fig.add_subplot(111)
        
        # Erstelle das Canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Erstelle die Toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, graph_frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Verbinde das Klick-Event
        self.canvas.mpl_connect("button_press_event", self.on_click)
        
        # Erstelle die Steuerelemente
        tk.Label(control_frame, text="Steuerelemente", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Zurück-Button
        self.back_button = tk.Button(control_frame, text="Zurück", command=self.go_back)
        self.back_button.pack(fill=tk.X, pady=5)
        self.back_button["state"] = "disabled"  # Anfangs deaktiviert
        
        # Tiefe-Steuerung
        depth_frame = tk.Frame(control_frame)
        depth_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(depth_frame, text="Max. Tiefe:").pack(side=tk.LEFT)
        self.depth_var = tk.StringVar(value=str(self.max_depth))
        depth_entry = tk.Entry(depth_frame, textvariable=self.depth_var, width=5)
        depth_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(depth_frame, text="Aktualisieren", command=self.update_depth).pack(side=tk.LEFT)
        
        # Knotengröße-Steuerung
        size_frame = tk.Frame(control_frame)
        size_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(size_frame, text="Knotengröße:").pack(side=tk.LEFT)
        self.size_var = tk.StringVar(value=str(self.node_size))
        size_entry = tk.Entry(size_frame, textvariable=self.size_var, width=5)
        size_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(size_frame, text="Aktualisieren", command=self.update_node_size).pack(side=tk.LEFT)
        
        # Textgröße-Steuerung
        font_frame = tk.Frame(control_frame)
        font_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(font_frame, text="Textgröße:").pack(side=tk.LEFT)
        self.font_var = tk.StringVar(value=str(self.font_size))
        font_entry = tk.Entry(font_frame, textvariable=self.font_var, width=5)
        font_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(font_frame, text="Aktualisieren", command=self.update_font_size).pack(side=tk.LEFT)
        
        # Suche
        search_frame = tk.Frame(control_frame)
        search_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(search_frame, text="Suche:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        tk.Button(search_frame, text="Suchen", command=self.search_context).pack(side=tk.LEFT)
        
        # Filter
        filter_frame = tk.Frame(control_frame)
        filter_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(filter_frame, text="Filter:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        # Checkbox für Web-Kontexte
        self.show_web = tk.BooleanVar(value=True)
        tk.Checkbutton(filter_frame, text="Web (blau)", variable=self.show_web, command=self.update_filter).pack(anchor=tk.W)
        
        # Checkbox für zufällige Kontexte
        self.show_random = tk.BooleanVar(value=True)
        tk.Checkbutton(filter_frame, text="Random (grün)", variable=self.show_random, command=self.update_filter).pack(anchor=tk.W)
        
        # Checkbox für Energie-Kontexte
        self.show_energy = tk.BooleanVar(value=True)
        tk.Checkbutton(filter_frame, text="Energy (rot)", variable=self.show_energy, command=self.update_filter).pack(anchor=tk.W)
        
        # Checkbox für Objekt-Kontexte
        self.show_object = tk.BooleanVar(value=True)
        tk.Checkbutton(filter_frame, text="Object (lila)", variable=self.show_object, command=self.update_filter).pack(anchor=tk.W)
        
        # Checkbox für Benutzereingabe-Kontexte
        self.show_userinput = tk.BooleanVar(value=True)
        tk.Checkbutton(filter_frame, text="UserInput (orange)", variable=self.show_userinput, command=self.update_filter).pack(anchor=tk.W)
        
        # Checkbox für Antwort-Kontexte
        self.show_response = tk.BooleanVar(value=True)
        tk.Checkbutton(filter_frame, text="Response (cyan)", variable=self.show_response, command=self.update_filter).pack(anchor=tk.W)
        
        # Checkbox für sonstige Kontexte
        self.show_other = tk.BooleanVar(value=True)
        tk.Checkbutton(filter_frame, text="Andere (grau)", variable=self.show_other, command=self.update_filter).pack(anchor=tk.W)
        
        # Checkbox für Honeypots
        self.show_honeypots = tk.BooleanVar(value=True)
        tk.Checkbutton(filter_frame, text="Honeypots (gold/dunkel)", variable=self.show_honeypots, command=self.update_filter).pack(anchor=tk.W)
        
        # Erstelle das Textfeld für die Details
        tk.Label(details_frame, text="Kontext-Details", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        self.details_text = tk.Text(details_frame, wrap=tk.WORD, height=10)
        self.details_text.pack(fill=tk.BOTH, expand=True)
        self.details_text.config(state=tk.DISABLED)
        
        # Erstelle die Statusleiste
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Setze den initialen Status
        self.update_status("Bereit")
    
    def initialize_graph(self):
        """Initialisiert den Graphen."""
        # Erstelle Verbindungen für die Visualisierung
        most_connected_label, self.honeypots = create_connections_for_visualization(self.contexts)
        
        # Setze den Wurzelknoten
        # Priorisiere Honeypots als Startpunkt
        honeypot_values = list(self.honeypots.values())
        if honeypot_values and honeypot_values[0] in self.contexts:
            self.set_root(honeypot_values[0])
        elif self.current_focus and self.current_focus in self.contexts:
            self.set_root(self.current_focus)
        elif most_connected_label:
            self.set_root(most_connected_label)
        else:
            messagebox.showinfo("Information", "Keine Kontexte gefunden.")
    
    def set_root(self, root_label):
        """Setzt den Wurzelknoten des Graphen."""
        if root_label not in self.contexts:
            messagebox.showerror("Fehler", f"Kontext {root_label} nicht gefunden.")
            return
        
        # Füge den aktuellen Wurzelknoten zur Historie hinzu, wenn es einen gibt
        if self.current_focus and self.current_focus != root_label:
            self.history.append(self.current_focus)
            if hasattr(self, 'back_button'):
                self.back_button["state"] = "normal"
            print(f"Füge {self.current_focus} zur Historie hinzu. Historienlänge: {len(self.history)}")
        
        # Setze den neuen Wurzelknoten
        self.current_focus = root_label
        
        # Aktualisiere den Graphen
        self.update_graph()
        
        # Zeige Details des Wurzelknotens an
        self.show_context_details(root_label)
        
        # Aktualisiere den Status
        self.update_status(f"Wurzel gesetzt: {root_label}")
    
    def update_graph(self):
        """Aktualisiert den Graphen basierend auf dem aktuellen Wurzelknoten."""
        if not self.current_focus:
            return
        
        # Lösche den alten Graphen
        self.G.clear()
        self.ax.clear()
        
        # Erstelle einen neuen Graphen
        self.build_graph(self.current_focus, self.max_depth)
        
        # Zeichne den Graphen
        self.draw_graph()
    
    def build_graph(self, root_label, max_depth, current_depth=0):
        """Baut den Graphen rekursiv auf."""
        if current_depth > max_depth or root_label not in self.contexts:
            return
        
        # Füge den Wurzelknoten hinzu, falls er noch nicht existiert
        if not self.G.has_node(root_label):
            self.G.add_node(root_label)
        
        # Hole die Verbindungen des Wurzelknotens
        connections = get_context_connections(self.contexts[root_label])
        
        # Filtere die Verbindungen basierend auf den Anzeigeeinstellungen
        filtered_connections = []
        for conn in connections:
            if conn in self.contexts:
                node_type = get_context_type(conn)
                if (node_type == "Web" and self.show_web.get() or
                    node_type == "Random" and self.show_random.get() or
                    node_type == "Energy" and self.show_energy.get() or
                    node_type == "Object" and self.show_object.get() or
                    node_type == "UserInput" and self.show_userinput.get() or
                    node_type == "Response" and self.show_response.get() or
                    node_type == "Other" and self.show_other.get()):
                    filtered_connections.append(conn)
        
        # Füge die Verbindungen hinzu
        for conn in filtered_connections:
            if not self.G.has_node(conn):
                self.G.add_node(conn)
            
            if not self.G.has_edge(root_label, conn):
                self.G.add_edge(root_label, conn)
            
            # Rekursiv für die Verbindungen
            if current_depth < max_depth:
                self.build_graph(conn, max_depth, current_depth + 1)
        
        # Berechne den Widerstand zu den Honeypots für die Knoten im aktuellen Graphen
        if current_depth == 0:  # Nur einmal am Ende der Rekursion
            self.contexts = calculate_resistance_to_honeypots(self.contexts, self.honeypots, self.G.nodes())
    
    def draw_graph(self):
        """Zeichnet den Graphen."""
        if not self.G.nodes():
            messagebox.showinfo("Information", "Keine Knoten im Graphen.")
            return
        
        # Lösche vorherige Inhalte
        self.ax.clear()
        
        # Berechne das Layout
        self.pos = nx.spring_layout(self.G, seed=42)
        
        # Bereite die Knotenfarben vor
        self.node_colors = []
        self.node_labels = {}
        self.node_sizes = []
        self.edge_colors = []
        self.node_to_index = {}
        self.index_to_node = {}
        
        for i, node in enumerate(self.G.nodes()):
            # Speichere die Zuordnung von Knoten zu Index
            self.node_to_index[node] = i
            self.index_to_node[i] = node
            
            # Bestimme die Farbe basierend auf dem Typ und Honeypot-Status
            if "is_honeypot" in self.contexts[node] and self.contexts[node]["is_honeypot"]:
                # Prüfe, ob es sich um einen ursprünglichen Honeypot handelt
                is_original = self.contexts[node].get("is_original_honeypot", False)
                
                honeypot_type = self.contexts[node].get("honeypot_type", "unknown")
                if honeypot_type == "energy_intake":
                    color = "darkred" if is_original else "red"
                elif honeypot_type == "regeneration":
                    color = "darkblue" if is_original else "blue"
                elif honeypot_type == "reproduction":
                    color = "darkgreen" if is_original else "green"
                else:
                    color = "gold"
            else:
                node_type = get_context_type(node)
                if node_type == "Web":
                    color = "lightblue"
                elif node_type == "Random":
                    color = "lightgreen"
                elif node_type == "Energy":
                    color = "pink"
                elif node_type == "Object":
                    color = "purple"
                elif node_type == "UserInput":
                    color = "orange"
                elif node_type == "Response":
                    color = "cyan"
                else:
                    color = "gray"
            
            self.node_colors.append(color)
            
            # Bestimme die Größe basierend auf dem Glückswert
            happiness = get_context_happiness(self.contexts[node])
            size = self.node_size * (0.5 + abs(happiness))
            
            # Vergrößere Honeypots
            if "is_honeypot" in self.contexts[node] and self.contexts[node]["is_honeypot"]:
                # Ursprüngliche Honeypots sind noch größer
                if self.contexts[node].get("is_original_honeypot", False):
                    size *= 2.0
                else:
                    size *= 1.5
                
            self.node_sizes.append(size)
            
            # Erstelle das Label
            text = get_context_text(self.contexts[node])
            if "is_honeypot" in self.contexts[node] and self.contexts[node]["is_honeypot"]:
                honeypot_type = self.contexts[node].get("honeypot_type", "unknown")
                if self.contexts[node].get("is_original_honeypot", False):
                    text = f"URSPRUNGS-HONEYPOT ({honeypot_type})"
                else:
                    text = f"Honeypot ({honeypot_type}): " + text
            
            if len(text) > 20:
                text = text[:17] + "..."
            self.node_labels[node] = text
        
        # Bereite die Kantenfarben vor
        for u, v in self.G.edges():
            # Bestimme die Farbe basierend auf der Beziehung und dem Widerstand
            if "is_honeypot" in self.contexts[u] and self.contexts[u]["is_honeypot"] or \
               "is_honeypot" in self.contexts[v] and self.contexts[v]["is_honeypot"]:
                color = "gold"  # Goldene Kanten zu Honeypots
            elif "UserInput" in u and "Response" in v or "Response" in u and "UserInput" in v:
                color = "red"
            else:
                # Färbe basierend auf dem Widerstand zum nächsten Honeypot
                resistance_u = self.contexts[u].get('resistance', -1)
                resistance_v = self.contexts[v].get('resistance', -1)
                
                if resistance_u >= 0 and resistance_v >= 0:
                    # Berechne den durchschnittlichen Widerstand
                    avg_resistance = (resistance_u + resistance_v) / 2
                    # Farbverlauf von Grün (niedrig) über Gelb zu Rot (hoch)
                    if avg_resistance <= 1:
                        color = "limegreen"
                    elif avg_resistance <= 2:
                        color = "yellowgreen"
                    elif avg_resistance <= 3:
                        color = "yellow"
                    elif avg_resistance <= 4:
                        color = "orange"
                    else:
                        color = "red"
                else:
                    color = "gray"
            
            self.edge_colors.append(color)
        
        # Zeichne den Graphen
        nx.draw_networkx_nodes(
            self.G, self.pos,
            node_color=self.node_colors,
            node_size=self.node_sizes,
            alpha=0.8
        )
        
        nx.draw_networkx_edges(
            self.G, self.pos,
            edge_color=self.edge_colors,
            width=1.0,
            alpha=0.5
        )
        
        nx.draw_networkx_labels(
            self.G, self.pos,
            labels=self.node_labels,
            font_size=self.font_size,
            font_family='sans-serif'
        )
        
        # Markiere den Wurzelknoten
        if self.current_focus in self.pos:
            self.ax.plot(
                self.pos[self.current_focus][0],
                self.pos[self.current_focus][1],
                'o',
                markersize=20,
                markerfacecolor='none',
                markeredgecolor='black',
                markeredgewidth=2
            )
        
        # Erstelle eine Legende für die Honeypot-Typen und Widerstandswerte
        legend_elements = [
            # Honeypot-Typen
            mpatches.Patch(color='darkred', label='Ursprungs-Honeypot: Energieaufnahme'),
            mpatches.Patch(color='darkblue', label='Ursprungs-Honeypot: Regeneration'),
            mpatches.Patch(color='darkgreen', label='Ursprungs-Honeypot: Reproduktion'),
            
            # Widerstandswerte (Kanten)
            mpatches.Patch(color='limegreen', label='Widerstand: 0-1'),
            mpatches.Patch(color='yellowgreen', label='Widerstand: 1-2'),
            mpatches.Patch(color='yellow', label='Widerstand: 2-3'),
            mpatches.Patch(color='orange', label='Widerstand: 3-4'),
            mpatches.Patch(color='red', label='Widerstand: >4'),
            mpatches.Patch(color='gold', label='Verbindung zu Honeypot')
        ]
        
        # Füge die Legende hinzu
        self.ax.legend(handles=legend_elements, loc='lower right', fontsize='x-small', framealpha=0.7)
        
        # Setze die Achsenbeschriftungen
        self.ax.set_title(f"Kontext-Baum (Wurzel: {self.current_focus})")
        self.ax.axis('off')
        
        # Aktualisiere das Canvas
        self.canvas.draw()
    
    def on_click(self, event):
        """Behandelt Mausklick-Events auf dem Canvas."""
        # Ignoriere Klicks außerhalb der Achsen oder wenn der Zoom/Pan-Modus aktiv ist
        if event.inaxes != self.ax or self.toolbar.mode != '':
            return
            
        # Ignoriere Klicks mit der rechten Maustaste (für Pan-Funktion reserviert)
        if event.button != 1:
            return
        
        if event.xdata is None or event.ydata is None:
            return
        
        # Finde den nächsten Knoten zum Klickpunkt
        min_dist = float('inf')
        closest_node = None
        
        for node, pos in self.pos.items():
            dist = np.sqrt((pos[0] - event.xdata)**2 + (pos[1] - event.ydata)**2)
            if dist < min_dist:
                min_dist = dist
                closest_node = node
        
        # Wenn der Klick nahe genug an einem Knoten ist
        if min_dist < 0.1 and closest_node:
            # Zeige Details des Knotens an
            self.show_context_details(closest_node)
            
            # Wenn der Knoten nicht der aktuelle Wurzelknoten ist, biete an, ihn als Wurzel zu setzen
            if closest_node != self.current_focus:
                if messagebox.askyesno("Wurzel ändern", f"Möchten Sie '{closest_node}' als neue Wurzel setzen?"):
                    self.set_root(closest_node)
    
    def show_context_details(self, label):
        """Zeigt Details eines Kontexts an."""
        if label not in self.contexts:
            return
        
        context = self.contexts[label]
        text = get_context_text(context)
        happiness = get_context_happiness(context)
        connections = get_context_connections(context)
        
        # Formatiere die Details
        details = f"Label: {label}\n\n"
        
        # Zeige Honeypot-Informationen an
        if "is_honeypot" in context and context["is_honeypot"]:
            honeypot_type = context.get("honeypot_type", "unknown")
            details += f"HONEYPOT TYP: {honeypot_type}\n\n"
        
        details += f"Text: {text}\n\n"
        details += f"Glückswert: {happiness:.4f}\n\n"
        
        # Zeige Widerstand zum nächsten Honeypot an
        resistance = context.get('resistance', -1)
        if resistance >= 0:
            nearest_honeypot = context.get('nearest_honeypot', 'unbekannt')
            details += f"Widerstand zum nächsten Honeypot ({nearest_honeypot}): {resistance}\n\n"
        else:
            details += f"Kein Pfad zu einem Honeypot gefunden.\n\n"
        
        details += f"Verbindungen ({len(connections)}):\n"
        
        # Filtere die Verbindungen basierend auf den Anzeigeeinstellungen
        filtered_connections = []
        for conn in connections:
            if conn in self.contexts:
                node_type = get_context_type(conn)
                if (node_type == "Web" and self.show_web.get() or
                    node_type == "Random" and self.show_random.get() or
                    node_type == "Energy" and self.show_energy.get() or
                    node_type == "Object" and self.show_object.get() or
                    node_type == "UserInput" and self.show_userinput.get() or
                    node_type == "Response" and self.show_response.get() or
                    node_type == "Other" and self.show_other.get()):
                    filtered_connections.append(conn)
        
        # Zeige die gefilterten Verbindungen an
        for i, conn in enumerate(filtered_connections[:10]):
            conn_text = get_context_text(self.contexts[conn])
            
            # Zeige Honeypot-Status und Widerstand in den Verbindungen an
            is_honeypot = "is_honeypot" in self.contexts[conn] and self.contexts[conn]["is_honeypot"]
            resistance = self.contexts[conn].get('resistance', -1)
            
            if is_honeypot:
                honeypot_type = self.contexts[conn].get("honeypot_type", "unknown")
                conn_text = f"[HONEYPOT: {honeypot_type}] " + conn_text
            
            if len(conn_text) > 30:
                conn_text = conn_text[:27] + "..."
                
            if resistance >= 0:
                details += f"  {i+1}. {conn}: {conn_text} (Widerstand: {resistance})\n"
            else:
                details += f"  {i+1}. {conn}: {conn_text}\n"
        
        if len(filtered_connections) > 10:
            details += f"  ... und {len(filtered_connections) - 10} weitere\n"
        
        # Aktualisiere das Textfeld
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, details)
        self.details_text.config(state=tk.DISABLED)
    
    def go_back(self):
        """Geht zurück zum vorherigen Wurzelknoten."""
        if not self.history:
            messagebox.showinfo("Information", "Keine vorherigen Knoten in der Historie.")
            return
        
        # Hole den letzten Wurzelknoten aus der Historie
        previous_root = self.history.pop()
        print(f"Gehe zurück zu {previous_root}. Verbleibende Historie: {len(self.history)}")
        
        # Wenn die Historie leer ist, deaktiviere den Zurück-Button
        if not self.history:
            self.back_button["state"] = "disabled"
        
        # Setze den vorherigen Wurzelknoten als aktuellen Wurzelknoten
        self.current_focus = previous_root
        
        # Aktualisiere den Graphen
        self.update_graph()
        
        # Zeige Details des Wurzelknotens an
        self.show_context_details(previous_root)
        
        # Aktualisiere den Status
        self.update_status(f"Zurück zu: {previous_root}")
    
    def update_depth(self):
        """Aktualisiert die maximale Tiefe des Baums."""
        try:
            new_depth = self.depth_var.get()
            if 1 <= new_depth <= 5:
                self.max_depth = new_depth
                self.update_graph()
                self.update_status(f"Maximale Tiefe auf {new_depth} gesetzt")
            else:
                messagebox.showerror("Fehler", "Die Tiefe muss zwischen 1 und 5 liegen.")
        except:
            messagebox.showerror("Fehler", "Ungültige Tiefe.")
    
    def update_node_size(self):
        """Aktualisiert die Größe der Knoten."""
        try:
            new_size = self.size_var.get()
            if 1000 <= new_size <= 5000:
                self.node_size = new_size
                self.update_graph()
                self.update_status(f"Knotengröße auf {new_size} gesetzt")
            else:
                messagebox.showerror("Fehler", "Die Knotengröße muss zwischen 1000 und 5000 liegen.")
        except:
            messagebox.showerror("Fehler", "Ungültige Knotengröße.")
    
    def update_font_size(self):
        """Aktualisiert die Textgröße."""
        try:
            new_font_size = self.font_var.get()
            if 8 <= new_font_size <= 72:
                self.font_size = new_font_size
                self.update_graph()
                self.update_status(f"Textgröße auf {new_font_size} gesetzt")
            else:
                messagebox.showerror("Fehler", "Die Textgröße muss zwischen 8 und 72 liegen.")
        except:
            messagebox.showerror("Fehler", "Ungültige Textgröße.")
    
    def search_context(self):
        """Sucht nach einem Kontext basierend auf dem Text."""
        search_text = self.search_var.get().lower()
        if not search_text:
            messagebox.showinfo("Information", "Bitte geben Sie einen Suchtext ein.")
            return
        
        # Suche nach Kontexten, die den Suchtext enthalten
        found_contexts = []
        for label, context in self.contexts.items():
            text = get_context_text(context).lower()
            if search_text in text:
                found_contexts.append((label, text))
        
        if not found_contexts:
            messagebox.showinfo("Information", f"Keine Kontexte mit '{search_text}' gefunden.")
            return
        
        # Erstelle ein Popup-Fenster mit den gefundenen Kontexten
        search_window = tk.Toplevel(self.root)
        search_window.title(f"Suchergebnisse für '{search_text}'")
        search_window.geometry("600x400")
        
        # Erstelle ein Listbox-Widget
        listbox_frame = ttk.Frame(search_window)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        listbox_label = ttk.Label(listbox_frame, text=f"Gefundene Kontexte ({len(found_contexts)}):")
        listbox_label.pack(anchor=tk.W)
        
        listbox = tk.Listbox(listbox_frame, width=80, height=20)
        listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=listbox.yview)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        listbox.config(yscrollcommand=scrollbar.set)
        
        # Fülle die Listbox mit den gefundenen Kontexten
        for i, (label, text) in enumerate(found_contexts):
            if len(text) > 50:
                text = text[:47] + "..."
            listbox.insert(tk.END, f"{label}: {text}")
        
        # Erstelle Buttons
        button_frame = ttk.Frame(search_window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def on_select():
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                label = found_contexts[index][0]
                search_window.destroy()
                self.set_root(label)
        
        select_button = ttk.Button(button_frame, text="Als Wurzel setzen", command=on_select)
        select_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = ttk.Button(button_frame, text="Abbrechen", command=search_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)
    
    def update_status(self, message):
        """Aktualisiert die Statusleiste."""
        self.status_var.set(message)
    
    def update_filter(self):
        """Aktualisiert den Filter."""
        # Aktualisiere den Graphen
        self.update_graph()
        
        # Aktualisiere die Detailansicht, falls ein Kontext ausgewählt ist
        if hasattr(self, 'current_focus') and self.current_focus:
            self.show_context_details(self.current_focus)
        
        self.update_status("Filter aktualisiert")
    
    def run(self):
        """Startet die Anwendung."""
        self.root.mainloop()

def main():
    """Hauptfunktion."""
    args = parse_arguments()
    
    # Lade den Zustand
    state = load_state(args.state_file)
    if not state:
        print("Fehler beim Laden des Zustands.")
        return
    
    # Erstelle den Visualisierer
    visualizer = ContextTreeVisualizer(state, args.max_depth, args.node_size)
    
    # Starte die Anwendung
    visualizer.run()

if __name__ == "__main__":
    main() 