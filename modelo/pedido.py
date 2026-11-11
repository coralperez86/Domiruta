"""Modelo de datos: Pedido y estado."""

from __future__ import annotations

from enum import Enum


class EstadoPedido(Enum):
    """Estados posibles de un pedido."""

    EN_ESPERA = "EN_ESPERA"
    ASIGNADO = "ASIGNADO"
    ENTREGADO = "ENTREGADO"
    CANCELADO = "CANCELADO"


class Pedido:
    """Pedido de domicilio de un cliente.

    Atributos:
        id: identificador del pedido.
        codigo_cliente: codigo del cliente dueño del pedido.
        descripcion: descripcion del pedido.
        valor: valor monetario del pedido.
        barrio_destino: barrio de destino.
        urgente: indica si el pedido es urgente.
        estado: estado actual del pedido.
    """

    _contador_id: int = 1

    def __init__(
        self,
        codigo_cliente: int,
        descripcion: str,
        valor: float,
        barrio_destino: str,
        urgente: bool = False,
    ) -> None:
        """Inicializa un pedido con estado EN_ESPERA."""
        self.id: int = Pedido._contador_id
        Pedido._contador_id += 1
        self.codigo_cliente: int = codigo_cliente
        self.descripcion: str = descripcion
        self.valor: float = valor
        self.barrio_destino: str = barrio_destino
        self.urgente: bool = urgente
        self.estado: EstadoPedido = EstadoPedido.EN_ESPERA

    def __repr__(self) -> str:
        """Representacion legible del pedido."""
        return (
            f"Pedido(id={self.id}, cliente={self.codigo_cliente}, "
            f"barrio={self.barrio_destino!r}, urgente={self.urgente}, "
            f"estado={self.estado.value})"
        )

    def __str__(self) -> str:
        """Representacion amigable del pedido."""
        return (
            f"Pedido #{self.id} | Cliente {self.codigo_cliente} | "
            f"{self.descripcion} | ${self.valor} | {self.barrio_destino} | "
            f"{'URGENTE' if self.urgente else 'normal'} | {self.estado.value}"
        )
