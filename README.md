this project implement a description logic reasoner using the
tableaux method.

in this project dl formulas are expressed as a python dictionary with the following syntax:

 - relations : {'relation':'R' } 
 - atomic concepts: {'concept':'C' } 
 - conjuntions: {'and':[C1,...,Cn]}
 - disjuntions: { 'or':[C1,...,Cn]} 
 - negations: { 'neg': C }
 - universal quantifiers: { 'forall':(R,C)} 
 - existential quantifiers: { 'exists':(R,C)} 


the main class is InferenceEngine, wich can be used to build a reasoner that check the
satisfactibility of a concept wrt a tbox. 

the constructor take as argument a tbox T wrt we want to check satisfability.
if no tbox is provided reasoner will consider tbox empty.

the method check_satisfy(C) allow us to check the satisfabillity of C wrt T.
this method will return an object CompletionGraph. 

A CompletionGraph is a graph in wich each node and edge has labels.
each node of completion graph represent an individual, each edge represent a relation between
two individals. each node have multiple labels, representing concept that subsist on that individual.
each edge has one label representing the name of the relation

given a completion graph G, the attribute G.last_individual represent the index of the last individual.
for a node x the labels of x are stored in list G.L[x]. meanwhile for a given relation with name 'R' the
edges are stored in G.L['R']


in lib.io there are some function to get input from manchester syntax
as well as function to render the completion graph in dot languange of graphviz, so that we can
export it or view it as pdf, image,...