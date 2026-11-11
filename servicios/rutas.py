"""Gestion de rutas sobre el grafo del mapa de Manizales."""

from __future__ import annotations

from estructuras.grafo import Grafo  # type: ignore


class Rutas:
    """Servicio de rutas sobre el grafo ponderado de barrios.

    Atributos:
        _grafo: grafo del mapa cargado desde mapa.txt.
    """

    def __init__(self, archivo_mapa: str = "datos/mapa.txt") -> None:
        """Carga el mapa desde el archivo indicado. # lee el archivo y arma el mapa."""
        self._grafo: Grafo = Grafo()
        self._grafo.cargar_desde_archivo(archivo_mapa)

    @property
    def grafo(self) -> Grafo:
        """Retorna el grafo del mapa. # es rapido."""
        return self._grafo

    def ver_mapa(self) -> None:
        """Imprime matriz y lista de adyacencia. # recorre todo dos veces, puede ser lento."""
        print("=== MATRIZ DE ADYACENCIA ===")
        self._grafo.imprimir_matriz()
        print("\n=== LISTA DE ADYACENCIA ===")
        self._grafo.imprimir_lista()

    def grado_barrio(self, barrio: str) -> None:
        """Imprime el grado de un barrio. # recorre todos los elementos."""
        print(f"Grado del barrio '{barrio}': {self._grafo.grado(barrio)}")

    def conectividad(self, inicio: str = "Centro") -> None:
        """Verifica conectividad desde un barrio e imprime orden BFS. # revisa barrios y vias."""
        visitados = self._grafo.bfs(inicio)
        print(f"BFS desde '{inicio}': {' -> '.join(visitados)}")
        total = self._grafo.orden()
        print(f"Barrios alcanzados: {len(visitados)} de {total}")
        if len(visitados) == total:
            print("El grafo es conexo desde este barrio.")
        else:
            print("El grafo NO es conexo desde este barrio.")

    def bfs(self, inicio: str) -> None:
        """Ejecuta BFS desde un barrio. # revisa barrios y vias."""
        orden = self._grafo.bfs(inicio)
        print(f"BFS desde '{inicio}': {' -> '.join(orden)}")

    def dfs_recursivo(self, inicio: str) -> None:
        """Ejecuta DFS recursivo desde un barrio. # revisa barrios y vias."""
        orden = self._grafo.dfs_recursivo(inicio)
        print(f"DFS recursivo desde '{inicio}': {' -> '.join(orden)}")

    def dfs_iterativo(self, inicio: str) -> None:
        """Ejecuta DFS iterativo desde un barrio. # revisa barrios y vias."""
        orden = self._grafo.dfs_iterativo(inicio)
        print(f"DFS iterativo desde '{inicio}': {' -> '.join(orden)}")

    def ruta_mas_corta(self, origen: str, destino: str) -> None:
        """Calcula e imprime la ruta mas corta con Dijkstra. # busca la ruta mas corta, puede tardar."""
        distancia, ruta = self._grafo.dijkstra(origen, destino)
        if distancia == float("inf"):
            print(f"No hay ruta de '{origen}' a '{destino}'.")
            return
        print(f"Ruta mas corta de '{origen}' a '{destino}':")
        print("  " + " -> ".join(ruta))
        print(f"  Distancia total: {distancia} km")

    def red_minima(self, algoritmo: str = "prim") -> None:
        """Calcula e imprime el arbol de expansion minima. # recorre todo dos veces, puede ser lento. o O(m log m)"""
        if algoritmo.lower() == "kruskal":
            aristas, total = self._grafo.kruskal()
            nombre = "Kruskal"
        else:
            aristas, total = self._grafo.prim()
            nombre = "Prim"
        print(f"Arbol de expansion minima ({nombre}):")
        for o, d, dist in aristas:
            print(f"  {o} -- {d} ({dist} km)")
        print(f"  Distancia total: {total} km")
        print(f"  Vias seleccionadas: {len(aristas)}")

    def floyd_warshall(self) -> None:
        """Imprime la matriz de distancias minimas entre todos los barrios. # revisa todas las combinaciones, puede ser muy lento."""
        dist = self._grafo.floyd_warshall()
        nombres = []
        for i in range(self._grafo.orden()):
            nombres.append(self._grafo._indices[i])
        print("Matriz de distancias minimas (Floyd-Warshall):")
        print("      ", end="")
        for nom in nombres:
            print(f"{nom:10}", end="")
        print()
        for i, nom_i in enumerate(nombres):
            print(f"{nom_i:10}", end="")
            for j in range(len(nombres)):
                d = dist[i][j]
                print(f"{d:10.1f}" if d != float("inf") else f"{'inf':10}", end="")
            print()
