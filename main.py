"""Menu principal de consola de DomiRuta Manizales."""

from __future__ import annotations

from servicios.gestor_pedidos import GestorPedidos  # type: ignore
from servicios.directorio_clientes import DirectorioClientes  # type: ignore
from servicios.rutas import Rutas  # type: ignore
from modelo.cliente import Cliente  # type: ignore
from modelo.pedido import EstadoPedido  # type: ignore
from pruebas import ejecutar_pruebas  # type: ignore


def menu_principal() -> None:
    """Ejecuta el menu principal de la aplicacion. # es rapido. por opcion"""
    gestor = GestorPedidos()
    directorio = DirectorioClientes()
    rutas = Rutas()

    while True:
        print("\n================ DOMIRUTA MANIZALES ================")
        print("1. Registrar cliente")
        print("2. Buscar cliente por codigo")
        print("3. Crear pedido")
        print("4. Asignar siguiente pedido")
        print("5. Cancelar pedido")
        print("6. Ver cola de espera")
        print("7. Deshacer ultima operacion")
        print("8. Reporte clientes ordenados")
        print("9. Reporte clientes en rango de codigos")
        print("10. Ver mapa (matriz y lista de adyacencia)")
        print("11. Grado de un barrio")
        print("12. Conectividad y BFS desde un barrio")
        print("13. DFS recursivo desde un barrio")
        print("14. DFS iterativo desde un barrio")
        print("15. Ruta mas corta (Dijkstra)")
        print("16. Red minima de vias (Prim/Kruskal)")
        print("17. Ejecutar pruebas")
        print("18. Floyd-Warshall (bonificacion)")
        print("0. Salir")
        print("==================================================")
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            _op_registrar_cliente(gestor, directorio)
        elif opcion == "2":
            _op_buscar_cliente(gestor)
        elif opcion == "3":
            _op_crear_pedido(gestor)
        elif opcion == "4":
            _op_asignar_pedido(gestor, rutas)
        elif opcion == "5":
            _op_cancelar_pedido(gestor)
        elif opcion == "6":
            _op_ver_cola(gestor)
        elif opcion == "7":
            _op_deshacer(gestor)
        elif opcion == "8":
            _op_reporte_ordenado(directorio)
        elif opcion == "9":
            _op_reporte_rango(directorio)
        elif opcion == "10":
            rutas.ver_mapa()
        elif opcion == "11":
            _op_grado(rutas)
        elif opcion == "12":
            _op_conectividad(rutas)
        elif opcion == "13":
            _op_dfs_recursivo(rutas)
        elif opcion == "14":
            _op_dfs_iterativo(rutas)
        elif opcion == "15":
            _op_ruta_mas_corta(rutas)
        elif opcion == "16":
            _op_red_minima(rutas)
        elif opcion == "17":
            ejecutar_pruebas()
        elif opcion == "18":
            rutas.floyd_warshall()
        elif opcion == "0":
            print("Saliendo de DomiRuta. ¡Hasta pronto!")
            break
        else:
            print("Opcion invalida. Intente de nuevo.")


def _op_registrar_cliente(gestor: GestorPedidos, directorio: DirectorioClientes) -> None:
    try:
        codigo = int(input("Codigo del cliente: ").strip())
    except ValueError:
        print("Codigo invalido.")
        return
    nombre = input("Nombre: ").strip()
    telefono = input("Telefono: ").strip()
    barrio = input("Barrio: ").strip()
    if gestor.registrar_cliente(codigo, nombre, telefono, barrio):
        directorio.insertar(Cliente(codigo, nombre, telefono, barrio))
        print("Cliente registrado.")
    else:
        print("El cliente ya existe.")


def _op_buscar_cliente(gestor: GestorPedidos) -> None:
    try:
        codigo = int(input("Codigo del cliente: ").strip())
    except ValueError:
        print("Codigo invalido.")
        return
    cliente = gestor.buscar_cliente(codigo)
    if cliente:
        print(cliente)
    else:
        print("Cliente no encontrado.")


def _op_crear_pedido(gestor: GestorPedidos) -> None:
    try:
        codigo_cliente = int(input("Codigo del cliente: ").strip())
    except ValueError:
        print("Codigo invalido.")
        return
    cliente = gestor.buscar_cliente(codigo_cliente)
    if not cliente:
        print("Cliente no encontrado.")
        return
    descripcion = input("Descripcion del pedido: ").strip()
    try:
        valor = float(input("Valor: ").strip())
    except ValueError:
        print("Valor invalido.")
        return
    barrio_destino = input("Barrio destino: ").strip()
    urgente = input("¿Urgente? (s/n): ").strip().lower() == "s"
    pedido = gestor.crear_pedido(
        codigo_cliente, descripcion, valor, barrio_destino, urgente
    )
    if pedido:
        print(f"Pedido creado: {pedido}")
    else:
        print("No se pudo crear el pedido.")


def _op_asignar_pedido(gestor: GestorPedidos, rutas: Rutas) -> None:
    pedido = gestor.asignar_siguiente_pedido()
    if pedido is None:
        print("No hay pedidos en espera.")
        return
    print(f"Pedido asignado: {pedido}")
    # Mostrar ruta mas corta desde Centro hasta el barrio destino
    print("Calculando ruta desde Centro hasta el destino del pedido...")
    rutas.ruta_mas_corta("Centro", pedido.barrio_destino)


def _op_cancelar_pedido(gestor: GestorPedidos) -> None:
    try:
        id_pedido = int(input("ID del pedido a cancelar: ").strip())
    except ValueError:
        print("ID invalido.")
        return
    if gestor.cancelar_pedido(id_pedido):
        print(f"Pedido {id_pedido} cancelado.")
    else:
        print("No se encontro el pedido pendiente o ya no esta en espera.")


def _op_ver_cola(gestor: GestorPedidos) -> None:
    print("Cola de espera:")
    print(gestor.ver_cola_espera())


def _op_deshacer(gestor: GestorPedidos) -> None:
    if gestor.deshacer():
        print("Ultima operacion deshecha.")
    else:
        print("No hay operaciones que deshacer.")


def _op_reporte_ordenado(directorio: DirectorioClientes) -> None:
    directorio.reporte_ordenado()


def _op_reporte_rango(directorio: DirectorioClientes) -> None:
    try:
        a = int(input("Codigo inicial: ").strip())
        b = int(input("Codigo final: ").strip())
    except ValueError:
        print("Codigos invalidos.")
        return
    directorio.reporte_rango(a, b)


def _op_grado(rutas: Rutas) -> None:
    barrio = input("Nombre del barrio: ").strip()
    rutas.grado_barrio(barrio)


def _op_conectividad(rutas: Rutas) -> None:
    inicio = input("Barrio de inicio (Enter = Centro): ").strip() or "Centro"
    rutas.conectividad(inicio)


def _op_dfs_recursivo(rutas: Rutas) -> None:
    inicio = input("Barrio de inicio: ").strip()
    rutas.dfs_recursivo(inicio)


def _op_dfs_iterativo(rutas: Rutas) -> None:
    inicio = input("Barrio de inicio: ").strip()
    rutas.dfs_iterativo(inicio)


def _op_ruta_mas_corta(rutas: Rutas) -> None:
    origen = input("Barrio origen: ").strip()
    destino = input("Barrio destino: ").strip()
    rutas.ruta_mas_corta(origen, destino)


def _op_red_minima(rutas: Rutas) -> None:
    algo = input("Algoritmo (prim/kruskal): ").strip() or "prim"
    rutas.red_minima(algo)


if __name__ == "__main__":
    menu_principal()
