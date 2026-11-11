"""Modelo de datos: Operacion para el historial de deshacer."""


class Operacion:
    """Operacion realizada por el operador, apilable para deshacer.

    Atributos:
        tipo: tipo de operacion (crear_pedido, cancelar_pedido, cambiar_estado).
        dato_afectado: identificador del dato afectado (ej. id del pedido).
        estado_anterior: estado previo antes de la operacion.
    """

    def __init__(self, tipo: str, dato_afectado, estado_anterior) -> None:
        """Inicializa una operacion registrable."""
        self.tipo: str = tipo
        self.dato_afectado = dato_afectado
        self.estado_anterior = estado_anterior

    def __repr__(self) -> str:
        """Representacion legible de la operacion."""
        return (
            f"Operacion(tipo={self.tipo!r}, dato={self.dato_afectado!r}, "
            f"estado_anterior={self.estado_anterior!r})"
        )
