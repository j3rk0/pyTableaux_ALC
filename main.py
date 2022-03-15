from lib.concept import *

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


# %%
import timeit
from lib.tableaux_noTbox import *

C = {'and':
         [{'exists': ({'relation': 'H'}, {'concept': 'G'})},
          {'exists': ({'relation': 'H'}, {'concept': 'W'})},
          {'forall': ({'relation': 'H'}, {'or':
                                              [{'neg': {'concept': 'G'}},
                                               {'neg': {'concept': 'W'}}
                                               ]})}]}

print(f"axiom: {to_str(C)}")

# %%
t = Tableaux()
t.check_satisfy(C)
t.print_tableaux()

# start = timeit.default_timer()

# for i in range(100):
#    t.check_satisfy(C)

# end = timeit.default_timer()

# print(f"elapsed time: {(end-start)/100}")


# %%

isFailureOf = {'relation': 'isFailureOf'}
column = {'concept': 'column'}
pillar = {'concept': 'pillar'}

C = nnf({'and': [{'exists': [isFailureOf, column]},
             {'exists': [isFailureOf, pillar]},
             {'neg': {'exists': [isFailureOf, {
                 'and': [pillar, column]
             }]}}]})
print(to_str(C))


t = Tableaux()
t.check_satisfy(C)
t.print_tableaux()
