import copy
import math

import networkx as nx

from database.dao import DAO


class Model:
    def __init__(self):
        self.dictTeam = DAO.readAllTeams()
        self.dictSalary = DAO.readAllSalary()
        self.dictAppearance = DAO.readAllAppearance()
        self.grafo = nx.Graph()

    def getAnno(self):
        result = set()
        for team in self.dictTeam.values():
            result.add(team.year)
        list(result)
        return result

    def getTeams(self, anno):
        result = []
        for team in self.dictTeam.values():
            if team.year == anno:
                result.append(team)
        return result

    def getSalarioSquadre(self, anno_selezionato: int):
        self.dictSalarioSquadre = {}
        for salary in self.dictSalary.values():
            if salary.year == anno_selezionato:
                if self.dictSalarioSquadre.get(salary.team_id):
                    self.dictSalarioSquadre[salary.team_id] += salary.salary
                else:
                    self.dictSalarioSquadre[salary.team_id] = salary.salary

    def getGrafo(self, anno):
        self.grafo.clear()
        listaSquadreFiltrtata = self.getTeams(anno)
        self.getSalarioSquadre(anno)
        dictSalarioSquadre = self.dictSalarioSquadre
        self.grafo.add_nodes_from(listaSquadreFiltrtata)
        for team1 in self.grafo.nodes():
            for team2 in self.grafo.nodes():
                if team1 != team2:
                    if not self.grafo.has_edge(team2, team1):
                        peso = dictSalarioSquadre[team1.id] + dictSalarioSquadre[team2.id]
                        self.grafo.add_edge(team1, team2, weight=peso)

    def getDettagli(self, team_alfa):
        vicini = self.grafo.neighbors(team_alfa)
        result = []
        for team in vicini:
            peso = self.grafo[team_alfa][team]['weight']
            result.append((team, peso))
        result.sort(key=lambda x: x[1], reverse=True)
        return result

    def getPercorso(self, start):
        self.percorsoOttimo = []
        self.pesoOttimo = 0
        self.ricorsione([start], 0)

    def ricorsione(self, parziale, peso_parziale):
        if peso_parziale > self.pesoOttimo:
            self.pesoOttimo = peso_parziale
            self.percorsoOttimo = parziale.copy()
        lista_iniziale = []
        nodo_corrente = parziale[-1]
        if len(parziale) < 2:
            for nodo in self.grafo.neighbors(nodo_corrente):
                if nodo not in parziale:
                    peso = self.grafo[nodo_corrente][nodo]['weight']
                    lista_iniziale.append((nodo, peso))
            lista_iniziale.sort(key=lambda x: x[1], reverse=True)
            lista_ottima = lista_iniziale[:3]
        else:
            for nodo in self.grafo.neighbors(nodo_corrente):
                if nodo not in parziale:
                    peso = self.grafo[nodo_corrente][nodo]['weight']
                    ultimo_peso = self.grafo[parziale[-2]][nodo_corrente]['weight']
                    if peso < ultimo_peso:
                        lista_iniziale.append((nodo, peso))
            lista_iniziale.sort(key=lambda x: x[1], reverse=True)
            lista_ottima = lista_iniziale[:3]

        for nodo, peso in lista_ottima:
            parziale.append(nodo)
            nuovo_peso_parziale = peso_parziale + peso
            self.ricorsione(parziale, nuovo_peso_parziale)
            parziale.pop()

    # CONSEGNA1
    '''Punto 1

    Si costruisca un grafo non orientato e pesato in cui:

    i nodi rappresentano le squadre

    esiste un arco tra due squadre se hanno almeno un giocatore che ha militato in entrambe

    il peso dell’arco è il numero totale di stagioni in cui i giocatori condivisi hanno giocato per entrambe le squadre

    📌 Note tipiche d’esame:

    una stagione conta una sola volta per giocatore

    più giocatori ⇒ somma delle stagioni

    non considerare stagioni fuori dal database

    🎯 Perché è plausibile:

    stesso identico schema concettuale di Baseball

    cambia solo la misura del peso

    perfetta per vedere se sai precomputare bene'''

    def dictGiocatori_x_team(self):
        result = {}
        for appearance in self.dictAppearance.values():
            if result.get(appearance.player_id):
                if result[appearance.player_id].get(appearance.team_code):
                    result[appearance.player_id][appearance.team_code] += 1
                else:
                    result[appearance.player_id][appearance.team_code] = 1
            else:
                result[appearance.player_id] = {appearance.team_code: 1}
        return result

    def grafo2(self):
        self.grafo2 = nx.Graph()
        dictGiocatori_x_team = self.dictGiocatori_x_team()
        # nodi
        result = []
        for team in self.dictTeam.values():
            result.append(team.team_code)
        nodi = list(set(result))
        self.grafo2.add_nodes_from(nodi)
        dictArchi = {}
        for giocatore, squadre in dictGiocatori_x_team.items():
            teams = list(squadre.keys())
            for i in range(len(teams)):
                for j in range(i + 1, len(teams)):
                    t1, t2 = teams[i], teams[j]
                    coppia = tuple(sorted((t1, t2)))
                    peso = min(squadre[t1], squadre[t2])
                    dictArchi[coppia] = dictArchi.get(coppia, 0) + peso
        for arco, peso in dictArchi.items():
            if self.grafo2.has_node(arco[0]) and self.grafo2.has_node(arco[1]):
                self.grafo2.add_edge(arco[0], arco[1], weight=peso)
        print(self.grafo2)
































