import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_dd_anno(self):
        listaAnni = self._model.getAnno()
        result = []
        for anno in listaAnni:
            result.append(ft.dropdown.Option(anno))
        return result

    def handle_squadre_anno(self, e):
        anno = int(self._view.dd_anno.value)
        self._view.txt_out_squadre.clean()
        lista_squadre_filtrate = self._model.getTeams(anno)
        num_squadre = len(lista_squadre_filtrate)
        self._view.txt_out_squadre.controls.append(ft.Text(f'Numero di squadre :{num_squadre}'))
        for team in lista_squadre_filtrate:
            self._view.txt_out_squadre.controls.append(ft.Text(f'{team.team_code} ({team.name})'))
        self._view.pulsante_crea_grafo.disabled = False
        self._view.update()




    def handle_crea_grafo(self, e):
        anno = int(self._view.dd_anno.value)
        self._model.getGrafo(anno)
        self._view.dd_squadra.clean()
        for team in self._model.grafo.nodes():
            self._view.dd_squadra.options.append(ft.dropdown.Option(text= f'{team.team_code} ({team.name})', key = team.id))
        self._view.dd_squadra.disabled = False
        self._view.update()

    def handle_dettagli(self, e):
        squadra_id = int(self._view.dd_squadra.value)
        squadra = self._model.dictTeam[squadra_id]
        listaVicini = self._model.getDettagli(squadra)
        self._view.txt_risultato.clean()
        for vicini in listaVicini:
            self._view.txt_risultato.controls.append(ft.Text(f'{vicini[0].team_code} ({vicini[0].name}): peso {vicini[1]}'))
        self._view.update()



    def handle_percorso(self, e):
        squadra_id = int(self._view.dd_squadra.value)
        squadra = self._model.dictTeam[squadra_id]

        self._view.txt_risultato.clean()
        self._model.getPercorso(squadra)
        listaPercorso = self._model.percorsoOttimo
        pesoTotale = self._model.pesoOttimo
        for i in range(len(listaPercorso)-1):
            s1 = listaPercorso[i]
            s2 = listaPercorso[i+1]
            peso = self._model.grafo[s1][s2]['weight']
            self._view.txt_risultato.controls.append(ft.Text(f'{s1.team_code} ({s1.name})-->{s2.team_code} ({s2.name}): peso - {peso}'))
        self._view.txt_risultato.controls.append(ft.Text(f'peso totale: {pesoTotale}'))
        self._view.update()

    def handle_abilita_pulsanti(self, e):
        self._view.pulsante_dettagli.disabled = False
        self._view.pulsante_percorso.disabled = False
        self._view.update()
        self._view.update()
