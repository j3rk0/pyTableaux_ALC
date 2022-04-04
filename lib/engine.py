from lib.formula import nnf


class CompletionGraph:

    def __init__(self):
        self.last_individual = 0
        self.L = []
        self.E = {}
        self.is_complete = []
        self.contain_clash = []

    def init(self, C):
        self.L.append([C])
        self.is_complete.append(False)
        self.contain_clash.append(False)

    def add_node(self):
        self.last_individual += 1
        self.L.append([])
        self.is_complete.append(False)
        self.contain_clash.append(False)

    def add_edge(self, rel, x, y):
        if rel['arg'] not in self.E.keys():
            self.E[rel['arg']] = []

        self.E[rel['arg']].append((x, y))

    def get_edges(self, rel):
        if rel['arg'] not in self.E.keys():
            return []
        return self.E[rel['arg']]

    def copy(self):
        G = CompletionGraph()
        G.last_individual = self.last_individual
        for i in range(G.last_individual + 1):
            G.L.append([t for t in self.L[i]])
            G.is_complete.append(self.is_complete[i])
            G.contain_clash.append(self.contain_clash[i])
        for rel in self.E.keys():
            G.E[rel] = [t for t in self.E[rel]]
        return G


class InferenceEngine:

    def __init__(self, T=None):
        self.graphs = []

        self.Tg = self.Tu = []
        if T is not None:
            self.Tu, self.Tg = self.tbox_partition(T)
            self.Tg = [self.gci_to_concept(t) for t in self.Tg]

    def gci_to_concept(self, t):
        if t['type'] == 'included':
            return nnf({'type': 'or', 'arg': [{'type': 'neg', 'arg': t['arg'][0]}, t['arg'][1]]})
        elif t['type'] == 'equival':
            return nnf(
                {'type': 'and', 'arg': [{'type': 'or', 'arg': [{'type': 'neg', 'arg': t['arg'][0]}, t['arg'][1]]},
                                        {'type': 'or', 'arg': [{'type': 'neg', 'arg': t['arg'][1]}, t['arg'][0]]}]})
        else:
            return t

    def unfoldable(self, X, Tu):
        return not any(axiom['arg'][0] == X['arg'][0] for axiom in Tu)

    def tbox_partition(self, tbox):
        Tu = []
        Tg = []
        for X in tbox:
            if self.unfoldable(X, Tu):
                Tu.append(X)
            else:
                Tg.append(X)
        return Tu, Tg

    def check_satisfy(self, C):
        C = nnf(C)
        G = CompletionGraph()
        G.init(C)
        G.L[0] += self.Tg
        self.graphs = []
        stack = [G]
        while not len(stack) == 0:
            curr = stack.pop()
            stack += self.expand_graph(curr)
            self.graphs.append(curr)
            if all(curr.is_complete) and not any(curr.contain_clash):
                return curr
        return None

    def is_blocked(self, G, j):
        for i in range(G.last_individual + 1):
            if i < j and all(xj in G.L[i] for xj in G.L[j]):
                return True
        return False

    def expand_graph(self, G):
        x = 0
        while not all(G.is_complete) and not any(G.contain_clash):
            if not G.is_complete[x] or G.contain_clash[x]:

                # check for clash
                if any(t1['arg'] == t2 for t1 in G.L[x] if t1['type'] == 'neg' for t2 in G.L[x]):
                    G.contain_clash[x] = True
                    return []

                # check for blocking
                if self.is_blocked(G, x):
                    G.is_complete[x] = True
                    continue

                # apply exhaustively and rule
                G.L[x] += [t for a in G.L[x] if a['type'] == 'and' for t in a['arg'] if t not in G.L[x]]

                # apply exhaustively exists-rule
                for a in G.L[x]:
                    if a['type'] == 'exists':
                        rel, conc = a['arg']

                        exists_z = False  # are there some z so that r(x,z) and c(z) is in abox?
                        for rx, rz in G.get_edges(rel):
                            if rx == x and conc in G.L[rz]:
                                exists_z = True
                                break

                        if not exists_z:  # does not exists z
                            G.add_node()
                            G.L[G.last_individual] += [conc] + self.Tg
                            G.add_edge(rel, x, G.last_individual)

                # apply exhaustively forall-rule
                for a in G.L[x]:
                    if a['type'] == 'forall':
                        rel, conc = a['arg']

                        # all the y so that r(x,y) in the abox but not c(y)
                        rcy = [ry for rx, ry in G.get_edges(rel)
                               if rx == x and conc not in G.L[ry]]

                        for y in rcy:
                            G.L[y].append(conc)

                # unfolding-1 rule
                G.L[x] += [C['arg'][1] for A in G.L[x] for C in self.Tu
                           if C['type'] == 'equival' and C['arg'][0] == A and C['arg'][1] not in G.L[x]]

                # unfolding-2 rule
                G.L[x] += [{'type': 'neg', 'arg': C['arg'][1]} for A in G.L[x] if A['type'] == 'neg'
                           for C in self.Tu if C['type'] == 'equival' and C['arg'][0] == A['arg']
                           and {'type': 'neg', 'arg': C['arg'][1]} not in G.L[x]]

                # unfolding-3 rule
                G.L[x] += [C['arg'][1] for A in G.L[x] for C in self.Tu
                           if C['type'] == 'included' and C['arg'][0] == A and C['arg'][1] not in G.L[x]]

                # apply an or rule
                for a in G.L[x]:
                    if a['type'] == 'or' and not any(t1 in G.L[x] for t1 in a['arg']):
                        ret = []
                        for t in a['arg']:  # build a new graph for each or term
                            new_G = G.copy()
                            new_G.L[x].append(t)
                            ret.append(new_G)
                        return ret

                G.is_complete[x] = True  # mark node as complete

            x += 1
        return []
