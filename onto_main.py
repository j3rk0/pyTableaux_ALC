import owlready2 as owl
from lib.onto import *
from lib.io import *


f = "file:///home/jerko/PycharmProjects/progetto_iweb/data/MusicaOnto.owl"
tbox = import_tbox(f)

for r in tbox:
    print(to_str(r))

