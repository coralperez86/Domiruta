"""Cola FIFO implementada con nodos enlazados."""

from __future__ import annotations

from typing import Generic, TypeVar

from estructuras.nodo import Nodo  # type: ignore

T = TypeVar("T")


class Cola(Generic[T]):
    """Cola FIFO implementada con nodos.

    Atributos:
        _frente: primer nodo o None.
        _final: ultimo nodo o None.
        _tamano: cantidad de elementos.
    """

    def __init__(self) -> None:
        """Crea una cola vacia."""
        self._frente: Nodo[T] | None = None
        self._final: Nodo[T] | None = None
        self._tamano: int = 0

    def encolar(self, dato: T) -> None:
        """Agrega un elemento al final de la cola. # es rapido."""
        nuevo = Nodo(dato)
        if self._final is None:
            self._frente = nuevo
            self._final = nuevo
        else:
            self._final._siguiente = nuevo
            self._final = nuevo
        self._tamano += 1

    def desencolar(self) -> T:
        """Retira y retorna el elemento del frente. # es rapido.

        Lanza IndexError si la cola esta vacia.
        """
        if self._frente is None:
            raise IndexError("Desencolar de cola vacia")
        dato = self._frente.dato
        self._frente = self._frente._siguiente
        if self._frente is None:
            self._final = None
        self._tamano -= 1
        return dato

    def frente(self) -> T:
        """Retorna el elemento del frente sin retirarlo. # es rapido.

        Lanza IndexError si la cola esta vacia.
        """
        if self._frente is None:
            raise IndexError("Frente de cola vacia")
        return self._frente.dato

    def esta_vacia(self) -> bool:
        """Indica si la cola esta vacia. # es rapido."""
        return self._tamano == 0

    def __len__(self) -> int:
        """Retorna la cantidad de elementos. # es rapido."""
        return self._tamano

    def __str__(self) -> str:
        """Representacion en cadena de la cola. # recorre todos los elementos."""
        elementos = []
        actual = self._frente
        while actual is not None:
            elementos.append(str(actual.dato))
            actual = actual._siguiente
        return " <- ".join(elementos) if elementos else "Cola vacia"
