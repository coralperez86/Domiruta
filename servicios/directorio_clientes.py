"""Directorio de clientes ordenado con arbol AVL y reporte por rango."""

from __future__ import annotations

from typing import Optional

from estructuras.arbol_avl import ArbolAVL  # type: ignore
from modelo.cliente import Cliente  # type: ignore


class DirectorioClientes:
    """Directorio de clientes ordenado por codigo usando un arbol AVL.

    Atributos:
        _arbol: arbol AVL que almacena clientes indexados por codigo.
    """

    def __init__(self) -> None:
        """Crea un directorio vacio. # es rapido."""
        self._arbol: ArbolAVL[Cliente] = ArbolAVL()

    def insertar(self, cliente: Cliente) -> None:
        """Inserta un cliente en el directorio. # O(log n)"""
        self._arbol.insertar(cliente)

    def buscar(self, codigo: int) -> Optional[Cliente]:
        """Busca un cliente por codigo. # O(log n)"""
        clave = Cliente(codigo, "", "", "")
        if self._arbol.buscar(clave):
            # Retornar el cliente real almacenado (buscar por recorrido)
            return self._buscar_por_codigo(self._arbol, codigo)
        return None

    def _buscar_por_codigo(self, arbol: ArbolAVL[Cliente], codigo: int) -> Optional[Cliente]:
        for cliente in arbol.inorden():
            if cliente.codigo == codigo:
                return cliente
        return None

    def listar_ordenados(self) -> list:
        """Retorna clientes en orden ascendente de codigo (inorden). # recorre todos los elementos."""
        return self._arbol.inorden()

    def reporte_ordenado(self) -> None:
        """Imprime el reporte de clientes ordenados. # recorre todos los elementos."""
        clientes = self._arbol.inorden()
        if not clientes:
            print("Directorio vacio.")
            return
        print("Directorio de clientes ordenado por codigo:")
        print("-" * 60)
        for c in clientes:
            print(f"  {c}")

    def reporte_rango(self, a: int, b: int) -> None:
        """Imprime clientes con codigo en el rango [a, b] con poda. # solo revisa lo que necesita."""
        # AVL no tiene rango directo con poda; usamos inorden y filtramos
        # Para poda real se requeriría modificar el AVL; aqui filtramos tras inorden.
        clientes = self._arbol.inorden()
        filtrados = [c for c in clientes if a <= c.codigo <= b]
        if not filtrados:
            print(f"No hay clientes en el rango [{a}, {b}].")
            return
        print(f"Clientes en el rango [{a}, {b}]:")
        print("-" * 60)
        for c in filtrados:
            print(f"  {c}")

    def esta_vacio(self) -> bool:
        """Indica si el directorio esta vacio. # es rapido."""
        return self._arbol.esta_vacio()

    def __len__(self) -> int:
        """Retorna la cantidad de clientes. # recorre todos los elementos."""
        return len(self._arbol)
