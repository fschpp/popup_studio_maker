# Plan: Popup Studio (nombre provisional)

**Versión 2.6** · 29 de octubre de 2026 · Refinada tras una investigación bibliográfica adicional; incorpora la confirmación del ángulo de apertura, el análisis de las fotos y el video del primer prototipo, el diagrama de diseño del cliente (con sus líneas confirmadas como líneas de pegado), el tutorial que usó y el uso de material transparente en las ventanas

Aplicación de escritorio para **Linux (Python + GTK 4)** que permite diseñar páginas de libros popup: el usuario arma el layout 3D con proxies, define el comportamiento de cada elemento, simula el plegado y desplegado, pega texturas PNG (recortadas por transparencia) y exporta PDFs para imprimir en papel sticker, pegar sobre cartulina, cortar a mano y armar. En fases posteriores la app **elige y genera los pliegues automáticamente** a partir de modelos 3D e imágenes, aplicando los trabajos científicos sobre arquitectura origámica y popups multi-mecanismo.

---

## 0. Cómo leer este documento

Cada afirmación lleva una etiqueta de origen:

| Etiqueta | Significa |
|---|---|
| **[Cliente]** | Lo dijo el cliente en la entrevista |
| **[Fuente]** | Surge de un paper o página consultada (se indica cuál) |
| **[Propuesta]** | Decisión de diseño del analista, a validar |
| **[Hipótesis]** | Algo que parece cierto pero no está confirmado |
| **[Pendiente]** | Falta un dato o una decisión |

**Estado de lectura de los papers.** *Leído completo*: Li et al. 2010, Iizuka et al. 2011, Ruiz et al. 2014. *Solo resumen o póster*: Liu et al. 2014, Le et al. 2014, Ruiz et al. 2013. *Solo referencia*: el resto (ver sección 21). Antes de implementar cada generador se lee el paper completo, incluidas las figuras, que no se pueden extraer como texto.

## 1. Resumen ejecutivo

- **Qué es:** un diseñador de páginas popup con simulación previa, que genera el material de armado (PDFs) y que, en niveles avanzados, decide solo qué mecanismo usar.
- **Cómo se organiza:** un **único núcleo** basado en un *grafo de parches* (parches planos, bisagras y pegados) y un solo espacio de trabajo. Los modos "básico, asistido, origámico y avanzado" son **niveles de capacidad** sobre ese espacio: los generadores automáticos producen elementos editables, no un resultado cerrado.
- **Hallazgo principal de la investigación:** hay dos familias de popups. Las tarjetas de **90°** (hoja única cortada y plegada, la arquitectura origámica de Chatani y Li et al. 2010) y las de **180°** (varias piezas pegadas, como el ejemplo del cliente). El método de Li et al. 2010 produce las de 90°; el que decide automáticamente entre varios mecanismos para estilos de 180° es el de Ruiz et al. 2014. El plan incorpora ambos.
- **Primera versión (criterio del cliente):** rehacer su ejemplo (casita y auto) con el modo básico.
- **Estrategia de riesgo:** seis *spikes* técnicos en la Fase 0 antes de comprometer la arquitectura (visor 3D en GTK 4, simulación, recorte por alfa, PDF a escala, voxelización de STL, prototipo en papel).

## 2. Cambios respecto de la versión 1

1. **Dos tipos de tarjeta (90° y 180°)** pasan a ser parte del modelo del proyecto y condicionan qué mecanismos y generadores se pueden usar.
2. El **catálogo de mecanismos** se rehace sobre la literatura: step-fold, tent-fold, v-fold (tipos 1 y 2), box-fold y cilindro elástico. La versión 1 tenía una lista genérica.
3. Se introduce el concepto de **par de parches base (BPP)**, que resuelve de forma natural la pregunta abierta "¿puede un resultado origámico ir como pieza dentro de otra página?" (sección 19.6).
4. Se agregan **reglas de validez analíticas** (plegabilidad y rangos de separación) tomadas de los papers, para validar sin simular.
5. La simulación pasa a ser **híbrida**: fórmulas cerradas donde existen, y un motor general (resortes o proyección de restricciones) para piezas curvas y mecanismos personalizados.
6. Las exportaciones contemplan el flujo **sticker sobre cartulina**: marcas de pliegue en los bordes, doble cara con contorno espejado, mapa de pegado en la página base.
7. Los modos avanzados se reorganizan como **generadores enchufables** y se agregan los trabajos de Ruiz et al. 2014 (multi-estilo), Li et al. 2011 (v-style), y otros.
8. Se agregan **ADRs** (decisiones de arquitectura), **backlog con criterios de aceptación**, estrategia de pruebas, registro de riesgos y protocolo de prototipo físico.
9. **Corrección de una afirmación mía anterior:** mencioné *popupCAD* como herramienta de popups. Es una herramienta para **dispositivos laminados** (robótica y MEMS), no para libros. No se usa en este plan.
10. Se plantea una **hipótesis concreta sobre el mecanismo de la casita** del ejemplo (los pliegues diagonales del piso), con qué dato falta para confirmarla (sección 11.5).
11. **Versión 2.1:** el cliente confirma que su único popup **se abre completamente (180°)** y que está **abierto a otras opciones** de ángulo de diseño. Se adopta 180° como predeterminado, se mantiene 90° disponible y se decide el orden de las fases (sección 25).
12. **Versión 2.2:** con las fotos del prototipo en papel blanco y del cierre de la página se precisa la descripción de la casita (caja con **fachada independiente con aberturas**, pared trasera con puerta y ventana, panel de techo trasero) y se observan **capas escalonadas en zigzag** al cerrar. Como las fotos no permiten deducir la red de bisagras, se agrega el **mecanismo definido por datos** desde la Fase 1 (RF-34) y la **exportación en modo boceto** (RF-35); se reescribe la sección 11.5.
13. **Versión 2.3:** el video del **primer prototipo** (papel blanco) muestra una tarjeta que se abre y deja una caja en el centro, con pliegues en X sobre la página. Refuerza la hipótesis de **v-fold tipo 1** para la casita y se adopta ese prototipo como **caso de referencia físico CR-1** para validar la simulación antes de abordar la casita completa (secciones 11.5 y 25).
14. **Versión 2.4:** el cliente explica su **diagrama de diseño** (rojo, negro y azul) y aporta la transcripción del **tutorial de Duncan Birmingham** del que aprendió. La casita pasa de hipótesis a **diseño declarado**: dos V-fold enfrentados que forman un rombo con la diagonal sobre el pliegue central, más un paralelogramo interior. Se adoptan sus tres principios (cruzar el valle, balance, los valles crean valles), las cinco variantes de V-fold y las tres de pliegue paralelo, sus reglas de oficio (pestañas, marcado de pliegues, gramaje), y el diagrama pasa a ser el modelo del **plano de pegado** de la app (secciones 4, 8.4, 11.1b, 11.5 y apéndice D).
15. **Versión 2.5:** el cliente confirma que las líneas del diagrama son **donde pega las solapas** de cada pieza. Se cierra la pregunta 12: el modelo de **tarjeta de 180° con piezas pegadas** queda confirmado para la casita y el diagrama se lee como **plano de pegado** sin reservas (sección 11.5 y apéndice D).
16. **Versión 2.6:** el cliente aclara que las **ventanas transparentes** de la fachada se imprimen en **papel transparente** y se pegan al resto de la impresión. **Se corrige una afirmación de versiones anteriores:** las aberturas de la fachada no son todas huecos cortados; las ventanas llevan **película transparente**. Se agregan las **regiones de material** (opaca, hueco, ventana transparente), la hoja de transparencias, RF-36, US-504 y la validación V-11 (secciones 14.4, 17.1 y 13).

## 3. Contexto del cliente

- **[Cliente]** Primer popup hecho a mano, con técnicas aprendidas en videos de YouTube, recreando una fotografía familiar sobre la fachada de una casa. El video muestra una **casita** (volumen con paredes, piso con pliegues diagonales, ventanas con persianas, techo y cornisa, fotos recortadas) y un **auto** (lámina curva con pestaña de soporte y una persona asomada), sobre una página con marco de cartulina.
- **[Cliente]** Imprime en **papel sticker**, lo pega sobre **cartulina** y corta a mano con cúter y tijera. Usa papel ISO mayor que A4.
- **[Cliente]** Trabaja en **Linux con GTK 4**.
- **[Cliente]** Su único popup **se abre completamente** (180°: página plana sobre la mesa con los elementos de pie). Está **abierto a otras opciones**, por ejemplo tarjetas de 90°.
- **[Cliente, fotos]** Antes de la versión con textura arma un **prototipo en papel blanco** (ya trabaja con la rutina "boceto primero, textura después" que el plan formaliza en la sección 18). Las fotos muestran la casita con fachada con aberturas por las que pasa la luz (las ventanas son de material transparente, ver más abajo) y el cierre de la página con las piezas apiladas.
- **[Cliente, video]** Aportó el video de su **primer prototipo** en papel blanco (unos 5 segundos): una tarjeta cerrada y plana que al abrirse deja una caja en el centro.
- **[Cliente, diagrama]** Dibujó un diagrama de la casita sobre una hoja con un pliegue vertical central: trazo **rojo** = una V (frente y costado de la casa), trazo **negro** = una V mirando hacia abajo (fachada y pared de costado), trazo **azul** = un paralelogramo (el interior de la casa). Las líneas son **donde pega las solapas** de cada pieza. Detalle y medición en la sección 11.5.
- **[Cliente]** La técnica de la caja la aprendió del tutorial de YouTube https://www.youtube.com/watch?v=aGJZbNh9Phs (Duncan Birmingham), cuya transcripción aportó. No pude abrir la página del video; el análisis se basa en la transcripción.
- **[Cliente]** Las **ventanas transparentes** de la fachada las imprimió en **papel transparente** y las pegó al resto de la impresión de la fachada.

### Trazabilidad: dolor del cliente → diseño → verificación

| Lo que le costó al cliente | Respuesta de diseño | Requisitos | Cómo se verifica |
|---|---|---|---|
| Saber qué pliegue usar | Catálogo de mecanismos, reglas de colocación y recomendador | RF-12, RF-13, RF-15 | Para cada proxy del ejemplo la app ofrece al menos un mecanismo válido con justificación |
| Que los bordes queden alineados | Fuente única de verdad: las dimensiones se derivan de los parámetros y las aristas compartidas tienen una sola longitud | RF-11, V-07 | Aristas compartidas coinciden dentro de la tolerancia del proyecto |
| No poder experimentar | Simulación antes de cortar y variantes del diseño | RF-16, RF-04 | El ejemplo se diseña y simula completo sin cortar papel |
| Fijar el layout apenas | Edición paramétrica con recálculo | RF-08, RF-13 | Mover una pieza recalcula pliegues, pestañas y PDFs |
| No poder adaptar | Proyecto reabrible y editable | RF-02, RF-13 | Reabrir, cambiar una medida y reexportar |

## 4. Hallazgos de la investigación que condicionan el diseño

**H1. Dos familias de tarjetas.** [Fuente: Iizuka et al. 2011] Las tarjetas de **90°** se hacen con una sola hoja con cortes y pliegues y se conocen como arquitectura origámica; las de **180°** se arman con varias piezas de papel y el volumen aparece al abrir 180°. Los métodos de una familia no sirven directamente para la otra. Consecuencia: el proyecto tiene un **ángulo de diseño** (90° o 180°) y cada mecanismo y generador declara con cuál es compatible.

**H2. Ya existen sistemas interactivos parecidos al flujo del cliente.** [Fuente: Iizuka et al. 2011; Okamura e Igarashi 2009, solo referencia] El usuario elige una primitiva, la coloca sobre una **arista base**, el sistema ajusta automáticamente las posiciones fijas para que plegue, el usuario edita ancho, alto, profundidad e inclinación sin romper las restricciones, y el sistema simula apertura y cierre avisando de **choques y partes que sobresalen**. Genera plantillas con pestañas y marcas de alineación (la correspondencia se distingue por colores). Reportan 10 a 20 minutos por tarjeta, sin contar texturas. Una crítica de un usuario de prueba: querer colocar una primitiva como "puente" entre dos primitivas separadas.

**H3. Ruiz et al. 2014 es lo más cercano al deseo original** ("que el programa vea qué pliegue hacer para cada tipo"). [Fuente] Define cuatro mecanismos (step-fold, tent-fold, v-fold, box-fold), da condiciones de validez, abstrae un modelo 3D con prismas, elige el mecanismo para cada prisma, genera parches con un enfoque basado en imágenes (conserva texturas y contornos) y produce layout de impresión con orden de ensamblaje. Funciona bien con objetos "de bloque" (autos, edificios) y mal con formas orgánicas.

**H4. Validez = plegable + estable.** [Fuente: Ruiz et al. 2014] *Plegable*: queda totalmente plano al cerrar las dos páginas, con partes rígidas, conectadas y sin pliegues nuevos. *Estable*: al sujetar las dos páginas en cualquier ángulo, todas las partes quedan quietas. Los modelos de los papers suponen **papel rígido sin espesor ni peso**; la app debe agregar espesor y holguras.

**H5. La plegabilidad general es NP-difícil.** [Fuente: Uehara y Teramoto 2006, citado en Ruiz et al.] Por eso el enfoque es **mecanismos constructivos con garantías** (verdes), más **simulación** como red de seguridad para lo que quede fuera de las reglas (amarillo).

**H6. Las piezas curvas son un caso aparte.** [Fuente: Iizuka; Ruiz] Ruiz et al. las excluyen porque exigen otro concepto de estabilidad con papel flexible. Iizuka et al. simulan un cilindro como 14 cuadriláteros con **resortes de bisagra** de ángulo de reposo 180°. El arco del auto del cliente cae en esta categoría.

**H7. Una pieza de 90° puede montarse sobre un par base de ángulo local 90°.** [Fuente + inferencia] En Ruiz et al., la step-fold (que despliega a 90°) solo se coloca entre un parche base y un lateral de una box-fold. Eso implica que el par de parches sobre el que se monta vale 90° cuando la página está abierta 180°. Es la base para integrar piezas origámicas dentro de páginas de 180° (sección 19.6).

**H8. Herramientas existentes.** [Fuente: Iizuka et al. 2011 y resultados de búsqueda] Hay sistemas académicos de diseño interactivo de tarjetas (Iizuka et al.; Okamura e Igarashi) y, según los resultados de búsqueda, programas comerciales que no evalué. Ninguno de los que encontré combina GTK 4, el flujo de pegatina sobre cartulina, texturas PNG con alfa, simulación y generadores automáticos para los dos tipos de tarjeta. Se tratan como antecedentes, no como dependencias.

**H9. ModernGL con GTK 4 es viable.** [Fuente: foro GNOME Discourse, reporte de comunidad] Funciona con `Gtk.GLArea` si el contexto de ModernGL se crea en el callback de render (o en `do_realize` tras `attach_buffers`), no en las señales `realize` o `create-context`, y se usa el framebuffer detectado con `ctx.detect_framebuffer()`. Se confirma en el spike S0.1.

**H10. Aviso de propiedad intelectual.** [Fuente: búsqueda, patente no analizada] Existe al menos una patente sobre creación de tarjetas popup desde modelos 3D (US10453255B2; solo vi el título). La app es de uso personal, pero si algún día se distribuye conviene revisar patentes y licencias de los algoritmos. No es asesoramiento legal.

