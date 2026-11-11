"""Funciones recursivas sobre listas enlazadas (sin ciclos)."""

from __future__ import annotations

import sys

from typing import Generic, TypeVar

from estructuras.lista_enlazada import Nodo  # type: ignore

T = TypeVar("T")

# Nota: Python no deja usar mucha recursion, tiene un limite de unas 1000 llamadas.


def sumar_valores(nodo: Nodo | None) -> float:
    """Suma el valor de todos los pedidos de un historial. # recorre todos los elementos.

    Caso base: si el nodo es None, retorna 0.
    Caso recursivo: suma el valor de este nodo y llama a la funcion con el siguiente.
    """
    if nodo is None:
        return 0.0
    return getattr(nodo.dato, "valor", 0) + sumar_valores(nodo._siguiente)


def contar_urgentes(nodo: Nodo | None) -> int:
    """Cuenta los pedidos urgentes en la lista. # recorre todos los elementos.

    Caso base: si el nodo es None, retorna 0.
    Caso recursivo: suma 1 si este nodo es urgente, y llama a la funcion con el siguiente.
    """
    if nodo is None:
        return 0
    es_urgente = 1 if getattr(nodo.dato, "urgente", False) else 0
    return es_urgente + contar_urgentes(nodo._siguiente)


def buscar_recursivo(nodo: Nodo | None, dato) -> bool:
    """Indica si un dato esta en la lista. # recorre todos los elementos.

    Caso base: si el nodo es None, retorna False.
    Caso recursivo: si el dato de este nodo es igual, retorna True; si no, busca en el siguiente.
    """
    if nodo is None:
        return False
    if nodo.dato == dato:
        return True
    return buscar_recursivo(nodo._siguiente, dato)


def imprimir_reversa_recursivo(nodo: Nodo | None) -> None:
    """Imprime una lista simple al reverso sin usar lista doble. # recorre todos los elementos.

    Caso base: si el nodo es None, no hace nada.
    Caso recursivo: primero llama a la funcion con el siguiente, y despues imprime este dato.
    """
    if nodo is None:
        return
    imprimir_reversa_recursivo(nodo._siguiente)
    print(nodo.dato, end=" <- ")


def invertir_lista(nodo: Nodo | None) -> Nodo | None:
    """Invierte fisicamente la lista simple y retorna la nueva cabeza. # recorre todos los elementos.

    Caso base: si el nodo es None o no tiene siguiente, retorna ese nodo.
    Caso recursivo: invierte el resto de la lista y luego reacomoda los enlaces de este nodo.
    """
    if nodo is None or nodo._siguiente is None:
        return nodo
    nueva_cabeza = invertir_lista(nodo._siguiente)
    nodo._siguiente._siguiente = nodo
    nodo._siguiente = None
    return nueva_cabeza


if __name__ == "__main__":
    print("Modulo de recursión listo. Límite de recursión:", sys.getrecursionlimit())
