from model.model import Model
model = Model()
model.getListaAnno()

model.getGrafoSquadre(2015)
print(model.G)

sol, pesi_archi, peso_tot = model.getPercorsoMassimo(2777)
print(len(sol))
print(sol)

print('finito')
