"""Arbol AVL con las cuatro rotaciones y rebalanceo tras insercion."""

from __future__ import annotations

from typing import Generic, TypeVar, Optional

from estructuras.arbol_bst import _NodoArbol  # type: ignore

T = TypeVar("T")


class ArbolAVL(Generic[T]):
    """Arbol AVL generico con rebalanceo tras cada insercion.

    Implementa las cuatro rotaciones: simple derecha (LL), simple izquierda (RR),
    doble izquierda-derecha (LR) y doble derecha-izquierda (RL). Cada vez que
    ocurre una rotacion se imprime un mensaje indicando el tipo y el nodo pivote.

    La eliminacion en AVL es opcional (bonificacion).

    Atributos:
        _raiz: raiz del arbol o None.
    """

    def __init__(self) -> None:
        """Crea un arbol AVL vacio."""
        self._raiz: Optional[_NodoArbol[T]] = None

    def insertar(self, dato: T) -> None:
        """Inserta un dato y rebalancea el arbol. # O(log n)"""
        self._raiz = self._insertar_recursivo(self._raiz, dato)

    def _altura(self, nodo: Optional[_NodoArbol[T]]) -> int:
        if nodo is None:
            return 0
        return 1 + max(self._altura(nodo.izquierda), self._altura(nodo.derecha))

    def _factor_equilibrio(self, nodo: Optional[_NodoArbol[T]]) -> int:
        if nodo is None:
            return 0
        return self._altura(nodo.izquierda) - self._altura(nodo.derecha)

    def _rotacion_simple_derecha(self, y: _NodoArbol[T]) -> _NodoArbol[T]:
        """Rotacion simple derecha (caso LL). # es rapido."""
        print(
            f"Rotacion simple derecha (LL), pivote: {y.dato}"
        )
        x = y.izquierda
        T2 = x.derecha
        x.derecha = y
        y.izquierda = T2
        return x

    def _rotacion_simple_izquierda(self, x: _NodoArbol[T]) -> _NodoArbol[T]:
        """Rotacion simple izquierda (caso RR). # es rapido."""
        print(
            f"Rotacion simple izquierda (RR), pivote: {x.dato}"
        )
        y = x.derecha
        T2 = y.izquierda
        y.izquierda = x
        x.derecha = T2
        return y

    def _rotacion_doble_izquierda_derecha(self, z: _NodoArbol[T]) -> _NodoArbol[T]:
        """Rotacion doble izquierda-derecha (caso LR). # es rapido."""
        print(
            f"Rotacion doble izquierda-derecha (LR), pivote: {z.dato}"
        )
        z.izquierda = self._rotacion_simple_izquierda(z.izquierda)
        return self._rotacion_simple_derecha(z)

    def _rotacion_doble_derecha_izquierda(self, z: _NodoArbol[T]) -> _NodoArbol[T]:
        """Rotacion doble derecha-izquierda (caso RL). # es rapido."""
        print(
            f"Rotacion doble derecha-izquierda (RL), pivote: {z.dato}"
        )
        z.derecha = self._rotacion_simple_derecha(z.derecha)
        return self._rotacion_simple_izquierda(z)

    def _insertar_recursivo(
        self, nodo: Optional[_NodoArbol[T]], dato: T
    ) -> _NodoArbol[T]:
        if nodo is None:
            return _NodoArbol(dato)
        if dato < nodo.dato:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, dato)
        elif dato > nodo.dato:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, dato)
        else:
            return nodo  # duplicados no permitidos

        balance = self._factor_equilibrio(nodo)

        # Caso LL
        if balance > 1 and dato < nodo.izquierda.dato:
            return self._rotacion_simple_derecha(nodo)
        # Caso RR
        if balance < -1 and dato > nodo.derecha.dato:
            return self._rotacion_simple_izquierda(nodo)
        # Caso LR
        if balance > 1 and dato > nodo.izquierda.dato:
            return self._rotacion_doble_izquierda_derecha(nodo)
        # Caso RL
        if balance < -1 and dato < nodo.derecha.dato:
            return self._rotacion_doble_derecha_izquierda(nodo)

        return nodo

    def buscar(self, dato: T) -> bool:
        """Indica si un dato esta en el arbol. # O(log n)"""
        return self._buscar_recursivo(self._raiz, dato) is not None

    def _buscar_recursivo(
        self, nodo: Optional[_NodoArbol[T]], dato: T
    ) -> Optional[_NodoArbol[T]]:
        if nodo is None:
            return None
        if dato == nodo.dato:
            return nodo
        if dato < nodo.dato:
            return self._buscar_recursivo(nodo.izquierda, dato)
        return self._buscar_recursivo(nodo.derecha, dato)

    def eliminar(self, dato: T) -> bool:
        """Elimina un dato con rebalanceo (bonificacion). # O(log n)

        Retorna True si se elimino, False si no existia.
        """
        if not self.buscar(dato):
            return False
        self._raiz, _ = self._eliminar_recursivo(self._raiz, dato)
        return True

    def _eliminar_recursivo(
        self, nodo: Optional[_NodoArbol[T]], dato: T
    ) -> tuple[Optional[_NodoArbol[T]], bool]:
        if nodo is None:
            return None, False
        if dato < nodo.dato:
            nodo.izquierda, eliminado = self._eliminar_recursivo(nodo.izquierda, dato)
        elif dato > nodo.dato:
            nodo.derecha, eliminado = self._eliminar_recursivo(nodo.derecha, dato)
        else:
            if nodo.izquierda is None and nodo.derecha is None:
                return None, True
            if nodo.izquierda is None:
                return nodo.derecha, True
            if nodo.derecha is None:
                return nodo.izquierda, True
            sucesor = self._minimo_nodo(nodo.derecha)
            nodo.dato = sucesor.dato
            nodo.derecha, _ = self._eliminar_recursivo(nodo.derecha, sucesor.dato)
            eliminado = True

        # Rebalancear tras eliminacion
        balance = self._factor_equilibrio(nodo)
        if balance > 1 and self._factor_equilibrio(nodo.izquierda) >= 0:
            return self._rotacion_simple_derecha(nodo), eliminado
        if balance > 1 and self._factor_equilibrio(nodo.izquierda) < 0:
            return self._rotacion_doble_izquierda_derecha(nodo), eliminado
        if balance < -1 and self._factor_equilibrio(nodo.derecha) <= 0:
            return self._rotacion_simple_izquierda(nodo), eliminado
        if balance < -1 and self._factor_equilibrio(nodo.derecha) > 0:
            return self._rotacion_doble_derecha_izquierda(nodo), eliminado
        return nodo, eliminado

    def _minimo_nodo(self, nodo: _NodoArbol[T]) -> _NodoArbol[T]:
        actual = nodo
        while actual.izquierda is not None:
            actual = actual.izquierda
        return actual

    def altura(self) -> int:
        """Retorna la altura del arbol AVL. # O(log n)"""
        return self._altura(self._raiz)

    def esta_vacio(self) -> bool:
        """Indica si el arbol esta vacio. # es rapido."""
        return self._raiz is None

    def __len__(self) -> int:
        """Retorna la cantidad de nodos. # recorre todos los elementos."""
        return self._contar(self._raiz)

    def _contar(self, nodo: Optional[_NodoArbol[T]]) -> int:
        if nodo is None:
            return 0
        return 1 + self._contar(nodo.izquierda) + self._contar(nodo.derecha)

    def inorden(self) -> list:
        """Retorna los elementos en inorden. # recorre todos los elementos."""
        resultado: list = []
        self._inorden(self._raiz, resultado)
        return resultado

    def _inorden(self, nodo: Optional[_NodoArbol[T]], resultado: list) -> None:
        if nodo is not None:
            self._inorden(nodo.izquierda, resultado)
            resultado.append(nodo.dato)
            self._inorden(nodo.derecha, resultado)

    def __str__(self) -> str:
        """Representacion en inorden del arbol AVL. # recorre todos los elementos."""
        if self.esta_vacio():
            return "Arbol vacio"
        return " -> ".join(str(d) for d in self.inorden())
