"""
Testskript für das künstliche Bewusstsein.

Dieses Skript demonstriert die Funktionalität des künstlichen Bewusstseins
mit verschiedenen Szenarien und Visualisierungen.
"""

from artificial_consciousness import ConsciousnessEngine
import matplotlib.pyplot as plt
import networkx as nx


def visualize_context_network(engine):
    """Visualisiert das Netzwerk von Kontexten als Graphen."""
    G = nx.Graph()
    
    # Füge Knoten hinzu
    for label, context in engine.contexts.items():
        G.add_node(label, happiness=context.happiness)
    
    # Füge Kanten hinzu
    for label, context in engine.contexts.items():
        for connected_context in context.connections:
            if connected_context.label:  # Nur benannte Kontexte hinzufügen
                G.add_edge(label, connected_context.label)
    
    # Erstelle Layout
    pos = nx.spring_layout(G, seed=42)
    
    # Zeichne Knoten mit Farben basierend auf Glückswerten
    node_colors = [engine.contexts[node].happiness for node in G.nodes()]
    
    # Erstelle eine Figur und Axes explizit
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Zeichne den Graphen auf die explizite Axes
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                          cmap=plt.cm.RdYlGn, node_size=500, alpha=0.8, ax=ax)
    nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.7, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold', ax=ax)
    
    # Füge Farbskala hinzu mit explizitem Axes-Kontext
    sm = plt.cm.ScalarMappable(cmap=plt.cm.RdYlGn, 
                              norm=plt.Normalize(vmin=-0.5, vmax=1.0))
    sm.set_array([])
    fig.colorbar(sm, ax=ax, label='Glückswert')
    
    ax.set_title('Kontext-Netzwerk mit Glückswerten')
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('context_network.png')
    plt.close()
    
    print("Netzwerkvisualisierung wurde als 'context_network.png' gespeichert.")


def track_happiness_over_time(engine, iterations=20):
    """Verfolgt den Glückswert über die Zeit während des Denkprozesses."""
    happiness_values = []
    path_history = []
    
    # Speichere den Ausgangszustand
    happiness_values.append(engine.calculate_path_happiness(engine.current_path))
    path_history.append([context.label for context in engine.current_path])
    
    # Führe den Denkprozess durch und verfolge die Werte
    for i in range(iterations):
        next_focus = engine.find_best_next_focus()
        if next_focus:
            engine.set_focus(next_focus)
        
        happiness_values.append(engine.calculate_path_happiness(engine.current_path))
        path_history.append([context.label for context in engine.current_path])
    
    # Visualisiere die Ergebnisse
    plt.figure(figsize=(12, 6))
    plt.plot(happiness_values, marker='o', linestyle='-', linewidth=2)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xlabel('Iteration')
    plt.ylabel('Gesamtglückswert')
    plt.title('Entwicklung des Glückswerts während des Denkprozesses')
    
    # Füge Beschriftungen für die Pfade hinzu
    for i, path in enumerate(path_history):
        plt.annotate(' → '.join(path), 
                    (i, happiness_values[i]),
                    textcoords="offset points",
                    xytext=(0, 10), 
                    ha='center',
                    fontsize=8,
                    rotation=45)
    
    plt.tight_layout()
    plt.savefig('happiness_over_time.png')
    plt.close()
    
    print("Glückswert-Entwicklung wurde als 'happiness_over_time.png' gespeichert.")
    
    return happiness_values, path_history


def create_custom_scenario():
    """Erstellt ein benutzerdefiniertes Szenario mit mehr Kontexten."""
    engine = ConsciousnessEngine()
    
    # Erstelle Kontexte für ein komplexeres Szenario
    c0 = engine.create_context("I want to be happy", "0", 0.5)
    cA = engine.create_context("I am happy when I achieve my goals", "A", 0.7)
    cB = engine.create_context("I achieve goals by working hard", "B", 0.4)
    cC = engine.create_context("I achieve goals by being smart", "C", 0.6)
    cD = engine.create_context("Working hard requires discipline", "D", 0.3)
    cE = engine.create_context("Being smart requires learning", "E", 0.5)
    cF = engine.create_context("Discipline is difficult", "F", -0.2)
    cG = engine.create_context("Learning is enjoyable", "G", 0.8)
    cH = engine.create_context("I enjoy reading books", "H", 0.7)
    cI = engine.create_context("I dislike physical exercise", "I", -0.3)
    cJ = engine.create_context("Books make me smarter", "J", 0.6)
    cK = engine.create_context("Exercise builds discipline", "K", 0.4)
    cL = engine.create_context("I read books every day", "L", 0.8)
    cM = engine.create_context("I exercise occasionally", "M", 0.1)
    
    # Verbinde die Kontexte
    engine.connect_contexts(c0, cA)
    engine.connect_contexts(cA, cB)
    engine.connect_contexts(cA, cC)
    engine.connect_contexts(cB, cD)
    engine.connect_contexts(cC, cE)
    engine.connect_contexts(cD, cF)
    engine.connect_contexts(cD, cK)
    engine.connect_contexts(cE, cG)
    engine.connect_contexts(cG, cH)
    engine.connect_contexts(cF, cI)
    engine.connect_contexts(cH, cJ)
    engine.connect_contexts(cI, cK)
    engine.connect_contexts(cH, cL)
    engine.connect_contexts(cK, cM)
    
    # Setze den initialen Fokus
    engine.set_focus(c0)
    
    return engine


def main():
    print("=== Test des künstlichen Bewusstseins ===\n")
    
    # Test mit dem Beispiel aus der Aufgabenstellung
    print("\n=== Beispiel aus der Aufgabenstellung ===")
    engine1 = ConsciousnessEngine()
    engine1.initialize_example()
    
    print("Initialer Zustand:")
    print(f"Fokus: {engine1.current_focus}")
    print(f"Pfad: {' -> '.join([str(c) for c in engine1.current_path])}")
    print(f"Aktuelles Glück: {engine1.calculate_path_happiness(engine1.current_path)}")
    
    print("\nDurchführung des Denkprozesses:")
    engine1.think(10)
    
    # Visualisiere das Netzwerk
    visualize_context_network(engine1)
    
    # Test mit einem benutzerdefinierten Szenario
    print("\n=== Benutzerdefiniertes Szenario ===")
    engine2 = create_custom_scenario()
    
    print("Initialer Zustand:")
    print(f"Fokus: {engine2.current_focus}")
    print(f"Pfad: {' -> '.join([str(c) for c in engine2.current_path])}")
    print(f"Aktuelles Glück: {engine2.calculate_path_happiness(engine2.current_path)}")
    
    # Verfolge die Entwicklung des Glückswerts
    print("\nVerfolgung der Glückswert-Entwicklung:")
    happiness_values, path_history = track_happiness_over_time(engine2, 15)
    
    # Visualisiere das Netzwerk des benutzerdefinierten Szenarios
    visualize_context_network(engine2)
    
    print("\n=== Test abgeschlossen ===")


if __name__ == "__main__":
    main() 