**H11. El tutorial del cliente coincide con la teoría de los papers y le da vocabulario práctico.** [Fuente: transcripción del primer tutorial de Duncan Birmingham; el autor remite a su libro *Pop-up Design and Paper Mechanics*] Enseña dos familias, los pliegues convergentes (**V-fold**) y los **pliegues paralelos**, y **tres principios**: (1) todo popup tiene que **cruzar un valle**, la hendidura del pliegue central; (2) tiene que estar **balanceado** a los dos lados del valle (en los V-fold se balancean los **ángulos** y en los pliegues paralelos las **longitudes**); (3) todo popup **crea valles nuevos** donde se pueden pegar otros popups. Agrega que casi todos los popups **combinan mecanismos**, por ejemplo un V-fold que levanta paralelogramos o una caja formada por un V-fold, que es lo que hace el cliente. En este plan el *valle* es el **BPP** (sección 6), el *balance* es la **condición de plegabilidad** (V-03) y el *apilado* es la **colocación sobre un BPP** (11.2).

---

## 5. Alcance

### 5.1 Un espacio de trabajo, cuatro niveles de capacidad

**[Cliente]** pidió varios modos: uno básico donde él le explica a la app cómo hace el popup y, después, un modo avanzado "ultra completo" que aplique los papers. **[Propuesta]** Se implementan como niveles sobre **un solo espacio de trabajo**, de modo que lo que genera un nivel superior siempre se puede seguir editando con las herramientas del nivel básico.

| Nivel | Qué agrega | Quién decide el pliegue |
|---|---|---|
| **Básico** | Layout con proxies, catálogo de mecanismos, simulación, texturas, PDF | El usuario |
| **Asistido** | Validaciones completas, recomendador de mecanismo, correcciones sugeridas, variantes | El usuario, con ayuda |
| **Origámico** | Generador desde STL de hoja única (Li et al. 2010), como página entera o como pieza sobre un par base | La app |
| **Avanzado** | Generadores multi-estilo y otros trabajos (sección 20) | La app, con ajustes del usuario |

### 5.2 Tipos de tarjeta

| | **180°** | **90°** |
|---|---|---|
| Construcción | Varias piezas cortadas y pegadas | Una sola hoja con cortes y pliegues |
| Volumen visible al abrir | 180° (página plana) | 90° (página en V); queda plana al abrir 180° |
| Familias típicas | tent-fold, v-fold, box-fold, cilindro | step-fold, arquitectura origámica |
| Ejemplo del cliente | **Sí** [Cliente] | No |
| Generador automático | Ruiz et al. 2014 (Fase 4) | Li et al. 2010 (Fase 3) |

El proyecto tiene un **ángulo de diseño**. Los mecanismos de 90° (step-fold) pueden convivir en un proyecto de 180° si se montan sobre un par base cuyo ángulo local sea 90° (H7).

### 5.3 Fuera de alcance por ahora

- Exportación a plotter de corte (SVG/DXF): la arquitectura de exportación lo permite, pero el cliente corta a mano.
- Mecanismos de movimiento (solapas, ruedas, tiras de tirar) y libros de túnel.
- Simulación de deformación por colisión y de la elasticidad real del papel (más allá de las bisagras elásticas).
- Libro completo con varias páginas y tapa (Fase 5).
- Edición de imágenes: el cliente entrega los PNG ya listos.

## 6. Glosario

| Término | Definición |
|---|---|
| **Parche** (*patch*) | Polígono plano rígido: es una pieza o una parte de una pieza |
| **Bisagra** (*hinge*) | Línea de pliegue entre dos parches |
| **Pestaña** o **solapa** (*flap*) | Aleta de pegado agregada a un borde de un parche |
| **Pegado** (*glue*) | Unión entre una pestaña y una región de otro parche |
| **Pliegue central** | Bisagra entre las dos páginas primarias |
| **Ground / backdrop** | Las dos páginas primarias: la mitad fija sobre la mesa y la mitad que se levanta |
| **BPP** (par de parches base) | Dos parches que comparten una bisagra y que sirven de "ground" y "backdrop" locales para colocar un mecanismo |
| **Mecanismo** | Estructura mínima de parches y bisagras que da su estilo al popup (step, tent, v, box, cilindro) |
| **Ángulo de apertura φ** | Ángulo interior entre las dos mitades de la página: 0° cerrada, 180° plana |
| **Plegable / estable / válido** | Definiciones de H4 |
| **Layout plano** | Disposición 2D de cortes, pliegues y pestañas para imprimir y cortar |

## 7. Convenciones

- **Unidades:** milímetros en todo el modelo; ángulos en grados en la interfaz y radianes internamente.
- **Ángulo de apertura φ:** ángulo interior entre las mitades. Coincide con el "fold angle" de Ruiz et al. 2014 y de Iizuka et al. 2011. **[Pendiente]** Li et al. 2010 usa su propia parametrización: se mapea a esta convención al implementar el generador origámico.
- **Ejes (ADR-04):** x a lo largo del pliegue central; y hacia la mitad fija (ground) sobre la mesa; z hacia arriba cuando φ = 180°. Es equivalente por rotación al marco simétrico de Ruiz et al. (z como bisectriz del ángulo interior).
- **Líneas de exportación** (por color **y** por trazo, para poder imprimir en blanco y negro):

| Elemento | Trazo | Color por defecto |
|---|---|---|
| Corte | Continuo | Negro |
| Pliegue valle | Discontinuo (guiones) | Azul |
| Pliegue montaña | Guión-punto | Rojo |
| Contorno de pegado (zona de pestaña) | Punteado fino | Gris |
| Marca de alineación | Cruz o muesca con ID | Del color del ID |

- **Identificadores:** cada pestaña lleva un **número** y, opcionalmente, un **símbolo** (●, ▲, ■, ◆) para distinguir pares sin depender del color. La zona receptora lleva el mismo número y símbolo.

## 8. Flujo de usuario

### 8.1 Pasos (confirmados por el cliente, con los agregados marcados)

1. **Hoja:** tamaño, posición y orientación del pliegue central, ángulo de diseño (180° por defecto), espesores de cartulina y sticker. *(agregado: espesores)*
2. **Layout con proxies:** rectángulos para imágenes planas, cubos o prismas para volúmenes, STL importado para formas más complejas.
3. **Comportamiento:** click en el elemento y elección del mecanismo. *(agregado: la app muestra sobre qué BPP se monta y qué opciones son válidas)*
4. **Previsualización** de apertura y cierre con formas simples, con avisos de choques y salidas del contorno.
5. **Texturas:** un PNG por cara; la app lee la transparencia y recorta.
6. **Segunda simulación** con la textura final.
7. **Exportar PDFs** con pestañas numeradas y mapa de pegado. *(agregado: hoja de ensamblaje y página de calibración)*

### 8.2 Esquema de la ventana principal (propuesta)

```
┌──────────────────────────────────────────────────────────────────────────┐
│ ☰  Popup Studio — casita_y_auto.popup        [Diseño] [Texturas] [Exportar]  │
├───────────────┬──────────────────────────────────────┬───────────────────┤
│ ÁRBOL         │  VISOR 3D                             │ PROPIEDADES       │
│ ▾ Página      │   (órbita, selección, vista cenital   │ Elemento: Casita  │
│   ▾ Casita ✔  │    2D conmutable, sombreado por       │ Mecanismo: Box ▾  │
│     · Pared A │    estado: verde / amarillo / rojo)   │  ancho  [ 60 mm]  │
│     · Piso    │                                       │  alto   [ 45 mm]  │
│   ▾ Auto   ⚠  │                                       │  prof.  [ 40 mm]  │
│   ▾ Persona ✔ │                                       │ Alternativas (2)  │
│               │                                       │ Textura: [PNG…]   │
├───────────────┴──────────────────────────────────────┴───────────────────┤
│ ◀ ▶ ⏵  φ ──●────────────── 180°    [Reproducir] [Bucle]                   │
│ Problemas (1): ⚠ Auto sobresale 6 mm del borde al cerrar  [Ir ▸]         │
└──────────────────────────────────────────────────────────────────────────┘
```

Los **generadores** (origámico, multi-estilo) se lanzan desde un menú *Generar desde…* y vuelcan su resultado como elementos normales en el árbol.

### 8.3 Estados de un elemento

| Color | Significado |
|---|---|
| Verde | Mecanismo con reglas de colocación **garantizadas** (sección 11.2) y sin problemas en la simulación |
| Amarillo | Fuera de las reglas garantizadas: válido solo según la simulación |
| Rojo | Tiene problemas (choque, sobresale, no pliega plano) |

### 8.4 Decisión de interfaz para reducir esfuerzo **[Propuesta]**

La vista cenital incluye el **plano de pegado**: las líneas de base de cada V-fold y de cada pliegue paralelo sobre la hoja, coloreadas por pieza, igual que el **diagrama del cliente** (sección 11.5). Es la forma en que él piensa el diseño, así que es la vista principal de edición.

Construir manipuladores 3D (gizmos) y selección con rayos en OpenGL propio es costoso. En la versión 1 la **colocación** se hace en una **vista cenital 2D con campos numéricos y arrastre**, y el visor 3D se usa para órbita, selección y simulación. Los gizmos 3D quedan para una fase posterior. Esto responde al flujo del cliente sin cambiarlo en lo esencial.

## 9. Requisitos

Prioridad **M**ust / **S**hould / **C**ould, y fase prevista.

### 9.1 Funcionales

| ID | Requisito | Prio | Fase |
|---|---|---|---|
| RF-01 | Crear proyecto: tamaño de hoja (mm), posición y orientación del pliegue central, ángulo de diseño 90°/180°, espesores | M | 1 |
| RF-02 | Guardar y abrir proyectos (`.popup`, ver ADR-05) | M | 1 |
| RF-03 | Deshacer y rehacer | M | 1 |
| RF-04 | Variantes (instantáneas) del diseño para comparar alternativas | S | 2 |
| RF-05 | Libro con varias páginas | C | 5 |
| RF-06 | Autoguardado y recuperación tras un cierre inesperado | S | 1 |
| RF-07 | Proxies: rectángulo, prisma/cubo, STL importado | M | 1 |
| RF-08 | Colocar, mover, rotar y escalar con campos numéricos, arrastre en vista cenital (con el **plano de pegado** coloreado por pieza, como el diagrama del cliente) y ajuste a grilla/bordes | M | 1 |
| RF-09 | Selección por click en el visor y en el árbol | M | 1 |
| RF-10 | Mostrar sobre qué BPP se monta cada elemento y ajustar automáticamente las posiciones fijas (como Iizuka et al.) | M | 1 |
| RF-11 | Cotas y guías de alineación; aristas compartidas con una única longitud | S | 1 |
| RF-12 | Catálogo base: capa plana, step-fold, tent-fold, v-fold (tipos 1 y 2), box-fold, cilindro/arco con pestaña | M | 1 |
| RF-13 | Asignar o cambiar el mecanismo desde el click en el elemento, con parámetros editables y recálculo inmediato | M | 1 |
| RF-14 | Editor gráfico de mecanismos personalizados (parches, bisagras, pegados) | S | 2 |
| RF-15 | Recomendador de mecanismo con ranking y justificación | S | 2 |
| RF-16 | Simulación con control de ángulo, reproducción y caché de poses | M | 1 |
| RF-17 | Validaciones V-01 a V-11 con panel de problemas y resaltado en 3D | M | 1 |
| RF-18 | Correcciones sugeridas con un click | S | 2 |
| RF-19 | Sombreado por estado (verde / amarillo / rojo) | S | 1 |
| RF-20 | PNG por cara, contorno desde el canal alfa, margen y ajuste de escala y posición | M | 1 |
| RF-21 | Simulación con textura final | M | 1 |
| RF-22 | Doble cara (A/B) con contorno espejado | S | 1 |
| RF-23 | Editor ligero de contorno (mover o borrar puntos) | C | 2 |
| RF-24 | PDF de pegatinas (textura + corte) y de plantilla de pliegues | M | 1 |
| RF-25 | Números y símbolos en pestañas y marcas de alineación en la zona receptora (mapa de pegado) | M | 1 |
| RF-26 | Reparto en hojas de tamaño configurable (nesting) | M | 1 |
| RF-27 | Hoja de ensamblaje: orden de pegado y tabla de correspondencias | S | 1 |
| RF-28 | Página de calibración (escala, líneas, espesores) | S | 1 |
| RF-29 | Exportar SVG/DXF para plotter | C | 5 |
| RF-30 | Generador origámico desde STL (Li et al. 2010) | M | 3 |
| RF-31 | Integración del resultado origámico como pieza sobre un BPP de 90° | S | 3 |
| RF-32 | Generador multi-estilo desde 3D (Ruiz et al. 2014) | S | 4 |
| RF-33 | Otros generadores (formas libres, imágenes 2D, sliceform, lattice 180°) | C | 4 |
| RF-34 | Mecanismo definido por **datos** (archivo de parches, bisagras y pegados), sin editor gráfico | M | 1 |
| RF-35 | Exportación en **modo boceto**: cortes, pliegues y pestañas sin texturas, para prototipo en papel blanco | S | 1 |
| RF-36 | **Ventanas transparentes:** marcar las regiones interiores de una cara como hueco o ventana; para las ventanas, generar la pieza de material transparente con margen de solape y su hoja de impresión | S | 1 |

### 9.2 No funcionales

| ID | Requisito |
|---|---|
| RNF-01 | Linux, GTK 4, Python 3.11 o superior |
| RNF-02 | **Local y sin red:** las fotos del cliente (familia) no salen de su equipo |
| RNF-03 | Visor a 30 fps o más con hasta 200 parches; recálculo de poses de una página típica en menos de 2 s en un hilo aparte, sin bloquear la interfaz *(objetivos a calibrar tras la Fase 0)* |
| RNF-04 | El motor geométrico no depende de GTK y se prueba sin interfaz |
| RNF-05 | Mecanismos y generadores son extensibles sin tocar el núcleo |
| RNF-06 | Geometría en `float64`; exportación con resolución de 0,01 mm; escala 1:1 |
| RNF-07 | Interfaz en español, preparada para traducción (gettext) |
| RNF-08 | No perder trabajo: autoguardado y archivos versionados |
| RNF-09 | Diseñar la página del ejemplo en 20 minutos o menos, sin contar texturas *(referencia: Iizuka et al. reportan 10 a 20 minutos)* |
| RNF-10 | Cada algoritmo documenta el paper de origen y sus desviaciones (trazabilidad científica) |

---

## 10. Modelo de dominio y de datos

### 10.1 Entidades (ADR-03: grafo de parches)

```
Proyecto
 ├─ ajustes: unidades, tolerancia, espesores (cartulina, sticker, pegamento), ángulo de diseño
 ├─ Página: tamaño de hoja, pliegue central (posición, orientación),
 │          dos mitades (ground, backdrop), cada una con caras texturizables
 ├─ ParesBase (BPP): par de parches + bisagra + función del ángulo local según φ
 ├─ Elementos[]
 │    ├─ proxy (rectángulo | prisma | malla STL)
 │    ├─ colocación (BPP, posición a lo largo de la bisagra, desplazamientos)
 │    └─ instancia de mecanismo (tipo + parámetros)  ──construye──►  GrafoDeParches
 ├─ GrafoDeParches
 │    ├─ Parche  (polígono 2D, marco 3D, lados A/B)
 │    ├─ Bisagra (parche1, parche2, arista, tipo: rígida | elástica, pliegue: montaña | valle)
 │    ├─ Pegado  (pestaña: parche+arista  →  destino: parche+región)
 │    └─ Aristas de corte (bordes sin bisagra)
 ├─ Texturas  (PNG, cara y lado, transformación, contorno derivado)
 ├─ Variantes[] (instantáneas del proyecto)
 └─ AjustesDeExportación
```

