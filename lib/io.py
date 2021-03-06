import graphviz as gviz
import re
from rdflib import Graph, URIRef, RDFS


class InputManager:

    def man_to_list(self, formula_ms):  # parse a manchester syntax string in a list

        # FORCE OPERATOR TO BE SYMBOL TO PREVENT MISMATCH WITH VARIABLES CONTAINING OPERATOR STRING
        formula_ms = re.sub(r"(?<=[)\s])and(?=[(\s])", '&', formula_ms)
        formula_ms = re.sub(r"(?<=[)\s])or(?=[(\s])", '|', formula_ms)
        formula_ms = re.sub(r"(?<=[)\s])Not(?=[(\s])", '-', formula_ms)
        formula_ms = re.sub(r"(?<=[)\s])some(?=[(\s])", '%', formula_ms)
        formula_ms = re.sub(r"(?<=[)\s])only(?=[(\s])", '£', formula_ms)
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
                res.append(self.man_to_list(formula_ms[i + 1:i + count]))
                buffer = ''
                i += count + 1
                continue

            buffer += formula_ms[i]
            i += 1

            sep = key
            if '&' in buffer:
                sep = '&'
                key = 'and'
            elif '-' in buffer:
                sep = '-'
                key = 'neg'
            elif '|' in buffer:
                sep = '|'
                key = 'or'
            elif '%' in buffer:
                sep = '%'
                key = 'some'
            elif '£' in buffer:
                sep = '£'
                key = 'only'

            if not key == '':
                res += buffer.split(sep) + [key]
                buffer = ''
                key = ''

        res.append(buffer)
        return [t for t in res if not t == '']

    def owl_to_man(self, formula_owl):  # parse owl string in manchester syntax
        formula_owl = formula_owl.replace('&', 'and')
        formula_owl = formula_owl.replace('|', 'or')
        formula_owl = formula_owl.replace('.only', ' only ')
        formula_owl = formula_owl.replace('.some', ' some ')
        formula_owl = formula_owl.replace('(', ' ( ')
        formula_owl = formula_owl.replace(')', ' ) ')

        s_entry = formula_owl.split(' ')
        for i in range(len(s_entry)):
            s_entry[i] = re.sub(r'.+[.]', '', s_entry[i])
        return ' '.join(s_entry)

    def list_to_dict(self, formula_list):  # parse a list in a string
        ret = None
        if len(formula_list) == 1:
            if type(formula_list[0]) == str:  # formula is an atomic concept
                ret = {'type': 'concept', 'arg': formula_list[0]}
            elif type(formula_list[0]) == list:  # formula is a parhentesis
                ret = self.list_to_dict(formula_list[0])
        elif 'and' in formula_list:
            ret = {'type': 'and', 'arg': []}
            i = j = 0
            while not j == len(formula_list):
                if formula_list[j] == 'and' and not i == j:  # convert each argument of the and
                    ret['arg'].append(self.list_to_dict(formula_list[i:j]))
                    i = j + 1
                j += 1
            ret['arg'].append(self.list_to_dict(formula_list[i:]))

        elif 'or' in formula_list:
            ret = {'type': 'or', 'arg': []}
            i = j = 0
            while not j == len(formula_list):
                if formula_list[j] == 'or' and not i == j:  # convert each argument of the or
                    ret['arg'].append(self.list_to_dict(formula_list[i:j]))
                    i = j + 1
                j += 1
            ret['arg'].append(self.list_to_dict(formula_list[i:]))
        elif formula_list[0] == 'neg':
            ret = {'type': 'neg', 'arg': self.list_to_dict(formula_list[1:])}  # convert not argument
            pass
        elif formula_list[1] == 'some':  # convert 'some' arguments
            ret = {'type': 'exists',
                   'arg': ({'type': 'relation', 'arg': formula_list[0]}, self.list_to_dict([formula_list[2]]))}
        elif formula_list[1] == 'only':  # convert 'only' arguments
            ret = {'type': 'forall',
                   'arg': ({'type': 'relation', 'arg': formula_list[0]}, self.list_to_dict([formula_list[2]]))}
        else:  # what appened ?
            print(f"PARSER ERROR: can't parse {formula_list}")
            return None

        return ret

    def parse_manchester(self, formula_ms):  # parse manchester string to dict
        return self.list_to_dict(self.man_to_list(formula_ms))

    def parse_owl(self, formula_owl):
        return self.parse_manchester(self.owl_to_man(formula_owl))


