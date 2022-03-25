import graphviz as gviz
import re


def to_str(concept):
    """ recursive function to print a concept in dict format to a string """
    ret = []  # buffer to build the string

    if 'and' in concept.keys():
        ret += [f"({to_str(concept['and'][0])}"] + [f"\u2293 {to_str(c)}" for c in concept['and'][1:]] + [')']

    elif 'or' in concept.keys():
        ret += [f"({to_str(concept['or'][0])}"] + [f"\u2294 {to_str(c)}" for c in concept['or'][1:]] + [')']

    elif 'neg' in concept.keys():  # recursively print neg argument
        ret.append(f"\uFFE2{to_str(concept['neg'])}")
    elif 'forall' in concept.keys():  # recursively print forall arguments
        ret.append(f"\u2200{to_str(concept['forall'][0])}.{to_str(concept['forall'][1])}")
    elif 'exists' in concept.keys():  # recursively print exists argumentsnot({
        ret.append(f"\u2203{to_str(concept['exists'][0])}.{to_str(concept['exists'][1])}")
    elif 'concept' in concept.keys():  # print concept name (recursion base case)
        ret.append(concept['concept'])
    elif 'relation' in concept.keys():  # print concept name (recursion base case)
        ret.append(concept['relation'])

    if 'args' in concept.keys():
        ret.append(f"( x{concept['args'][0]}")
        for x in concept['args'][1:]:
            ret.append(f", x{x}")
        ret.append(")")

    return " ".join(ret)  # join buffer element


def build_dot_graph(G, show='all', shape='box'):
    dot = gviz.Digraph('tableaux', comment='Tableaux result', format='png')
    for i in range(G.last_individual + 1):

        if show == 'all':
            lc = '\n'.join([to_str(c) for c in G.L[i]])
            dot.node(f"x{i}", f"x{i}\n--------\n{lc}", shape=shape)
        elif show == 'atomic':
            lc = "; ".join([to_str(c) for c in G.L[i] if 'concept' in c.keys() or
                            ('neg' in c.keys() and 'concept' in c['neg'].keys())])
            dot.node(f"x{i}", f"x{i}:{{{lc}}}", shape=shape)
        else:
            dot.node(f"x{i}", shape=shape)

    for rel in G.E.keys():
        for rx, ry in G.E[rel]:
            dot.edge(f"x{rx}", f"x{ry}", label=rel)

    return dot


def man_to_list(formula_ms):  # parse a manchester syntax string in a list

    # FORCE OPERATOR TO BE SYMBOL TO PREVENT MISMATCH WITH VARIABLES CONTAINING OPERATOR STRING
    formula_ms = formula_ms.replace(' or ', '|')
    formula_ms = formula_ms.replace(')or ', ')|')
    formula_ms = formula_ms.replace(' or(', '|(')
    formula_ms = formula_ms.replace(')or(', ')|(')
    formula_ms = formula_ms.replace(' and ', '&')
    formula_ms = formula_ms.replace(')and ', ')&')
    formula_ms = formula_ms.replace(' and(', '&(')
    formula_ms = formula_ms.replace(')and(', ')&(')
    formula_ms = formula_ms.replace(' Not ', '-')
    formula_ms = formula_ms.replace(')Not ', ')-')
    formula_ms = formula_ms.replace(' Not(', '-(')
    formula_ms = formula_ms.replace(')Not(', ')-(')
    formula_ms = formula_ms.replace(' some ', '%')
    formula_ms = formula_ms.replace(')some ', ')%')
    formula_ms = formula_ms.replace(' some(', '%(')
    formula_ms = formula_ms.replace(')some(', ')%(')
    formula_ms = formula_ms.replace(' only ', '£')
    formula_ms = formula_ms.replace(')only ', ')£')
    formula_ms = formula_ms.replace(' only(', '£(')
    formula_ms = formula_ms.replace(')only(', ')£(')
    formula_ms = formula_ms.replace(' ', '')
    buffer = ''
    res = []
    i = 0
    key = ''
    while i < len(formula_ms):

        if formula_ms[i] == '(':  # unpack parhentesis
            level = 1
            count = 0
            while not level == 0 and count + i < len(formula_ms):
                count += 1
                if formula_ms[i + count] == '(':
                    level += 1
                elif formula_ms[i + count] == ')':
                    level -= 1
            assert level == 0 and 'ERROR: PARHENTESIS NOT MATCHING'
            res.append(man_to_list(formula_ms[i + 1:i + count]))
            buffer = ''
            i += count + 1
            continue

        buffer += formula_ms[i]
        i += 1

        sep = key
        if '&' in buffer:
            sep = '&'
            key = 'and'
        elif '-' in buffer:
            sep = '-'
            key = 'neg'
        elif '|' in buffer:
            sep = '|'
            key = 'or'
        elif '%' in buffer:
            sep = '%'
            key = 'some'
        elif '£' in buffer:
            sep = '£'
            key = 'only'

        if not key == '':
            res += buffer.split(sep) + [key]
            buffer = ''
            key = ''

    res.append(buffer)
    return [t for t in res if not t == '']


def owl_to_man(formula_owl):  # parse owl string in manchester syntax
    formula_owl = formula_owl.replace('&', 'and')
    formula_owl = formula_owl.replace('|', 'or')
    formula_owl = formula_owl.replace('.only', ' only ')
    formula_owl = formula_owl.replace('.some', ' some ')
    formula_owl = formula_owl.replace('(', ' ( ')
    formula_owl = formula_owl.replace(')', ' ) ')

    s_entry = formula_owl.split(' ')
    for i in range(len(s_entry)):
        s_entry[i] = re.sub(r'.+[.]', '', s_entry[i])
    return ' '.join(s_entry)


def list_to_dict(formula_list):  # parse a list in a string
    ret = None
    if len(formula_list) == 1:
        if type(formula_list[0]) == str:  # formula is an atomic concept
            ret = {'concept': formula_list[0]}
        elif type(formula_list[0]) == list:  # formula is a parhentesis
            ret = list_to_dict(formula_list[0])
    elif 'and' in formula_list:
        ret = {'and': []}
        i = j = 0
        while not j == len(formula_list):
            if formula_list[j] == 'and' and not i == j:  # convert each argument of the and
                ret['and'].append(list_to_dict(formula_list[i:j]))
                i = j + 1
            j += 1
        ret['and'].append(list_to_dict(formula_list[i:]))

    elif 'or' in formula_list:
        ret = {'or': []}
        i = j = 0
        while not j == len(formula_list):
            if formula_list[j] == 'or' and not i == j:  # convert each argument of the or
                ret['or'].append(list_to_dict(formula_list[i:j]))
                i = j + 1
            j += 1
        ret['or'].append(list_to_dict(formula_list[i:]))
    elif formula_list[0] == 'not':
        ret = {'neg': list_to_dict(formula_list[1:])}  # convert not argument
        pass
    elif formula_list[1] == 'some':  # convert 'some' arguments
        ret = {'exists': ({'relation': formula_list[0]}, list_to_dict(formula_list[2]))}
    elif formula_list[1] == 'only':  # convert 'only' arguments
        ret = {'forall': ({'relation': formula_list[0]}, list_to_dict(formula_list[2]))}
    else:  # what appened ?
        print('PARSER ERROR')
        return None

    return ret


def parse_manchester(formula_ms):  # parse manchester string to dict
    return list_to_dict(man_to_list(formula_ms))


def parse_owl(formula_owl):
    return parse_manchester(owl_to_man(formula_owl))
