from lib.concept import *

# %% definiamo alcuni concetti e predicati per costruire degli esempi

A = {'c_name': 'A'}
B = {'c_name': 'B'}
C = {'c_name': 'C'}
D = {'c_name': 'D'}
E = {'c_name': 'E'}

R = {'r_name': 'R'}
S = {'r_name': 'S'}

#%% esempio di concetti composti

C1 = {'and': [A, {'exists': (R, B)}, {'exists': (R, {'neg': B})}]}
C2 = {'and': [{'forall': (S, A)}, {'exists': (R, B)}, {'forall': (R, A)}]}

print(to_str(C1))

# %% conversione a nnf


x = {'neg':
         {'and': [{'neg': C},
                  {'or': [{'neg': D},
                          E]}]}}

nnf_x = nnf(x)
print(to_str(nnf_x))

#%%
x = {'and':[ {'neg':{'exists':(R,A)}},
             {'exists':(R,B)},
             {'neg':{'and':[A,B]}},
             {'neg':{'forall':(R,{'or':[A,B]})}}]}

print(to_str(nnf(x)))
