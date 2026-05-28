import networkx as nx
import collections
from database.DAO import DAO


class Model:
    def __init__(self):
        # Mappe "Globali" (Non dipendono dal singolo genere, quindi va bene caricarle una volta sola qui)
        self.idMapGenere = {}
        self.idMapPopolarita = {}

        for p in DAO.getPop():
            self.idMapPopolarita[p[0]] = p[1]

        for g in DAO.getGeneri():
            self.idMapGenere[g[0]] = g[1]

        # Variabili relative al singolo Grafo (Verranno resettate in creaGrafo)
        self.grafo = nx.DiGraph()
        self.idMapArtisti = {}
        self.dizionarioClienteArtisti = collections.defaultdict(set)

    def creaGrafo(self, genere):
        # --- 1. RESET TOTALE DEI DATI DEL GRAFO ---
        self.grafo.clear()
        self.idMapArtisti.clear()  # FONDAMENTALE! Altrimenti tieni in memoria artisti di generi vecchi
        self.dizionarioClienteArtisti.clear()

        # --- 2. CREAZIONE NODI ---
        listaNodi = DAO.getAllNodi(genere)
        if len(listaNodi) == 0:
            print("attenzione nessun nodo")
            return  # Se non ci sono nodi, fermo subito tutto

        self.grafo.add_nodes_from(listaNodi)

        # idmap artista id - nome
        for artista in listaNodi:
            self.idMapArtisti[artista.ArtistId] = artista

        # --- 3. PREPARAZIONE DATI PER GLI ARCHI ---
        archi = DAO.getArchi(genere)  # La query che estrae (Cliente, Artista)

        for c, aID in archi:
            # sfrutto dizionario di artisti del genere selezionato
            if int(aID) in self.idMapArtisti:
                self.dizionarioClienteArtisti[c].add(int(aID)) #essendo un set lo aggiunge una sola volta l' artista per cliente

        # Stampa di controllo: .items() per vedere sia la chiave (cliente) che il valore (set di artisti)
        for chiaveCliente, valoreSetArtisti in self.dizionarioClienteArtisti.items():
            print(f"Cliente {chiaveCliente} - artisti:  {valoreSetArtisti}")
        #cilcerei sui nodi e se artista in lista cliente 1 allora posso joinarlo con artsita 2 (!=) e faccio if popolarità
        for chiaveCliente, valoreSetArtisti in self.dizionarioClienteArtisti.items():
            listaArtisti = list(valoreSetArtisti)
            for i in range(len(listaArtisti)):
                for j in range(i+1, len(listaArtisti)):
                    idartista1 = listaArtisti[i]
                    idartista2 = listaArtisti[j]
                    a1 = self.idMapArtisti[idartista1]
                    a2 = self.idMapArtisti[idartista2]
                    pop1 = self.idMapPopolarita[idartista1]
                    pop2 = self.idMapPopolarita[idartista2]
                    tot = pop1 + pop2
                    if pop1 > pop2:
                        self.grafo.add_edge(a1, a2, weight=tot)
                    elif pop1 < pop2:
                        self.grafo.add_edge(a2, a1, weight=tot)
                    else: #pop1 == pop2
                        self.grafo.add_edge(a1, a2, weight=tot)
                        self.grafo.add_edge(a2, a1, weight=tot)



        print(self.getStatisticheGrafo())
        






    def getStatisticheGrafo(self):
        return self.grafo.number_of_nodes(), self.grafo.number_of_edges()