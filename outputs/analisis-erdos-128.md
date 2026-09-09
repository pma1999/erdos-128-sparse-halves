# Erdős #128: límite verificado de una vía de demostración

Estado: la conjetura general no está resuelta por este análisis. No se ha obtenido un contraejemplo.

## Objetivo exacto

Demostrar que todo grafo sin triángulos con n vértices tiene un conjunto de exactamente floor(n/2) vértices que induce como máximo n²/50 aristas. Esta formulación es equivalente a la del archivo: basta considerar conjuntos del tamaño mínimo, porque añadir vértices no elimina aristas.

## Fórmula examinada

La prueba parcial de Amir Sarid emplea, para grado máximo menor que n/2, la desigualdad

β*(G) ≤ ρ/8 − t(C₄,G)/(4ρ),

donde ρ=2e(G)/n², t(C₄,G)=hom(C₄,G)/n⁴ y β* es el coste mínimo normalizado de una mitad fraccionaria. Su lema de redondeo permite pasar a una mitad entera sin incrementar el coste normalizado. Véanse el lema de anclaje y el lema de redondeo en la [fuente del artículo](https://raw.githubusercontent.com/aimir/erdos-128-sparse-halves/main/sparse_halves_simple.tex).

Para que el miembro derecho sea ≤1/50, sería necesario que

t(C₄,G) ≥ ρ²/2 − 2ρ/25.

Esta última desigualdad NO es válida para todos los grafos sin triángulos.

## Verificación independiente: grafo de Clebsch

Construcción: los 16 vectores binarios de longitud cuatro son los vértices; dos son adyacentes si su distancia de Hamming es uno o cuatro. Cada vértice tiene cinco vecinos. No hay triángulos, como comprueba el script inspeccionando la intersección de las vecindades de cada arista.

Los cálculos exactos dan:

| Cantidad | Valor |
| --- | --- |
| Vértices | 16 |
| Aristas | 40 |
| ρ | 5/16 |
| hom(C₄,G) | 1040 |
| t(C₄,G) | 65/4096 |
| ρ/8 − t(C₄,G)/(4ρ) | 27/1024 |
| t(C₄,G) exigido por esa fórmula para alcanzar 1/50 | 61/2560 |
| Mínimo real de aristas entre las 12.870 mitades | 4 |

En particular, 65/4096 < 61/2560 y 27/1024 > 1/50. No existe una mejora válida de la estimación inferior de t(C₄,G) que haga que ESTA fórmula alcance 1/50 en todos los grafos: en este ejemplo ya se ha introducido el valor exacto.

Para cada arista uv se probaron también las dos mitades fraccionarias del argumento: valor uno en N(u) (o N(v)), cero en la otra vecindad y 1/2 en los seis vértices restantes. Todas tienen coste sin normalizar 27/4. La pérdida no procede aquí de promediar diferentes costes.

El conjunto {0,1,6,7,10,11,12,13}, con los vectores identificados por sus valores binarios, induce cuatro aristas. Se enumeraron todas las combinaciones de ocho vértices: diez de ellas alcanzan ese mínimo. Como 4 < 256/50, este grafo satisface la conjetura y NO es un contraejemplo.

## Consecuencia para continuar

Queda descartado resolver el problema únicamente fortaleciendo el recuento de C₄ dentro de la fórmula anterior. Haría falta otro argumento, una construcción más eficaz de mitades, o una división en casos que trate por separado los grafos donde esa fórmula falla. Este cálculo no descarta mejoras mediante redondeo, perturbaciones adicionales ni el método completo de Sarid, que dispone de otra rama.

La comprobación es finita y usa aritmética racional exacta; no demuestra una afirmación universal sobre todos los grafos. El script reproducible y sus resultados están en esta misma carpeta.

## Una obstrucción más fuerte: completar una vecindad tampoco basta

La siguiente modificación natural también falla: fijar una vecindad completa y escoger óptimamente los vértices restantes de la mitad, permitiendo escogerlos en cualquier parte del grafo.

**Proposición.** En el grafo de Clebsch, toda mitad que contiene N(u), para algún vértice u, induce al menos seis aristas. Este mínimo se alcanza. En cambio, el mínimo entre todas las mitades es cuatro.

**Demostración del límite inferior.** Se puede suponer u=0000, porque sumar un vector binario fijo preserva las distancias. Los cinco vecinos de u son los cuatro vectores de peso uno y 1111. Cada vértice exterior distinto de u tiene peso dos o tres y exactamente dos vecinos en N(u): para peso dos son los dos vectores unitarios contenidos en él; para peso tres son 1111 y el vector unitario de la coordenada ausente. El propio u tiene cinco vecinos en N(u). Una mitad que contiene los cinco vértices de N(u) debe añadir otros tres; cada uno aporta al menos dos aristas hacia N(u). Por tanto induce al menos seis aristas. La enumeración independiente encuentra mitades de este tipo con exactamente seis.

La desigualdad 6 > 256/50 demuestra que esta familia de selecciones no basta, aunque se optimice exactamente el completado. Además, se enumeraron todos los conjuntos independientes: la independencia máxima es cinco y los 16 conjuntos que la alcanzan son precisamente las vecindades. Así, tampoco basta imponer que la mitad contenga un conjunto independiente de tamaño máximo.

La obstrucción persiste en las ampliaciones equilibradas del grafo: sustituir cada vértice por t gemelos independientes produce 16t vértices. Una mitad que contiene la vecindad completa de un vértice contiene 5t vértices fijados y debe añadir 3t más. Cada vértice añadido tiene al menos 2t vecinos en la parte fijada; el coste es al menos 6t² > (16t)²/50. El mismo argumento se aplica a selecciones fraccionarias con valor uno en toda esa vecindad.

Esta proposición descarta una estrategia, no la conjetura. Obliga a permitir que una construcción universal abandone parte de cualquier vecindad que haya usado inicialmente.

## Búsqueda exacta de contraejemplos

El archivo `search-counterexample.py` implementa generación de restricciones con Z3. Para un orden n fija k=floor(n/2) y q=floor(n²/50)+1. Usa una variable booleana por arista, prohíbe cada triángulo y añade progresivamente las restricciones e(S)≥q para conjuntos S de tamaño k.

Dos restricciones iniciales necesarias reducen la búsqueda sin excluir contraejemplos: el grado máximo es menor que k, porque toda vecindad es independiente; y el número de aristas es al menos ceil(q n(n−1)/(k(k−1))), por promedio sobre todas las mitades. Ordenar los grados de forma decreciente solo fija un etiquetado.

Cada grafo propuesto se comprueba con un buscador independiente de mitades que usa enteros de Python y ramificación exhaustiva. Su poda suma las menores contribuciones hacia los vértices ya seleccionados; omitir las aristas entre futuras incorporaciones da una cota inferior válida. Se contrastó este procedimiento con enumeración completa en 84 grafos pequeños, con 168 comprobaciones de umbral.

Un resultado `unresolved_solver_unknown` o `budget_exhausted` no demuestra inexistencia. Las restricciones se guardan y pueden retomarse. Un resultado negativo del solver solo afecta al orden especificado y requeriría un certificado revisable antes de presentarlo como un teorema formalmente verificado. Un candidato positivo debe reproducirse independientemente antes de anunciar un contraejemplo.
