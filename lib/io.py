from lib.engine import CompletionGraph
import graphviz as gviz
from lib.formula import *


def plot_graph(G, print='all', shape='box'):
    dot = gviz.Digraph('tableaux', comment='Tableaux result', format='png')
    for i in range(G.last_individual + 1):

        if print == 'all':
            lc = '\n'.join([to_str(c) for c in G.L[i]])
            dot.node(f"x{i}", f"x{i}\n--------\n{lc}", shape=shape)
        elif print == 'atomic':
            lc = "; ".join([to_str(c) for c in G.L[i] if 'concept' in c.keys() or
                            ('neg' in c.keys() and 'concept' in c['neg'].keys())])
            dot.node(f"x{i}", f"x{i}:{{{lc}}}", shape=shape)
        else:
            dot.node(f"x{i}", shape=shape)

    for rel in G.E.keys():
        for rx, ry in G.E[rel]:
            dot.edge(f"x{rx}", f"x{ry}", label=rel)

    return dot
