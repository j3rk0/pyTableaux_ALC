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

from lib.engine import *
from lib.io import *

isFailureOf = {'relation': 'isFailureOf'}
column = {'concept': 'column'}
pillar = {'concept': 'pillar'}

C = nnf({'and': [{'exists': [isFailureOf, column]},
                 {'exists': [isFailureOf, pillar]},
                 {'neg': {'exists': [isFailureOf, {
                     'and': [pillar, column]
                 }]}}]})

tab = InferenceEngine()
res = tab.check_satisfy(C)

# %% plot del grafo risultante del tableaux

graph = plot_graph(res, show='atomic')
graph.view()

# %% benchmark tbox vuota

import timeit

setup = """from lib.engine import InferenceEngine
C={'and':
         [{'exists': ({'relation': 'H'}, {'concept': 'G'})},
          {'exists': ({'relation': 'H'}, {'concept': 'W'})},
          {'forall': ({'relation': 'H'}, {'or':
                                              [{'neg': {'concept': 'G'}},
                                               {'neg': {'concept': 'W'}}
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

S = {'relation': 'S'}
R = {'relation': 'R'}
C = {'concept': 'C'}
D = {'concept': 'D'}
C1 = {'and': [{'exists': (S, C)},
              {'forall': (S, {'or': [{'neg': C}, {'neg': D}]})},
              {'exists': (R, C)},
              {'forall': (R, {'exists': (R, C)})}]}

print(to_str(C1))
t = InferenceEngine()
res = t.check_satisfy(C1)
graph = plot_graph(res, show='all', shape='box')
graph.view()

# %% example with tbox
from lib.engine import *
from lib.io import *

tbox = {'and': [{'or': [{'neg': A}, B]},
                {'or': [{'neg': B}, C]},
                {'or': [{'neg': C}, {'exists': (R, D)}]},
                {'or': [{'neg': D}, {'neg': A}]},
                {'or': [{'neg': A}, {'forall': (R, A)}]}]}

C1 = {'and': [B, C, {'exists': (R, {'neg': A})}, {'forall': (R, C)}]}

print(f'tbox: {to_str(tbox)}\nconcept: {to_str(C1)}')

eng = InferenceEngine(T=tbox)
res = eng.check_satisfy(C1)
if res is not None:
    graph = plot_graph(res, show='atomic', shape='box')
    graph.view()
else:
    print('not satisfabile wrt tbox')

# %%BENCHMARK CON TBOX

import timeit

setup = """from lib.engine import InferenceEngine
tbox = {'and': [{'or': [{'neg': {'concept':'A'}}, {'concept':'D'}]},
                {'or': [{'neg': {'concept':'B'}}, {'concept':'C'}]},
                {'or': [{'neg': {'concept':'C'}}, {'exists': ({'relation':'R'}, {'concept':'D'})}]},
                {'or': [{'neg': {'concept':'D'}}, {'neg': {'concept':'A'}}]},
                {'or': [{'neg': {'concept':'A'}}, {'forall': ({'relation':'R'}, {'concept':'A'})}]}]}

C1 = {'and': [{'concept':'B'}, {'concept':'C'}, {'exists': ({'relation':'R'}, {'neg': {'concept':'A'}})}, {'forall':(
{'relation':'R'},{'concept':'C'})}]} 
engine = InferenceEngine(tbox) """

stmt = """res = engine.check_satisfy(C1)"""

number = 10000
time = timeit.timeit(stmt, setup, number=number)

print(f"time for iter: {(time / number):.6f}")

# %% INPUT FROM MANCHESTER
from lib.engine import *
from lib.io import *
from lib.formula import *

manch = "Pizza and not (hasTopping some FishTopping) and not (hasTopping some MeaTopping )"

res = parse_manchester(manch)
print(f"manchester syntax: {manch}\n"
      f"parsed formula: {to_str(res)}")
model = InferenceEngine().check_satisfy(res)
graph = plot_graph(model, show='atomic', shape='box')
graph.view()
