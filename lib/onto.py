import owlready2 as owl
from lib.io import *

"""
{'included':(A,B)}
{'equival': (A,B)}

"""


def import_tbox(file):
    onto = owl.get_ontology(file).load()
    tbox = []
    for C in onto.classes():
        tbox += [{'equival': ({'concept': C.name}, parse_owl(str(D)))} for D in C.equivalent_to]
        tbox += [{'included': ({'concept': C.name}, parse_owl(str(D)))} for D in C.is_a if not 'Thing' in str(D)]
    return tbox


def unfoldable(X, Tu):
    A = X[list(X.keys())[0]][0]
    return not any(axiom[list(axiom.keys())[0]][0] == A for axiom in Tu)


def tbox_partition(tbox):
    Tu = []
    Tg = []
    for X in tbox:
        if unfoldable(X, Tu):
            Tu.append(X)
        else:
            Tg.append(X)
    return Tu, Tg


def gci_to_str(gci):
    key = list(gci.keys())[0]
    if key == 'included':
        return f" {to_str(gci[key][0])} \u2291 {to_str(gci[key][1])}"
    else:
        return f" {to_str(gci[key][0])} \u2263 {to_str(gci[key][1])}"



