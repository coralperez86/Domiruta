# ANALISIS.md — DomiRuta Manizales

## 1. Tabla consolidada de complejidades (Big O)

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

### Fase 2 — Pilas, colas y tabla hash

| Operación | Complejidad | Notas |
|-----------|-------------|-------|
| Pila.apilar / desapilar / cima | O(1) | Tope directo |
| Cola.encolar / desencolar / frente | O(1) | Frente y final directos |
| ColaPrioridad.encolar | O(1) | Dos colas internas (urgentes/normales) |
| ColaPrioridad.desencolar | O(1) | Atiende urgentes primero |
| TablaHash.insertar | O(1) promedio | Encadenamiento + redimensionamiento amortizado |
| TablaHash.buscar | O(1) promedio | Encadenamiento |
| TablaHash.eliminar | O(1) promedio | Encadenamiento |
| TablaHash.factor_carga | O(1) | División directa |

### Fase 3 — Árboles BST y AVL

| Operación | BST | AVL | Notas |
|-----------|-----|-----|-------|
| insertar | O(h) | O(log n) | h = altura |
| buscar | O(h) | O(log n) | |
| eliminar | O(h) | O(log n) | Tres casos en BST |
| minimo / maximo | O(h) | O(h) | |
| altura | O(n) recursivo | O(n) | |
| contar_nodos / contar_hojas | O(n) recursivo | O(n) | |
| preorden / inorden / postorden | O(n) | O(n) | Recursivos |
| por niveles | O(n) | — | Usa Cola (Fase 2) |

### Fase 4 — Grafos

| Operación | Complejidad | Notas |
|-----------|-------------|-------|
| Grafo.agregar_vertice / agregar_arista | O(n²) | Redimensionamiento de matriz |
| Grafo.grado | O(n) | Longitud de lista de adyacencia |
| Grafo.orden | O(1) | Contador de vértices |
| Grafo.son_adyacentes | O(n) | Acceso a matriz |
| BFS | O(n + m) | Usa Cola (Fase 2) |
| DFS recursivo | O(n + m) | Recursivo |
| DFS iterativo | O(n + m) | Usa Pila (Fase 2) |
| Dijkstra | O((n + m) log n) | Usa ColaPrioridad + pila para ruta |
| Prim | O(n²) | Arbol de expansión mínima |
| Kruskal | O(m log m) | Arbol de expansión mínima |
| Floyd-Warshall | O(n³) | Bonificación |

## 2. Experimentos

### Experimento A — Lista enlazada vs Tabla hash (Fase 2)
Se cargaron 10 000 clientes generados aleatoriamente y se midieron 1 000
búsquedas con `time.perf_counter()`.

| Estructura | Tiempo 1 000 búsquedas | Comentario |
|------------|------------------------|------------|
| Lista enlazada | ~ O(n) por búsqueda, lineal creciente | Peor caso recorre toda la lista |
| Tabla hash | ~ O(1) promedio | Constante, independiente de n |

Resultado: la tabla hash es significativamente más rápida que la búsqueda
lineal en la lista enlazada, especialmente a medida que crece la cantidad de
clientes. La búsqueda lineal tiene complejidad O(n) mientras que la tabla hash
tiene O(1) promedio gracias al encadenamiento y la función hash.

### Experimento B — Altura BST vs AVL (Fase 3)
Se insertaron los códigos 1, 2, 3, ..., 500 en orden.

| Árbol | Altura final | Comentario |
|-------|--------------|------------|
| BST | 500 | Se degrada en una lista enlazada (peor caso) |
| AVL | ~9 (logarítmica) | Se mantiene balanceado tras cada inserción |

Diferencia: el BST insertado en orden queda completamente desbalanceado (altura
igual al número de nodos), lo que hace que sus operaciones pasen de O(log n) a
O(n). El AVL, gracias a las cuatro rotaciones (LL, RR, LR, RL), se mantiene
balanceado con altura O(log n), preservando el rendimiento de búsqueda,
inserción y eliminación.

Reto opcional (2 000 claves): el BST degenerado provoca `RecursionError` al
superar el límite de recursión de Python (~1000), mientras que el AVL sigue
funcionando correctamente.

## 3. Respuestas a las preguntas de análisis

**P1: ¿Por qué se elige una lista enlazada para el historial de pedidos de cada cliente?**
Permite insertar pedidos al final en O(1) y, al ser doblemente enlazada, recorrer
del más reciente al más antiguo en O(n) usando el puntero anterior. Además es la
estructura base para el encadenamiento de la tabla hash.

**P2: ¿Por qué una tabla hash para buscar clientes por código?**
Ofrece búsqueda O(1) promedio frente a O(n) de la lista enlazada, lo que es
crítico cuando hay miles de clientes. El manejo de colisiones por encadenamiento
con listas enlazadas y el redimensionamiento al superar el factor de carga 0.75
mantienen el rendimiento estable.

**P3: ¿Por qué el AVL en lugar de un BST simple para el directorio de clientes?**
El BST simple puede degradarse a O(n) si se insertan códigos ordenados (altura
igual a n). El AVL se auto-balancea tras cada inserción con rotaciones,
garantizando O(log n) y reportes ordenados eficientes mediante inorden.

**P4: ¿Cómo se integra todo el sistema en la asignación de un pedido?**
Al asignar el siguiente pedido (cola de prioridad, Fase 2), se calcula la ruta
más corta desde Centro hasta el barrio destino con Dijkstra sobre el grafo
(Fase 4), se muestra al operador, y el pedido se agrega al historial del cliente
(lista doble, Fase 1). Además, la operación se apila en la pila de deshacer
(Fase 2).

## 4. Estructuras reutilizadas entre fases
- `ListaEnlazada` (Fase 1): base del encadenamiento de `TablaHash` (Fase 2) y de
  la lista de adyacencia de `Grafo` (Fase 4).
- `Cola` (Fase 2): usada en BFS y recorrido por niveles del BST (Fase 3).
- `Pila` (Fase 2): usada en DFS iterativo (Fase 4) y reconstrucción de ruta de
  Dijkstra.
- `ColaPrioridad` (Fase 2): usada en la cola de espera de pedidos y en Dijkstra.
- `ArbolAVL` (Fase 3): usado en `DirectorioClientes` para reportes ordenados.
