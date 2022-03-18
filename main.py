from lib.formula import *

# %% definiamo alcuni concetti e predicati per costruire degli esempi

A = {'concept': 'A'}
B = {'concept': 'B'}
C = {'concept': 'C'}
D = {'concept': 'D'}
E = {'concept': 'E'}

R = {'relation': 'R'}
S = {'relation': 'S'}

# %% esempio di concetti composti

C1 = {'and': [A, {'exists': (R, B)}, {'exists': (R, {'neg': B})}]}
C2 = {'and': [{'forall': (S, A)}, {'exists': (R, B)}, {'forall': (R, A)}]}

print("a concept:")
print(to_str(C1))
print("another concept:")
print(to_str(C2))

# %% conversione a nnf


x = {'neg':
         {'and': [{'neg': C},
                  {'or': [{'neg': D},
                          E]}]}}

print("concept:")
print(to_str(x))
print("concept in nnf:")
nnf_x = nnf(x)
print(to_str(nnf_x))

x = {'and': [{'neg': {'exists': (R, A)}},
             {'exists': (R, B)},
             {'neg': {'and': [A, B]}},
             {'neg': {'forall': (R, {'or': [A, B]})}}]}

print("another concept:")
print(to_str(x))
print("concept in nnf:")
print(to_str(nnf(x)))

# %%
from lib.etc.tableaux_noTBox import *

C = {'and':
         [{'exists': ({'relation': 'H'}, {'concept': 'G'})},
          {'exists': ({'relation': 'H'}, {'concept': 'W'})},
          {'forall': ({'relation': 'H'}, {'or':
                                              [{'neg': {'concept': 'G'}},
                                               {'neg': {'concept': 'W'}}
                                               ]})}]}

print(f"axiom: {to_str(C)}")

t = Tableaux()
start = time()
t.check_satisfy(C)
print(time() - start)

# %% esempio con tbox vuota

from lib.tableaux_notbox import *
from lib.io import *

isFailureOf = {'relation': 'isFailureOf'}
column = {'concept': 'column'}
pillar = {'concept': 'pillar'}

C = nnf({'and': [{'exists': [isFailureOf, column]},
                 {'exists': [isFailureOf, pillar]},
                 {'neg': {'exists': [isFailureOf, {
                     'and': [pillar, column]
                 }]}}]})

tab = Tableaux()
res = tab.check_satisfy(C)

graph = plot_graph(res)
graph.view()

# %% benchmark tbox vuota

import timeit

setup = """from lib.TableauxGraph import Tableaux
C={'and':
         [{'exists': ({'relation': 'H'}, {'concept': 'G'})},
          {'exists': ({'relation': 'H'}, {'concept': 'W'})},
          {'forall': ({'relation': 'H'}, {'or':
                                              [{'neg': {'concept': 'G'}},
                                               {'neg': {'concept': 'W'}}
                                               ]})}]}
"""

stmt = """res = Tableaux().check_satisfy(C)"""

number = 10000
time = timeit.timeit(stmt, setup, number=number)

print(f"time for iter: {(time / number):.6f}")

# %%
