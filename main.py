import owlready2 as owl

onto = owl.get_ontology("http://www.lesfleursdunormal.fr/static/_downloads/pizza_onto.owl")
onto.load()

# %%


# {'name':'C'}
# {'and':[C1,...,Cn]}
# { 'or':[C1,...,Cn]}
# { 'neg': C }
# { 'forall':(R,C)}
# { 'exists':(R,C)}

H = {'name': 'H'}
G = {'name': 'G'}
W = {'name': 'W'}

C = {'and': [{'exists': (H, G)},
             {'exists': (H, W)},
             {'forall': (H, {'or': [{'neg': G}, {'neg': W}]})}]}
