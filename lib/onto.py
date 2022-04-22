import owlready2 as owl

from lib.io import *

"""
{'included':(A,B)}
{'equival': (A,B)}

"""


class Ontology:

    def __init__(self):
        self.uris = {}
        self.tbox = None
        self.input_manager = InputManager()

    def import_onto(self, file):
        onto = owl.get_ontology(file).load()
        tbox = []

        for P in onto.properties():
            self.uris[str(P).split('.')[-1]] = f"{str(P.namespace.base_iri)}/{str(P).split('.')[-1]}"

        for C in onto.classes():
            self.uris[C.name] = C.iri
            tbox += [{'type': 'equival',
                      'arg': ({'type': 'concept', 'arg': C.name}, self.input_manager.parse_owl(str(D)))}
                     for D in C.equivalent_to]

            tbox += [{'type': 'included',
                      'arg': ({'type': 'concept', 'arg': C.name}, self.input_manager.parse_owl(str(D)))}
                     for D in C.is_a if 'Thing' not in str(D)]
            tbox += [
                {'type': 'included',
                 'arg': ({'type': 'concept', 'arg': C.name},
                         {'type': 'neg', 'arg': self.input_manager.parse_owl(str(D))})}
                for p in C.disjoints() for D in p.entities if not D == C]

        self.tbox = tbox
        return tbox

    def print_gci(self):
        return '\n'.join([to_str(gci) for gci in self.tbox])
