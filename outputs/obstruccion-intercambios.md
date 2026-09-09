# Por qué los intercambios locales no resuelven por sí solos Erdős #128

El objetivo sigue siendo la conjetura completa. El resultado siguiente descarta una estrategia de prueba; no es un contraejemplo a la conjetura ni se afirma que sea inédito.

## Una familia infinita de mínimos locales por encima de la cota

**Proposición.** Para todo entero t≥1 existe un grafo sin triángulos de n=16t vértices con una mitad S que induce 6t² aristas, más que n²/50, y tal que sustituir r≤t vértices de S por otros r de su complemento nunca reduce ese número. Para r<t, todo intercambio no vacío aumenta estrictamente el número de aristas.

**Construcción.** En el grafo de Clebsch, representado por los enteros 0,…,15 en binario, son adyacentes los pares cuya distancia de Hamming es uno o cuatro. Tomemos

S₀={0,1,2,5,6,7,11,12}.

Induce seis aristas. Los grados hacia S₀ de sus propios vértices son 2,2,2,2,2,2,0,0. Los de los ocho vértices exteriores son 5,5,3,3,3,3,3,3, salvo el orden. Por tanto, el grado hacia S₀ es como máximo dos dentro y como mínimo tres fuera.

Sustituyamos cada vértice por t gemelos independientes, con todas las aristas entre clases correspondientes a una arista original. Sea S la unión de las ocho clases de S₀. El grafo sigue sin triángulos, |S|=8t y e(S)=6t². Los grados hacia S son como máximo 2t dentro y como mínimo 3t fuera.

**Prueba del límite para intercambios.** Sean R⊆S y U⊆V\S, con |R|=|U|=r. Para cualquier grafo, la variación exacta es

\[
e((S\setminus R)\cup U)-e(S)
=\sum_{u\in U}d_S(u)-\sum_{v\in R}d_S(v)
+e(R)+e(U)-e(R,U).
\]

Usando los grados anteriores, e(R),e(U)≥0 y e(R,U)≤r², obtenemos

\[
e((S\setminus R)\cup U)-e(S)\ge3tr-2tr-r^2=r(t-r).
\]

Esto es no negativo para r≤t y positivo para 0<r<t. Finalmente,

\[
\frac{e(S)}{n^2}=\frac6{256}=\frac3{128}>\frac1{50}.
\]

Por otra parte, la mitad {0,1,6,7,10,11,12,13} del grafo original induce cuatro aristas. Su ampliación induce 4t²<n²/50. Así que la construcción cumple la conjetura; solo la mitad localmente estable es demasiado densa.

## Alcance exacto

Para cualquier radio fijo k de intercambio, elegir t>k produce una mitad que supera la cota y desde la cual todo intercambio no vacío de hasta k vértices aumenta el coste. Por tanto, no basta demostrar que un procedimiento de descenso llega a un mínimo local de radio fijo. Tampoco basta la condición de no admitir una mejora en un solo intercambio de hasta n/16 vértices.

Esto no descarta algoritmos que permitan aumentar temporalmente el coste, cambios mayores, reinicios o argumentos que comparen directamente con un mínimo global.

El script `exchange-barrier.py` comprobó la identidad de intercambio para las 12.870 mitades del grafo base. El mínimo por número r de vértices sustituidos es:

| r | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Aristas mínimas | 6 | 6 | 4 | 6 | 4 | 6 | 4 | 6 | 6 |

La demostración para todos los t es algebraica y no depende de extrapolar estos datos.

## Reducción usada para reforzar la búsqueda general

Si existe un contraejemplo, se pueden añadir aristas mientras no creen triángulos. Cada mitad conserva o aumenta su número de aristas, de modo que sigue siendo un contraejemplo. El proceso finito termina en un grafo maximal sin triángulos.

En tal grafo, cada par no adyacente tiene un vecino común: de lo contrario se podría añadir su arista sin crear triángulos. Recíprocamente, esta condición junto con la ausencia de triángulos expresa exactamente la maximalidad.

El buscador incorpora ahora esta condición, además de conservar las restricciones de mitades obtenidas anteriormente. Esta reducción preserva la existencia de contraejemplos de un orden dado; no presupone que todos los grafos sin triángulos sean maximales.
