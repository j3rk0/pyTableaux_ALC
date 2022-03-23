import owlready2 as owl
from lib.io import *


def import_tbox(file):
    onto = owl.get_ontology(file).load()
    tbox = []
    equivalences = []
    inclusions = []
    for C in onto.classes():
        equivalences += [({'concept': C.name}, parse_owl(str(D))) for D in C.equivalent_to]
        inclusions += [({'concept': C.name}, parse_owl(str(D))) for D in C.is_a]
    tbox += [{'or': [{'neg': C}, D]} for C, D in inclusions if not D == {'concept': 'Thing'}]
    tbox += [{'and': [{'or': [{'neg': C}, D]}, {'or': [C, {'neg': D}]}]} for C, D in equivalences]
    return tbox
