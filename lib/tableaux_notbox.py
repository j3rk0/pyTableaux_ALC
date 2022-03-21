from lib.formula import *


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
        if rel['relation'] not in self.E.keys():
            self.E[rel['relation']] = []

        self.E[rel['relation']].append((x, y))

    def get_edges(self, rel):
        if rel['relation'] not in self.E.keys():
            return []
        return self.E[rel['relation']]

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


class Tableaux:

    def __init__(self):
        self.graphs = []

    def check_satisfy(self, C):
        C = nnf(C)
        G = CompletionGraph()
        G.init(C)

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

                # check for blocking
                if self.is_blocked(G, x):
                    G.is_complete[x] = True
                    continue

                # apply exhaustively and rule
                G.L[x] += [t for a in G.L[x] if 'and' in a.keys() for t in a['and'] if t not in G.L[x]]

                # apply exhaustively exists-rule
                for a in G.L[x]:
                    if 'exists' in a.keys():
                        rel, conc = a['exists']

                        exists_z = False  # are there some z so that r(x,z) and c(z) is in abox?
                        for rx, rz in G.get_edges(rel):
                            if rx == x and conc in G.L[rz]:
                                exists_z = True
                                break

                        if not exists_z:  # does not exists z
                            G.add_node()
                            G.L[G.last_individual].append(conc)
                            G.add_edge(rel, x, G.last_individual)

                # apply exhaustively forall-rule
                for a in G.L[x]:
                    if 'forall' in a.keys():
                        rel, conc = a['forall']

                        # all the y so that r(x,y) in the abox but not c(y)
                        rcy = [ry for rx, ry in G.get_edges(rel)
                               if rx == x and conc not in G.L[ry]]

                        for y in rcy:
                            G.L[y].append(conc)

                # apply an or rule
                for a in G.L[x]:
                    if 'or' in a.keys() and not (a['or'][0] in G.L[x] or a['or'][1] in G.L[x]):
                        ret = []
                        for t in a['or']:  # build a new graph for each or term
                            new_G = G.copy()
                            new_G.L[x].append(t)
                            ret.append(new_G)
                        return ret

                G.is_complete[x] = True  # mark node as complete
                # check for clash
                if any(t1['neg'] == t2 for t1 in G.L[x] if 'neg' in t1.keys() for t2 in G.L[x]):
                    G.contain_clash[x] = True
                    return []

            x += 1
        return []