### 10.2 Reglas del modelo

- **Fuente única de verdad.** Los polígonos de los parches se **derivan** de los parámetros del mecanismo; nunca se dibujan a mano. Los parches vecinos comparten objetos *arista*, de modo que la longitud de una arista común es la misma en las dos caras. Esto ataca directamente el problema de "bordes que no alinean".
- **Cadena de dependencias:** parámetros → geometría 3D → poses por ángulo → validaciones → layout plano → PDF. Cada etapa se cachea y se recalcula solo si cambia su entrada.
- **Operaciones como comandos** (patrón *command*) para deshacer y rehacer.
- **Elementos de los generadores:** un generador devuelve un grafo de parches con el mismo formato; el usuario puede "congelarlo" en un elemento editable.

---

## 11. Catálogo de mecanismos

### 11.1 Mecanismos base (Fase 1)

Basados en Ruiz et al. 2014 (cuatro mecanismos) e Iizuka et al. 2011 (cilindro). Los nombres varían entre autores; este plan usa los de Ruiz et al.

| Mecanismo | Estructura (resumen) | Despliega a | Condición o nota de validez | Fuente |
|---|---|---|---|---|
| **Capa plana** | 1 parche con pestañas pegado a una superficie | Siempre plana | Pestañas dentro del contorno al cerrar | Propuesta |
| **Step-fold** | 4 parches con dos pares paralelos (S1∥S3, S2∥S4); sección transversal en paralelogramo | **90°** del BPP donde se monta | Plegable: lados opuestos iguales cumplen a+b=c+d; no se desplaza a lo largo del pliegue al plegar | Ruiz et al.; Li et al. 2011 lo llama mecanismo D2 |
| **Tent-fold** | 4 parches con pliegues paralelos; long(T1)=long(T2), long(T3)=long(T4), long(T3)>long(T1); simétrico respecto de la bisagra central | **180°** | Plegable por a+b=c+d; no se desplaza a lo largo del pliegue | Ruiz et al., tomado de Hara y Sugihara 2009 |
| **V-fold tipo 1** | 8 parches (G, B, FL, FR, BL, BR, TG, TB): a 180° forma una **caja completa**; los frontales y traseros son perpendiculares a G y B y forman 45° con el pliegue central; los superiores son paralelos a G y B | **180°** | Se inclina hacia +x al cerrar; no se pegan {TB,BR} ni {TG,BL} para que la tapa suba | Ruiz et al.; mecanismo D1 de Li et al. 2011 |
| **V-fold tipo 2** | Como el tipo 1, pero forma solo **media caja triangular** y no tiene los parches traseros BL y BR | **180°** | Rango de exclusión similar al tipo 1 | Ruiz et al. |
| **Box-fold** | 11 parches (G, B, L, R, FL, FR, BL, BR, TG, TB, C); laterales L y R equidistantes del pliegue central y con ángulos iguales respecto de G y B; "columna" C pegada perpendicular a G y B; pliegues principales paralelos al central | **180°** | Plegable si b+r=c+tb y g+l=c+tg; estable gracias a los parches frontales y traseros que evitan el cizallamiento | Ruiz et al. (primera formulación detallada) |
| **Cilindro / arco elástico** | Superficie curva aproximada con cuadriláteros (14 en Iizuka) y **bisagras elásticas** de ángulo de reposo 180° | Según su base | No admite validez analítica rígida: se valida por simulación | Iizuka et al.; excluido de Ruiz et al. |

Notas:
- Las **figuras 5 y 6** de Ruiz et al. (patrones de parches) y la **figura 3** de Iizuka et al. (catálogo de 14 primitivas: a–f v-fold, g–n pliegues paralelos) son la referencia visual para implementar. **[Pendiente]** consultarlas del PDF al implementar cada mecanismo.
- **[Propuesta]** Iizuka et al. basan sus primitivas en el libro *Elements of Pop Up*; el catálogo de la app es ampliable con más primitivas en la Fase 2 sin tocar el núcleo.

### 11.1b Variantes y reglas de oficio (tutorial de Birmingham)

**Variantes de V-fold** (pliegues convergentes en un punto del pliegue central). α = ángulo en la base entre la línea de pegado y el pliegue central; β = ángulo en la pieza. **Balance:** α_izq + β_izq = α_der + β_der. [Fuente: transcripción]

| Variante | Descripción |
|---|---|
| Ángulo recto | Los dos ángulos de la pieza valen 90° (el caso de la casita del cliente, con base de 45° a cada lado) |
| Agudo | Ángulos de la pieza iguales y menores de 90° |
| Puntiagudo | Variante más extrema del agudo |
| Obtuso | Ángulos de la pieza iguales y mayores de 90° |
| Asimétrico | Los cuatro ángulos distintos, pero base + pieza suman lo mismo de ambos lados |

**Variantes de pliegue paralelo** (todos los pliegues paralelos al central). b = distancia del pegado al pliegue central; p = largo de la pieza. **Balance:** b_izq + p_izq = b_der + p_der. [Fuente: transcripción; la suma de ambos lados coincide con la condición a + b = c + d de V-03]

| Variante | Descripción |
|---|---|
| Simétrico igual | Mismos largos y misma distancia al pliegue a ambos lados |
| Paralelogramo | A un lado pieza corta y base larga; al otro, base corta y pieza larga |
| Asimétrico | Los cuatro largos distintos, con suma igual de ambos lados |

Las variantes **no son mecanismos distintos**: son valores de los parámetros (α, β o b, p) con la restricción de balance. La interfaz solo ofrece combinaciones balanceadas.

**Reglas de oficio** [Fuente: transcripción]:
- Pestañas de pegado de **al menos 1 cm** (media pulgada): soportan el esfuerzo de abrir y cerrar. Se recortan sus esquinas para que se enganchen menos.
- **Solo importa la posición del pliegue**, no la de la pestaña (adentro o afuera). Todas las medidas se toman hasta el pliegue y el pegamento llega hasta el pliegue.
- Los pliegues se **marcan con un bolígrafo sin tinta**, que comprime las fibras sin cortarlas.
- Cartulina de **160 g/m²**, hasta 220 g/m² para piezas grandes. Recomienda adhesivo al solvente: el de base acuosa deforma la cartulina y seca lento; el de barra se agrieta con el tiempo.
- La mayoría de los popups **combinan mecanismos** (V-fold que levanta paralelogramos, cajas formadas por V-fold).

### 11.2 Reglas de colocación

**Garantizadas (estado verde).** [Fuente: Ruiz et al. §3.3.1 y restricción 3] Un mecanismo nuevo solo puede montarse sobre un **BPP**. Cada vez que se agrega un mecanismo aparecen nuevos BPP (por ejemplo, un prisma rectangular sobre el par {B, G} genera tres BPP más). Con las reglas del paper:
- tent-fold, v-fold y box-fold se colocan sobre el pliegue central o entre TG y TB de una box-fold;
- una step-fold se coloca entre un parche base y un lateral (L o R) de una box-fold;
- un parche base puede ser una página primaria o TB/TG de una box-fold; se puede apilar una box-fold sobre otra;
- un prisma triangular puede ir sobre uno rectangular pero no a su costado (esa combinación podría no plegar).

**Libres (estado amarillo).** [Fuente: Iizuka et al.] Una primitiva puede colocarse sobre cualquier arista base; una primitiva colocada sobre una arista que pliega plana también pliega plana. Lo que no esté cubierto por las reglas garantizadas se valida **solo por simulación**.

### 11.3 Recomendador de mecanismo (RF-15, Fase 2)

Para cada elemento, la app prueba los mecanismos candidatos compatibles con su proxy y su BPP, descarta los inválidos y ordena el resto.

| Proxy | Candidatos típicos |
|---|---|
| Rectángulo plano paralelo al pliegue | capa plana, step-fold (si el BPP vale 90°), tent-fold |
| Prisma rectangular alineado con el pliegue central | box-fold, v-fold tipo 1 |
| Prisma triangular | tent-fold, v-fold tipo 2 |
| Superficie curva | cilindro elástico |
| STL | generador origámico (90°) o multi-estilo (180°) |

**[Propuesta]** Puntaje = validez (condición obligatoria) + cobertura − complejidad − riesgo:

```
puntaje = w_c · (1 − error_cobertura)        # cuánto del proxy cubren las caras principales
        − w_s · (n_parches + n_pestañas)     # simplicidad
        − w_f · distancia_al_proxy           # fidelidad geométrica
        − w_r · fuera_de_reglas_garantizadas # 1 si queda en amarillo
```

La idea de *cobertura* viene de Ruiz et al. (error_cover = 1 − Σ área de caras principales / Σ área de caras). Los pesos se calibran con ejemplos reales. La app muestra el ranking con una **justificación en una línea** ("box-fold: cubre 92 % del volumen, 11 parches, regla garantizada").

La tabla de mapeo primitiva-mecanismo de Ruiz et al. (Tabla 1) se transcribe desde el PDF al implementar esta función. **[Pendiente]**

### 11.4 Mecanismo personalizado (RF-34 en Fase 1, RF-14 en Fase 2)

El cliente pidió un modo donde "le explica a la app cómo hace el popup". La Fase 1 lo cubre con un catálogo **y con mecanismos definidos por datos** (RF-34): un archivo que lista parches, bisagras y pegados, que la app simula y exporta igual que uno del catálogo. Sirve de red de seguridad si la casita no coincide con ningún mecanismo conocido. La Fase 2 agrega un **editor gráfico**: dibujar parches, definir bisagras (montaña/valle, rígida/elástica) y pegados, y guardar el resultado como plantilla reutilizable. Como todos los mecanismos comparten el mismo grafo de parches, el simulador y los validadores funcionan sin cambios.

### 11.5 El ejemplo del cliente: video, fotos, prototipo y diagrama

**El diagrama del cliente [Cliente].** Una hoja (rectángulo) con su pliegue central (línea vertical) y tres tipos de trazo:

| Trazo | Qué representa, según el cliente | Lectura en los términos del plan |
|---|---|---|
| **Rojo** | Una V: el frente de la casa y un costado | V-fold de ángulo recto con base a 45° (parches frontales FL y FR del v-fold tipo 1 de Ruiz et al.) |
| **Negro** | Una V mirando hacia abajo: la fachada y la pared de costado | V-fold enfrentado al rojo (parches traseros BL y BR) **[Hipótesis]** |
| **Azul** | Un paralelogramo: el interior de la casa | Pliegue paralelo levantado por los V-fold, como el "V-fold que levanta paralelogramos" del tutorial |

**Geometría medida sobre la imagen** (medición propia, en píxeles del diagrama; **falta la escala real**):

| Dato | Valor |
|---|---|
| Hoja | 775 × 447 px (proporción 1,73); el pliegue está en el 50,5 % del ancho, prácticamente al centro |
| Rombo | Vértices superior (393, 28) e inferior (389, 309) **sobre el pliegue**; izquierdo (252, 173) y derecho (531, 166), a 139 y 140 px del pliegue |
| Lados | 192 a 204 px (media 199) con ángulos de 45,0° a 45,4° respecto del pliegue; diagonales de 281 y 279 px: es un **cuadrado girado 45°** con una diagonal sobre el pliegue |
| Tira azul | 202 × 49 px, paralela al lado superior izquierdo del rombo (43,6°) y adosada a él |
| Distancia a los bordes | Vértice superior a 28 px del borde superior (6 % de la altura); vértice inferior a 137 px del borde inferior; la punta de la tira azul toca el borde superior de la hoja |

(Coordenadas con origen en la esquina superior izquierda de la hoja.) El dibujo es casi simétrico, con desvíos de 2 a 3 %, que parecen tolerancia de dibujo manual.

**Qué dice la teoría sobre este diseño:**
- Base de 45° a cada lado y pieza de 90° en cada lado dan **α + β = 135° de ambos lados**: el V-fold queda **balanceado** (principio 2). **[Hipótesis]** si las piezas son de ángulo recto.
- Un cuadrado girado 45° con una diagonal sobre el pliegue es la huella en planta de una **caja completa** de cuatro paredes, que es lo que describe el paper para el v-fold tipo 1: parches frontales y traseros a 45° del pliegue central.
- Los puntos que V-01 va a vigilar al cerrar: el vértice superior del rombo, a solo 6 % de la altura del borde, y la punta de la tira azul, que roza el borde.

**Cómo se leen las líneas [Cliente]:** son las líneas donde se pegan las **solapas** de cada pieza sobre la hoja; no son cortes ni pliegues de la propia hoja. Coincide con la forma de trabajo del tutorial (lo que importa es la posición del pliegue) y confirma el modelo de **tarjeta de 180° con piezas pegadas** (sección 5.2) para la casita.

**Qué se ve** (video y fotos del ejemplo terminado, del prototipo en papel blanco, de la fachada de frente y del cierre):

| Elemento | Lo que se observa | Mecanismo | Dato que falta |
|---|---|---|---|
| **Casita (caja)** | Piso, dos paredes laterales grandes, **pared trasera** con ventana con persiana y puerta, y un **panel de techo** en la parte trasera. En el video aparecen **pliegues diagonales** en el piso. En las fotos la página está levantada a mano, así que las paredes se ven inclinadas por la apertura parcial y por la perspectiva | **Dos V-fold enfrentados + paralelogramo interior** según el diagrama del cliente (equivale al v-fold tipo 1 con el interior levantado por un paralelogramo) | Altura de las paredes; cuál de las dos V es la del frente; cómo se une la fachada |
| **Fachada** | Capa **independiente** delante de la caja, con aberturas (puerta, ventanas), dos pilastras con textura de piedra y una **cornisa ondulada** arriba. **[Cliente]** Las **ventanas transparentes** están impresas en **papel transparente** y pegadas al resto de la impresión de la fachada, y por eso la sombra sobre la hoja deja pasar la luz por ellas | Capa plana con aberturas, algunas cubiertas con **material transparente**, montada sobre la caja con pestañas **[Hipótesis]**, o un parche más del mecanismo | Cómo se une a las paredes laterales; qué aberturas son huecos y cuáles llevan película |
| **Auto** | Lámina curva (media caña) con el auto impreso y una persona asomada; pestaña de soporte hacia atrás | **[Hipótesis]** cilindro elástico con pestaña | Cómo se fija la pestaña y a qué distancia del pliegue |
| **Capas escalonadas** | Al cerrar la página se ven **bordes en zigzag** (dientes de sierra) y la casita colapsa en capas apiladas | **[Hipótesis]** pliegues paralelos (step-fold o tent-fold) debajo o junto a la casita, o cortes de la propia página | Vista lateral a 90° o patrón |
| **Personas** | Recortes pegados en aberturas y asomados al auto | Capas planas texturizadas | Ninguno |
| **Página** | Mitad de abajo blanca (ground) y tapa de cartulina con marco (backdrop) | Página con texturas por mitad | Ninguno |

