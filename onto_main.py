import owlready2 as owl
from lib.onto import *
from lib.io import *

f = "file:///home/jerko/PycharmProjects/progetto_iweb/data/MusicaOnto.owl"

#%%
tbox = import_tbox(f)

for t in tbox:
    print(gci_to_str(t))

# %%

C = parse_manchester('Compositore and ( haScritto some Traccia )')
print(to_str(C))

# %%
from lib.engine import InferenceEngine

eng = InferenceEngine(T=tbox)

res = eng.check_satisfy(C)

#%%
graph = build_dot_graph(res, show='atomic', shape='box')
graph.view()
