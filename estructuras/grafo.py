"""Grafo ponderado no dirigido: matriz y lista de adyacencia."""

from __future__ import annotations

from typing import Optional

from estructuras.lista_enlazada import ListaEnlazada  # type: ignore
from estructuras.cola import Cola  # type: ignore
from estructuras.pila import Pila  # type: ignore
from estructuras.cola_prioridad import ColaPrioridad  # type: ignore


class _Arista:
    """Arista del grafo: destino y distancia."""

    def __init__(self, destino: int, distancia: float) -> None:
        self.destino: int = destino
        self.distancia: float = distancia

    def __repr__(self) -> str:
        return f"Arista(destino={self.destino}, distancia={self.distancia})"


class _TablaNombres:
    """Tabla propia para traducir nombre de barrio a indice (sin dict).

    Usa una lista enlazada de pares (nombre, indice).
    """

    def __init__(self) -> None:
        self._pares: ListaEnlazada[tuple[str, int]] = ListaEnlazada()

    def obtener_indice(self, nombre: str) -> Optional[int]:
        """Retorna el indice del nombre o None. # recorre todos los elementos."""
        temp = self._pares._cabeza
        while temp is not None:
            nom, idx = temp.dato
            if nom == nombre:
                return idx
            temp = temp._siguiente
        return None

    def agregar(self, nombre: str, indice: int) -> None:
        """Asocia nombre con indice si no existe ya. # recorre todos los elementos."""
        if self.obtener_indice(nombre) is None:
            self._pares.insertar_final((nombre, indice))

    def obtener_nombre(self, indice: int) -> Optional[str]:
        """Retorna el nombre asociado al indice. # recorre todos los elementos."""
        temp = self._pares._cabeza
        while temp is not None:
            nom, idx = temp.dato
            if idx == indice:
                return nom
            temp = temp._siguiente
        return None