**Primer prototipo (video de unos 5 segundos, papel blanco):**
- Empieza como una **tarjeta cerrada y plana**. Al abrirla, una **caja emerge del pliegue central**. Abierta del todo se ve una caja mayor atrás y un **cubo más pequeño adelante cuya parte inferior parece quedar sobre la hoja**, con una cara inclinada y su sombra debajo.
- En la mitad de abajo de la hoja se ven **pliegues en forma de X** que parten del centro.
- Es coherente con el diagrama: una **caja formada con V-fold** a 45° del pliegue central. **[Hipótesis, confianza media]:** el video es corto, tiene movimiento y la mano tapa partes de la pieza.

**Lo que falta confirmar:**
1. La **altura** de las paredes y de los paneles superiores: el diagrama fija dónde va cada pieza, no cuánto sobresale, y eso define el cierre (V-01).
2. Cuál de las dos V es la del frente y cómo se une la fachada.
3. Las **medidas reales** de la hoja y de la casita.
4. Cómo se pega la película transparente (por detrás o por delante) y con cuánto solape (pregunta 14).

Mientras tanto la casita puede declararse por datos (RF-34, apéndice D), de modo que no depende de la hipótesis.

**Consecuencias para el diseño:**
- La fachada mezcla **tres tipos de región**: opaca (sticker sobre cartulina), **hueco** (se corta y queda abierto) y **ventana transparente** (se corta el hueco y se cubre con una película impresa aparte). El contorno extraído del PNG debe distinguirlas (sección 14.4) y la exportación debe incluir una hoja para el material transparente (17.1).
- El flujo "**boceto en blanco primero, textura después**" que ya usa el cliente justifica la exportación en modo boceto (RF-35).
- Una caja con fachada independiente confirma que la **fachada y la caja son elementos separados con su propia validación**, aunque se pegan entre sí.
- El **diagrama es un plano de pegado**: la app debe poder mostrarlo, editarlo y también generarlo como "mapa de pegado" para el armado (secciones 8.4 y 17.2).

---

## 12. Simulación

### 12.1 Estrategia híbrida (ADR-02)

| Capa | Para qué | Cómo |
|---|---|---|
| **Fórmulas cerradas** | Step-fold y tent-fold (sección transversal plana) | Poses exactas a cualquier φ; sirven además como **oráculos de prueba** |
| **Motor general** | V-fold, box-fold, cilindro y mecanismos personalizados | Red de resortes (o proyección de restricciones) construida automáticamente desde el grafo de parches |
| **Validadores analíticos** | Comprobar condiciones del paper sin simular | Sección 13 |

### 12.2 Línea base del motor general

[Fuente: Iizuka et al. 2011] Cada polígono se representa como una red de resortes (3 resortes por triángulo; 6 por cuadrilátero, con diagonales). Los vértices de las aristas fijas siguen a la página o a otro mecanismo; el resto se mueve para mantener las longitudes de reposo. Las aristas que deben conservar su ángulo llevan **resortes de bisagra**. Integración explícita de Euler con los parámetros publicados k = 8, amortiguación D = 0,02, masa m = 100, k de bisagra = 0,02. Con esto simulan 14 primitivas, incluido el cilindro.

**[Propuesta]** El *spike* S0.2 compara esa línea base con una **proyección de restricciones** (position-based dynamics) vectorizada con NumPy, que suele ser más estable con pasos de tiempo grandes. Se elige la que dé poses correctas con menos tiempo por cuadro.

### 12.3 Control y caché de poses

1. La página mantiene la mitad fija (ground) y mueve la otra con el ángulo φ.
2. Se calculan poses **por continuación**: cada φ parte de la pose del paso anterior, de 180° hacia 0° y de vuelta, para seguir la rama correcta de movimiento (hay singularidades en los estados planos).
3. Las poses se guardan en una **caché por φ** (por ejemplo cada 1° a 2°); el deslizador solo lee y interpola. Se recalcula en un hilo secundario cuando cambia un parámetro (con espera breve para no recalcular en cada tecla).

### 12.4 Espesor y holguras

Los papers suponen papel rígido sin espesor (H4). La app agrega:
- **margen de colisión** igual al espesor total (cartulina + sticker + pegamento) al comprobar choques y contornos;
- **compensación en bisagras y pestañas** al generar el layout (parámetros iniciales a calibrar con prototipos; **[Pendiente]** el cliente indica el gramaje o espesor de su cartulina y de su sticker).

### 12.5 Límites conocidos

- [Fuente: Iizuka et al.] Los agujeros que aparecen al aplicar una textura transparente no cambian la red de resortes; las colisiones se calculan con el polígono del parche. **[Propuesta]** En la Fase 2 el contorno recortado puede usarse como proxy de colisión.
- Las colisiones no deforman las piezas: solo se informan.

---

## 13. Validaciones

| ID | Validación | Detalle | Fuente | Fase |
|---|---|---|---|---|
| V-01 | **Cierra plano dentro de la hoja** | A φ = 0° todos los vértices (más el espesor) quedan dentro del contorno de la hoja | Iizuka et al. (protrusión) | 1 |
| V-02 | **Sin choques en el recorrido** | De 0° a 180° ninguna arista penetra el polígono de otro parche, con margen por espesor | Iizuka et al. | 1 |
| V-03 | **Plegabilidad y balance** | Cuadrilátero de sección con lados a, b, c, d en orden: a + b = c + d. Box-fold: b + r = c + tb y g + l = c + tg. **Balance del tutorial:** V-fold α_izq + β_izq = α_der + β_der; pliegue paralelo b_izq + p_izq = b_der + p_der | Ruiz et al. (tomando a Hara y Sugihara 2009); Birmingham | 1 |
| V-04 | **Estabilidad (1 grado de libertad)** | Con las páginas quietas no queda movimiento residual. Las plantillas del catálogo son estables por construcción; para mecanismos personalizados se verifica el rango del jacobiano de restricciones | Definición de Ruiz et al.; chequeo numérico propuesto | 1 (plantillas) / 2 (personalizados) |
| V-05 | **Rangos de exclusión sobre el pliegue central** | Ninguna otra pieza sobre B y G en [xB − d/2, xF + d/2] para una box-fold (d = espesor de la caja en y); en [xB, xF + l/√2] para una v-fold tipo 1 (l = altura en z a 180°); el tipo 2 es similar | Ruiz et al. §3.3.2 | 1 |
| V-06 | **Reglas de colocación** | Solo sobre BPP; reglas de 11.2; lo que quede fuera pasa a amarillo | Ruiz et al. | 1 |
| V-07 | **Alineación de bordes** | Aristas compartidas con igual longitud y extremos coincidentes dentro de la tolerancia del proyecto (valor inicial 0,2 mm, a calibrar) | Propuesta | 1 |
| V-08 | **Pestañas** | Ancho mínimo de **10 mm**; esquinas recortadas; sin solaparse con otros parches ni cruzar el contorno de corte | Birmingham (ancho y esquinas); propuesta | 1 |
| V-09 | **Resolución de textura** | Resolución efectiva (ppp) sobre el tamaño impreso por encima de un umbral configurable (valor inicial 150 ppp, a calibrar) | Propuesta | 1 |
| V-10 | **Geometría de corte** | Polígonos válidos, sin autointersecciones, rasgo mínimo cortable a mano, islas flotantes avisadas | Propuesta | 1 |
| V-11 | **Ventanas transparentes** | Cada ventana tiene su pieza transparente con solape mínimo alrededor del hueco, sin invadir el contorno de la cara ni otras ventanas | Propuesta | 1 |

Cada hallazgo informa **severidad** (error, aviso), **ubicación** (elemento, parche, ángulo φ), **mensaje claro** y, en la Fase 2, una **corrección sugerida**.

---

## 14. Texturas y contornos

**[Cliente]** A cada "cara" aprobada se le pega un PNG; la app detecta la transparencia y recorta; luego se repite la simulación con la textura final.

### 14.1 Del PNG al contorno de corte

1. Leer el PNG con canal alfa (Pillow). Si no tiene alfa, avisar y ofrecer usar el rectángulo completo.
2. Umbralizar el alfa (umbral configurable) y extraer contornos externos e internos (OpenCV `findContours` o scikit-image).
3. Convertir a polígonos con *shapely*, **simplificar** (Douglas-Peucker con tolerancia en mm) y suavizar picos.
4. Aplicar un **margen de corte** configurable (desplazamiento hacia afuera, valor inicial 0,5 mm a calibrar) para no comerse el dibujo al cortar a mano.
5. Resolver los casos especiales: **regiones interiores** (ventanas y puertas de una fachada, ojos de una silueta), que pueden ser **huecos** o **ventanas transparentes** según lo que indique el usuario (14.4); **islas** sueltas (se avisan, V-10), y rasgos más finos que el mínimo cortable a mano.

### 14.2 Mapeo sobre la cara

- La textura se ubica sobre el polígono del parche con escala, posición y rotación editables; por defecto se ajusta al borde más largo de la cara.
- El contorno de corte se recorta contra el polígono de la cara más sus pestañas.
- **[Propuesta]** Un editor ligero de contorno (mover y borrar puntos) queda para la Fase 2 (RF-23).

### 14.3 Simulación con textura

El visor aplica la textura con transparencia real (los píxeles con alfa cero no se dibujan) y dibuja las **ventanas transparentes** como superficies translúcidas con la imagen de su película. Las colisiones siguen usando el polígono del parche hasta que se habilite el proxy de colisión recortado (sección 12.5).


### 14.4 Regiones de material: opaca, hueco y ventana transparente

**[Cliente]** Las ventanas transparentes de la fachada se imprimen en **papel transparente** y se pegan al resto de la impresión. La app lo modela como tres tipos de región dentro de una cara:

| Tipo | Qué es | Qué hace la app |
|---|---|---|
| **Opaca** | Sticker sobre cartulina | Textura y contorno de corte normales |
| **Hueco** | Abertura que queda abierta | Corta el hueco y lo marca como "cortar" en el PDF |
| **Ventana transparente** | Abertura cubierta con material transparente impreso | Corta el hueco en la cartulina y genera la **pieza transparente** con un **margen de solape** alrededor, con su número, para imprimir aparte |

**Proceso [Propuesta]:**
1. Tras extraer los contornos interiores (14.1), la app lista las regiones interiores de la cara y el usuario marca cada una como **hueco** (valor por defecto) o **ventana**.
2. Para una ventana puede asignar un PNG para la película (reflejo, marco, persiana).
3. La simulación dibuja la ventana con transparencia y mezcla la imagen de la película.
4. La exportación incluye la hoja de transparencias (`04_transparencias.pdf`, 17.1).

**Parámetros iniciales a calibrar:** margen de solape alrededor de cada ventana y lado de pegado de la película (por defecto, por detrás de la fachada). **[Pendiente]** El cliente indica cómo la pega y con cuánto solape (pregunta 14); además, la prueba con su papel transparente y su impresora se anota en la bitácora (sección 18).

---

## 15. Pestañas, identificadores y doble cara

### 15.1 Pestañas de pegado

[Fuente: Ruiz et al. §4.4; Iizuka et al. §5] Los parches se disponen **separados** en la hoja y se agrega una **pestaña** a cada borde donde se unen con otro parche. Si dos parches vecinos están limitados por líneas de corte y su bisagra común, se mantienen **conectados** en el layout y solo requieren un pliegue, sin pegado. Se asignan identificadores a parches y pestañas.

**[Propuesta]** Parámetros de las pestañas: ancho, chaflán de las esquinas, distancia mínima a otras pestañas y a la bisagra (valores iniciales a calibrar con el prototipo, sección 18). El tutorial del cliente indica no bajar de unos 10 mm de ancho y recortar las esquinas.

### 15.2 Identificadores

- Cada pestaña lleva **número + símbolo** (opcional) impresos en la parte que queda **oculta** al armar (la propia pestaña), de modo que no estropean la textura visible.
- En la parte receptora se imprime una **marca de alineación** con el mismo número y símbolo, **en el mapa de pegado** (sección 17.2) y, si el cliente lo prefiere, también como una cruz o muesca en el borde de la página base.
- [Fuente: Iizuka et al.] En el paper distinguen los pares por color; el plan agrega número y símbolo para impresión en blanco y negro.

### 15.3 Sticker sobre cartulina: doble cara **[Propuesta, a validar con el cliente]**

El flujo del cliente es: imprimir en sticker, **despegar y pegar sobre cartulina**, y recién entonces cortar. De eso se derivan reglas:

- **Cada parche tiene dos lados (A y B).** Solo se texturiza el lado que quedará visible. Si ambos lados son visibles (por ejemplo, las paredes de la casita por dentro y por fuera), se necesitan **dos pegatinas pegadas dorso con dorso**.
- El contorno del lado B se **espeja** respecto del lado A para que las siluetas coincidan al pegarlas dorso con dorso. La app genera ambas versiones y las etiqueta.
- Como el corte se hace sobre la pegatina ya pegada, las líneas de **corte** deben verse bien en la pegatina; las de **pliegue** se marcan de la forma de 17.3.

---

## 16. Generación del layout plano

Para cada mecanismo el generador de patrones transforma el grafo de parches en piezas 2D:

1. **Despliegue de cada pieza:** los parches conectados por bisagra se despliegan a un plano común.
2. **Pestañas:** se agregan según los pegados definidos (15.1) y se numeran.
3. **Compensación por espesor:** se ajustan holguras en bisagras y pestañas con los espesores del proyecto (12.4).
4. **Orden de ensamblaje:** **[Propuesta]** para la versión 1, el orden sigue la **jerarquía de colocación** (el parche base antes que lo que se monta sobre él; los mecanismos en el orden en que se colocaron). [Fuente: Ruiz et al.] Para ensamblajes más complejos emplean un método de instrucciones paso a paso para componentes rígidos (Agrawala et al. 2003); se evalúa en la Fase 4.
5. **Alineación entre piezas:** las marcas de la zona receptora se calculan con las mismas posiciones 3D que usó la simulación, de modo que lo que se pega en papel coincide con lo que se vio en pantalla.

---

## 17. Exportación

### 17.1 Conjunto de PDFs **[Propuesta]**

Cada archivo puede exportarse en **modo boceto** (RF-35): solo cortes, pliegues, pestañas e IDs, sin texturas, para armar primero un prototipo en papel blanco, como hace el cliente.

| Archivo | Contenido | Se imprime en |
|---|---|---|
| `01_pegatinas.pdf` | Texturas de todas las caras con contorno de corte, pestañas con ID y marcas de pliegue en los bordes (17.3), repartidas en hojas | Papel sticker |
| `02_pagina_base.pdf` | Texturas de las mitades de la página (ground y backdrop) y **mapa de pegado** con zonas numeradas | Sticker o papel común |
| `03_ensamblaje.pdf` | Tabla de correspondencias número ↔ pieza ↔ destino, orden de pegado y una vista del resultado final con los IDs | Papel común |
| `00_calibracion.pdf` | Cuadrado de 100 mm, regla, leyenda de líneas y prueba de pestañas | Papel común (primero) |
| `04_transparencias.pdf` | Piezas de material transparente (ventanas) con margen de solape, número y marcas de registro para alinearlas | Papel transparente apto para la impresora del cliente |

**[Pendiente]** Confirmar si el cliente prefiere un solo PDF multipágina. El motor genera cada página de forma independiente, así que es un cambio de empaquetado.

