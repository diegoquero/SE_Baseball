import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        anno = int(self._view.dd_anno.value)
        self._model.getGrafoSquadre(anno)

        for n in self._model.G.nodes():
            self._view.dd_squadra.options.append(ft.dropdown.Option(text=f'{n.team_code} ({n.name})', key=n.id))
        self._view.update()

        print(self._model.G)

    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""
        dictSalariVicini = {}
        nodo_sorgente = self._model.dictSquadreFiltrato[int(self._view.dd_squadra.value)]
        for n in self._model.G.neighbors(nodo_sorgente):
            peso = self._model.G[n][nodo_sorgente]['weight']
            dictSalariVicini[peso] = n.id
        lista_pesi = sorted(dictSalariVicini.keys(), reverse=True)
        self._view.txt_risultato.clean()
        for peso in lista_pesi:
            self._view.txt_risultato.controls.append(ft.Text(f'{self._model.dictSquadreFiltrato[dictSalariVicini[peso]].team_code} '
                                                             f'({self._model.dictSquadreFiltrato[dictSalariVicini[peso]].name})- peso {peso}'))
        self._view.update()


    def handle_percorso(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del percorso """""
        lista_nodi, lista_pesi_archi, peso_tot = self._model.getPercorsoMassimo(int(self._view.dd_squadra.value))
        self._view.txt_risultato.clean()
        for i in range(len(lista_nodi)-1) :
            self._view.txt_risultato.controls.append(ft.Text(f'{lista_nodi[i].team_code} ({lista_nodi[i].name})-->'
                                                             f'{lista_nodi[i+1].team_code} ({lista_nodi[i+1].name}) (peso: {lista_pesi_archi[i]})'))
        self._view.txt_risultato.controls.append(ft.Text(f'Peso totale:{peso_tot}'))
        self._view.update()



    """ Altri possibili metodi per gestire di dd_anno """""
    def handle_dd_anno(self):
        """ Handler per gestire i dd_anno """""
        self._model.getListaAnno()
        result = []
        for anno in self._model.lista_anno:
            result.append(ft.dropdown.Option(anno))
        return result

    def handle_squadre_anno(self, e):
        """ Handler per gestire i squadre_anno """""
        self._view.txt_out_squadre.clean()
        counter = 0
        for t in self._model.dictTeams.keys():
            if self._model.dictTeams[t].year == int(self._view.dd_anno.value):
                counter += 1
        self._view.txt_out_squadre.controls.append(ft.Text(f'numero squadre : {counter}'))


        for t in self._model.dictTeams.keys():
            if self._model.dictTeams[t].year == int(self._view.dd_anno.value):
                counter += 1
                self._view.txt_out_squadre.controls.append(ft.Text(f'{self._model.dictTeams[t].team_code} ({self._model.dictTeams[t].name})'))
        self._view.update()
