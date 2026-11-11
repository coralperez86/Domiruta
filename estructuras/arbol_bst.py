"""Arbol binario de búsqueda implementado con nodos, sin colecciones del lenguaje."""

from __future__ import annotations

from typing import Generic, TypeVar, Optional

from estructuras.cola import Cola  # type: ignore

T = TypeVar("T")


class _NodoArbol(Generic[T]):
    """Nodo interno del arbol binario."""

    def __init__(self, dato: T) -> None:
        self.dato: T = dato
        self.izquierda: Optional[_NodoArbol[T]] = None
        self.derecha: Optional[_NodoArbol[T]] = None


class ArbolBST(Generic[T]):
    """Arbol binario de busqueda generico.

    Los elementos deben ser comparables con <. Soporta insercion, busqueda,
    eliminacion (tres casos), recorridos en profundidad y por niveles.

    Atributos:
        _raiz: raiz del arbol o None.
    """

    def __init__(self) -> None:
        """Crea un arbol vacio."""
        self._raiz: Optional[_NodoArbol[T]] = None

    def insertar(self, dato: T) -> None:
        """Inserta un dato en el arbol. # depende de que tan alto sea el arbol."""
        self._raiz = self._insertar_recursivo(self._raiz, dato)

    def _insertar_recursivo(
        self, nodo: Optional[_NodoArbol[T]], dato: T
    ) -> _NodoArbol[T]:
        if nodo is None:
            return _NodoArbol(dato)
        if dato < nodo.dato:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, dato)
        elif dato > nodo.dato:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, dato)
        return nodo

    def buscar(self, dato: T) -> bool:
        """Indica si un dato esta en el arbol. # depende de la altura del arbol."""
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
        """Elimina un dato (tres casos: hoja, un hijo, dos hijos). # depende de la altura del arbol.

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
            return nodo, eliminado
        if dato > nodo.dato:
            nodo.derecha, eliminado = self._eliminar_recursivo(nodo.derecha, dato)
            return nodo, eliminado
        # Caso encontrado: nodo.dato == dato
        if nodo.izquierda is None and nodo.derecha is None:
            return None, True  # hoja
        if nodo.izquierda is None:
            return nodo.derecha, True  # un hijo derecho
        if nodo.derecha is None:
            return nodo.izquierda, True  # un hijo izquierdo
        # Dos hijos: reemplazar por el minimo del subarbol derecho
        sucesor = self._minimo_nodo(nodo.derecha)
        nodo.dato = sucesor.dato
        nodo.derecha, _ = self._eliminar_recursivo(nodo.derecha, sucesor.dato)
        return nodo, True

    def _minimo_nodo(self, nodo: _NodoArbol[T]) -> _NodoArbol[T]:
        actual = nodo
        while actual.izquierda is not None:
            actual = actual.izquierda
        return actual

    def minimo(self) -> T:
        """Retorna el valor minimo del arbol. # depende de la altura del arbol.

        Lanza ValueError si el arbol esta vacio.
        """
        if self._raiz is None:
            raise ValueError("Arbol vacio")
        return self._minimo_nodo(self._raiz).dato

    def maximo(self) -> T:
        """Retorna el valor maximo del arbol. # depende de la altura del arbol.

        Lanza ValueError si el arbol esta vacio.
        """
        if self._raiz is None:
            raise ValueError("Arbol vacio")
        actual = self._raiz
        while actual.derecha is not None:
            actual = actual.derecha
        return actual.dato

    def altura(self) -> int:
        """Retorna la altura del arbol (recursivo). # recorre todos los elementos."""
        return self._altura_recursiva(self._raiz)

    def _altura_recursiva(self, nodo: Optional[_NodoArbol[T]]) -> int:
        if nodo is None:
            return 0
        return 1 + max(
            self._altura_recursiva(nodo.izquierda),
            self._altura_recursiva(nodo.derecha),
        )

    def contar_nodos(self) -> int:
        """Retorna la cantidad de nodos (recursivo). # recorre todos los elementos."""
        return self._contar_nodos_recursivo(self._raiz)

    def _contar_nodos_recursivo(self, nodo: Optional[_NodoArbol[T]]) -> int:
        if nodo is None:
            return 0
        return 1 + self._contar_nodos_recursivo(nodo.izquierda) + self._contar_nodos_recursivo(
            nodo.derecha
        )

    def contar_hojas(self) -> int:
        """Retorna la cantidad de hojas (recursivo). # recorre todos los elementos."""
        return self._contar_hojas_recursivo(self._raiz)

    def _contar_hojas_recursivo(self, nodo: Optional[_NodoArbol[T]]) -> int:
        if nodo is None:
            return 0
        if nodo.izquierda is None and nodo.derecha is None:
            return 1
        return self._contar_hojas_recursivo(nodo.izquierda) + self._contar_hojas_recursivo(
            nodo.derecha
        )

    def preorden(self) -> list:
        """Retorna los elementos en preorden (recursivo). # recorre todos los elementos."""
        resultado: list = []
        self._preorden_recursivo(self._raiz, resultado)
        return resultado

    def _preorden_recursivo(self, nodo: Optional[_NodoArbol[T]], resultado: list) -> None:
        if nodo is not None:
            resultado.append(nodo.dato)
            self._preorden_recursivo(nodo.izquierda, resultado)
            self._preorden_recursivo(nodo.derecha, resultado)

    def inorden(self) -> list:
        """Retorna los elementos en inorden (recursivo). # recorre todos los elementos."""
        resultado: list = []
        self._inorden_recursivo(self._raiz, resultado)
        return resultado

    def _inorden_recursivo(self, nodo: Optional[_NodoArbol[T]], resultado: list) -> None:
        if nodo is not None:
            self._inorden_recursivo(nodo.izquierda, resultado)
            resultado.append(nodo.dato)
            self._inorden_recursivo(nodo.derecha, resultado)

    def postorden(self) -> list:
        """Retorna los elementos en postorden (recursivo). # recorre todos los elementos."""
        resultado: list = []
        self._postorden_recursivo(self._raiz, resultado)
        return resultado

    def _postorden_recursivo(self, nodo: Optional[_NodoArbol[T]], resultado: list) -> None:
        if nodo is not None:
            self._postorden_recursivo(nodo.izquierda, resultado)
            self._postorden_recursivo(nodo.derecha, resultado)
            resultado.append(nodo.dato)

    def por_niveles(self) -> list:
        """Retorna los elementos por niveles / anchura usando Cola. # recorre todos los elementos."""
        resultado: list = []
        if self._raiz is None:
            return resultado
        cola: Cola[_NodoArbol[T]] = Cola()
        cola.encolar(self._raiz)
        while not cola.esta_vacia():
            nodo = cola.desencolar()
            resultado.append(nodo.dato)
            if nodo.izquierda is not None:
                cola.encolar(nodo.izquierda)
            if nodo.derecha is not None:
                cola.encolar(nodo.derecha)
        return resultado

    def rango(self, a: T, b: T) -> list:
        """Retorna elementos en el rango [a, b] con poda de ramas. # solo revisa lo que necesita."""
        resultado: list = []
        self._rango_recursivo(self._raiz, a, b, resultado)
        return resultado

    def _rango_recursivo(
        self, nodo: Optional[_NodoArbol[T]], a: T, b: T, resultado: list
    ) -> None:
        if nodo is None:
            return
        if a < nodo.dato:
            self._rango_recursivo(nodo.izquierda, a, b, resultado)
        if a <= nodo.dato <= b:
            resultado.append(nodo.dato)
        if nodo.dato < b:
            self._rango_recursivo(nodo.derecha, a, b, resultado)

    def esta_vacio(self) -> bool:
        """Indica si el arbol esta vacio. # es rapido."""
        return self._raiz is None

    def __len__(self) -> int:
        """Retorna la cantidad de nodos. # recorre todos los elementos."""
        return self.contar_nodos()

    def __str__(self) -> str:
        """Representacion en inorden del arbol. # recorre todos los elementos."""
        return " -> ".join(str(d) for d in self.inorden()) if not self.esta_vacio() else "Arbol vacio"