### 17.2 Mapa de pegado de la página base

La página base no solo se imprime: lleva **dibujadas las zonas de pegado** (rectángulos o regiones) con el número y símbolo de la pestaña que va allí, con trazo fino y claro para que quede debajo de la pieza pegada. Es la contraparte de las pestañas numeradas y resuelve el problema de "dónde va cada cosa".

### 17.3 Marcas de pliegue sobre pegatina **[Propuesta, a validar]**

Como la pegatina queda visible, dibujar el pliegue completo ensuciaría la textura. Opciones configurables:

| Opción | Descripción | Predeterminada |
|---|---|---|
| **Marcas en los extremos** | Pequeñas muescas de montaña/valle donde la bisagra toca el borde de la pieza; el usuario las une con una regla y marca con una punta roma (sobre el dorso o sobre la pegatina) | Sí |
| **Línea completa** | Trazo completo (discontinuo para valle, guión-punto para montaña) | No |
| **Plantilla aparte** | Hoja de plantilla de pliegues a imprimir en papel común y calcar | No |

La leyenda de la sección 7 aplica a todas. Para marcar el pliegue entre muescas, el tutorial recomienda un **bolígrafo sin tinta** (comprime las fibras sin cortarlas) [Fuente: Birmingham].

### 17.4 Reparto en hojas (nesting)

- Tamaño de hoja de impresión **independiente** del tamaño de la página del libro (el cliente usa ISO mayor que A4).
- Empaquetado de piezas con *shapely* y un empaquetador sencillo (estantes o `rectpack`), con rotaciones múltiplos de 90° y margen de seguridad.
- Cada hoja lleva número y marcas de registro; las piezas conservan su ID entre hojas.
- **[Propuesta, opcional]** Dirección de fibra de la cartulina: si el cliente lo desea, los pliegues largos se orientan paralelos a la fibra.

### 17.5 Detalles técnicos del PDF

- Generación con `pycairo` (superficie PDF en milímetros), sin escalado de la impresora (el PDF avisa "imprimir al 100 %").
- Texto de los IDs en una fuente legible a tamaños pequeños; grosores de línea de 0,2 a 0,35 mm configurables.
- Imágenes incrustadas con la resolución del PNG original (sin recompresión con pérdida cuando sea posible).
- El motor de exportación usa una interfaz común para poder agregar más adelante SVG/DXF (RF-29).

---

## 18. Prototipado físico y calibración

La simulación no reemplaza al papel: los papers suponen espesor cero. El plan incluye una **rutina de calibración** antes de usar la app en un diseño largo:

1. **Escala:** imprimir `00_calibracion.pdf` al 100 % y medir el cuadrado de 100 mm con regla o calibre. Si hay diferencia, ajustar la impresión o aplicar un factor de corrección en la app.
2. **Espesores y gramaje:** el cliente mide con calibre una cartulina sola y una cartulina con sticker, y anota el gramaje; esos valores van a los ajustes del proyecto. El tutorial usa cartulina de 160 g/m² y llega hasta 220 g/m² para piezas grandes.
3. **Pestañas:** la página de calibración incluye pestañas de varios anchos para elegir el más cómodo al pegar.
4. **Prototipo en papel de boceto:** antes de gastar cartulina, armar el mecanismo en papel común impreso desde la app.
5. **Registro de pruebas:** cada ajuste (espesor, holgura, tolerancia) queda documentado en `docs/pruebas_fisicas.md` con fecha, material y resultado.
6. **Casos de referencia:** los prototipos que el cliente ya hizo (CR-1 y CR-2, sección 25) se usan como pruebas de aceptación visual: la simulación debe comportarse como sus videos.
7. **Material transparente:** imprimir una prueba en el papel transparente del cliente, comprobar cómo seca y se adhiere la tinta, qué cara se imprime y qué solape resulta cómodo al pegar; anotar el resultado.

---

## 19. Generador origámico (Li et al. 2010)

Referencia: *Popup: Automatic Paper Architectures from 3D Models*, X.-Y. Li, C.-H. Shen, S.-S. Huang, T. Ju, S.-M. Hu. ACM Transactions on Graphics 29(4), 2010. **[Estado: leído completo.]**

### 19.1 Idea central

[Fuente] Una arquitectura de papel se hace con **una sola hoja**, sin pegado ni uniones. Dos regiones exteriores, el **backdrop** y el **ground**, se unen en el **pliegue central**. El resultado aproxima el modelo con parches planos en **solo dos orientaciones** y está garantizado como físicamente realizable (plegable y estable).

### 19.2 Entradas y salida

- **Entrada:** malla triangular (abierta o cerrada) y la posición de backdrop y ground respecto del modelo. En el paper son planos ortogonales (pliegue de **90°**); el algoritmo puede adaptarse a otros ángulos.
- **Salida:** el *layout* plano (líneas de corte y de pliegue, montaña y valle) y la superficie desplegada.

### 19.3 Algoritmo y plan de implementación en Python

| Paso | Qué hace según el paper | Implementación propuesta |
|---|---|---|
| **1. Superficie visible (plegable)** | Grilla cartesiana N×N×N (N = 128 en el paper). Se marcan los cubos que cruza la malla y se toman las caras de grilla "visibles" desde fuera mirando en la dirección (0, −1, −1). Esa elección asegura que las proyecciones no se solapen, y por lo tanto que sea plegable (Proposición 1) | Voxelización de superficie con `trimesh` o intersección triángulo-cubo vectorizada con NumPy; grilla booleana (128³ ≈ 2 MB); barrido por columnas paralelas a la dirección de vista |
| **2. Superficie realizable (estable)** | Crecimiento **voraz de regiones** con cola de prioridad. Parte de los parches de backdrop y ground y avanza hacia adentro; para cada celda de la base elige la cara candidata con **menor error** respecto de la superficie visible (suma de distancias entre centros de caras). Cada parche nuevo debe cumplir el orden de la Proposición 2 (apoyarse en dos parches paralelos no coplanares ya colocados, o en una pareja conectada apoyada en parches previos) | `heapq` sobre celdas; arreglos NumPy para candidatos y errores; `numba` opcional si Python puro es lento |
| **3. Refinamiento geométrico** | Suavizado iterativo de las fronteras en zig-zag, moviendo un vértice por vez dentro de **zonas seguras** que mantienen la realizabilidad | Iteración vectorizada con restricciones; comprobar con la validación V-03/V-04 después de cada pasada |

**Rendimiento.** El paper informa tiempos menores a un segundo en sus ejemplos. En Python puro se espera bastante más: por eso la vista previa usa N = 64 y la exportación final N = 128 (valores iniciales a calibrar en el spike S0.5).

**Lista de lectura antes de implementar** (requiere las figuras del PDF): patrones de camino de la figura 8; enunciado exacto de las proposiciones 1 y 2; definición de zona segura; regla para clasificar cada pliegue como montaña o valle; pasos de generación del layout.

### 19.4 Alcance y límites

- Funciona mejor con modelos de **planos mayormente horizontales y verticales**, bien apoyados en backdrop y ground (arquitectura). Las superficies inclinadas o curvas se aproximan con escalones.
- Con modelos **orgánicos** o flotantes el resultado puede distorsionarse; el propio paper sugiere que en esos casos haría falta más de una hoja.
- Supone papel **rígido y de grosor cero** (la app agrega holguras, 12.4).

### 19.5 Ediciones que ofrece la app sobre el resultado

[Fuente] Mover backdrop y ground, ajustar las líneas de corte para dar estilo y **recortar regiones** para formar huecos (ventanas, figuras). Como el resultado es un grafo de parches editable, además se puede reasignar texturas, mover el conjunto y recalcular pestañas.

### 19.6 Integración con el resto del diseño

| Uso | Cómo se resuelve | Condición |
|---|---|---|
| **Página entera de 90°** | El proyecto tiene ángulo de diseño 90° y el generador usa las dos mitades de la página como backdrop y ground | El libro se muestra abierto a 90°; a 180° la estructura queda plana |
| **Pieza dentro de otra página** | La hoja generada se monta como una "tarjeta dentro de la tarjeta" sobre un **BPP** cuyo ángulo local ψ valga **90° cuando la página está en su ángulo de diseño** | **[Hipótesis a validar con prototipo]** Se pegan sus paneles exteriores (backdrop y ground de la pieza) sobre los dos parches del BPP, con su pliegue central alineado con la bisagra del BPP |

Razonamiento: [Fuente + inferencia, H7] Ruiz et al. solo montan la step-fold (90°) entre un parche base y un lateral de una box-fold, lo que indica que ese par vale 90° con la página abierta 180°. Una pieza origámica montada sobre el par {página, página} de una tarjeta de 180° quedaría **plana** al abrir completamente, así que no tendría sentido allí. La app lo comprueba con una validación específica: `ψ(φ_diseño) = 90° ± tolerancia`.

Para modelar esto cada BPP expone una función `ψ(φ)` (ángulo local según el ángulo de apertura de la página) y los generadores 90° reciben un BPP, no una página.

---

## 20. Generadores avanzados (modo avanzado)

### 20.1 Interfaz común de generador (ADR-08)

```python
class Generator(Protocol):
    id: str                      # p. ej. "origamic-li2010"
    label: str                   # "Arquitectura origámica (Li et al. 2010)"
    card_angle: int              # 90 | 180
    def params_schema(self) -> ParamSchema: ...
    def run(self, inp: GeneratorInput, params: dict,
            progress: ProgressCb) -> GeneratorResult: ...

@dataclass
class GeneratorResult:
    patch_graph: PatchGraph      # parches, bisagras, pegados
    base_pair: BasePairRef       # sobre qué BPP se monta
    report: ValidityReport       # plegable / estable según el paper
    meta: dict                   # parámetros, versión del algoritmo, referencias
```

Cada generador corre en un hilo aparte, informa progreso y devuelve un grafo de parches que el usuario puede congelar en un elemento editable.

### 20.2 Multi-estilo (Ruiz et al. 2014): la pieza que decide el pliegue para cada parte

Referencia: *Multi-style Paper Pop-up Designs from 3D Models*, C. R. Ruiz Jr., S. N. Le, J. Yu, K.-L. Low. Computer Graphics Forum 33(2), 2014. **[Estado: leído completo.]** Es el trabajo más alineado con el deseo original del cliente.

| Etapa | Qué hace según el paper | Notas de implementación |
|---|---|---|
| **1. Alineación** | Análisis de componentes principales de las **normales ponderadas por el área** de las caras; el eje principal pasa a ser y. Se calcula la caja envolvente alineada a ejes y el plano de simetría; la base de la caja da ground y backdrop iniciales, y su intersección con el plano de simetría da el pliegue central | NumPy; el usuario puede reorientar el modelo |
| **2. Ajuste de primitivas** | Prismas **rectangulares y triangulares** con restricciones: ángulos rectos; aristas laterales paralelas u ortogonales al pliegue central; colocación solo sobre un BPP. Ajuste volumétrico por **RANSAC** con error `error_fit = w1·atípicos + w2·distancia + w3·cobertura` (pesos entre 0 y 1 que suman 1) y selección de la mejor combinación por **programación dinámica**. Se agregan vértices auxiliares para repartir bien los puntos en la superficie | Los pesos controlan cuántas primitivas se generan: más peso en cobertura y atípicos da menos primitivas y más grandes |
| **3. Mapeo primitiva → mecanismo** | Pocas combinaciones posibles: **búsqueda exhaustiva** con criterio `error_cobertura = 1 − Σ área caras principales / Σ área caras`. Se verifica la validez con las condiciones analíticas, **sin simular**. Se permite **reajustar** primitivas mientras se cumpla la plegabilidad (p. ej. laterales inclinados de una box-fold si b+r=c+tb y g+l=c+tg) y **recortar** parches frontales o traseros si no hay separación suficiente | Reutiliza V-03, V-05 y V-06 (sección 13) |
| **4. Generación de parches** | Enfoque **basado en imágenes**: proyección ortográfica de la malla sobre un plano coplanar a cada cara principal; para box-fold, varias capas a distintas profundidades obtenidas segmentando mapas de profundidad y de normales con un ajuste local de superficie cuadrática | Render offscreen con ModernGL o rasterizador propio; `scipy` para el ajuste |
| **5. Layout y ensamblaje** | Parches separados en la hoja con pestañas en cada borde de unión; los vecinos que solo comparten bisagra quedan conectados; IDs y orden de ensamblaje | Reutiliza secciones 15 y 16 |

**Resultados y límites [Fuente].** Corre en segundos a minutos (el ajuste de primitivas es lo más lento) con modelos de hasta unos 30 000 vértices. Va bien con objetos en bloque (autos, camiones, edificios); las formas orgánicas y redondeadas necesitan primitivas más complejas y no se resuelven bien; los objetos difíciles de alinear a los ejes principales se aproximan peor. **Las partes curvas quedan fuera** (solo prismas rectangulares y triangulares), lo que significa que el arco del auto del cliente seguiría siendo un elemento manual.

**Por qué importa para el cliente.** Con esta etapa, importar el STL de un auto podría proponer automáticamente una box-fold para el cuerpo y otros mecanismos para las partes, que es la idea original de "la app elige el pliegue".

### 20.3 Otros trabajos candidatos

| Trabajo | Aporte | Lectura | Notas |
|---|---|---|---|
| Li, Ju, Gu, Hu 2011, *A geometric study of v-style pop-ups* | Extiende la noción de validez a v-style y tiene una herramienta interactiva desde 3D | Solo referencia | Según Ruiz et al., usa voxelización y se limita a tres orientaciones de parche |
| Le et al. 2014, *Surface and contour-preserving origamic architecture paper pop-ups* (IEEE TVCG 20(2)) | OA para formas más libres: segmentación de superficie en el dominio de la imagen, representación con parches paralelos y condiciones geométricas de plegabilidad y estabilidad | Solo resumen | Candidata a reemplazar o complementar a Li 2010 en modelos orgánicos |
| Liu et al. 2014, *Image-based Paper Pop-up Design* (póster SIGGRAPH) | OA desde **imágenes 2D**: segmentación en parches, pliegues iniciales en los bordes izquierdo y derecho de cada parche, árbol de decisión sobre añadir o quitar pliegues, programación cuadrática para posiciones, y métrica de calidad para elegir entre varias propuestas | Solo póster de una página | Encaja con la entrada de PNG del cliente |
| Le-Nguyen et al. 2013, *Automatic Paper Sliceform Design from 3D Solid Models* (IEEE TVCG) | Estilo "lattice": dos conjuntos de parches paralelos encajados | Solo resumen | Familia distinta (sliceforms) |
| Mitani y Suzuki 2003, 180° con secciones tipo reticulado | Generación para tarjetas de 180° desde mallas | Solo referencia | Según Iizuka et al., la construcción solo se apoya en el pliegue central |
| Hoiem, Efros, Hebert 2005, *Automatic photo pop-up* | Popups simples a partir de fotografías | Solo referencia | Útil si el cliente quiere partir de fotos de escenas |
| Abel et al. 2012, *Universality results for pop-up cards* | Teoría: subdividir un polígono en un mecanismo de un grado de libertad | Solo referencia | Teórico; prioridad baja |

---

## 21. Mapa de trabajos: aporte, módulo y estado de lectura

