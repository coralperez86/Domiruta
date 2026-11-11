"""Casos de prueba mínimos del proyecto DomiRuta.

Ejecutar con: python pruebas.py
"""

from __future__ import annotations

from estructuras.lista_enlazada import ListaEnlazada  # type: ignore
from estructuras.pila import Pila  # type: ignore
from estructuras.cola import Cola  # type: ignore
from estructuras.cola_prioridad import ColaPrioridad  # type: ignore
from estructuras.tabla_hash import TablaHash  # type: ignore
from estructuras.arbol_bst import ArbolBST  # type: ignore
from estructuras.arbol_avl import ArbolAVL  # type: ignore
from estructuras.grafo import Grafo  # type: ignore
from modelo.pedido import Pedido, EstadoPedido  # type: ignore
from util.recursion import invertir_lista  # type: ignore


def _caso(nombre: str, condicion: bool, detalle: str = "") -> bool:
    estado = "PASS" if condicion else "FAIL"
    print(f"[{estado}] {nombre}" + (f" - {detalle}" if detalle else ""))
    return condicion


def prueba_1_eliminar_lista_vacia() -> bool:
    """Eliminar de una lista vacía retorna false sin lanzar error."""
    lista = ListaEnlazada[int]()
    try:
        resultado = lista.eliminar(5)
        return _caso("1. Eliminar de lista vacia", resultado is False, "retorna False")
    except Exception as e:
        return _caso("1. Eliminar de lista vacia", False, f"lanzo excepcion: {e}")


def prueba_2_invertir_recursiva() -> bool:
    """Invertir recursivamente 1 -> 2 -> 3 -> 4 da 4 -> 3 -> 2 -> 1."""
    lista = ListaEnlazada[int]()
    for v in (1, 2, 3, 4):
        lista.insertar_final(v)
    nueva_cabeza = invertir_lista(lista._cabeza)  # type: ignore[arg-type]
    lista._cabeza = nueva_cabeza
    # Reconstruir cola
    actual = lista._cabeza
    lista._cola = None
    lista._tamano = 0
    while actual is not None:
        lista._tamano += 1
        if actual._siguiente is None:
            lista._cola = actual
        actual = actual._siguiente
    valores = [x for x in lista]
    return _caso(
        "2. Invertir recursivamente 1-2-3-4",
        valores == [4, 3, 2, 1],
        f"resultado: {valores}",
    )


def prueba_3_crear_cancelar_deshacer() -> bool:
    """Crear pedido, cancelarlo y deshacer: el pedido vuelve a EN_ESPERA."""
    from servicios.gestor_pedidos import GestorPedidos  # type: ignore

    gestor = GestorPedidos()
    gestor.registrar_cliente(1, "Ana", "300", "Centro")
    pedido = gestor.crear_pedido(1, "Descripcion", 10.0, "Centro", urgente=False)
    assert pedido is not None
    assert pedido.estado == EstadoPedido.EN_ESPERA
    gestor.cancelar_pedido(pedido.id)
    assert pedido.estado == EstadoPedido.CANCELADO
    gestor.deshacer()
    resultado = pedido.estado == EstadoPedido.EN_ESPERA
    return _caso("3. Crear, cancelar y deshacer", resultado, f"estado={pedido.estado.value}")


def prueba_4_cola_prioridad() -> bool:
    """Enc: normal A, urgente B, normal C, urgente D -> desencolar: B, D, A, C."""
    cola = ColaPrioridad[str]()
    cola.encolar("A", urgente=False)
    cola.encolar("B", urgente=True)
    cola.encolar("C", urgente=False)
    cola.encolar("D", urgente=True)
    secuencia = []
    while not cola.esta_vacia():
        secuencia.append(cola.desencolar())
    return _caso(
        "4. Cola de prioridad",
        secuencia == ["B", "D", "A", "C"],
        f"resultado: {secuencia}",
    )


def prueba_5_tabla_hash_colisiones() -> bool:
    """Insertar codigos 3, 14 y 25 (capacidad 11) quedan en posicion 3 y se encuentran."""
    tabla = TablaHash[int, str]()
    for c in (3, 14, 25):
        tabla.insertar(c, f"cliente{c}")
    encontrados = all(
        tabla.buscar(c) == f"cliente{c}" for c in (3, 14, 25)
    )
    return _caso(
        "5. Hash colisiones (3,14,25 en pos 3)",
        encontrados,
        "todos se encuentran",
    )


