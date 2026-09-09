# Búsqueda en ampliaciones desiguales: reducción exacta

El objetivo completo sigue pendiente. Esta representación permite buscar contraejemplos finitos mediante grafos pequeños y multiplicidades, sin confundir la búsqueda de pesos con una prueba universal.

## Representación

Sea H un grafo simple sin triángulos con vértices 1,…,k y sean a₁,…,aₖ enteros no negativos. Sustituimos el vértice i por aᵢ gemelos independientes y cada arista ij por todas las aristas entre sus clases. El grafo resultante sigue sin triángulos y tiene N=Σaᵢ vértices.

Una mitad queda descrita por enteros xᵢ que satisfacen

\[
0\le x_i\le a_i,\qquad \sum_i x_i=h=\lfloor N/2\rfloor.
\]

Su número de aristas es exactamente

\[
F(x)=\sum_{ij\in E(H)}x_ix_j.
\]

Esta representación no restringe teóricamente el problema, porque cualquier grafo se obtiene tomando una clase de tamaño uno por vértice. La búsqueda efectuada sí restringe el número y la forma de las clases: eso debe mantenerse separado de la equivalencia matemática.

## Lema de minimización exacta

**Existe una mitad óptima en la que como mucho una clase está parcialmente ocupada.**

Para demostrarlo, relajamos inicialmente xᵢ a números reales y elegimos un minimizador con el menor número posible de coordenadas estrictamente entre cero y aᵢ. Existe un minimizador por compacidad.

Si dos coordenadas i,j fueran parciales, podemos reemplazarlas por xᵢ+t y xⱼ−t. Esto conserva la suma y es factible en un intervalo cerrado cuyos extremos saturan al menos una coordenada. En ese intervalo, F es afín cuando ij no es arista, y tiene término cuadrático −t² cuando ij es arista. Es, por tanto, cóncava. Alguno de los dos extremos no aumenta F, contradiciendo la elección del minimizador.

Queda a lo sumo una coordenada parcial. Todas las demás valen cero o aᵢ; como h y los aᵢ son enteros, la coordenada restante también es entera. Por tanto, el mínimo de la relajación coincide con el mínimo entre mitades reales del grafo expandido.

Este es el mismo principio de redondeo por transferencias utilizado en el argumento fraccionario examinado al inicio; aquí se aplica a capacidades desiguales para construir el buscador exacto.

## Fórmula finita

Para un conjunto I de clases completas y una clase j exterior, definamos A(I)=Σᵢ∈ᴵ aᵢ. Siempre que

\[
A(I)\le h\le A(I)+a_j,
\]

el candidato correspondiente tiene coste

\[
F(I,j)=\sum_{uv\in E(H[I])}a_ua_v
+(h-A(I))\sum_{i\in I\cap N_H(j)}a_i.
\]

También se incluyen los conjuntos completos con A(I)=h. El mínimo sobre estos candidatos es exactamente el mínimo de aristas de una mitad. El número de candidatos depende de k, con una cota O(k2ᵏ), y no de las combinaciones de N vértices.

Para pesos de suma par, aumentar todas las multiplicidades por un factor entero t multiplica N por t y el mínimo por t². Así, cualquier contraejemplo de esta forma produce otros de tamaños arbitrariamente grandes.

## Cómo se ha usado

`search-weighted-templates.py` prueba multiplicidades de suma 80 sobre Petersen, Mycielski de C₅ y Clebsch. Las propuestas de pesos son heurísticas, pero cada mínimo se calcula con enteros y con la enumeración anterior. El algoritmo admite disminuciones temporales de su función objetivo para no limitarse a un ascenso local.

Antes de ejecutar la búsqueda, se contrastó el optimizador con la enumeración de todas las mitades de 40 ampliaciones explícitas de diez vértices. `verify-weighted-search.py` comprueba por separado los mejores resultados guardados, enumerando directamente los candidatos sin reutilizar la recurrencia ni las podas del buscador.

Para refutar la conjetura, un resultado debe satisfacer estrictamente 50·min F>N². Alcanzar la igualdad no es un contraejemplo. No encontrar una violación entre los pesos probados tampoco demuestra su ausencia para todos los pesos, otros grafos base o todos los órdenes.

## Resultado de las ejecuciones

La primera ejecución mantuvo fija la estructura de cada grafo base y cambió las multiplicidades. La segunda permitió también cambiar aristas: quitó algunas y añadió otras solo cuando no creaban triángulos. Incluyó como puntos iniciales ampliaciones equilibradas de ciclos de longitud cinco, para disponer del control conocido de igualdad.

| Ejecución | Clases disponibles | Evaluaciones registradas | Mayor mínimo encontrado, con N=80 |
|---|---:|---:|---:|
| Petersen fijo | 10 | 228.003 | 128 |
| Mycielski de C₅ fijo | 11 | 150.863 | 128 |
| Clebsch fijo | 16 | 7.317 | 110 |
| Aristas y pesos, desde Petersen | 10 | 198.984 | 128 |
| Aristas y pesos, desde Mycielski de C₅ | 11 | 122.510 | 128 |
| Aristas y pesos, desde Clebsch | 16 | 14.665 | 128 |

Son 722.342 evaluaciones registradas en conjunto, no una enumeración de grafos no isomorfos ni de todos los pesos. La cota objetivo es 80²/50=128; refutarla exige que el mínimo sea al menos 129. No se encontró ese caso.

El resultado de 110 en la primera búsqueda sobre Clebsch no es una cota sobre toda su familia: la búsqueda no alcanzó entonces el caso conocido de igualdad soportado en un ciclo de longitud cinco. La segunda ejecución lo incluyó explícitamente. Esta diferencia muestra por qué el resultado de una búsqueda heurística no debe presentarse como el máximo verdadero de una familia.

Los dos archivos `weighted-search-80.json` y `weighted-search-80-joint.json` contienen las aristas, las multiplicidades y una mitad óptima de los mejores casos guardados. Los archivos con sufijo `-independent-verification.json` registran la comprobación directa de sus mínimos. No se obtuvo una demostración general ni un contraejemplo.
