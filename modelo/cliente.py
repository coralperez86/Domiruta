"""Modelo de datos: Cliente."""

from __future__ import annotations


class Cliente:
    """Cliente de DomiRuta.

    El codigo es la llave para la tabla hash y el arbol.
    """

    def __init__(self, codigo: int, nombre: str, telefono: str, barrio: str) -> None:
        """Inicializa un cliente con sus datos basicos."""
        self.codigo: int = codigo
        self.nombre: str = nombre
        self.telefono: str = telefono
        self.barrio: str = barrio
        self.historial = None  # ListaDoble de pedidos (Fase 1)

    def __lt__(self, otro: object) -> bool:
        """Compara por codigo para orden en el arbol AVL."""
        if not isinstance(otro, Cliente):
            return NotImplemented
        return self.codigo < otro.codigo

    def __eq__(self, otro: object) -> bool:
        """Compara igualdad por codigo."""
        if not isinstance(otro, Cliente):
            return NotImplemented
        return self.codigo == otro.codigo

    def __hash__(self) -> int:
        """Hash basado en el codigo."""
        return hash(self.codigo)

    def __repr__(self) -> str:
        """Representacion legible del cliente."""
        return f"Cliente(codigo={self.codigo}, nombre={self.nombre!r}, barrio={self.barrio!r})"

    def __str__(self) -> str:
        """Representacion amigable del cliente."""
        return f"[{self.codigo}] {self.nombre} - {self.telefono} - {self.barrio}"
