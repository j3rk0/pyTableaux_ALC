"""
an abox is a list of axiom with arg setted
a tableaux is defined like a structure with a set of terms, an abox, a set of childs, and a rule that link
itself with his childs
"""


from copy import copy
from lib.concept import *


def abox_to_str(abox):
    ret = [to_str(c) for c in abox]
    ret = ", ".join(ret)
    return f"{{{ret}}}"


def assign(concept, args):
    t = copy(concept)
    t['args'] = args
    return t


class TNode:

    def __init__(self):
        self.terms = 0  # numero delle variabili
        self.abox = []  # insieme di assiomi
        self.childs = []  # lista di TNode figli
        self.rule = ''  # regola che lega il TNode al figlio
        self.clashes = []  # listsa di clash

    def init_tree(self, concept):
        self.abox = [copy(concept)]
        self.abox[0]['args'] = [0]

    def to_str(self, skip=0, offset=0):

        ret = skip * [' '] + offset * ["="] + [f"> abox:{abox_to_str(self.abox)}\n"]
        if self.rule == 'complete':
            ret += (offset + skip) * [" "] + ['  abox complete']
        elif self.rule == 'clash':
            ret += (offset + skip) * [" "] + ['  contains clashes']
        else:
            ret += (offset + skip) * [" "] + [f'  {self.rule}']
        return "".join(ret)


class Tableaux:

    def __init__(self):
        self.root = TNode()

    def check_satisfy(self, concept, grow_all=False):
        concept = nnf(concept)
        self.root.init_tree(concept)
        queue = [self.root]

        ret = False
        while len(queue) > 0:
            curr = queue.pop()
            queue += [n for n in self.expand_node(curr) if not self.calculate_clashes(n)]
            if curr.rule == 'complete':
                ret = True
                if not grow_all:
                    return ret
        return ret

    def calculate_clashes(self, node):
        node.clashes = [(t1, t2) for t1 in node.abox if 'neg' in t1.keys()
                        for t2 in node.abox if t2 == assign(t1['neg'], t1['args'])]

        if len(node.clashes) > 0:
            node.rule = 'clash'
            return True
        return False

    def expand_node(self, node):
        and_terms = []
        exists_terms = []
        forall_terms = []
        or_terms = []
        concepts = []
        relations = []

        new_node = TNode()  # the new tableaux node
        new_node.terms = node.terms

        for t in node.abox:  # group abox elements respect to operator
            if 'and' in t.keys():
                and_terms.append(t)
            elif 'exists' in t.keys():
                exists_terms.append(t)
            elif 'forall' in t.keys():
                forall_terms.append(t)
            elif 'or' in t.keys():
                or_terms.append(t)
            elif 'concept' in t.keys():
                concepts.append(t)
            elif 'relation' in t.keys():
                relations.append(t)

        if len(and_terms) > 0:  # and rule
            node.rule = '\u2293-rule'
            # if not already in abox add each element
            new_node.abox = [assign(t, a['args']) for a in and_terms for t in a['and']
                             if assign(t, a['args']) not in node.abox] + \
                            exists_terms + forall_terms + or_terms + concepts + relations

            node.childs.append(new_node)
            return [new_node]

        elif len(exists_terms) > 0:  # exists rule

            node.rule = '\u2203-rule'
            new_node.abox = forall_terms + or_terms + concepts + relations

            for e in exists_terms:
                r, c = e['exists']
                x = e['args'][0]  # x is the individual of our exists

                # all z so that r(x,z) is in the abox
                rz = set([rel['args'][1] for rel in relations
                          if rel['relation'] == r['relation'] and rel['args'][0] == x])
                # all z so that c(z) is in the abox
                cz = set([con['args'][0] for con in node.abox if concept_equal(c, con)])

                # there are no individual z such that r(x,z) and c(z) are in abox
                if len(rz.intersection(cz)) == 0:
                    z = new_node.terms = new_node.terms + 1
                    new_node.abox += [{'relation': r['relation'], 'args': [x, z]}, assign(c, [z])]

            node.childs.append(new_node)
            return [new_node]

        elif len(forall_terms) > 0:  # forall rule

            node.rule = '\u2200-rule'
            new_node.abox = or_terms + concepts + relations

            for f in forall_terms:
                r, c = f['forall']
                x = f['args'][0]  # x is the individual of our forall
                # all y so that r(x,y) is in the abox
                rxy = set(
                    [rel['args'][1] for rel in relations if rel['relation'] == r['relation'] and rel['args'][0] == x])
                # all y so that c(y) is in the abox
                cy = set([con['args'][0] for con in node.abox if concept_equal(c, con)])

                for y in rxy.difference(cy):  # all the y so that r(x,y) is in the abox but not c(y)
                    new_node.abox.append(assign(c, [y]))

            node.childs.append(new_node)
            return [new_node]

        elif len(or_terms) > 0:  # or rule
            node.rule = '\u2294-rule'

            new_node1 = TNode()
            new_node1.terms = node.terms

            or_term = or_terms.pop(0)
            new_node.abox = [assign(or_term['or'][0], or_term['args'])] + or_terms + concepts + relations
            new_node1.abox = [assign(or_term['or'][1], or_term['args'])] + or_terms + concepts + relations

            node.childs.append(new_node)
            node.childs.append(new_node1)
            return [new_node, new_node1]

        if not node.rule == 'clash':
            node.rule = 'complete'
        return []

    def print_tableaux(self):
        skip = [0]
        offset = [1]
        queue = [self.root]

        while len(queue) > 0:
            curr_skip = skip.pop(0)
            curr_offset = offset.pop(0)
            curr_node = queue.pop(0)
            print(curr_node.to_str(curr_skip, curr_offset))
            for node in curr_node.childs:
                skip.append(curr_skip + curr_offset + 1)
                offset.append(3)
                queue.append(node)


def blocking(abox):
    pass
