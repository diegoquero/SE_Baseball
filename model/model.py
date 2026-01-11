import copy
import math

import networkx as nx

from database.dao import DAO


class Model:
    def __init__(self):
        self.dictTeams = DAO.readAllTeams()
        self.G = nx.Graph()


    def getListaAnno (self):
        self.lista_anno = []
        dictTeams= DAO.readAllTeams()
        for t in dictTeams.keys():
            if dictTeams[t].year >= 1980:
                self.lista_anno.append(dictTeams[t].year)
        self.lista_anno = set(self.lista_anno)
        return self.lista_anno



    def getSalarioSquadre(self):
        self.salario_squadre = {}
        self.dictSalario = DAO.readAllSalary()
        for s in self.dictSalario.keys():
            team_id = self.dictSalario[s].team_id
            if self.salario_squadre.get(team_id):
                self.salario_squadre[team_id] += self.dictSalario[s].salary
            else:
                self.salario_squadre[team_id] = self.dictSalario[s].salary
        return self.salario_squadre

    def getGrafoSquadre(self, anno):
        self.dictSquadreFiltrato = {}
        dictSalario = self.getSalarioSquadre()
        for team in self.dictTeams.keys():
            if self.dictTeams[team].year == int(anno):
                self.dictSquadreFiltrato[team] = self.dictTeams[team]
        for i in self.dictSquadreFiltrato.keys():
            for j in self.dictSquadreFiltrato.keys():
                if i != j:
                    if dictSalario.get(i) and dictSalario.get(j):
                        self.G.add_edge(self.dictSquadreFiltrato[i], self.dictSquadreFiltrato[j], weight= dictSalario[i] + dictSalario[j])

    def getPercorsoMassimo(self, start):
        oggetto_start = self.dictSquadreFiltrato[start]
        self._bestPath = [oggetto_start]
        self._bestEdgeWeights = []
        self._bestTotal = 0
        self.neighbors_sorted = {}
        for v in self.G.nodes():
            list = []
            for u in self.G.neighbors(v):
                w = self.G[v][u].get("weight")
                list.append((u, w))
            list.sort(key=lambda x: x[1], reverse=True)
            self.neighbors_sorted[v] = list

        self.dfs([oggetto_start], [], 0, math.inf)

        return self._bestPath, self._bestEdgeWeights, self._bestTotal

    # --- DFS con backtracking ---
    def dfs(self,path, edgeW, total, last_w):
        # aggiorno best (cammino valido sempre, anche lunghezza 1)
        if total > self._bestTotal:
            self._bestTotal = total
            self._bestPath = path.copy()
            self._bestEdgeWeights = edgeW.copy()

        last = path[-1]

        # Considera solo i primi K archi (in ordine decrescente),
        # ma saltando quelli che non rispettano vincoli.
        considered = 0
        for (nxt, w) in self.neighbors_sorted[last]:
            if considered >= 3:
                break

            # vincolo pesi strettamente decrescenti
            if w >= last_w:
                continue

            # vincolo cammino semplice
            if nxt in path:
                continue

            # questo arco è un candidato valido => lo conto nei "K considerati"
            considered += 1

            path.append(nxt)
            edgeW.append(w)
            self.dfs(path, edgeW, total + w, w)
            edgeW.pop()
            path.pop()






