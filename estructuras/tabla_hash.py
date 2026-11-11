"""Tabla hash con encadenamiento y redimensionamiento."""

from __future__ import annotations

from typing import Generic, TypeVar

from estructuras.lista_enlazada import ListaEnlazada  # type: ignore

K = TypeVar("K")
V = TypeVar("V")


def _es_primo(n: int) -> bool:
    """Indica si un numero es primo. # O(sqrt(n))"""
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def _siguiente_primo(n: int) -> int:
    """Retorna el primo mayor o igual a n. # busca el siguiente primo."""
    candidato = max(2, n)
    while not _es_primo(candidato):
        candidato += 1
    return candidato


class TablaHash(Generic[K, V]):
    """Tabla hash con llave generica y encadenamiento por listas enlazadas.

    Usa un arreglo de tamaño fijo creado con [None] * capacidad como unico arreglo
    permitido por las reglas tecnicas. Cada posicion guarda una ListaEnlazada de
    pares (clave, valor) para manejar colisiones.

    Atributos:
        _capacidad: capacidad actual del arreglo.
        _tamano: cantidad de elementos insertados.
        _tabla: arreglo de listas enlazadas (o None).
    """

    def __init__(self, capacidad_inicial: int = 11) -> None:
        """Crea la tabla hash con capacidad inicial prima (por defecto 11). # O(c)"""
        self._capacidad: int = _siguiente_primo(capacidad_inicial)
        self._tamano: int = 0
        self._tabla: list = [None] * self._capacidad

    def _funcion_hash(self, clave: K) -> int:
        """Calcula la posicion de la clave. # normalmente es rapido."""
        return hash(clave) % self._capacidad

    def _rehash(self) -> None:
        """Duplica la capacidad al siguiente primo y reubica todos los elementos. # recorre todos los elementos."""
        vieja_tabla = self._tabla
        vieja_capacidad = self._capacidad
        self._capacidad = _siguiente_primo(vieja_capacidad * 2)
        self._tabla = [None] * self._capacidad
        self._tamano = 0
        for i in range(vieja_capacidad):
            lista = vieja_tabla[i]
            if lista is not None:
                for par in lista:
                    self.insertar(par[0], par[1])

    def insertar(self, clave: K, valor: V) -> None:
        """Inserta o actualiza la clave con el valor dado. # normalmente es rapido."""
        indice = self._funcion_hash(clave)
        lista = self._tabla[indice]
        if lista is None:
            lista = ListaEnlazada()
            self._tabla[indice] = lista
        # Buscar si ya existe la clave para actualizar
        encontrado = False
        pos = 0
        tupla_existente = None
        temp = lista._cabeza
        while temp is not None:
            if temp.dato[0] == clave:
                encontrado = True
                tupla_existente = temp.dato
                break
            temp = temp._siguiente
            pos += 1
        if encontrado:
            # Eliminar la tupla existente e insertar actualizada en la misma posicion
            lista.eliminar(tupla_existente)
            lista.insertar_en(pos, (clave, valor))
        else:
            lista.insertar_final((clave, valor))
            self._tamano += 1

        if self.factor_carga() > 0.75:
            self._rehash()

    def buscar(self, clave: K) -> V | None:
        """Retorna el valor asociado a la clave o None si no existe. # normalmente es rapido."""
        indice = self._funcion_hash(clave)
        lista = self._tabla[indice]
        if lista is None:
            return None
        temp = lista._cabeza
        while temp is not None:
            if temp.dato[0] == clave:
                return temp.dato[1]
            temp = temp._siguiente
        return None

    def eliminar(self, clave: K) -> bool:
        """Elimina la clave de la tabla. # normalmente es rapido.

        Retorna True si se elimino, False si no existia.
        """
        indice = self._funcion_hash(clave)
        lista = self._tabla[indice]
        if lista is None:
            return False
        # Buscar la posición
        pos = 0
        temp = lista._cabeza
        while temp is not None:
            if temp.dato[0] == clave:
                break
            temp = temp._siguiente
            pos += 1
        if temp is None:
            return False
        # Reconstruir lista sin el elemento (eliminar por dato requiere igualdad de tupla)
        # Usamos eliminar con la tupla exacta
        valor = temp.dato[1]
        resultado = lista.eliminar((clave, valor))
        if resultado:
            self._tamano -= 1
        return resultado

    def factor_carga(self) -> float:
        """Retorna el factor de carga actual. # es rapido."""
        return self._tamano / self._capacidad

    def __len__(self) -> int:
        """Retorna la cantidad de elementos. # es rapido."""
        return self._tamano

    def __str__(self) -> str:
        """Representacion en cadena de la tabla hash. # recorre todos los elementos."""
        partes = []
        for i in range(self._capacidad):
            lista = self._tabla[i]
            if lista is not None and not lista.esta_vacia():
                partes.append(f"[{i}]: {lista}")
        return "\n".join(partes) if partes else "Tabla hash vacia"
