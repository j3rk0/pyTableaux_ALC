
""" in this project axioms are expressed as dictionary as following:

 {'r_name':'R'} // relation
 {'c_name':'C'} //atomic concept

 {'and':[C1,...,Cn]} //conjunction
 { 'or':[C1,...,Cn]} //disjunction

 { 'neg': C } //negation

 { 'forall':(R,C)} //universal quantifier
 { 'exists':(R,C)} //existential quantifier

"""


def nnf(concept):
    """ this function convert an axiom to his nnf form"""

    if 'c_name' in concept.keys():  # nnf(c) = c
        return concept
    elif 'and' in concept.keys(): # nnf( c1 and c2) = nnf(c1) and nnf(c2)
        return {'and': [nnf(c) for c in concept['and']]}
    elif 'or' in concept.keys():  # nnf(c1 or c2) = nnf(c1) or nnf(c2)
        return {'or': [nnf(c) for c in concept['or']]}
    elif 'forall' in concept.keys(): # nnf( forall R.C) = forall R.nnf(C)
        return {'forall': (concept['forall'][0], nnf(concept['forall'][1]))}
    elif 'exists' in concept.keys(): # nnf(exists R.C) = exists R.nnf(C)
        return {'exists': (concept['exists'][0], nnf(concept['exists'][1]))}
    elif 'neg' in concept.keys():
        arg_neg = concept['neg']
        if 'neg' in arg_neg.keys(): # nnf( neg neg C ) = nnf(C)
            return nnf(arg_neg['neg'])
        elif 'c_name' in arg_neg.keys(): # nnf(neg C) = neg C
            return concept
        elif 'and' in arg_neg.keys():  # nnf( neg(C1 and C2) ) = nnf(neg C1) or nnf(neg C2)
            return {'or': [ nnf({'neg': c}) for c in arg_neg['and']]}
        elif 'or' in arg_neg.keys():  # nnf( neg(C1 or C2) ) = nnf(neg C1) and nnf(neg C2)
            return {'and': [ nnf({'neg': c}) for c in arg_neg['or']]}
        elif 'forall' in arg_neg.keys():  # nnf( neg(forall R.C)  ) = exists R.nnf(neg C)
            return {'exists': (arg_neg['forall'][0], nnf({'neg':arg_neg['forall'][1]}))}
        elif 'exists' in arg_neg.keys():  # nnf( neg(exists R.C) ) = forall R.nnf(neg C)
            return {'forall': (arg_neg['exists'][0], nnf({'neg':arg_neg['exists'][1]}))}

def to_str(concept):
    """print a concept in dict format to a string"""
    ret = []
    if 'and' in concept.keys():
        ret.append("(")
        for c in concept['and']:
            ret.append(to_str(c))
            ret.append('and')
        ret.pop()  # rimuovo and inutile
        ret.append(')')
    elif 'or' in concept.keys():
        ret.append('(')
        for c in concept['or']:
            ret.append(to_str(c))
            ret.append('or')
        ret.pop()
        ret.append(')')
    elif 'neg' in concept.keys():
        ret.append(f"not({to_str(concept['neg'])})")
    elif 'forall' in concept.keys():
        ret.append(f"forall {to_str(concept['forall'][0])}.{to_str(concept['forall'][1])}")
    elif 'exists' in concept.keys():
        ret.append(f"exists {to_str(concept['exists'][0])}.{to_str(concept['exists'][1])}")
    elif 'c_name' in concept.keys():
        ret.append(concept['c_name'])
    elif 'r_name' in concept.keys():
        ret.append(concept['r_name'])

    return " ".join(ret)
