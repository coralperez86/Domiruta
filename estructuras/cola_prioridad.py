"""Cola de prioridad: urgentes antes que normales, FIFO dentro de igual prioridad."""

from __future__ import annotations

from typing import Generic, TypeVar

from estructuras.cola import Cola  # type: ignore
from estructuras.nodo import Nodo  # type: ignore

T = TypeVar("T")


class ColaPrioridad(Generic[T]):
    """Cola de prioridad con dos colas internas: una para urgentes y otra para normales.

    Los pedidos urgentes se atienden antes que los normales. Entre pedidos de igual
    prioridad se respeta el orden de llegada.

    Justificacion de diseno: se usan dos colas internas (Urgentes y Normales) en lugar
    de una lista ordenada para mantener encolar y desencolar en O(1) en el caso comun,
    evitando el O(n) de insertar ordenado. Se sacrifica un poco de memoria por simplicidad
    y rendimiento.

    Atributos:
        _urgentes: cola de elementos urgentes.
        _normales: cola de elementos normales.
        _tamano: cantidad total de elementos.
    """

    def __init__(self) -> None:
        """Crea una cola de prioridad vacia."""
        self._urgentes: Cola[T] = Cola()
        self._normales: Cola[T] = Cola()
        self._tamano: int = 0

    def encolar(self, dato: T, urgente: bool = False) -> None:
        """Agrega un elemento segun su prioridad. # es rapido.

        Si urgente es True va a la cola de urgentes, si no a la de normales.
        """
        if urgente:
            self._urgentes.encolar(dato)
        else:
            self._normales.encolar(dato)
        self._tamano += 1

    def desencolar(self) -> T:
        """Retira y retorna el elemento de mayor prioridad. # es rapido.

        Primero atiende urgentes; si no hay, atiende normales.
        Lanza IndexError si la cola esta vacia.
        """
        if not self._urgentes.esta_vacia():
            self._tamano -= 1
            return self._urgentes.desencolar()
        if not self._normales.esta_vacia():
            self._tamano -= 1
            return self._normales.desencolar()
        raise IndexError("Desencolar de cola de prioridad vacia")

    def frente(self) -> T:
        """Retorna el elemento de mayor prioridad sin retirarlo. # es rapido.

        Lanza IndexError si la cola esta vacia.
        """
        if not self._urgentes.esta_vacia():
            return self._urgentes.frente()
        if not self._normales.esta_vacia():
            return self._normales.frente()
        raise IndexError("Frente de cola de prioridad vacia")

    def esta_vacia(self) -> bool:
        """Indica si la cola esta vacia. # es rapido."""
        return self._tamano == 0

    def __len__(self) -> int:
        """Retorna la cantidad total de elementos. # es rapido."""
        return self._tamano

    def __str__(self) -> str:
        """Representacion en cadena de la cola de prioridad. # recorre todos los elementos."""
        urg = str(self._urgentes)
        nor = str(self._normales)
        partes = []
        if urg != "Cola vacia":
            partes.append(f"Urgentes: {urg}")
        if nor != "Cola vacia":
            partes.append(f"Normales: {nor}")
        return " | ".join(partes) if partes else "Cola de prioridad vacia"
