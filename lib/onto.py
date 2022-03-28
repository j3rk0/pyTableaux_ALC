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
        tbox += [{'included': ({'concept': C.name}, parse_owl(str(D)))} for D in C.is_a if 'Thing' not in str(D)]
        tbox += [{'included': ({'concept': C.name}, {'neg': parse_owl(str(D))})} for p in C.disjoints()
                 for D in p.entities if not D == C]
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
    elif key== 'equival':
        return f" {to_str(gci[key][0])} \u2263 {to_str(gci[key][1])}"
    else:
        print('GCI Print ERROR')
        return 'ERR'


def gci_to_concept(t):
    if 'included' in t.keys():
        return {'or': [{'neg': t['included'][0]}, t['included'][1]]}
    elif 'equival' in t.keys():
        return {'and': [{'or': [{'neg': t['equival'][0]}, t['equival'][1]]},
                        {'or': [{'neg': t['equival'][1]}, t['equival'][0]]}]}
    else:
        return t
