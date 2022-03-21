"""
 in this project axioms are expressed as dictionary as following:

 {'relation':'R' } // relation
 {'concept':'C' } //atomic concept

 {'and':[C1,...,Cn]} //conjunction
 { 'or':[C1,...,Cn]} //disjunction

 { 'neg': C } //negation

 { 'forall':(R,C)} //universal quantifier
 { 'exists':(R,C)} //existential quantifier

"""


def delete_redundant_parenthesis(concept):
    key = list(concept.keys())[0]

    if key == 'or' or key == 'and':
        for c in concept[key]:
            if key in c.keys():
                concept[key] += c[key]
                concept[key].remove(c)
        for i in range(len(concept[key])):
            concept[key][i] = delete_redundant_parenthesis(concept[key][i])
    elif key == 'exists' or key == 'forall':
        concept[key] = (concept[key][0], delete_redundant_parenthesis(concept[key][1]))
    elif key == 'neg':
        concept[key] = delete_redundant_parenthesis(concept[key])
    return concept


def cnf(concept):
    key = list(concept.keys())[0]

    # group the operators in couples
    if (key == 'and' or key == 'or') and len(concept[key]) > 2:
        new_term = {key: concept[key][1:]}
        concept[key] = [concept[key][0], new_term]

    if key == 'forall' or key == 'exists':
        concept[key] = (concept[key][0], cnf(concept[key][1]))

    elif key == 'or' or key == 'and':
        x1 = cnf(concept[key][0])
        x2 = cnf(concept[key][1])

        if 'and' not in x1.keys():  # x1 is atomic
            x1 = {'and': [x1]}

        if 'and' not in x2.keys():  # x2 is atomic
            x2 = {'and': [x2]}

        if key == 'and':
            concept = {'and': x1['and'] + x2['and']}
        elif key == 'or':
            concept = {'and': [{'or': [t1, t2]} for t1 in x1['and'] for t2 in x2['and']]}

    elif key == 'neg':
        if 'neg' in concept[key].keys():
            concept = cnf(concept[key][key])
        elif 'and' in concept[key].keys():  # demorgan
            concept = {'or': [{'neg': concept[key]['and'][0]}, {'neg': concept[key]['and'][1]}]}
        elif 'or' in concept[key].keys():
            concept = {'and': [{'neg': concept[key]['or'][0]}, {'neg': concept[key]['or'][1]}]}
    return concept


def nnf(concept):
    """ this recursive function convert an axiom to his nnf form"""

    if 'concept' in concept.keys():  # nnf(c) = c ( recursion base case)
        return concept
    elif 'and' in concept.keys():  # nnf( c1 and c2) = nnf(c1) and nnf(c2)
        return {'and': [nnf(c) for c in concept['and']]}
    elif 'or' in concept.keys():  # nnf(c1 or c2) = nnf(c1) or nnf(c2)
        return {'or': [nnf(c) for c in concept['or']]}
    elif 'forall' in concept.keys():  # nnf( forall R.C) = forall R.nnf(C)
        return {'forall': (concept['forall'][0], nnf(concept['forall'][1]))}
    elif 'exists' in concept.keys():  # nnf(exists R.C) = exists R.nnf(C)
        return {'exists': (concept['exists'][0], nnf(concept['exists'][1]))}
    elif 'neg' in concept.keys():
        arg_neg = concept['neg']  # the argument of tge negation
        if 'neg' in arg_neg.keys():  # nnf( neg neg C ) = nnf(C)
            return nnf(arg_neg['neg'])
        elif 'concept' in arg_neg.keys():  # nnf(neg C) = neg C
            return concept
        elif 'and' in arg_neg.keys():  # nnf( neg(C1 and C2) ) = nnf(neg C1) or nnf(neg C2)
            return {'or': [nnf({'neg': c}) for c in arg_neg['and']]}
        elif 'or' in arg_neg.keys():  # nnf( neg(C1 or C2) ) = nnf(neg C1) and nnf(neg C2)
            return {'and': [nnf({'neg': c}) for c in arg_neg['or']]}
        elif 'forall' in arg_neg.keys():  # nnf( neg(forall R.C)  ) = exists R.nnf(neg C)
            return {'exists': (arg_neg['forall'][0], nnf({'neg': arg_neg['forall'][1]}))}
        elif 'exists' in arg_neg.keys():  # nnf( neg(exists R.C) ) = forall R.nnf(neg C)
            return {'forall': (arg_neg['exists'][0], nnf({'neg': arg_neg['exists'][1]}))}
