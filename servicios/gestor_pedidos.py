"""Gestion de pedidos: pila de deshacer, cola de prioridad y tabla hash de clientes."""

from __future__ import annotations

from typing import Optional

from estructuras.pila import Pila  # type: ignore
from estructuras.cola_prioridad import ColaPrioridad  # type: ignore
from estructuras.tabla_hash import TablaHash  # type: ignore
from modelo.cliente import Cliente  # type: ignore
from modelo.pedido import Pedido, EstadoPedido  # type: ignore
from modelo.operacion import Operacion  # type: ignore
from util.recursion import sumar_valores, contar_urgentes, imprimir_reversa_recursivo  # type: ignore


class GestorPedidos:
    """Coordina clientes, pedidos, cola de prioridad y pila de deshacer.

    Atributos:
        _clientes: tabla hash que mapea codigo de cliente a objeto Cliente.
        _pedidos_espera: cola de prioridad de pedidos pendientes.
        _historial_desahacer: pila de operaciones realizadas.
        _siguiente_id_pedido: contador para ids de pedidos.
    """

    def __init__(self) -> None:
        """Inicializa el gestor de pedidos. # es rapido."""
        self._clientes: TablaHash[int, Cliente] = TablaHash()
        self._pedidos_espera: ColaPrioridad[Pedido] = ColaPrioridad()
        self._historial_desahacer: Pila[Operacion] = Pila()
        self._siguiente_id_pedido: int = 1

    def registrar_cliente(
        self, codigo: int, nombre: str, telefono: str, barrio: str
    ) -> bool:
        """Registra un cliente en la tabla hash. # normalmente es rapido."""
        if self._clientes.buscar(codigo) is not None:
            return False
        cliente = Cliente(codigo, nombre, telefono, barrio)
        self._clientes.insertar(codigo, cliente)
        op = Operacion("registrar_cliente", codigo, None)
        self._historial_desahacer.apilar(op)
        return True

    def buscar_cliente(self, codigo: int) -> Optional[Cliente]:
        """Busca un cliente por codigo. # normalmente es rapido."""
        return self._clientes.buscar(codigo)

    def listar_clientes(self) -> list:
        """Retorna todos los clientes registrados. # recorre todos los elementos."""
        resultado: list = []
        # Recorrer todas las posiciones de la tabla
        tabla = self._clientes  # type: ignore[attr-defined]
        for i in range(tabla._capacidad):
            lista = tabla._tabla[i]
            if lista is not None:
                temp = lista._cabeza
                while temp is not None:
                    resultado.append(temp.dato[1])
                    temp = temp._siguiente
        return resultado

    def crear_pedido(
        self,
        codigo_cliente: int,
        descripcion: str,
        valor: float,
        barrio_destino: str,
        urgente: bool = False,
    ) -> Optional[Pedido]:
        """Crea un pedido y lo encola en espera. # normalmente es rapido."""
        cliente = self._clientes.buscar(codigo_cliente)
        if cliente is None:
            return None
        pedido = Pedido(codigo_cliente, descripcion, valor, barrio_destino, urgente)
        pedido.id = self._siguiente_id_pedido
        self._siguiente_id_pedido += 1
        self._pedidos_espera.encolar(pedido, urgente=urgente)
        # Agregar al historial del cliente (lista doble)
        if cliente.historial is None:
            from estructuras.lista_doble import ListaDoble  # type: ignore

            cliente.historial = ListaDoble()
        cliente.historial.insertar_final(pedido)
        op = Operacion("crear_pedido", pedido.id, None)
        self._historial_desahacer.apilar(op)
        return pedido

    def asignar_siguiente_pedido(self) -> Optional[Pedido]:
        """Desencola el pedido de mayor prioridad y lo marca ASIGNADO. # es rapido."""
        if self._pedidos_espera.esta_vacia():
            return None
        pedido = self._pedidos_espera.desencolar()
        estado_anterior = pedido.estado
        pedido.estado = EstadoPedido.ASIGNADO
        op = Operacion("cambiar_estado", pedido.id, estado_anterior)
        self._historial_desahacer.apilar(op)
        return pedido

    def cancelar_pedido(self, id_pedido: int) -> bool:
        """Cancela un pedido pendiente. # recorre todos los elementos. en la cola de espera"""
        # Buscar el pedido en la cola de espera (no podemos indexar, recorremos)
        # Como la cola no soporta busqueda, cancelamos por id si esta al frente o lo buscamos
        # Implementacion simple: recorremos la cola interna (urgentes y normales)
        encontrado = self._buscar_en_cola(id_pedido)
        if not encontrado:
            return False
        pedido = encontrado
        if pedido.estado != EstadoPedido.EN_ESPERA:
            return False
        estado_anterior = pedido.estado
        pedido.estado = EstadoPedido.CANCELADO
        op = Operacion("cancelar_pedido", id_pedido, estado_anterior)
        self._historial_desahacer.apilar(op)
        return True

    def _buscar_en_cola(self, id_pedido: int) -> Optional[Pedido]:
        """Busca un pedido por id en la cola de prioridad (recorre colas internas). # recorre todos los elementos."""
        for cola in (self._pedidos_espera._urgentes, self._pedidos_espera._normales):
            temp = cola._frente
            while temp is not None:
                if temp.dato.id == id_pedido:
                    return temp.dato
                temp = temp._siguiente
        return None

    def deshacer(self) -> bool:
        """Deshace la ultima operacion registrada. # es rapido. / O(n) segun operacion"""
        if self._historial_desahacer.esta_vacia():
            return False
        op = self._historial_desahacer.desapilar()
        if op.tipo == "registrar_cliente":
            self._clientes.eliminar(op.dato_afectado)
        elif op.tipo == "crear_pedido":
            self._quitar_pedido_espera(op.dato_afectado)
        elif op.tipo == "cambiar_estado":
            pedido = self._buscar_en_cola(op.dato_afectado)
            if pedido is not None:
                pedido.estado = op.estado_anterior
            else:
                # Buscar en historial de clientes para restaurar estado
                self._restaurar_estado_en_historial(op.dato_afectado, op.estado_anterior)
        elif op.tipo == "cancelar_pedido":
            pedido = self._buscar_en_cola(op.dato_afectado)
            if pedido is not None:
                pedido.estado = op.estado_anterior
        return True

    def _quitar_pedido_espera(self, id_pedido: int) -> None:
        """Quita un pedido de la cola de espera reconstruyendo las colas. # recorre todos los elementos."""
        urgentes: list = []
        normales: list = []
        while not self._pedidos_espera._urgentes.esta_vacia():
            p = self._pedidos_espera._urgentes.desencolar()
            if p.id != id_pedido:
                urgentes.append(p)
        while not self._pedidos_espera._normales.esta_vacia():
            p = self._pedidos_espera._normales.desencolar()
            if p.id != id_pedido:
                normales.append(p)
        for p in urgentes:
            self._pedidos_espera.encolar(p, urgente=True)
        for p in normales:
            self._pedidos_espera.encolar(p, urgente=False)

    def _restaurar_estado_en_historial(self, id_pedido: int, estado: EstadoPedido) -> None:
        """Restaura el estado de un pedido en el historial del cliente. # recorre todos los elementos."""
        for i in range(self._clientes._capacidad):
            lista = self._clientes._tabla[i]
            if lista is not None:
                temp = lista._cabeza
                while temp is not None:
                    cliente = temp.dato[1]
                    if cliente.historial is not None:
                        temp2 = cliente.historial._cabeza
                        while temp2 is not None:
                            if temp2.dato.id == id_pedido:
                                temp2.dato.estado = estado
                                return
                            temp2 = temp2._siguiente
                    temp = temp._siguiente

    def ver_cola_espera(self) -> str:
        """Retorna representacion de la cola de espera. # recorre todos los elementos."""
        return str(self._pedidos_espera)

    def total_pedidos_cliente(self, codigo_cliente: int) -> float:
        """Total recursivo de los pedidos de un cliente. # recorre todos los elementos."""
        cliente = self._clientes.buscar(codigo_cliente)
        if cliente is None or cliente.historial is None:
            return 0.0
        # Convertir historial doble a nodos simples para recursion
        # sumar_valores espera nodos de lista simple; usamos la cabeza del historial doble
        return sumar_valores(cliente.historial._cabeza)  # type: ignore[arg-type]

    def contar_urgentes_cliente(self, codigo_cliente: int) -> int:
        """Cuenta pedidos urgentes del cliente recursivamente. # recorre todos los elementos."""
        cliente = self._clientes.buscar(codigo_cliente)
        if cliente is None or cliente.historial is None:
            return 0
        return contar_urgentes(cliente.historial._cabeza)  # type: ignore[arg-type]

    def imprimir_historial_cliente(self, codigo_cliente: int) -> None:
        """Imprime el historial de un cliente (normal y reverso). # recorre todos los elementos."""
        cliente = self._clientes.buscar(codigo_cliente)
        if cliente is None:
            print("Cliente no encontrado.")
            return
        print(f"Historial de {cliente.nombre} (codigo {cliente.codigo}):")
        if cliente.historial is None or cliente.historial.esta_vacia():
            print("  (sin pedidos)")
            return
        temp = cliente.historial._cabeza
        while temp is not None:
            print("  ", temp.dato)
            temp = temp._siguiente
        print("  Reversa:")
        imprimir_reversa_recursivo(cliente.historial._cabeza)  # type: ignore[arg-type]
        print()
