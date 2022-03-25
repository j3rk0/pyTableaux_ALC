import owlready2 as owl
from lib.onto import *
from lib.io import *


f = "file:///home/jerko/PycharmProjects/progetto_iweb/data/DrogaOnto.owl"
tbox = import_tbox(f)

for t in tbox:
    print(gci_to_str(t))


Tu,Tg = tbox_partition(tbox)

