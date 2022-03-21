from lib.formula import *

# definiamo alcuni concetti e predicati per costruire degli esempi

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

# %%eliminazione parentesi ridondanti

C1 = {'and': [{'and': [A, B]},
              {'exists': (R, {'and': [{'and': [A, B]}, B]})}
              ]}
print(to_str(C1))

C2 = delete_redundant_parenthesis(C1)
print(to_str(C2))

# %% conversione a cnf

C1 = {'or': [{'neg': {'or': [A, B]}},
             {'or': [
                 {'neg': C},
                 D
             ]}]}

print('a concept:')
print(to_str(C1))
C2 = cnf(C1)
C3 = delete_redundant_parenthesis(C2)
print('concept in cnf:')
print(to_str(C3))

print('another concept')
C1 = {'or': [{'neg': {'and': [{'neg': A}, B]}}, C]}
print(to_str(C1))
C2 = cnf(C1)
C3 = delete_redundant_parenthesis(C2)
print('another concept in cnf:')
print(to_str(C3))

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

# %% plot del grafo risultante del tableaux

graph = plot_graph(res, print='atomic')
graph.view()

# %% benchmark tbox vuota

import timeit

setup = """from lib.tableaux_notbox import Tableaux
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
from lib.tableaux_notbox import Tableaux
from lib.io import *

S = {'relation': 'S'}
R = {'relation': 'R'}
C = {'concept': 'C'}
D = {'concept': 'D'}
C1 = {'and': [{'exists': (S, C)},
              {'forall': (S, {'or': [{'neg': C}, {'neg': D}]})},
              {'exists': (R, C)},
              {'forall': (R, {'exists': (R, C)})}]}

print(to_str(C1))
t = Tableaux()
res = t.check_satisfy(C1)
graph = plot_graph(res, print='all', shape='box')
graph.view()

#%%
from owlready2 import *




