# Agente de IA para Hex con MCTS

Este proyecto implementa un agente de inteligencia artificial para el juego de mesa **Hex** utilizando **Monte Carlo Tree Search** (MCTS) con mejoras comunes que incluyen **Upper Confidence Bounds for Trees** (UCT), **All Moves As First** (AMAF) y **Rapid Action Value Estimation** (RAVE). El agente está diseñado para tomar decisiones estratégicas en Hex, un juego de estrategia basado en conexiones jugado en una cuadrícula hexagonal.

## Acerca de Hex
Hex es un juego de estrategia para dos jugadores que se juega en un tablero en forma de rombo compuesto por celdas hexagonales. Los jugadores se turnan para colocar piezas (generalmente negras y blancas) en celdas vacías, con el objetivo de conectar sus dos lados opuestos del tablero con una cadena continua de piezas.

## Glosario
- **MCTS**: Algoritmo central de búsqueda para la selección de movimientos.
- **UCT**: Equilibra la exploración y la explotación en el árbol de búsqueda.
- **AMAF**: Incorpora información heurística de todos los movimientos en las simulaciones.
- **RAVE**: Acelera el aprendizaje compartiendo estimaciones de valor entre movimientos relacionados.

## Detalles
- **MCTS**: Un algoritmo de búsqueda basado en simulación que construye un árbol de juego muestreando de forma aleatoria todos los movimientos posibles.
- **UCT**: Guía la fase de selección (seleccionar el primer movimiento) priorizando nodos con alto potencial, equilibrando exploración (probar nuevos movimientos) y explotación (centrarse en movimientos prometedores).
- **AMAF**: Mejora las simulaciones tratando todos los movimientos en una simulación aleatoria como si fueran jugados primero, es decir, compartiendo estimaciones de valor entre movimientos que conducen a estados de tablero iguales pero en orden distinto, acelerando la convergencia en el árbol de búsqueda.
- **RAVE**: Combina los valores de **UCT** y **AMAF** para comenzar la exploración de forma puramente heurística hasta un límite de visitas para cada nodo en particular.

## MCTS: Ventajas y Desventajas

### Ventajas de MCTS

- **Escalabilidad**: MCTS puede manejar juegos con espacios de búsqueda enormes debido a su naturaleza basada en simulaciones aleatorias y no en la exploración exhaustiva del árbol de búsqueda.
- **Adaptabilidad**: No requiere un modelo de juego perfecto, heurística explícita o evaluación precisa de las posiciones.
- **Eficiencia en el tiempo**: MCTS encuentra una solución suficientemente buena de manera eficiente y converge a Minimax.

### Desventajas de MCTS

- **Requiere una gran cantidad de simulaciones**: Para obtener resultados precisos, MCTS necesita realizar un gran número de simulaciones, lo que puede ser costoso en términos de tiempo. Se intenta aliviar este problema mediante **AMAF**.
- **Subóptimo en juegos pequeños**: En juegos con pocos movimientos posibles (por ejemplo, tableros pequeños), MCTS puede ser menos eficiente que otros enfoques como Minimax con alfa-beta prunning.
