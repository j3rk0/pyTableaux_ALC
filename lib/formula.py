"""
 in this project axioms are expressed as dictionary as following:

 {'relation':'R' } // relation  {'type':'relation', arg:'R'}
 {'concept':'C' } //atomic concept

 {'and':[C1,...,Cn]} //conjunction
 { 'or':[C1,...,Cn]} //disjunction

 { 'neg': C } //negation

 { 'forall':(R,C)} //universal quantifier
 { 'exists':(R,C)} //existential quantifier

"""


def delete_redundant_parenthesis(concept):
    if concept['type'] in ('and', 'or'):
        for c in concept['arg']:
            if concept['type'] == c['type']:
                concept['arg'] += c['arg']
                concept['arg'].remove(c)
        for i in range(len(concept['arg'])):
            concept['arg'][i] = delete_redundant_parenthesis(concept['arg'][i])
    elif concept['type'] in ('exists', 'forall'):
        concept['arg'] = (concept['arg'][0], delete_redundant_parenthesis(concept['arg'][1]))
    elif concept['type'] == 'neg':
        concept['arg'] = delete_redundant_parenthesis(concept['arg'])
    return concept


def cnf(concept):
    # group the operators in couples
    if concept['type'] in ('and', 'or') and len(concept['arg']) > 2:
        new_term = {'type': concept['type'], 'arg': concept['arg'][1:]}
        concept['arg'] = [concept['arg'][0], new_term]

    if concept['type'] in ('forall', 'exists'):
        concept['arg'] = (concept['arg'][0], cnf(concept['arg'][1]))

    elif concept['type'] in ('or', 'and'):
        x1 = cnf(concept['arg'][0])
        x2 = cnf(concept['arg'][1])

        if not x1['type'] == 'and':  # x1 is atomic
            x1 = {'type': 'and', 'arg': [x1]}

        if not x2['type'] == 'and':  # x2 is atomic
            x2 = {'type': 'and', 'arg': [x2]}

        if concept['type'] == 'and':
            concept = {'type': 'and', 'arg': x1['and'] + x2['and']}
        elif concept['type'] == 'or':
            concept = {'type': 'and', 'arg': [{'type': 'or', 'arg': [t1, t2]} for t1 in x1['arg'] for t2 in x2['arg']]}

    elif concept['type'] == 'neg':
        if concept['arg']['type'] == 'neg':
            concept = cnf(concept['arg']['arg'])
        elif concept['arg']['type'] == 'and':  # demorgan
            concept = {'type': 'or', 'arg': [{'type': 'neg', 'arg': concept['arg']['arg'][0]},
                                             {'type': 'neg', 'arg': concept['arg']['arg'][1]}]}
        elif concept['arg']['type'] == 'or':
            concept = {'type': 'and',
                       'arg': [{'type': 'neg', 'arg': concept['arg']['arg'][0]},
                               {'type': 'neg', 'arg': concept['arg']['arg'][1]}]}
    return concept


def nnf(concept):
    """ this recursive function convert an axiom to his nnf form"""
    if concept['type'] == 'concept':  # nnf(c) = c ( recursion base case)
        return concept
    elif concept['type'] == 'and':  # nnf( c1 and c2) = nnf(c1) and nnf(c2)
        return {'type': 'and', 'arg': [nnf(c) for c in concept['arg']]}
    elif concept['type'] == 'or':  # nnf(c1 or c2) = nnf(c1) or nnf(c2)
        return {'type': 'or', 'arg': [nnf(c) for c in concept['arg']]}
    elif concept['type'] == 'forall':  # nnf( forall R.C) = forall R.nnf(C)
        return {'type': 'forall', 'arg': (concept['arg'][0], nnf(concept['arg'][1]))}
    elif concept['type'] == 'exists':  # nnf(exists R.C) = exists R.nnf(C)
        return {'type': 'exists', 'arg': (concept['arg'][0], nnf(concept['arg'][1]))}
    elif concept['type'] == 'neg':
        arg_neg = concept['arg']  # the argument of tge negation
        if arg_neg['type'] == 'neg':  # nnf( neg neg C ) = nnf(C)
            return nnf(arg_neg['arg'])
        elif arg_neg['type'] == 'concept':  # nnf(neg C) = neg C
            return concept
        elif arg_neg['type'] == 'and':  # nnf( neg(C1 and C2) ) = nnf(neg C1) or nnf(neg C2)
            return {'type': 'or', 'arg': [nnf({'type': 'neg', 'arg': c}) for c in arg_neg['arg']]}
        elif arg_neg['type'] == 'or':  # nnf( neg(C1 or C2) ) = nnf(neg C1) and nnf(neg C2)
            return {'type': 'and', 'arg': [nnf({'type': 'neg', 'arg': c}) for c in arg_neg['arg']]}
        elif arg_neg['type'] == 'forall':  # nnf( neg(forall R.C)  ) = exists R.nnf(neg C)
            return {'type': 'exists', 'arg': (arg_neg['arg'][0], nnf({'type': 'neg', 'arg': arg_neg['arg'][1]}))}
        elif arg_neg['type'] == 'exists':  # nnf( neg(exists R.C) ) = forall R.nnf(neg C)
            return {'type': 'forall', 'arg': (arg_neg['arg'][0], nnf({'type': 'neg', 'arg': arg_neg['arg'][1]}))}