| Trabajo | Aporte a la app | Módulo | Fase | Lectura |
|---|---|---|---|---|
| Chatani (años 80) | Origen de la arquitectura origámica | Contexto de `origamic/` | 3 | Solo referencia |
| **Li et al. 2010** | Generación automática de OA desde 3D con garantías | `origamic/` | 3 | **Completo** |
| **Iizuka et al. 2011** | Flujo interactivo, aristas base, simulación con resortes, detección de choques y de protrusión, plantillas con pestañas | `sim/`, `validate/`, `ui/` | 1–2 | **Completo** |
| **Ruiz et al. 2014** | Mecanismos con validez analítica, mapeo primitiva → mecanismo, parches basados en imágenes, layout y orden de ensamblaje | `mechanisms/`, `validate/`, generador multi-estilo | 1 y 4 | **Completo** |
| Ruiz et al. 2013 (SIGGRAPH Asia, nota técnica) | Antecedente del anterior; condiciones de validez para box-style | Referencia de `mechanisms/` | 4 | Solo resumen |
| Li et al. 2011 (v-style) | Validez general de v-style | `mechanisms/`, Fase 4 | 4 | Solo referencia |
| Le et al. 2014 | OA de formas libres | Generador adicional | 4 | Solo resumen |
| Liu et al. 2014 | OA desde imágenes 2D | Generador adicional | 4 | Solo póster |
| Mitani y Suzuki 2003 y 2004; Mitani, Suzuki y Uno 2003 | OA con voxeles y con polígonos; 180° con reticulado | Referencia de `origamic/` | 3–4 | Solo referencia |
| Glassner 2002 (partes 1 y 2) | Movimiento analítico de v-fold y single-slit | Referencia de `mechanisms/` | 1–2 | Solo referencia |
| Okamura e Igarashi 2009 | Interfaz con cinco primitivas y solución analítica | Referencia de `ui/` | 2 | Solo referencia |
| Hara y Sugihara 2009 | Tent-fold y plegabilidad del cuadrilátero (a+b=c+d) | `validate/` (V-03) | 1 | Solo referencia |
| **Birmingham, tutorial 1 (YouTube)** | Tres principios, cinco variantes de V-fold, tres de pliegue paralelo, reglas de oficio | `mechanisms/`, `validate/` (V-03, V-08), `export/` | 1 | **Transcripción completa** (el libro del autor no se consultó) |
| Lee, Tor y Soo 1996 | Restricciones geométricas de v-folds y simulación | Referencia de `sim/` | 1–2 | Solo referencia |
| Hendrix y Eisenberg 2006 | Diseño de patrón plano por agregado de primitivas | Referencia de `export/` | 2 | Solo referencia |
| Uehara y Teramoto 2006 | La plegabilidad general es NP-difícil | Justificación de ADR-02 | — | Solo referencia |
| Agrawala et al. 2003 | Instrucciones de ensamblaje paso a paso | Hoja de ensamblaje | 4 | Solo referencia |
| Furuta et al. 2007 | Modelo de resortes para origami (base de Iizuka) | `sim/` | 1 | Solo referencia |
| *Elements of Pop Up* (libro) | Catálogo de primitivas | `mechanisms/` | 2 | No consultado |

---

## 22. Arquitectura técnica

### 22.1 Capas

```
┌─────────────────────────────────────────────────────────────┐
│ UI (GTK 4)       ventanas, visor 3D, vista cenital, paneles │
├─────────────────────────────────────────────────────────────┤
│ Aplicación       comandos (deshacer/rehacer), proyecto,     │
│                  hilos de trabajo, caché                    │
├─────────────────────────────────────────────────────────────┤
│ Dominio          proyecto, página, elementos, grafo de      │
│                  parches, BPP, texturas, variantes          │
├─────────────────────────────────────────────────────────────┤
│ Motores          mecanismos · simulación · validación ·     │
│                  patrones/layout · exportación · generadores│
├─────────────────────────────────────────────────────────────┤
│ E/S              proyecto .popup · STL · PNG · PDF          │
└─────────────────────────────────────────────────────────────┘
```

Regla de dependencias: **dominio y motores no importan GTK**. Eso permite probarlos sin interfaz (RNF-04) y reutilizarlos desde la línea de comandos.

**Hilos.** Simulación y generadores corren en hilos de trabajo con **cancelación** y progreso; el resultado vuelve a la interfaz con `GLib.idle_add`. La interfaz nunca espera cálculo.

### 22.2 Pila tecnológica **[Propuesta, a confirmar en la Fase 0]**

| Componente | Rol | Notas |
|---|---|---|
| Python 3.11+ | Lenguaje | |
| PyGObject + GTK 4 (libadwaita opcional) | Interfaz | Se instalan desde los paquetes de la distribución; el entorno virtual se crea con acceso a los paquetes del sistema |
| ModernGL | Render 3D | Dentro de `Gtk.GLArea` con búfer de profundidad activado (propiedad `has-depth-buffer`); ver H9 |
| NumPy, SciPy | Álgebra, solver, ajuste cuadrático, futura programación cuadrática (Liu et al.) | |
| trimesh | Lectura de STL y mallas, voxelización | |
| shapely 2.x | Geometría 2D: polígonos, desplazamientos, uniones, empaquetado | |
| Pillow y OpenCV (versión sin interfaz) o scikit-image | PNG y extracción de contornos | |
| pycairo | PDF en milímetros | `reportlab` como alternativa |
| numba (opcional) | Acelerar voxelización, crecimiento de regiones y RANSAC | Solo si Python puro no alcanza |
| pytest, hypothesis, ruff, mypy | Calidad | |

### 22.3 Decisiones de arquitectura (ADR)

| ID | Decisión | Opciones | Estado y criterio |
|---|---|---|---|
| **ADR-01** | **Visor 3D** | A) `Gtk.GLArea` + ModernGL (recomendada, Python puro). B) WebKitGTK + three.js (trae órbita, selección y manipuladores hechos, pero agrega JavaScript y un puente). C) Render isométrico 2D con cairo (plan de contingencia) | Pendiente de **spike S0.1**: elegir A si da órbita, profundidad, texturas con alfa y selección a 30 fps o más en el equipo del cliente |
| **ADR-02** | **Simulación** | Híbrida: fórmulas cerradas + motor general. Motor general: A) resortes de Iizuka. B) proyección de restricciones (PBD) | Pendiente de **spike S0.2** |
| **ADR-03** | **Representación**: grafo de parches con bisagras, pegados y BPP | Alternativa descartada: una clase especial por mecanismo con geometría a mano | Decidida |
| **ADR-04** | **Convenciones** de unidades, ángulos y ejes (sección 7) | | Decidida; se verifica al implementar Li et al. |
| **ADR-05** | **Formato `.popup`**: archivo zip con `project.json` versionado y carpeta `assets/` (PNG y STL), con migraciones entre versiones | JSON plano con rutas externas (frágil si se mueven los archivos) | Decidida |
| **ADR-06** | **PDF** con pycairo | reportlab | Confirmar en **spike S0.4** |
| **ADR-07** | **Idioma:** código e identificadores en inglés; interfaz en español con gettext | Todo en español | Decidida; ajustable |
| **ADR-08** | **Generadores como plugins** con una interfaz común (sección 20.1) | Algoritmos incrustados en el núcleo | Decidida |

### 22.4 Rendimiento

- Poses en **caché por ángulo**; el deslizador solo interpola (12.3).
- **Dos resoluciones** en generadores: vista previa (N bajo) y exportación (N alto).
- Mallas STL grandes: simplificación en la importación para el visor; el generador usa la malla original.
- Presupuesto de referencia (RNF-03): visor a 30 fps o más; recálculo en menos de 2 s en una página típica.

### 22.5 Entorno y empaquetado

- Proyecto con `pyproject.toml` y comando `python -m popup_studio`.
- Entorno virtual con `--system-site-packages` para reutilizar PyGObject del sistema.
- **[Propuesta, Fase 5]** Empaquetado Flatpak con el runtime de GNOME; es pesado por las dependencias numéricas, así que se difiere hasta que la app sea estable.

### 22.6 Privacidad

La app es **local**: no hace conexiones de red, no envía telemetría y no sube imágenes. Las fotos de familia del cliente permanecen en su equipo (RNF-02).

### 22.7 Registro y diagnóstico

- Registro con `logging` en archivo rotativo.
- Un **panel de depuración** opcional muestra tiempos del solver, número de iteraciones y residuo de restricciones por ángulo.

---

## 23. Estrategia de pruebas

| Tipo | Qué cubre | Ejemplos |
|---|---|---|
| **Unitarias de geometría** | Cada mecanismo con vectores de prueba conocidos | Step-fold con h = g = 40 mm: la posición de M a φ = 0°, 45°, 90°, 135° y 180° coincide con el apéndice B dentro de 0,05 mm |
| **Propiedades** (`hypothesis`) | Invariantes con parámetros aleatorios válidos | Las longitudes de aristas se conservan a cualquier φ (rigidez); a φ = 0° todo es plano; no hay valores NaN; el resultado es determinista |
| **De contrato de validadores** | Cada validación con casos válidos e inválidos construidos a propósito | Una box-fold con b + r ≠ c + tb falla V-03; una pieza que sobresale 6 mm falla V-01 |
| **Contraste con oráculos** | El motor general frente a fórmulas cerradas | Step-fold y tent-fold simulados con el motor general coinciden con las fórmulas |
| **De regresión (golden)** | Patrones y PDFs de un proyecto de referencia ("casita y auto") | Comparación geométrica de trazos, no byte a byte |
| **De generadores** | Ejemplos de los papers cuando se tengan los modelos | Layout sin solapamientos (plegable), cumplimiento de la condición de estabilidad, tiempo máximo |
| **De rendimiento** | Presupuestos de RNF-03 | Benchmarks con umbral |
| **De humo de la interfaz** | La ventana abre, carga un proyecto y reproduce una animación | `xvfb-run` o `GDK_BACKEND=broadway` en CI |
| **Físicas** | Prototipo en papel y calibración (sección 18) | Registro en `docs/pruebas_fisicas.md` |

**Calidad de código.** `ruff` y `mypy` (estricto en dominio y motores). Objetivo inicial de cobertura de 80 % en dominio y motores. **[Propuesta]**

---

## 24. Estructura del repositorio

```
popup-studio/
├─ pyproject.toml
├─ README.md
├─ docs/
│  ├─ plan.md                    # este documento
│  ├─ adr/                       # una nota por decisión (ADR-01…08)
│  ├─ papers/                    # notas de lectura propias (no los PDFs)
│  └─ pruebas_fisicas.md         # bitácora de prototipos y calibración
├─ src/popup_studio/
│  ├─ core/                      # proyecto, página, elementos, grafo de parches, BPP
│  ├─ mechanisms/                # capa, step, tent, vfold, box, cilindro, personalizado
│  ├─ sim/                       # fórmulas cerradas, motor general, caché de poses
│  ├─ validate/                  # V-01 … V-11
│  ├─ textures/                  # PNG con alfa → contorno → recorte
│  ├─ layout/                    # despliegue, pestañas, IDs, nesting
│  ├─ export/                    # PDF (pycairo), interfaz de exportadores
│  ├─ generators/
│  │   ├─ origamic_li2010/
│  │   └─ multistyle_ruiz2014/
│  ├─ io/                        # .popup, STL, PNG
│  └─ ui/                        # GTK 4: ventanas, visor, paneles, comandos
├─ tests/
│  ├─ unit/  ├─ property/  ├─ golden/  └─ perf/
└─ examples/
   └─ casita_y_auto/             # el proyecto de referencia del cliente
```

En `docs/papers/` se guardan **notas propias** (resumen, ecuaciones relevantes, dudas) de cada paper, no copias de los PDFs, para respetar los derechos de autor.

---

## 25. Plan por fases

Tamaños **relativos** (S, M, L, XL): se calibran con tiempos reales al terminar la Fase 0. No se prometen fechas.

```
F0 Spikes ──► F1 Núcleo + modo básico ──► F2 Asistido ──┬──► F3 Origámico (Li 2010, 90°)
                    (mi ejemplo)                         └──► F4 Avanzado (Ruiz 2014 y otros) ──► F5 Pulido
```

F3 y F4 dependen de los BPP, los validadores y el grafo de parches de F1 y F2, por eso van después.

### Fase 0: Spikes técnicos (tamaño M en total)

Cada spike tiene un límite de tiempo, produce una nota (ADR o hallazgo) y su código puede descartarse.

**Datos que el cliente aporta antes de empezar:** tres PNG con alfa (persona recortada, auto, ventana), un STL simple (cubo o un auto sencillo), una foto del interior de la casita con la página a medio cerrar (o su patrón), el espesor de su cartulina y de su sticker, y los PDFs de los papers que tenga.

| Spike | Qué se prueba | Criterio de salida |
|---|---|---|
| **S0.1 Visor** | Ventana GTK 4 con `Gtk.GLArea` + ModernGL: cubo con textura con alfa, cámara orbital, búfer de profundidad, selección por rayo | 30 fps o más con 200 parches simulados; selección correcta → decide **ADR-01** |
| **S0.2 Simulación** | Step-fold con (A) resortes de Iizuka (k = 8, D = 0,02, m = 100, k de bisagra = 0,02) y (B) proyección de restricciones; cilindro de 14 cuadriláteros con bisagras elásticas | Error ≤ 0,1 mm frente a la fórmula del apéndice B en φ = 0°, 45°, 90°, 135°, 180°; elegir motor → **ADR-02** |
| **S0.3 Contorno desde PNG** | Con los PNG reales: alfa → polígono simplificado, huecos, islas, margen | Polígonos válidos; error de contorno ≤ 0,3 mm |
| **S0.4 PDF a escala** | pycairo: cuatro estilos de línea, IDs, 1:1; imprimir y medir | Cuadrado de 100 mm con diferencia ≤ 0,5 mm → confirma **ADR-06** |
| **S0.5 STL y voxelización** | Cargar STL; voxelizar a 64³ y 128³; caras visibles | 128³ en 10 s o menos sin numba (si no, evaluar numba) |
| **S0.6 Prototipos en papel** | Armar a mano una step-fold y una box-fold con piezas impresas desde S0.4 | Cierra plano y queda estable; holguras registradas en la bitácora |

### Fase 1: Núcleo + modo básico, primera versión (tamaño XL)

**Estrategia:** primero una **rebanada vertical** completa con el mecanismo más simple (capa plana + step-fold: de proxy a PDF armado), y recién después sumar mecanismos. Así se descubren pronto los problemas de integración.

Orden interno: capa plana → step-fold → exportación mínima → tent-fold → v-fold → box-fold → cilindro → texturas completas → pulido y validaciones.

