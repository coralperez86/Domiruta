"""Nodos base para las estructuras enlazadas del proyecto."""

from typing import Generic, TypeVar

T = TypeVar("T")


class Nodo(Generic[T]):
    """Nodo de una lista enlazada simple.

    Atributos:
        dato: valor almacenado en el nodo.
        _siguiente: referencia al siguiente nodo o None.
    """

    def __init__(self, dato: T) -> None:
        """Inicializa un nodo con el dato dado y sin siguiente."""
        self.dato: T = dato
        self._siguiente: "Nodo[T] | None" = None

    def __repr__(self) -> str:
        """Representacion legible del nodo."""
        return f"Nodo({self.dato!r})"


class NodoDoble(Generic[T]):
    """Nodo de una lista doblemente enlazada.

    Atributos:
        dato: valor almacenado en el nodo.
        _siguiente: referencia al siguiente nodo o None.
        _anterior: referencia al nodo anterior o None.
    """

    def __init__(self, dato: T) -> None:
        """Inicializa un nodo doble con el dato dado y sin enlaces."""
        self.dato: T = dato
        self._siguiente: "NodoDoble[T] | None" = None
        self._anterior: "NodoDoble[T] | None" = None

    def __repr__(self) -> str:
        """Representacion legible del nodo doble."""
        return f"NodoDoble({self.dato!r})"
