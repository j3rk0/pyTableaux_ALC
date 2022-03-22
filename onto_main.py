import owlready2 as owl

onto = owl.get_ontology("file:///home/jerko/PycharmProjects/progetto_iweb/data/MusicaOnto.owl").load()

print('concepts:')
for c in onto.classes():  # classi
    if c.name == 'Gruppo':
        eq = c
    print('\n')
    print(str(c.name).split('.')[-1])
    print('---------------')
    if not c.equivalent_to == []:
        print(c.equivalent_to)

    for g in c.is_a:
        print(f"{str(g)}")

# %%
print('\nrelations:')
for p in onto.properties():
    print(p.name)