| Historia | Descripción | RF | Tamaño | Criterio de aceptación |
|---|---|---|---|---|
| US-101 | Crear proyecto | 01 | S | Con hoja de 420 × 297 mm y 180° se crea la página con su pliegue central y espesores; se rechazan valores ≤ 0 |
| US-102 | Guardar y abrir `.popup`, autoguardado | 02, 06 | M | Ida y vuelta idéntica; si falta una textura se avisa y no falla; tras un cierre forzado se recupera el último estado |
| US-103 | Deshacer y rehacer | 03 | M | 50 niveles; cada acción del editor es un comando |
| US-201 | Visor: órbita, zoom, desplazamiento | — | M | Según S0.1 |
| US-202 | Vista cenital con colocación numérica y por arrastre; ajuste a grilla y bordes | 08, 11 | L | Mover un elemento actualiza posición, pestañas y validaciones en menos de 2 s |
| US-203 | Selección en visor y árbol | 09 | M | El elemento elegido se resalta y su panel de propiedades se actualiza |
| US-204 | BPP visibles y ajuste automático de posiciones fijas | 10 | L | Al colocar un mecanismo se muestra su BPP y las posiciones fijas se ajustan para que pliegue |
| US-301 | Capa plana con pestañas | 12 | S | Se pega, se simula y se exporta |
| US-302 | Pliegue paralelo / step-fold (fórmula cerrada, V-03) con sus tres variantes (simétrico, paralelogramo, asimétrico) | 12 | M | Coincide con el apéndice B dentro de 0,05 mm; solo admite combinaciones balanceadas |
| US-303 | Tent-fold | 12 | M | Cumple V-03; simétrico respecto del pliegue central |
| US-304 | V-fold tipos 1 y 2, con las cinco variantes de ángulos (recto, agudo, puntiagudo, obtuso, asimétrico) | 12 | L | Plegable y sin choques con parámetros típicos; balance de ángulos (V-03) y rango de exclusión (V-05) calculados; reproduce el diagrama del cliente (dos V-fold enfrentados a 45°) |
| US-305 | Box-fold | 12 | XL | Cumple b + r = c + tb y g + l = c + tg; estable (sin cizallamiento) en la simulación |
| US-306 | Cilindro elástico con pestaña | 12 | L | Se mantiene curvo a cualquier φ y cierra plano |
| US-307 | Mecanismo definido por datos (archivo de parches, bisagras y pegados) | 34 | M | La casita se declara con un archivo y se simula, valida y exporta igual que un mecanismo del catálogo |
| US-401 | Deslizador de ángulo y reproducción con caché | 16 | M | Fluido a 30 fps; recalculo en segundo plano |
| US-402 | Validaciones V-01 a V-11 con panel y resaltado | 17 | L | Cada validación detecta su caso inválido de prueba y no falla en el válido |
| US-403 | Estados verde / amarillo / rojo | 19 | S | Un elemento fuera de las reglas pasa a amarillo; con un choque, a rojo |
| US-501 | PNG por cara, recorte por alfa, margen, escala y posición | 20 | L | El contorno coincide con la silueta dentro de 0,3 mm |
| US-502 | Simulación con textura | 21 | M | Píxeles transparentes no se dibujan |
| US-503 | Doble cara con contorno espejado | 22 | M | Las dos siluetas coinciden al superponerlas dorso con dorso |
| US-504 | Regiones de material: hueco y ventana transparente, con su pieza y su hoja de impresión | 36 | M | Marcar una región como ventana genera su pieza transparente con solape y la incluye en `04_transparencias.pdf`; la simulación la muestra translúcida |
| US-601 | PDF de pegatinas con corte, pestañas con ID y marcas de pliegue; modo boceto sin texturas | 24, 25, 35 | L | Escala 1:1; todas las pestañas tienen ID legible; el modo boceto produce el mismo patrón sin imágenes |
| US-602 | Mapa de pegado de la página base | 25 | M | Cada zona tiene el mismo número y símbolo que su pestaña |
| US-603 | Reparto en hojas | 26 | M | Ninguna pieza se superpone ni sale de la hoja |
| US-604 | Hoja de ensamblaje y página de calibración | 27, 28 | M | La tabla lista todas las piezas y destinos |

**Casos de referencia físicos.** El cliente ya tiene dos prototipos que sirven como pruebas de aceptación:
- **CR-1:** el primer prototipo en papel blanco (caja sobre v-fold). Se reproduce **antes** que la casita completa, junto con US-304. Criterios: la tarjeta cierra plana; al abrir a 180° aparece la caja en el centro; los pliegues en X de la página coinciden con los del patrón; la animación simulada es cualitativamente igual a la del video en 45°, 90° y 135°.
- **CR-2:** la casita con fachada y el auto con textura (proyecto "casita y auto").

**Criterios de aceptación de la fase (proyecto de referencia "casita y auto"):**
1. El cliente diseña la página completa (casita, auto y personas) en **20 minutos o menos**, sin contar texturas.
2. La simulación no muestra choques ni salidas del contorno (V-01, V-02).
3. Con los PDFs se arma el popup físico y **cierra plano**.
4. Las aristas compartidas están alineadas dentro de la tolerancia del proyecto (V-07), también en el prototipo.
5. Se reabre el proyecto, se cambia una medida y se reexporta sin rehacer nada.
6. El **plano de pegado** que genera la app para la casita coincide con el diagrama del cliente (rombo a 45° con una diagonal sobre el pliegue y tira interior adosada).

### Fase 2: Modo asistido (tamaño L)

El recomendador de esta fase usa la **cobertura y las reglas de validez de Ruiz et al.** (11.3) para elementos colocados a mano; es la parte de ese paper que responde a "qué pliegue usar" sin necesidad del ajuste automático de primitivas, que llega en la Fase 4a.

| Historia | Descripción | RF | Criterio de aceptación |
|---|---|---|---|
| US-801 | Variantes del diseño | 04 | Se guardan, comparan y restauran variantes |
| US-802 | Recomendador de mecanismo | 15 | Para los elementos del proyecto de referencia, el mecanismo usado por el cliente aparece entre las tres primeras propuestas |
| US-803 | Correcciones sugeridas | 18 | Con errores intencionales, se propone al menos una corrección válida |
| US-804 | Mecanismo personalizado | 14 | Se crea, se simula y se exporta una plantilla propia |
| US-805 | Estabilidad por jacobiano (V-04) para personalizados | — | Detecta un mecanismo con grados de libertad de más |
| US-806 | Editor de contorno y proxy de colisión recortado | 23 | Los huecos de una textura se respetan en colisiones |
| US-807 | Catálogo ampliado (primitivas de Iizuka) | — | Al menos tres primitivas nuevas con tests |

### Fase 3: Modo origámico, Li et al. 2010 (tamaño XL)

**Entrada obligatoria:** lectura completa del paper incluyendo figuras (lista de 19.3). Un spike inicial reproduce el pipeline con un modelo simple.

| Historia | Descripción | RF | Criterio de aceptación |
|---|---|---|---|
| US-901 | Importar STL y fijar backdrop y ground | 30 | Se ve el modelo con los planos editables |
| US-902 | Voxelización y superficie visible | 30 | Proyecciones sin solapes (foldable) |
| US-903 | Crecimiento de regiones realizable | 30 | Cumple el orden de la Proposición 2 en todos los parches |
| US-904 | Refinamiento geométrico | 30 | Contornos suavizados sin perder realizabilidad |
| US-905 | Layout y exportación de hoja única | 30 | Cortes y pliegues montaña/valle correctos en el PDF |
| US-906 | Simulación y validaciones del resultado | 30 | La animación abre y cierra plano; V-01 y V-02 sin errores |
| US-907 | Ediciones: mover planos, recortar regiones | 30 | Un recorte produce un hueco y mantiene la validez |
| US-908 | Página entera de 90° | 30 | Proyecto de 90° con la hoja generada |
| US-909 | Pieza sobre un BPP de 90° **(experimento)** | 31 | Prototipo físico plano al cerrar y estable a su ángulo de diseño; si falla, se documenta y se descarta |

**Criterios de aceptación de la fase:** reproducir un ejemplo arquitectónico del paper o equivalente, armarlo físicamente y comprobar que queda plano al cerrar y estable a 90°. Tiempo de vista previa dentro del presupuesto fijado en S0.5.

### Fase 4: Modo avanzado (tamaño XL, en subfases)

| Subfase | Trabajo | Tamaño | Notas |
|---|---|---|---|
| **4a** | **Multi-estilo (Ruiz et al. 2014):** alineación, ajuste de primitivas por RANSAC, mapeo a mecanismos, parches basados en imágenes, layout y orden de ensamblaje | XL | Reutiliza validadores V-03, V-05 y V-06; no cubre partes curvas |
| **4b** | Formas libres (Le et al. 2014) | L | Complemento de F3 para modelos orgánicos |
| **4c** | OA desde imágenes (Liu et al. 2014) | L | Árbol de decisión de pliegues y programación cuadrática |
| **4d** | Sliceform y lattice 180° | L | Familias distintas |
| **4e** | Instrucciones paso a paso (Agrawala et al.) | M | Mejora la hoja de ensamblaje |

**Orden de F3 y F4a [Decisión por defecto; el cliente está abierto a opciones].** Las dos fases son independientes entre sí, así que el orden es cuestión de valor y de riesgo:

| Opción | A favor | En contra |
|---|---|---|
| **A. Li 2010 primero (F3)** *(elegida por defecto)* | Es lo que más le interesa al cliente; no depende de los mecanismos de 180°; el algoritmo es determinista y está bien descrito | Produce tarjetas de 90° (otra familia que su ejemplo) y exige una exportación de hoja única |
| **B. Ruiz 2014 primero (4a)** | Genera el estilo de su ejemplo (180°, piezas pegadas) y reutiliza pestañas, IDs y layout de la Fase 1 | Depende de que v-fold y box-fold estén sólidos; el ajuste de primitivas y los parches por imagen son más trabajo de ingeniería |

**Por qué se mantiene A:** el dolor principal del cliente, "saber qué pliegue usar", ya queda cubierto en la **Fase 2** por el recomendador, que aplica a elementos manuales el mapeo y las reglas de validez de Ruiz et al. (11.3). Lo que se pospone es la parte automática (ajuste de primitivas desde un STL), no la ayuda para elegir. Si el cliente prefiere B, F3 y 4a se intercambian sin tocar el resto del plan. Cada subfase incluye lectura completa del paper, spike, generador, pruebas y prototipo físico.

### Fase 5: Pulido (tamaño L)

Libro con varias páginas (RF-05), exportación para plotter (RF-29), manipuladores 3D, empaquetado Flatpak, ayuda integrada y biblioteca de plantillas.

---

## 26. Criterios de listo y de terminado

**Definición de listo (DoR)** para empezar una historia: tiene criterio de aceptación, los papers que la sustentan están leídos (con figuras) y existen los datos de ejemplo necesarios.

**Definición de terminado (DoD):**
- Código con pruebas que pasan (sección 23), `ruff` y `mypy` sin errores en dominio y motores.
- Las validaciones relevantes cubren los casos válidos e inválidos.
- Si toca mecanismos o exportación: **prueba física** registrada en `docs/pruebas_fisicas.md`.
- Nota del paper de origen o ADR actualizados (RNF-10).
- Ejemplo agregado o actualizado en `examples/`.

---

## 27. Riesgos

| ID | Riesgo | Prob. | Impacto | Mitigación | Señal de alerta |
|---|---|---|---|---|---|
| R-01 | `Gtk.GLArea` con ModernGL da problemas en el equipo del cliente | Media | Alto | Spike S0.1; alternativas B (WebKitGTK + three.js) y C (cairo 2D) | Menos de 30 fps o artefactos |
| R-02 | El mecanismo real de la casita no coincide con el modelado | Alta | Medio | Patrón plano del prototipo blanco; mecanismo definido por datos desde F1 (RF-34) y editor gráfico en F2 | La simulación no reproduce el video |
| R-03 | Los papers suponen espesor cero y la cartulina real no cierra plana | Alta | Medio | Espesores, holguras, calibración y prototipos (sección 18) | Piezas que rozan o sobresalen al cerrar |
| R-04 | El origámico como pieza sobre un BPP resulta geométricamente inválido | Media | Medio | Tratarlo como hipótesis; prototipo físico antes de comprometerlo | Falla `ψ(φ_diseño) = 90°` o hay choques |
| R-05 | Alcance "ultra completo" demasiado grande | Alta | Alto | Fases con criterio de aceptación; generadores como plugins | Una fase supera el doble de lo estimado |
| R-06 | Papers leídos solo por resumen (Le, Liu, Li 2011, etc.) | Media | Medio | Leerlos completos antes de su fase; notas en `docs/papers/` | Dudas de implementación por falta de figuras |
| R-07 | Python lento en voxelización, RANSAC o crecimiento de regiones | Media | Medio | NumPy vectorizado, `numba`, N bajo en vista previa | Tiempos por encima del presupuesto |
| R-08 | Singularidades del solver en estados planos | Media | Alto | Continuación de poses, oráculos de fórmula cerrada, PBD | Saltos de rama o poses que se invierten |
| R-09 | Marcas de pliegue sobre sticker poco claras | Media | Bajo | Opciones de 17.3 y prueba física | El cliente no encuentra los pliegues |
| R-10 | Doble cara y contorno espejado confunden | Media | Medio | Etiquetas claras y vista previa de ambos lados | Errores al pegar dorso con dorso |
| R-11 | Propiedad intelectual (patentes sobre popups desde 3D) | Baja | Medio, si se distribuye | Uso personal; revisión antes de publicar | Intención de distribuir la app |
| R-12 | Instalación de dependencias pesadas (OpenCV, Flatpak) | Media | Bajo | OpenCV sin interfaz o scikit-image; entorno documentado | Falla la instalación en limpio |
| R-13 | Privacidad de las fotos familiares | Baja | Alto | App local sin red | Cualquier conexión saliente |

---

## 28. Decisiones por defecto y preguntas abiertas

Para no bloquear el trabajo, cada pregunta abierta tiene un **supuesto por defecto**. Si el cliente responde otra cosa, se ajusta el plan.

| # | Pregunta | Supuesto por defecto | Qué cambia si la respuesta es otra |
|---|---|---|---|
| 1 | ¿Las páginas se abren a **180°** o a **90°**? | **Resuelta [Cliente]:** su único popup se abre completamente (180°) y está abierto a otras opciones. Se usa 180° por defecto y 90° queda disponible | — |
| 2 | ¿Cómo se pliega la casita y dónde van los pegados? | **Casi resuelta** con el diagrama y el tutorial (11.5): dos V-fold enfrentados a 45° más un paralelogramo interior. Faltan alturas, orientación y unión de la fachada | Parámetros de US-304, US-305 y US-307 |
| 3 | ¿Un proyecto es **una página** o un libro? | Una página por proyecto en la versión 1 | RF-05 se adelanta desde la Fase 5 |
| 4 | ¿Cómo prefiere marcar los pliegues sobre el sticker? | Muescas en los extremos (17.3) | Opciones de exportación |
| 5 | ¿PDFs separados o un único PDF multipágina? | Separados (17.1) | Empaquetado de exportación |
| 6 | ¿Qué tamaño de hoja usa con más frecuencia? | A3, configurable | Reparto en hojas |
| 7 | ¿Qué espesor tienen su cartulina y su sticker? | A medir con calibre | Holguras y compensaciones (12.4) |
| 8 | ¿Orden de F3 (Li 2010) y 4a (Ruiz 2014)? | **Decidida por defecto:** Li primero, con el mapeo de Ruiz ya en F2 (sección 25) | Si el cliente prefiere Ruiz primero, se intercambian F3 y 4a |
| 9 | ¿Tiene los PDFs de los papers? | No se asume | Hacen falta las figuras para implementar mecanismos (F1) y generadores (F3, F4) |
| 10 | ¿Qué otros mecanismos vio en YouTube que quiera en el catálogo? | El catálogo de 11.1 | Backlog de la Fase 2 |
| 11 | "La hoja mide X por Y": ¿es el pliego completo abierto o cada mitad? | Pliego completo, con el pliegue en el centro | Dimensiones y reparto en hojas |
| 12 | ¿Las líneas del diagrama son de pegado o cortes y pliegues de la propia hoja? | **Resuelta [Cliente]:** son las líneas donde pega las solapas de cada pieza | — |
| 13 | ¿Cuál de las dos V es la del frente y qué altura tienen las paredes? | Rojo es la más cercana al espectador; alturas a medir | Cierre de la casita (V-01) |
| 14 | ¿Cómo se pega la película transparente (por detrás o por delante de la fachada) y cuánto solape se deja alrededor de cada ventana? | Por detrás, con solape inicial a calibrar | Parámetros de 14.4 y V-11 |

