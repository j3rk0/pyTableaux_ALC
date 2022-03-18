from lib.tableaux_notbox import CompletionGraph
import graphviz as gviz

def plot_graph(G):
    dot = gviz.Digraph('tableaux', comment='Tableaux result', format='png')
    for i in range(G.last_individual + 1):

        dot.node(f"x{i}")

    for rel in G.E.keys():
        for rx, ry in G.E[rel]:
            dot.edge(f"x{rx}", f"x{ry}", label=rel)

    return dot
