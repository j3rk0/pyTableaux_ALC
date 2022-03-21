from lib.engine import CompletionGraph
import graphviz as gviz
from lib.formula import *


def plot_graph(G, show='all', shape='box'):
    dot = gviz.Digraph('tableaux', comment='Tableaux result', format='png')
    for i in range(G.last_individual + 1):

        if show == 'all':
            lc = '\n'.join([to_str(c) for c in G.L[i]])
            dot.node(f"x{i}", f"x{i}\n--------\n{lc}", shape=shape)
        elif show == 'atomic':
            lc = "; ".join([to_str(c) for c in G.L[i] if 'concept' in c.keys() or
                            ('neg' in c.keys() and 'concept' in c['neg'].keys())])
            dot.node(f"x{i}", f"x{i}:{{{lc}}}", shape=shape)
        else:
            dot.node(f"x{i}", shape=shape)

    for rel in G.E.keys():
        for rx, ry in G.E[rel]:
            dot.edge(f"x{rx}", f"x{ry}", label=rel)

    return dot


def man_to_list(formula_ms):  # parse a manchester syntax string in a list
    formula_ms = formula_ms.replace(' ', '')
    buffer = ''
    res = []
    i = 0
    key = ''
    while i < len(formula_ms):

        if formula_ms[i] == '(':  # unpack parhentesis
            level = 1
            count = 0
            while not level == 0 and count + i < len(formula_ms):
                count += 1
                if formula_ms[i + count] == '(':
                    level += 1
                elif formula_ms[i + count] == ')':
                    level -= 1
            assert level == 0 and 'ERROR: PARHENTESIS NOT MATCHING'
            res.append(man_to_list(formula_ms[i + 1:i + count]))
            buffer = ''
            i += count + 1
            continue

        buffer += formula_ms[i]
        i += 1

        if 'and' in buffer:
            key = 'and'
        elif 'not' in buffer:
            key = 'not'
        elif 'or' in buffer:
            key = 'or'
        elif 'some' in buffer:
            key = 'some'
        elif 'only' in buffer:
            key = 'only'

        if not key == '':
            res += buffer.split(key) + [key]
            buffer = ''
            key = ''

    res.append(buffer)

    return [t for t in res if not t == '']


def parse_manchester(formula_ms):  # parse manchester string to dict
    if type(formula_ms) == str:  # executes only on first call, parse the string to a list
        return parse_manchester(man_to_list(formula_ms))

    ret = None
    if len(formula_ms) == 1:
        if type(formula_ms[0]) == str:
            ret = {'concept': formula_ms[0]}
        elif type(formula_ms[0]) == list:
            ret = parse_manchester(formula_ms[0])
    elif 'and' in formula_ms:
        ret = {'and': []}
        i = j = 0
        while not j == len(formula_ms):
            if formula_ms[j] == 'and' and not i == j:
                ret['and'].append(parse_manchester(formula_ms[i:j]))
                i = j + 1
            j += 1
        ret['and'].append(parse_manchester(formula_ms[i:]))

    elif 'or' in formula_ms:
        ret = {'or': []}
        i = j = 0
        while not j == len(list):
            if formula_ms[j] == 'or' and not i == j:
                ret['or'].append(parse_manchester(formula_ms[i:j]))
                i = j + 1
            j += 1
        ret['or'].append(parse_manchester(formula_ms[i:]))
    elif formula_ms[0] == 'not':
        ret = {'neg': parse_manchester(formula_ms[1:])}
        pass
    elif formula_ms[1] == 'some':
        ret = {'exists': ({'relation': formula_ms[0]}, parse_manchester(formula_ms[2]))}
    elif formula_ms[1] == 'only':
        ret = {'forall': ({'relation': formula_ms[0]}, parse_manchester(formula_ms[2]))}
    else:
        print('PARSER ERROR')
        return None

    return ret