def prueba_6_redimensionamiento() -> bool:
    """Insertar 12 elementos en hash capacidad 11: se redimensiona y conserva datos."""
    tabla = TablaHash[int, str]()
    for i in range(1, 13):
        tabla.insertar(i, f"v{i}")
    conservados = all(tabla.buscar(i) == f"v{i}" for i in range(1, 13))
    return _caso(
        "6. Redimensionamiento (12 elementos)",
        conservados and tabla.factor_carga() <= 0.75,
        f"factor_carga={tabla.factor_carga():.2f}",
    )


def prueba_7_avl_ll() -> bool:
    """Insertar AVL 10, 20, 30: rotacion simple izquierda, raiz = 20."""
    avl = ArbolAVL[int]()
    for v in (10, 20, 30):
        avl.insertar(v)
    raiz = avl._raiz  # type: ignore[attr-defined]
    rotacion_ok = raiz is not None and raiz.dato == 20
    return _caso(
        "7. AVL insert 10,20,30 -> rotacion RR, raiz=20",
        rotacion_ok,
        f"raiz={raiz.dato if raiz else None}",
    )


def prueba_8_avl_lr() -> bool:
    """Insertar AVL 30, 10, 20: rotacion doble izquierda-derecha, raiz = 20."""
    avl = ArbolAVL[int]()
    for v in (30, 10, 20):
        avl.insertar(v)
    raiz = avl._raiz  # type: ignore[attr-defined]
    rotacion_ok = raiz is not None and raiz.dato == 20
    return _caso(
        "8. AVL insert 30,10,20 -> rotacion LR, raiz=20",
        rotacion_ok,
        f"raiz={raiz.dato if raiz else None}",
    )


def prueba_9_grado_centro() -> bool:
    """Grado del barrio Centro es 4."""
    grafo = Grafo()
    grafo.cargar_desde_archivo("datos/mapa.txt")
    grado = grafo.grado("Centro")
    return _caso(
        "9. Grado del barrio Centro",
        grado == 4,
        f"grado={grado}",
    )


def prueba_10_bfs_centro() -> bool:
    """BFS desde Centro visita los 12 barrios."""
    grafo = Grafo()
    grafo.cargar_desde_archivo("datos/mapa.txt")
    orden = grafo.bfs("Centro")
    return _caso(
        "10. BFS desde Centro visita 12 barrios",
        len(orden) == 12,
        f"visitados={len(orden)}",
    )


def prueba_11_ruta_misma_barrio() -> bool:
    """Ruta mas corta de un barrio a si mismo: distancia 0."""
    grafo = Grafo()
    grafo.cargar_desde_archivo("datos/mapa.txt")
    distancia, ruta = grafo.dijkstra("Centro", "Centro")
    return _caso(
        "11. Ruta de un barrio a si mismo",
        distancia == 0 and ruta == ["Centro"],
        f"distancia={distancia}, ruta={ruta}",
    )


def prueba_12_arbol_expansion_minima() -> bool:
    """Arbol de expansion minima tiene exactamente 11 vias (n-1)."""
    grafo = Grafo()
    grafo.cargar_desde_archivo("datos/mapa.txt")
    aristas, total = grafo.prim()
    return _caso(
        "12. Arbol expansion minima (11 vias)",
        len(aristas) == 11,
        f"vias={len(aristas)}, total={total}",
    )


def ejecutar_pruebas() -> None:
    """Ejecuta todos los casos de prueba y muestra un resumen. # recorre todos los elementos."""
    print("\n================ EJECUTANDO PRUEBAS ================")
    pruebas = [
        prueba_1_eliminar_lista_vacia,
        prueba_2_invertir_recursiva,
        prueba_3_crear_cancelar_deshacer,
        prueba_4_cola_prioridad,
        prueba_5_tabla_hash_colisiones,
        prueba_6_redimensionamiento,
        prueba_7_avl_ll,
        prueba_8_avl_lr,
        prueba_9_grado_centro,
        prueba_10_bfs_centro,
        prueba_11_ruta_misma_barrio,
        prueba_12_arbol_expansion_minima,
    ]
    resultados = [p() for p in pruebas]
    pasadas = sum(1 for r in resultados if r)
    print(f"\nResultado: {pasadas}/{len(resultados)} pruebas pasadas.")
    if pasadas == len(resultados):
        print("¡Todas las pruebas pasaron!")
    else:
        print("Algunas pruebas fallaron. Revisar detalles arriba.")
    print("====================================================")


if __name__ == "__main__":
    ejecutar_pruebas()