## 29. Próximos pasos inmediatos

1. **El cliente** reúne los datos de la Fase 0: tres PNG, un STL simple, la foto del interior de la casita (o su patrón), los espesores y, si los tiene, los PDFs de los papers.
2. **El cliente** aporta las medidas reales de la hoja y de la casita y la altura de las paredes (pregunta 13), indica cómo pega la película transparente (pregunta 14) y responde la pregunta 3 (una página o un libro).
3. **Se ejecutan los spikes S0.1 a S0.6** y se cierran los ADR-01, ADR-02 y ADR-06.
4. **Se arranca la Fase 1** con la rebanada vertical (capa plana + step-fold, de proxy a PDF armado).

## 30. Métricas de éxito

| Métrica | Objetivo |
|---|---|
| Tiempo para diseñar la página del ejemplo (sin texturas) | 20 minutos o menos |
| Popup armado que cierra plano, con los PDFs generados | Sí, en el primer intento de la Fase 1 |
| Cambiar una medida y reexportar | 2 minutos o menos |
| Concordancia de las poses simuladas con las fórmulas cerradas | 0,1 mm o menos |
| Exactitud de escala de impresión | 0,5 mm o menos en 100 mm |
| Autonomía | El cliente arma un segundo popup distinto del ejemplo sin ayuda |

---

## 31. Referencias

Se indica entre corchetes si se leyó el texto completo. Los demás se conocen por su resumen o porque los citan los trabajos leídos.

**Leídos completos**
- Birmingham, D. Primer tutorial de una serie sobre diseño de popups (video de YouTube): https://www.youtube.com/watch?v=aGJZbNh9Phs. Solo se leyó la transcripción que aportó el cliente (no pude abrir la página del video). El autor remite a su libro *Pop-up Design and Paper Mechanics*, no consultado.
- Li, X.-Y., Shen, C.-H., Huang, S.-S., Ju, T., Hu, S.-M. *Popup: Automatic Paper Architectures from 3D Models.* ACM Transactions on Graphics 29(4), art. 111, 2010. DOI 10.1145/1778765.1778848. PDF: https://www.cs.wustl.edu/~taoju/research/popup_final.pdf. Página del proyecto: https://cg.cs.tsinghua.edu.cn/people/~xianying/Papers/Popup/index.html
- Iizuka, S., Endo, Y., Mitani, J., Kanamori, Y., Fukui, Y. *An interactive design system for pop-up cards with a physical simulation.* The Visual Computer 27, 605–612, 2011. DOI 10.1007/s00371-011-0564-0. https://www.cgg.cs.tsukuba.ac.jp/projects/2011/popupcard/paper/fulltext.pdf
- Ruiz Jr., C. R., Le, S. N., Yu, J., Low, K.-L. *Multi-style Paper Pop-up Designs from 3D Models.* Computer Graphics Forum 33(2), 2014. DOI 10.1111/cgf.12320. https://www.comp.nus.edu.sg/~lowkl/publications/multistyle_popup_eg2014.pdf

**Solo resumen o póster**
- Le, S. N., Leow, S.-J., Le-Nguyen, T.-V., Ruiz, C., Low, K.-L. *Surface and contour-preserving origamic architecture paper pop-ups.* IEEE TVCG 20(2), 276–288, 2014. DOI 10.1109/TVCG.2013.108. https://www.comp.nus.edu.sg/~lowkl/publications/oa_tvcg2013_lowres.pdf
- Liu, C., Yang, Y.-L., Lee, Y.-H., Chu, H.-K. *Image-based Paper Pop-up Design.* Póster, SIGGRAPH 2014. https://history.siggraph.org/wp-content/uploads/2022/12/2014-Poster-55-Liu_Image-based-Paper-Pop-up-Design.pdf
- Ruiz Jr., C. R., Le, S. N., Low, K.-L. *Generating Multi-style Paper Pop-up Designs using 3D Primitive Fitting.* SIGGRAPH Asia 2013 Technical Briefs. DOI 10.1145/2542355.2542360. https://www.comp.nus.edu.sg/~lowkl/publications/multistyle_popup_sa2013.pdf
- Le-Nguyen, T.-V., Low, K.-L., Ruiz Jr., C., Le, S. N. *Automatic Paper Sliceform Design from 3D Solid Models.* IEEE TVCG, 2013. Listado en https://www.comp.nus.edu.sg/~lowkl/

**Solo referencia (citados por los anteriores)**
- Li, X.-Y., Ju, T., Gu, Y., Hu, S.-M. *A geometric study of v-style pop-ups: theories and algorithms.* ACM SIGGRAPH 2011, 98:1–98:10.
- Glassner, A. *Interactive pop-up card design, part 1 y part 2.* IEEE Computer Graphics and Applications 22(1) 79–86 y 22(2) 74–85, 2002.
- Okamura, S., Igarashi, T. *An interface for assisting the design and production of pop-up card.* Smart Graphics 2009, 68–78.
- Hara, T., Sugihara, K. *Computer-aided design of pop-up books with two-dimensional v-fold structures.* 7th Japan Conf. on Computational Geometry and Graphs, 2009.
- Lee, Y. T., Tor, S. B., Soo, E. L. *Mathematical modelling and simulation of pop-up books.* Computers & Graphics 20(1), 21–31, 1996.
- Hendrix, S. L., Eisenberg, M. A. *Computer-assisted pop-up design for children: computationally enriched paper engineering.* Advanced Technology for Learning 3(2), 119–127, 2006.
- Mitani, J., Suzuki, H. *Computer aided design for origamic architecture models with polygonal representation.* Computer Graphics International 2004, 93–99.
- Mitani, J., Suzuki, H., Uno, H. *Computer aided design for origamic architecture models with voxel data structure.* Trans. IPSJ 44(5), 1372–1379, 2003.
- Mitani, J., Suzuki, H. *Computer aided design for 180-degree flat fold origamic architecture with lattice-type cross sections.* J. Graphic Science of Japan 37, 2003.
- Furuta, Y., Kimoto, H., Mitani, J., Fukui, Y. *Computer model and mouse interface for interactive virtual origami operation.* IPSJ Journal 48(12), 3658–3669, 2007.
- Hoiem, D., Efros, A. A., Hebert, M. *Automatic photo pop-up.* ACM SIGGRAPH 2005, 577–584.
- Abel, Z., Demaine, E. D., Demaine, M. L., et al. *Universality results for pop-up cards.* Preprint, 2012.
- Uehara, R., Teramoto, S. *The complexity of a pop-up book.* 18th Canadian Conference on Computational Geometry, 2006.
- Agrawala, M., Phan, D., Heiser, J., et al. *Designing effective step-by-step assembly instructions.* ACM TOG 22(3), 828–837, 2003.
- Chatani, M. y colaboradores. Libros sobre arquitectura origámica (décadas de 1980 en adelante), citados en Li et al. 2010 y Liu et al. 2014.
- *Elements of Pop Up: A Pop Up Book for Aspiring Paper Engineers* (citado por Iizuka et al.).

**Tecnología y otros**
- Documentación de `GtkGLArea` (GTK 4): https://docs.gtk.org/gtk4/class.GLArea.html
- Conversación de la comunidad sobre ModernGL con GTK 4: https://discourse.gnome.org/t/moderngl-python-with-gtk4/18826 (reporte de usuarios, no documentación oficial; se valida en S0.1).
- *popupCAD* (laminados para robótica, no para libros): https://asu.elsevierpure.com/en/publications/an-analytic-framework-for-developing-inherently-manufacturable-po
- Patente sobre popups desde modelos 3D, citada solo como aviso (no analizada): https://patents.google.com/patent/US10453255

---

## Apéndice A. Ejemplo de `project.json` (esquema, ADR-05)

JSON con comentarios para explicar (el archivo real no lleva comentarios):

```jsonc
{
  "format_version": 1,
  "units": "mm",
  "settings": {
    "design_angle": 180,              // 90 | 180
    "tolerance_mm": 0.2,              // V-07
    "thickness_mm": { "cardstock": null, "sticker": null, "glue": null }  // a medir
  },
  "page": {
    "sheet_mm": [420, 297],
    "central_fold": { "orientation": "short_side", "position_mm": 210 },
    "halves": {
      "ground":   { "texture": "assets/base_ground.png" },
      "backdrop": { "texture": "assets/base_backdrop.png" }
    }
  },
  "base_pairs": [
    { "id": "bpp0", "patches": ["ground", "backdrop"], "local_angle": "phi" }
  ],
  "elements": [
    {
      "id": "casita",
      "proxy": { "type": "prism", "size_mm": [60, 45, 40] },
      "placement": { "bpp": "bpp0", "along_fold_mm": 150 },
      "mechanism": { "type": "box_fold", "params": { } }
    },
    {
      "id": "auto",
      "proxy": { "type": "rect", "size_mm": [80, 35] },
      "placement": { "bpp": "bpp0", "along_fold_mm": 60 },
      "mechanism": { "type": "cylinder", "params": { "segments": 14 } }
    }
  ],
  "textures": [
    { "face": "auto/outer", "side": "A", "png": "assets/auto.png",
      "transform": { "scale": 1.0, "offset_mm": [0, 0], "rotation_deg": 0 },
      "cut_margin_mm": 0.5 }
  ],
  "variants": [],
  "export": { "sheet": "A3", "fold_marks": "edge_ticks", "symbols": true }
}
```

Los valores son ilustrativos. Cada mecanismo define su propio esquema de `params` (por ejemplo, para el step-fold: `h`, `g` y el largo a lo largo del pliegue).

## Apéndice B. Sección transversal del step-fold (derivación propia)

**Estado: derivación a partir de la definición de step-fold (dos pares de parches paralelos); se verifica en el spike S0.2 y con el prototipo S0.6.**

Se trabaja en el plano y–z (perpendicular al pliegue central; x sale del plano).

- Ground (mitad fija) a lo largo de +y; backdrop a lo largo de **u(φ) = (cos φ, sin φ)**.
- Puntos de fijación: **A = h·u(φ)** sobre el backdrop (a distancia h del pliegue) y **G = (g, 0)** sobre el ground (a distancia g).
- El paralelogramo S–A–M–G, con S en el pliegue central, da **M = A + G**. El parche AM queda paralelo al ground y el parche MG paralelo al backdrop a cualquier φ.
- Longitudes: SA = h, AM = g, MG = h, GS = g. Los lados opuestos son iguales, por lo que **a + b = c + d** (condición de plegabilidad V-03).
- Se elige la rama de movimiento por **continuidad desde φ = 90°**.

Con h = g = 40 mm:

| φ | A (y, z) | M (y, z) | Observación |
|---|---|---|---|
| 0° | (40,00 ; 0) | (80,00 ; 0) | Cerrada: la pieza llega a 80 mm del pliegue |
| 45° | (28,28 ; 28,28) | (68,28 ; 28,28) | |
| 90° | (0 ; 40,00) | (40,00 ; 40,00) | Escalón completo: tabla horizontal a z = 40 y contrahuella vertical en y = 40 |
| 135° | (−28,28 ; 28,28) | (11,72 ; 28,28) | |
| 180° | (−40,00 ; 0) | (0 ; 0) | Abierta plana: la pieza queda aplastada sobre la página |

**Consecuencia para V-01 (cierra plano dentro de la hoja):** a φ = 0° la pieza se extiende **h + g** desde el pliegue; la mitad de la página, medida perpendicular al pliegue, debe ser mayor que h + g más el espesor y un margen.

Estos valores son el **oráculo** de las pruebas unitarias del step-fold (sección 23).

## Apéndice C. Checklist de prototipo físico

1. Imprimir `00_calibracion.pdf` al 100 % y medir el cuadrado de 100 mm. Anotar la diferencia.
2. Medir con calibre cartulina sola y cartulina con sticker; cargar los valores en el proyecto.
3. Imprimir en papel común el patrón de un mecanismo (empezar con step-fold); cortar, marcar pliegues y pegar según los números.
4. Probar **10 aperturas y cierres**: ¿cierra plano? ¿sobresale del borde? ¿roza otra pieza? ¿se mantiene quieto a 45°, 90° y 135°?
5. Anotar holguras donde roza y comparar con las que predijo la simulación.
6. Repetir con cartulina y sticker reales.
7. Registrar fecha, material, ajustes y resultado en `docs/pruebas_fisicas.md`.

## Apéndice D. Diagrama del cliente como mecanismo definido por datos (borrador)

**Estado:** borrador. Las líneas son de pegado (pregunta 12, resuelta por el cliente); faltan la pregunta 13 y las medidas reales (sección 28). Las coordenadas son las medidas sobre el diagrama, en píxeles, con origen en la esquina superior izquierda de la hoja. La escala real y las alturas faltan (`null`). Sirve como primer caso de prueba del mecanismo por datos (RF-34, US-307) y como oráculo del plano de pegado (criterio 6 de la Fase 1).

```jsonc
{
  "format_version": 1,
  "name": "casita (diagrama del cliente, borrador)",
  "units": "px_del_diagrama",
  "scale_mm_per_px": null,                       // pendiente: medidas reales
  "page": { "size": [775, 447], "central_fold": { "orientation": "vertical", "x": 391 } },
  "pieces": [
    {
      "id": "v_rojo",                            // trazo rojo: frente y costado
      "mechanism": "v_fold", "variant": "angulo_recto",
      "apex": [389, 309],                        // sobre el pliegue central
      "glue_lines": [ [[389, 309], [252, 173]], [[389, 309], [531, 166]] ],
      "base_angle_deg": [45, 45], "piece_angle_deg": [90, 90],
      "height": null                             // pendiente
    },
    {
      "id": "v_negro",                           // trazo negro: fachada y pared de costado
      "mechanism": "v_fold", "variant": "angulo_recto",
      "apex": [393, 28],
      "glue_lines": [ [[393, 28], [252, 173]], [[393, 28], [531, 166]] ],
      "base_angle_deg": [45, 45], "piece_angle_deg": [90, 90],
      "height": null
    },
    {
      "id": "paralelogramo_azul",               // trazo azul: interior de la casa
      "mechanism": "parallel_fold", "variant": "paralelogramo",
      "glue_lines": [ [[252, 173], [393, 28]], [[216, 137], [362, -2]] ],
      "width": 49, "length": 202,
      "raised_by": "v_negro"                     // hipótesis: adosado al lado superior izquierdo
    }
  ],
  "checks_expected": {
    "balance_v_fold": "alfa + beta = 135 grados a ambos lados",
    "touches_page_edge": ["paralelogramo_azul"]  // la punta (362, -2) roza o sobrepasa el borde superior
  }
}
```
