# DomiRuta Manizales

Sistema de gestión de domicilios en Python con estructuras de datos implementadas desde cero.

## Proyecto académico
- **Curso:** Estructuras de datos aplicadas — Código 230G8F (3 créditos)
- **Docente:** Julián David Buitrago Orozco
- **Nivel:** Intermedio (requisito: Programación Orientada a Objetos)
- **Lenguaje:** Python 3.10+

## Integrantes
- Coral Dayane Pérez Manrique
- Juan David Castro Higuera

## Estructura del proyecto
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

## Requisitos
- Python 3.10 o superior.
- No se requieren paquetes externos.

## Ejecución
Desde la carpeta `domiruta/`:

```bash
python main.py
```

Para ejecutar solo las pruebas:

```bash
python pruebas.py
```

## Menú principal
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
Consulte `ANALISIS.md` para la tabla consolidada de complejidades (Big O), los
resultados de los experimentos y las respuestas al análisis.

## Reglas técnicas
- Todas las estructuras se construyen con nodos enlazados; no se usan `list`,
  `dict`, `set`, `tuple`, `collections`, `heapq`, `queue` ni `bisect` como
  soporte de las estructuras (salvo el arreglo de tamaño fijo de la tabla hash
  y la matriz de adyacencia).
- Cada clase y método público tiene docstring y comentario de complejidad Big O.
- Anotaciones de tipo (`typing.Generic`) y PEP 8.
