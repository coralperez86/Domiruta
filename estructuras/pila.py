"""Pila implementada con nodos enlazados."""

from __future__ import annotations

from typing import Generic, TypeVar

from estructuras.nodo import Nodo  # type: ignore

T = TypeVar("T")


class Pila(Generic[T]):
    """Pila LIFO implementada con nodos.

    Atributos:
        _tope: nodo del tope o None.
        _tamano: cantidad de elementos.
    """

    def __init__(self) -> None:
        """Crea una pila vacia."""
        self._tope: Nodo[T] | None = None
        self._tamano: int = 0

    def apilar(self, dato: T) -> None:
        """Agrega un elemento al tope. # es rapido."""
        nuevo = Nodo(dato)
        nuevo._siguiente = self._tope
        self._tope = nuevo
        self._tamano += 1

    def desapilar(self) -> T:
        """Retira y retorna el elemento del tope. # es rapido.

        Lanza IndexError si la pila esta vacia.
        """
        if self._tope is None:
            raise IndexError("Desapilar de pila vacia")
        dato = self._tope.dato
        self._tope = self._tope._siguiente
        self._tamano -= 1
        return dato

    def cima(self) -> T:
        """Retorna el elemento del tope sin retirarlo. # es rapido.

        Lanza IndexError si la pila esta vacia.
        """
        if self._tope is None:
            raise IndexError("Cima de pila vacia")
        return self._tope.dato

    def esta_vacia(self) -> bool:
        """Indica si la pila esta vacia. # es rapido."""
        return self._tamano == 0

    def __len__(self) -> int:
        """Retorna la cantidad de elementos. # es rapido."""
        return self._tamano

    def __str__(self) -> str:
        """Representacion en cadena de la pila. # recorre todos los elementos."""
        elementos = []
        actual = self._tope
        while actual is not None:
            elementos.append(str(actual.dato))
            actual = actual._siguiente
        return " | ".join(elementos) if elementos else "Pila vacia"
