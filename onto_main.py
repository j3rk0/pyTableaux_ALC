import owlready2 as owl
from lib.onto import *
from lib.io import *

f = "file:///home/jerko/PycharmProjects/progetto_iweb/data/MusicaOnto.owl"


#%%
onto = Ontology()
tbox = onto.import_onto(f)

for t in tbox:
    print(to_str(t))

# %%

input_mgr = InputManager()

C = input_mgr.parse_manchester('Musicista')
print(to_str(C))

# %%
from lib.engine import InferenceEngine

eng = InferenceEngine(T=tbox)

res = eng.check_satisfy(C)

#%%
output_mgr = OutputManager(onto)
graph = output_mgr.build_dot_graph(res, show='atomic', shape='box')
graph.view()

