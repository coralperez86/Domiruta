"""Lista doblemente enlazada implementada con nodos, sin colecciones del lenguaje."""

from __future__ import annotations

from typing import Generic, TypeVar

from .nodo import NodoDoble

T = TypeVar("T")


class ListaDoble(Generic[T]):
    """Lista doblemente enlazada generica.

    Permite recorrer hacia adelante y hacia atras. Se usa para el historial de
    pedidos de cada cliente, pudiendo verse del mas reciente al mas antiguo.

    Atributos:
        _cabeza: primer nodo o None.
        _cola: ultimo nodo o None.
        _tamano: cantidad de elementos.
    """

    def __init__(self) -> None:
        """Crea una lista doble vacia."""
        self._cabeza: NodoDoble[T] | None = None
        self._cola: NodoDoble[T] | None = None
        self._tamano: int = 0

    def insertar_inicio(self, dato: T) -> None:
        """Agrega un elemento al inicio de la lista. # es rapido."""
        nuevo = NodoDoble(dato)
        if self._cabeza is None:
            self._cabeza = nuevo
            self._cola = nuevo
        else:
            nuevo._siguiente = self._cabeza
            self._cabeza._anterior = nuevo
            self._cabeza = nuevo
        self._tamano += 1

    def insertar_final(self, dato: T) -> None:
        """Agrega un elemento al final de la lista. # es rapido."""
        nuevo = NodoDoble(dato)
        if self._cola is None:
            self._cabeza = nuevo
            self._cola = nuevo
        else:
            nuevo._anterior = self._cola
            self._cola._siguiente = nuevo
            self._cola = nuevo
        self._tamano += 1

    def insertar_en(self, pos: int, dato: T) -> None:
        """Inserta un elemento en la posicion dada (0-indexada). # recorre todos los elementos.

        Lanza IndexError si la posicion no es valida.
        """
        if pos < 0 or pos > self._tamano:
            raise IndexError("Posicion invalida")
        if pos == 0:
            self.insertar_inicio(dato)
            return
        if pos == self._tamano:
            self.insertar_final(dato)
            return
        actual = self._cabeza
        for _ in range(pos - 1):
            if actual is None:
                break
            actual = actual._siguiente
        if actual is None:
            raise IndexError("Posicion invalida")
        nuevo = NodoDoble(dato)
        siguiente = actual._siguiente
        nuevo._anterior = actual
        nuevo._siguiente = siguiente
        actual._siguiente = nuevo
        if siguiente is not None:
            siguiente._anterior = nuevo
        self._tamano += 1

    def eliminar(self, dato: T) -> bool:
        """Elimina la primera coincidencia del dato. # recorre todos los elementos.

        Retorna True si se elimino, False si no se encontro.
        """
        actual = self._cabeza
        while actual is not None:
            if actual.dato == dato:
                if actual._anterior is None:
                    self._cabeza = actual._siguiente
                else:
                    actual._anterior._siguiente = actual._siguiente
                if actual._siguiente is None:
                    self._cola = actual._anterior
                else:
                    actual._siguiente._anterior = actual._anterior
                self._tamano -= 1
                return True
            actual = actual._siguiente
        return False

    def buscar(self, dato: T) -> int:
        """Retorna la posicion del dato o -1 si no esta. # recorre todos los elementos."""
        actual = self._cabeza
        pos = 0
        while actual is not None:
            if actual.dato == dato:
                return pos
            actual = actual._siguiente
            pos += 1
        return -1

    def obtener(self, pos: int) -> T:
        """Retorna el dato en la posicion dada. # recorre todos los elementos.

        Lanza IndexError si la posicion no es valida.
        """
        if pos < 0 or pos >= self._tamano:
            raise IndexError("Posicion invalida")
        actual = self._cabeza
        for _ in range(pos):
            if actual is None:
                break
            actual = actual._siguiente
        if actual is None:
            raise IndexError("Posicion invalida")
        return actual.dato

    def __len__(self) -> int:
        """Retorna la cantidad de elementos. # es rapido."""
        return self._tamano

    def esta_vacia(self) -> bool:
        """Indica si la lista esta vacia. # es rapido."""
        return self._tamano == 0

    def __str__(self) -> str:
        """Representacion en cadena de la lista. # recorre todos los elementos."""
        elementos = []
        actual = self._cabeza
        while actual is not None:
            elementos.append(str(actual.dato))
            actual = actual._siguiente
        return " <-> ".join(elementos) if elementos else "Lista vacia"

    def imprimir_reversa(self) -> None:
        """Imprime los elementos del mas reciente al mas antiguo. # recorre todos los elementos."""
        if self._cola is None:
            print("Lista vacia")
            return
        elementos = []
        actual = self._cola
        while actual is not None:
            elementos.append(str(actual.dato))
            actual = actual._anterior
        print(" <-> ".join(elementos))

    def __iter__(self):
        """Permite iterar sobre los elementos de la lista. # recorre todos los elementos."""
        actual = self._cabeza
        while actual is not None:
            yield actual.dato
            actual = actual._siguiente