class OutputManager:

    def __init__(self, onto):
        self.onto = onto

    def build_dot_graph(self, G, show='all', shape='box'):
        dot = gviz.Digraph('tableaux', comment='Tableaux result', format='png')
        for i in range(G.last_individual + 1):

            if show == 'all':
                lc = '\n'.join([to_str(c) for c in G.L[i]])
                dot.node(f"x{i}", f"x{i}\n--------\n{lc}", shape=shape)
            elif show == 'atomic':
                lc = ",\n".join([to_str(c) for c in G.L[i] if c['type'] == 'concept'])
                dot.node(f"x{i}", f"x{i}:{{{lc}}}", shape=shape)
            else:
                dot.node(f"x{i}", shape=shape)

        for rel in G.E.keys():
            for rx, ry in G.E[rel]:
                dot.edge(f"x{rx}", f"x{ry}", label=rel)

        return dot

    def export_rdf(self, G):

        graph = Graph()
        individuals = [URIRef(f'http://www.completion_graph/individual/x{individual}')
                       for individual in range(G.last_individual+1)]

        uris = {}
        for concept in self.onto.uris.keys():
            uris[concept] = URIRef(self.onto.uris[concept])

        for i in range(G.last_individual+1):
            for label in G.L[i]:
                if label['type'] == 'concept':
                    graph.add((individuals[i], RDFS.subClassOf, uris[label['arg']]))

        print(individuals)
        for prop in G.E.keys():
            for edge in G.E[prop]:
                graph.add((individuals[edge[0]], uris[prop], individuals[edge[1]]))
        graph.serialize(destination='./exported_graph.rdf', format='xml')
        return graph


def to_str(concept):
    """ recursive function to print a concept in dict format to a string """
    ret = []  # buffer to build the string

    if concept['type'] == 'and':
        ret += [f"({to_str(concept['arg'][0])}"] + [f"\u2293 {to_str(c)}" for c in concept['arg'][1:]] + [')']
    elif concept['type'] == 'or':
        ret += [f"({to_str(concept['arg'][0])}"] + [f"\u2294 {to_str(c)}" for c in concept['arg'][1:]] + [')']
    elif concept['type'] == 'neg':  # recursively print neg argument
        ret.append(f"\uFFE2{to_str(concept['arg'])}")
    elif concept['type'] == 'forall':  # recursively print forall arguments
        ret.append(f"\u2200{to_str(concept['arg'][0])}.{to_str(concept['arg'][1])}")
    elif concept['type'] == 'exists':  # recursively print exists argumentsnot({
        ret.append(f"\u2203{to_str(concept['arg'][0])}.{to_str(concept['arg'][1])}")
    elif concept['type'] == 'concept':  # print concept name (recursion base case)
        ret.append(concept['arg'])
    elif concept['type'] == 'relation':  # print concept name (recursion base case)
        ret.append(concept['arg'])
    elif concept['type'] == 'included':
        return f" {to_str(concept['arg'][0])} \u2291 {to_str(concept['arg'][1])}"
    elif concept['type'] == 'equival':
        return f" {to_str(concept['arg'][0])} \u2263 {to_str(concept['arg'][1])}"
    elif concept['type'] == 'disjoint':
        return f" {to_str(concept['arg'][0])} disjoint {to_str(concept['arg'][1])}"
    else:
        print('Print ERROR')
        return 'ERR'
    return " ".join(ret)
