# DomiRuta Manizales

Sistema de gestión de domicilios en Python con estructuras de datos implementadas desde cero.

## Proyecto académico
- **Curso:** Estructuras de datos aplicadas 
- **Docente:** Julián David Buitrago Orozco

## Integrantes
- Coral Dayane Pérez Manrique
- Juan David Castro Higuera

## Ejecución
Desde la carpeta `domiruta/`:

```bash
python main.py
```

Para ejecutar solo las pruebas:

```bash
python pruebas.py
```

## Menú principal (Así quedará) - Más o menos :)
1. Registrar cliente
2. Buscar cliente por código
3. Crear pedido
4. Asignar siguiente pedido (cola de prioridad + Dijkstra)
5. Cancelar pedido
6. Ver cola de espera
7. Deshacer última operación (pila)
8. Reporte clientes ordenados (AVL inorden)
9. Reporte clientes en rango de códigos
10. Ver mapa (matriz y lista de adyacencia)
11. Grado de un barrio
12. Conectividad y BFS desde un barrio
13. DFS recursivo desde un barrio
14. DFS iterativo desde un barrio
15. Ruta más corta (Dijkstra)
16. Red mínima de vías (Prim / Kruskal)
17. Ejecutar pruebas
18. Floyd-Warshall (bonificación)
0. Salir

## Complejidades
### Fase 1 — Listas y recursión

| Operación | Complejidad | Notas |
|-----------|-------------|-------|
| ListaEnlazada.insertar_inicio | O(1) | Cabeza directa |
| ListaEnlazada.insertar_final | O(1) | Mantiene referencia a cola |
| ListaEnlazada.insertar_en | O(n) | Recorrido hasta la posición |
| ListaEnlazada.eliminar | O(n) | Búsqueda y reencadenado |
| ListaEnlazada.buscar | O(n) | Recorrido secuencial |
| ListaEnlazada.obtener | O(n) | Recorrido hasta la posición |
| ListaEnlazada.__len__ / esta_vacia | O(1) | Contador mantenido |
| ListaDoble.imprimir_reversa | O(n) | Recorrido con puntero anterior |
| sumar_valores | O(n) | Recursión lineal, caso base nodo None |
| contar_urgentes | O(n) | Recursión lineal |
| buscar_recursivo | O(n) | Recursión lineal |
| imprimir_reversa_recursivo | O(n) | Recursión lineal (no de cola) |
| invertir_lista / invertir | O(n) | Recursión lineal (no de cola) |

Límite de recursión de Python: ~1000 llamadas (sys.getrecursionlimit()). Se
menciona porque el BST degenerado con 500 claves ordenadas se acerca a ese
límite; con 2000 claves provocaría RecursionError.

## Reglas técnicas
- Todas las estructuras se construyen con nodos enlazados; no se usan `list`,
  `dict`, `set`, `tuple`, `collections`, `heapq`, `queue` ni `bisect` como
  soporte de las estructuras (salvo el arreglo de tamaño fijo de la tabla hash
  y la matriz de adyacencia).
- Cada clase y método público tiene docstring y comentario de complejidad Big O.
- Anotaciones de tipo (`typing.Generic`) y PEP 8.


## Esta sería la estructura del proyecto (Más o menos) :)
```
domiruta/
├── estructuras/          # Biblioteca propia de estructuras de datos
│   ├── __init__.py
│   ├── nodo.py           # Nodo, NodoDoble
│   ├── lista_enlazada.py # ListaEnlazada
│   ├── lista_doble.py    # ListaDoble
│   ├── pila.py           # Pila
│   ├── cola.py           # Cola
│   ├── cola_prioridad.py # ColaPrioridad
│   ├── tabla_hash.py     # TablaHash
│   ├── arbol_bst.py      # ArbolBST
│   ├── arbol_avl.py      # ArbolAVL
│   └── grafo.py          # Grafo
├── modelo/               # Clases del negocio
│   ├── cliente.py        # Cliente
│   ├── pedido.py         # Pedido, EstadoPedido
│   └── operacion.py      # Operacion
├── servicios/            # Logica de negocio
│   ├── gestor_pedidos.py      # GestorPedidos
│   ├── directorio_clientes.py # DirectorioClientes
│   └── rutas.py               # Rutas
├── util/
│   ├── __init__.py
│   └── recursion.py     # Funciones recursivas
├── datos/
│   └── mapa.txt         # Mapa de Manizales (12 barrios, 18 vias)
├── docs/                # Seguimiento AVL y diagrama de clases
├── pruebas.py           # Casos de prueba minimos (12)
├── main.py              # Menu principal
├── README.md
└── ANALISIS.md
```
