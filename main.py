from lib.concept import *





# %% esempi dagli appunti dalle slide
A = {'c_name': 'A'}
B = {'c_name': 'B'}
R = {'r_name': 'R'}
S = {'r_name': 'S'}

C1 = {'and': [A, {'exists': (R, B)}, {'exists': (R, {'neg': B})}]}

C2 = {'and': [{'forall': (S, A)}, {'exists': (R, B)}, {'forall': (R, A)}]}

print(to_str(C1))

# %%


C = {'c_name': 'C'}
D = {'c_name': 'D'}
E = {'c_name': 'E'}

x = {'neg':
         {'and': [{'neg': C},
                  {'or': [{'neg': D},
                          E]}]}}

nnf_x = nnf(x)
print(to_str(nnf_x))
