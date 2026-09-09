# Una vía espectral para Erdős #128

Este argumento resuelve una subfamilia, no el problema general. Se ha desarrollado y comprobado aquí; no se afirma que sea inédito en la literatura.

## Resultado

Sea G un grafo simple sin triángulos cuyos vértices son los vectores de F₂^r, con x e y adyacentes cuando x+y pertenece a un conjunto fijo D que no contiene el vector cero. Es decir, G es un grafo de Cayley de un grupo binario, también llamado cubelike. Escribamos N=2^r.

Existe una mitad S con

\[
e(S)\le \frac N4\left\lfloor N\left(\frac32-\sqrt2\right)\right\rfloor.
\]

En particular, G satisface la cota de Erdős e(S)≤N²/50 cuando N≤128. El caso N=1 es trivial.

Para cualquier orden, la primera desigualdad también da

\[
e(S)\le\frac{3-2\sqrt2}{8}N^2\approx0.02144661N^2.
\]

Esta última constante todavía es mayor que 1/50.

## Demostración

Escribamos d=|D|. Si d=0, cualquier mitad sirve. Supongamos d>0; necesariamente d<N.

Para cada vector a, la función χₐ(x)=(-1)^(a·x) es un autovector de la matriz de adyacencia, con autovalor

\[
\lambda_a=\sum_{s\in D}(-1)^{a\cdot s}.
\]

Los N caracteres son ortogonales y forman una base, así que estos son todos los autovalores, contando multiplicidades. El correspondiente a a=0 es d. Sea λ el menor autovalor entre los caracteres no triviales.

Como el grafo es d-regular, la traza del cuadrado de su matriz de adyacencia es Nd. Como no tiene triángulos, la traza del cubo es cero: cada recorrido cerrado de longitud tres en un grafo simple corresponde a un triángulo orientado con un origen elegido. Por tanto,

\[
\sum_{a\ne0}\lambda_a^2=Nd-d^2,
\qquad
\sum_{a\ne0}\lambda_a^3=-d^3.
\]

Cada λₐ satisface λₐ³≥λλₐ², porque λₐ²(λₐ−λ)≥0. Sumando obtenemos

\[
-d^3\ge\lambda(Nd-d^2),
\qquad
\lambda\le-\frac{d^2}{N-d}.
\]

Elijamos un carácter no trivial que alcance λ. El hiperplano S={x:a·x=0} tiene exactamente N/2 vértices. Si p es el número de generadores s de D con a·s=0, cada vértice de S tiene exactamente p vecinos dentro de S y

\[
2p-d=\lambda,
\qquad
e(S)=\frac{Np}{4}.
\]

Aquí p es un entero no negativo. La cota espectral implica

\[
p=\frac{d+\lambda}{2}
\le \frac{d(N-2d)}{2(N-d)}.
\]

Poniendo t=d/N, la expresión de la derecha, dividida por N, es

\[
f(t)=\frac{t(1-2t)}{2(1-t)}.
\]

Para 0≤t<1 se cumple

\[
\left(\frac32-\sqrt2\right)-f(t)
=\frac{\left(t-1+1/\sqrt2\right)^2}{1-t}\ge0.
\]

Luego p≤N(3/2−√2). Como p es entero, se puede tomar la parte entera. Al sustituir en e(S)=Np/4 queda demostrada la primera desigualdad.

## Redondeo exacto para N≤128

| N | Cota entera para p | Cota para e(S) | N²/50 |
|---:|---:|---:|---:|
| 2 | 0 | 0 | 0.08 |
| 4 | 0 | 0 | 0.32 |
| 8 | 0 | 0 | 1.28 |
| 16 | 1 | 4 | 5.12 |
| 32 | 2 | 16 | 20.48 |
| 64 | 5 | 80 | 81.92 |
| 128 | 10 | 320 | 327.68 |

Los valores de la parte entera se verificaron sin coma flotante. Para b=floor(N(3/2−√2)), se comprueba 3N−2b≥0 y (3N−2b)²≥8N², y que b+1 ya no satisface ambas condiciones.

El resultado también se transmite a ampliaciones equilibradas de estos grafos: una mitad del grafo original se levanta a una mitad con t veces más vértices y t² veces más aristas.

## Comprobación y límites

El archivo `cubelike-spectral-check.py` verifica las identidades y las desigualdades con enteros. Recorrió exhaustivamente los 32.768 conjuntos de generadores posibles en F₂⁴; 3.049 producen grafos sin triángulos, y todos pasaron. También comprobó 300 conjuntos adicionales en órdenes 32, 64 y 128. Estas comprobaciones corroboran el argumento; la demostración general de la subfamilia es la derivación anterior, no el muestreo.

El grafo de Clebsch aparece con D formado por los cuatro vectores unitarios y 1111. Un carácter de peso tres deja un solo generador dentro de su hiperplano, dando una mitad con cuatro aristas. Esta construcción puede abandonar parte de cada vecindad completa, justo lo que no permitía la estrategia anterior.

El obstáculo para extender el argumento a todos los grafos es preciso: en general, un autovector mínimo no toma solamente los valores +1 y −1, ni sus signos definen necesariamente una partición equilibrada. La identidad e(S)=N(d+λ)/8 depende aquí de los caracteres del grupo binario. Además, incluso dentro de esta familia, la cota continua 0.02144661 no alcanza 0.02 para todos los órdenes.

## Estado de la búsqueda general realizada en paralelo

La primera ejecución para n=24 descartó 240 candidatos y guardó 3.813 restricciones sobre mitades. Terminó a los 180 segundos con respuesta `unknown` del solver y motivo `canceled`, al agotarse el tiempo disponible para esa ejecución. Una segunda ejecución, incorporando la reducción a grafos maximales sin triángulos, elevó los totales a 277 candidatos descartados y 4.157 restricciones; también terminó a los 180 segundos sin resolución. No se encontró un contraejemplo ni se demostró su inexistencia. El archivo `search-n24.json` conserva las restricciones para retomar la búsqueda.
