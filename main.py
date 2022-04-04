from lib.formula import *
from lib.io import *
from lib.engine import *

# definiamo alcuni concetti e predicati per costruire degli esempi

A = {'type': 'concept', 'arg': 'A'}
B = {'type': 'concept', 'arg': 'B'}
C = {'type': 'concept', 'arg': 'C'}
D = {'type': 'concept', 'arg': 'D'}
E = {'type': 'concept', 'arg': 'E'}

R = {'type': 'relation', 'arg': 'R'}
S = {'type': 'relation', 'arg': 'S'}

# %% esempio di concetti composti

C1 = {'type': 'and',
      'arg': [A, {'type': 'exists', 'arg': (R, B)}, {'type': 'exists', 'arg': (R, {'type': 'neg', 'arg': B})}]}
C2 = {'type': 'and',
      'arg': [{'type': 'forall', 'arg': (S, A)}, {'type': 'exists', 'arg': (R, B)}, {'type': 'forall', 'arg': (R, A)}]}

print("a concept:")
print(to_str(C1))
print("another concept:")
print(to_str(C2))

# %%eliminazione parentesi ridondanti

C1 = {'type': 'and', 'arg': [{'type': 'and', 'arg': [A, B]},
                             {'type': 'exists', 'arg': (R, {'type': 'and', 'arg': [{'type': 'and', 'arg': [A, B]}, B]})}
                             ]}
print(to_str(C1))

C2 = delete_redundant_parenthesis(C1)
print(to_str(C2))

# %% conversione a cnf

C1 = {'type': 'or', 'arg': [{'type': 'neg', 'arg': {'type': 'or', 'arg': [A, B]}},
                            {'type': 'or', 'arg': [
                                {'type': 'neg', 'arg': C},
                                D
                            ]}]}

print('a concept:')
print(to_str(C1))
C2 = cnf(C1)
C3 = delete_redundant_parenthesis(C2)
print('concept in cnf:')
print(to_str(C3))

print('another concept')
C1 = {'type': 'or', 'arg': [{'type': 'neg', 'arg': {'type': 'and', 'arg': [{'type': 'neg', 'arg': A}, B]}}, C]}
print(to_str(C1))
C2 = cnf(C1)
C3 = delete_redundant_parenthesis(C2)
print('another concept in cnf:')
print(to_str(C3))

# %% conversione a nnf


x = {'type': 'neg', 'arg':
    {'type': 'and', 'arg': [{'type': 'neg', 'arg': C},
                            {'type': 'or', 'arg': [{'type': 'neg', 'arg': D},
                                                   E]}]}}

print("concept:")
print(to_str(x))
print("concept in nnf:")
nnf_x = nnf(x)
print(to_str(nnf_x))

x = {'type': 'and', 'arg': [{'type': 'neg', 'arg': {'type': 'exists', 'arg': (R, A)}},
                            {'type': 'exists', 'arg': (R, B)},
                            {'type': 'neg', 'arg': {'type': 'and', 'arg': [A, B]}},
                            {'type': 'neg', 'arg': {'type': 'forall', 'arg': (R, {'type': 'or', 'arg': [A, B]})}}]}

print("another concept:")
print(to_str(x))
print("concept in nnf:")
print(to_str(nnf(x)))

# %% esempio con tbox vuota

from lib.engine import *
from lib.io import *

isFailureOf = {'type': 'relation', 'arg': 'isFailureOf'}
column = {'type': 'concept', 'arg': 'column'}
pillar = {'type': 'concept', 'arg': 'pillar'}

C = nnf({'type': 'and', 'arg': [{'type': 'exists', 'arg': [isFailureOf, column]},
                                {'type': 'exists', 'arg': [isFailureOf, pillar]},
                                {'type': 'neg', 'arg': {'type': 'exists', 'arg': [isFailureOf, {
                                    'type': 'and', 'arg': [pillar, column]
                                }]}}]})

tab = InferenceEngine()
res = tab.check_satisfy(C)

# %% plot del grafo risultante del tableaux

graph = build_dot_graph(res, show='all')
graph.view()

# %% benchmark tbox vuota

import timeit

setup = """from lib.engine import InferenceEngine
C={'type':'and', 'arg':
         [{'type':'exists','arg': ({'type':'relation','arg': 'H'}, {'type':'concept','arg': 'G'})},
          {'type':'exists', 'arg': ({'type':'relation','arg': 'H'}, {'type':'concept', 'arg': 'W'})},
          {'type':'forall', 'arg': ({'type':'relation', 'arg': 'H'}, {'type':'or', 'arg':
                                              [{'type':'neg','arg': {'type':'concept','arg': 'G'}},
                                               {'type':'neg', 'arg': {'type':'concept','arg': 'W'}}
                                               ]})}]}
engine=InferenceEngine()
"""

stmt = """res = engine.check_satisfy(C)"""

number = 10000
time = timeit.timeit(stmt, setup, number=number)

print(f"time for iter: {(time / number):.6f}")

# %%
from lib.engine import InferenceEngine
from lib.io import *

S = {'type': 'relation', 'arg': 'S'}
R = {'type': 'relation', 'arg': 'R'}
C = {'type': 'concept', 'arg': 'C'}
D = {'type': 'concept', 'arg': 'D'}
C1 = {'type': 'and', 'arg': [{'type': 'exists', 'arg': (S, C)},
                             {'type': 'forall', 'arg': (
                             S, {'type': 'or', 'arg': [{'type': 'neg', 'arg': C}, {'type': 'neg', 'arg': D}]})},
                             {'type': 'exists', 'arg': (R, C)},
                             {'type': 'forall', 'arg': (R, {'type': 'exists', 'arg': (R, C)})}]}

print(to_str(C1))
t = InferenceEngine()
res = t.check_satisfy(C1)
graph = build_dot_graph(res, show='all', shape='box')
graph.view()

# %% INPUT FROM MANCHESTER
from lib.engine import *
from lib.io import *
from lib.formula import *

manch = "Pizza and not (hasTopping some FishTopping) and not (hasTopping some MeaTopping )"

res = parse_manchester(manch)
print(f"manchester syntax: {manch}\n"
      f"parsed formula: {to_str(res)}")
# %%
model = InferenceEngine().check_satisfy(res)
graph = build_dot_graph(model, show='atomic', shape='box')
graph.view()