class Grafo:
    """Grafo ponderado no dirigido con matriz y lista de adyacencia.

    Soporta ambos modos de representacion. La conversion nombre-indice se hace
    con una estructura propia (lista enlazada de pares), no con dict.

    Atributos:
        _dirigido: si el grafo es dirigido (False por defecto).
        _nombres: tabla propia nombre -> indice.
        _indices: lista de nombres por indice.
        _matriz: matriz de adyacencia (arreglo [[0.0]*n for _ in range(n)]).
        _lista: lista de adyacencia (ListaEnlazada de Arista por vertice).
    """

    def __init__(self, dirigido: bool = False) -> None:
        """Crea un grafo vacio. # es rapido."""
        self._dirigido: bool = dirigido
        self._nombres = _TablaNombres()
        self._indices: list[str] = []
        self._matriz: list = []
        self._lista: list = []

    def _indice_de(self, nombre: str) -> int:
        """Retorna el indice del barrio, agregandolo si es nuevo. # recorre todos los elementos."""
        indice = self._nombres.obtener_indice(nombre)
        if indice is None:
            indice = len(self._indices)
            self._nombres.agregar(nombre, indice)
            self._indices.append(nombre)
            n = len(self._indices)
            # Crear nueva fila y columna en la matriz
            nueva_matriz: list = [[0.0] * n for _ in range(n)]
            for i in range(n - 1):
                for j in range(n - 1):
                    nueva_matriz[i][j] = self._matriz[i][j]
            self._matriz = nueva_matriz
            nueva_lista: list = []
            for i in range(n - 1):
                nueva_lista.append(self._lista[i])
            nueva_lista.append(ListaEnlazada())
            self._lista = nueva_lista
        return indice

    def agregar_vertice(self, nombre: str) -> None:
        """Agrega un vertice (barrio) al grafo. # recorre todo dos veces, puede ser lento. por redimension matriz"""
        self._indice_de(nombre)

    def agregar_arista(self, origen: str, destino: str, distancia: float) -> None:
        """Agrega una arista bidireccional con la distancia dada. # recorre todo dos veces, puede ser lento."""
        i = self._indice_de(origen)
        j = self._indice_de(destino)
        self._matriz[i][j] = distancia
        if not self._dirigido:
            self._matriz[j][i] = distancia
        # Lista de adyacencia: evitar duplicados
        self._insertar_arista_lista(i, j, distancia)
        if not self._dirigido:
            self._insertar_arista_lista(j, i, distancia)

    def _insertar_arista_lista(self, i: int, j: int, distancia: float) -> None:
        temp = self._lista[i]._cabeza
        existe = False
        while temp is not None:
            if temp.dato.destino == j:
                temp.dato.distancia = distancia
                existe = True
                break
            temp = temp._siguiente
        if not existe:
            self._lista[i].insertar_final(_Arista(j, distancia))

    def grado(self, barrio: str) -> int:
        """Retorna el grado del barrio (numero de aristas). # recorre todos los elementos."""
        indice = self._nombres.obtener_indice(barrio)
        if indice is None:
            return 0
        return self._lista[indice].__len__()

    def orden(self) -> int:
        """Retorna el numero de vertices. # es rapido."""
        return len(self._indices)

    def son_adyacentes(self, a: str, b: str) -> bool:
        """Indica si hay arista directa entre dos barrios. # recorre todos los elementos."""
        ia = self._nombres.obtener_indice(a)
        ib = self._nombres.obtener_indice(b)
        if ia is None or ib is None:
            return False
        return self._matriz[ia][ib] != 0.0

    def _vecinos_ordenados(self, indice: int) -> list[int]:
        """Retorna los indices de vecinos ordenados alfabeticamente por nombre. # O(n log n)"""
        vecinos: list[int] = []
        temp = self._lista[indice]._cabeza
        while temp is not None:
            vecinos.append(temp.dato.destino)
            temp = temp._siguiente
        vecinos.sort(key=lambda idx: self._indices[idx])
        return vecinos

    def imprimir_matriz(self) -> None:
        """Imprime la matriz de adyacencia. # recorre todo dos veces, puede ser lento."""
        n = self.orden()
        print("      ", end="")
        for i in range(n):
            print(f"{self._indices[i]:12}", end="")
        print()
        for i in range(n):
            print(f"{self._indices[i]:12}", end="")
            for j in range(n):
                print(f"{self._matriz[i][j]:12.1f}", end="")
            print()

    def imprimir_lista(self) -> None:
        """Imprime la lista de adyacencia. # revisa barrios y vias."""
        n = self.orden()
        for i in range(n):
            nombre = self._indices[i]
            vecinos = self._vecinos_ordenados(i)
            partes = []
            for j in vecinos:
                arista = self._obtener_arista(i, j)
                dist = arista.distancia if arista else 0.0
                partes.append(f"{self._indices[j]}({dist})")
            print(f"{nombre}: {' -> '.join(partes) if partes else '(sin vecinos)'}")

    def _obtener_arista(self, i: int, j: int) -> Optional[_Arista]:
        temp = self._lista[i]._cabeza
        while temp is not None:
            if temp.dato.destino == j:
                return temp.dato
            temp = temp._siguiente
        return None

    def cargar_desde_archivo(self, ruta: str) -> None:
        """Carga aristas desde un archivo con formato origen;destino;distancia. # lee el archivo y arma el mapa."""
        with open(ruta, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea or linea.startswith("#"):
                    continue
                partes = linea.split(";")
                if len(partes) != 3:
                    continue
                origen, destino, distancia = partes
                self.agregar_arista(origen.strip(), destino.strip(), float(distancia.strip()))

    # ---------- Recorridos ----------

    def bfs(self, inicio: str) -> list[str]:
        """Busqueda en anchura desde un barrio, visitando vecinos en orden alfabetico. # revisa barrios y vias."""
        indice = self._nombres.obtener_indice(inicio)
        if indice is None:
            return []
        visitados: list[bool] = [False] * self.orden()
        orden_visita: list[str] = []
        cola: Cola[int] = Cola()
        visitados[indice] = True
        cola.encolar(indice)
        while not cola.esta_vacia():
            actual = cola.desencolar()
            orden_visita.append(self._indices[actual])
            for vecino in self._vecinos_ordenados(actual):
                if not visitados[vecino]:
                    visitados[vecino] = True
                    cola.encolar(vecino)
        return orden_visita

    def dfs_recursivo(self, inicio: str) -> list[str]:
        """Busqueda en profundidad recursiva desde un barrio. # revisa barrios y vias."""
        indice = self._nombres.obtener_indice(inicio)
        if indice is None:
            return []
        visitados: list[bool] = [False] * self.orden()
        orden_visita: list[str] = []

        def dfs(idx: int) -> None:
            visitados[idx] = True
            orden_visita.append(self._indices[idx])
            for vecino in self._vecinos_ordenados(idx):
                if not visitados[vecino]:
                    dfs(vecino)

        dfs(indice)
        return orden_visita

    def dfs_iterativo(self, inicio: str) -> list[str]:
        """Busqueda en profundidad iterativa con Pila. # revisa barrios y vias."""
        indice = self._nombres.obtener_indice(inicio)
        if indice is None:
            return []
        visitados: list[bool] = [False] * self.orden()
        orden_visita: list[str] = []
        pila: Pila[int] = Pila()
        pila.apilar(indice)
        while not pila.esta_vacia():
            actual = pila.desapilar()
            if visitados[actual]:
                continue
            visitados[actual] = True
            orden_visita.append(self._indices[actual])
            # Insertar vecinos en reversa para visitar en orden alfabetico
            vecinos = self._vecinos_ordenados(actual)
            for vecino in reversed(vecinos):
                if not visitados[vecino]:
                    pila.apilar(vecino)
        return orden_visita

    def es_conexo_desde(self, inicio: str) -> bool:
        """Verifica si todos los barrios son alcanzables desde un barrio. # revisa barrios y vias."""
        return len(self.bfs(inicio)) == self.orden()

    # ---------- Dijkstra ----------

    def dijkstra(self, origen: str, destino: str) -> tuple[float, list[str]]:
        """Ruta mas corta entre dos barrios con Dijkstra. # busca la ruta mas corta, puede tardar.

        Retorna (distancia_minima, ruta_completa) reconstruida con la pila.
        """
        io = self._nombres.obtener_indice(origen)
        id_ = self._nombres.obtener_indice(destino)
        if io is None or id_ is None:
            return float("inf"), []
        n = self.orden()
        distancias: list[float] = [float("inf")] * n
        predecesores: list[Optional[int]] = [None] * n
        visitados: list[bool] = [False] * n
        distancias[io] = 0.0

        cola_prio: ColaPrioridad[tuple[float, int]] = ColaPrioridad()
        cola_prio.encolar((0.0, io), urgente=True)

        while not cola_prio.esta_vacia():
            d_actual, actual = cola_prio.desencolar()
            if visitados[actual]:
                continue
            visitados[actual] = True
            if actual == id_:
                break
            for vecino in self._vecinos_ordenados(actual):
                if visitados[vecino]:
                    continue
                arista = self._obtener_arista(actual, vecino)
                if arista is None:
                    continue
                nueva_dist = d_actual + arista.distancia
                if nueva_dist < distancias[vecino]:
                    distancias[vecino] = nueva_dist
                    predecesores[vecino] = actual
                    cola_prio.encolar((nueva_dist, vecino), urgente=True)

        # Reconstruir ruta con pila
        ruta: list[str] = []
        if distancias[id_] == float("inf"):
            return float("inf"), []
        pila_ruta: Pila[int] = Pila()
        actual: Optional[int] = id_
        while actual is not None:
            pila_ruta.apilar(actual)
            actual = predecesores[actual]
        while not pila_ruta.esta_vacia():
            ruta.append(self._indices[pila_ruta.desapilar()])
        return distancias[id_], ruta

    # ---------- Arbol de expansion minima ----------

    def prim(self) -> tuple[list[tuple[str, str, float]], float]:
        """Arbol de expansion minima con Prim desde el primer vertice. # recorre todo dos veces, puede ser lento.

        Retorna (aristas_seleccionadas, distancia_total).
        """
        n = self.orden()
        if n == 0:
            return [], 0.0
        visitados: list[bool] = [False] * n
        aristas: list[tuple[str, str, float]] = []
        total = 0.0
        visitados[0] = True
        for _ in range(n - 1):
            mejor: Optional[tuple[int, int, float]] = None
            for i in range(n):
                if not visitados[i]:
                    continue
                for vecino in self._vecinos_ordenados(i):
                    if visitados[vecino]:
                        continue
                    arista = self._obtener_arista(i, vecino)
                    if arista is None:
                        continue
                    if mejor is None or arista.distancia < mejor[2]:
                        mejor = (i, vecino, arista.distancia)
            if mejor is None:
                break
            i, j, d = mejor
            visitados[j] = True
            aristas.append((self._indices[i], self._indices[j], d))
            total += d
        return aristas, total

    def kruskal(self) -> tuple[list[tuple[str, str, float]], float]:
        """Arbol de expansion minima con Kruskal. # ordena las vias."""
        aristas: list[tuple[float, int, int]] = []
        n = self.orden()
        for i in range(n):
            temp = self._lista[i]._cabeza
            while temp is not None:
                if i < temp.dato.destino:
                    aristas.append((temp.dato.distancia, i, temp.dato.destino))
                temp = temp._siguiente
        # Ordenar por distancia (insercion directa, no sort prohibido sobre arreglos de nodos)
        aristas_ordenadas: list[tuple[float, int, int]] = []
        for a in aristas:
            insertada = False
            for k in range(len(aristas_ordenadas)):
                if a[0] < aristas_ordenadas[k][0]:
                    aristas_ordenadas.insert(k, a)
                    insertada = True
                    break
            if not insertada:
                aristas_ordenadas.append(a)

        padre: list[int] = list(range(n))

        def encontrar(x: int) -> int:
            while padre[x] != x:
                padre[x] = padre[padre[x]]
                x = padre[x]
            return x

        def unir(x: int, y: int) -> bool:
            rx, ry = encontrar(x), encontrar(y)
            if rx == ry:
                return False
            padre[rx] = ry
            return True

        seleccionadas: list[tuple[str, str, float]] = []
        total = 0.0
        for d, i, j in aristas_ordenadas:
            if unir(i, j):
                seleccionadas.append((self._indices[i], self._indices[j], d))
                total += d
                if len(seleccionadas) == n - 1:
                    break
        return seleccionadas, total

    def floyd_warshall(self) -> list[list[float]]:
        """Matriz de distancias minimas entre todos los barrios (bonificacion). # revisa todas las combinaciones, puede ser muy lento."""
        n = self.orden()
        INF = float("inf")
        dist: list[list[float]] = [[INF] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0.0
            temp = self._lista[i]._cabeza
            while temp is not None:
                dist[i][temp.dato.destino] = temp.dato.distancia
                temp = temp._siguiente
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        return dist
