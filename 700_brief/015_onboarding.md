# Brief — Flujo 015 Onboarding (Mapeo de la estructura de datos del cliente)

> **Tipo:** Brief de enmarque (alto nivel, previo al diseño agéntico). NO es la definición agéntica fina.
> **Proyecto:** FODA (Forecast Optimization Driven Agentic) — plano de **construcción** del motor.
> **Flujo:** `015` de 14 — `015_onboarding` (segundo flujo de la tubería; se ejecuta una vez al inicio + en modo Ajuste cuando cambia el contrato de datos).
> **Posición en la tubería:** consume `010_discovery` (`contract_data.json` + `client_register.yaml`) → entrega a `Ingestion` (siguiente flujo).
> **Capa de datos que toca:** `—` (pre-ingestión: no produce bronze/silver/gold; produce la **especificación de mapeo** que rige la carga en bronze).
> **Fuente de verdad:** `990_documents/expected_workflow.md` (§2 Onboarding) + `990_documents/expected_solution.md`.
> **Método de construcción:** `950_guideline/methodology.md` + `950_guideline/principles.md`.
> **Decisiones que lo enmarcan:** `D-001` (dos planos), `D-014` (grain producto × geo), `D-015` (walking skeleton), `D-016` (brief + escalera) · **Estado:** `APROBADO` · **Fecha:** `2026-06-28` · **Aprobado por:** `usuario`.

---

## 0. Aclaración de planos — leer primero

Este brief describe un **componente del MOTOR FODA que estamos fabricando** (plano de *construcción*).
No describe el mapeo de una empresa concreta: describe la **maquinaria genérica y reutilizable** que, al
*operarse* sobre la carpeta de un cliente arbitrario, traduce el **contrato de datos** de Discovery en una
**especificación de mapeo** (`map_client_data.json`) que dice exactamente qué archivos espera el sistema
y cómo se corresponden con la estructura interna (grain producto × geografía). El diseño no debe acoplarse
a un dominio de negocio concreto ni asumir un esquema de archivos fijo.

- **Insumo del flujo al operar:** `contract_data.json` y `client_register.yaml` producidos por
  `010_discovery` en la carpeta del cliente. Cambian por cliente.
- **Salida de runtime que produce al operar:** `map_client_data.json` (especificación de mapeo).
  Pertenece al **plano instancia** (`fda-*`); **nunca** vuelve a la memoria de construcción del motor.
- **Grain del cliente (`D-014`):** Onboarding es donde el grain **declarado** en Discovery se **mapea** a
  la representación interna del sistema: jerarquía de producto (familia→categoría→subcategoría→clase) y de
  geografía (región→país→ciudad→sede). Es el flujo que materializa el grain como estructura operable.

## 1. Objetivo

Transformar el **contrato de datos** acordado en Discovery en una **especificación de mapeo accionable**:
qué número exacto de archivos enviará el cliente, qué columnas/campos trae cada uno, y cómo se
corresponden con la estructura interna del sistema FODA (dimensiones de producto y geografía, métrica de
demanda, periodicidad). Onboarding **no carga datos** ni crea la capa bronze: produce el "molde" contra el
cual Ingestion validará y cargará la información histórica, evitando que el cliente envíe información
incompleta o sobrante.

> En una frase: transformar `contract_data.json` (+ `client_register.yaml`) en un `map_client_data.json`
> que mapea la estructura de datos del cliente a la representación interna del motor, validado y aprobado
> por el científico de datos.

## 2. Alcance — qué hace

**Modo Inicio (mapeo, una vez al arranque del proyecto cliente):**

- **Lectura del contrato:** lee `contract_data.json` (y `client_register.yaml`) para conocer qué archivos
  declaró el cliente, sus medios de acceso y el grain/periodicidad acordados.
- **Mapeo del número exacto de archivos:** si el contrato declara que el cliente enviará **X archivos** de
  información histórica, mapea **ese número exacto**, de modo que el cliente sepa con precisión qué debe
  enviar (ni incompleto ni adicional).
- **Definición de los parámetros de producto:** establece la jerarquía **familia → categoría →
  subcategoría → clase** del cliente y su correspondencia con los campos de los archivos.
- **Definición de la geografía de centros de distribución:** establece la jerarquía **región → país →
  ciudad → sede** (sucursal/oficina/centro de despacho) y su correspondencia con los campos.
- **Construcción del `map_client_data.json`:** ensambla todo lo necesario para mapear la estructura de
  datos del cliente en el sistema (archivos esperados, campos por archivo, dimensiones de producto y
  geografía, métrica de demanda y periodicidad), consistente con el contrato.
- **Validación y firma humana:** presenta el mapeo; el **científico de datos** revisa la correspondencia
  con el contrato, corrige y **aprueba explícitamente** antes de habilitar Ingestion.

**Modo Ajuste (re-mapeo cuando cambia el contrato):**

- Reabre el flujo cuando Discovery muta el `contract_data.json` (nuevos archivos, nueva geografía, nuevo
  nivel de producto) y actualiza `map_client_data.json` **sin destruir** el mapeo aprobado, re-firmando.

## 3. Alcance — qué NO hace (límites)

- **No** define el problema de negocio, las hipótesis ni el contrato de datos → eso es el **flujo
  `010_discovery`** (que Onboarding consume).
- **No** carga, copia ni versiona datos del cliente, ni crea la capa **bronze**, ni coteja la carga real
  contra `client_register.yaml` → eso es el **flujo Ingestion** (que consume `map_client_data.json`).
- **No** mide la salud de los datos ni calcula pareto → eso es el **flujo Profiling**.
- **No** limpia, deriva ni agrega la demanda → eso es de los flujos Cleaning/Derivation aguas abajo.
- **No** diseña la **maquinaria agéntica fina** de este flujo (instancias A/B/C, workers, checkpoints,
  rúbrica del evaluador, contratos de herramientas) → eso es el **diseño del flujo `015_onboarding`**,
  paso siguiente a este brief.

## 4. Insumos disponibles

| ID | Insumo | Origen |
|----|--------|--------|
| I-1 | Definición del flujo Onboarding en la tubería FODA | `990_documents/expected_workflow.md` (§2) |
| I-2 | Visión de solución y dos planos motor/instancia | `990_documents/expected_solution.md` |
| I-3 | Metodología y principios de construcción (P*, E*, NC*, patrón A/B/C, modelo plano) | `950_guideline/methodology.md`, `950_guideline/principles.md` |
| I-4 | Memoria de construcción (estado, decisiones, lecciones) | `800_persistence/` (`D-001`, `D-014`, `D-015`, `D-016`) |
| I-5 | Brief aprobado del flujo anterior (forma de `contract_data.json`/`client_register.yaml`) | `700_brief/010_discovery.md` |

> **Insumo en tiempo de operación (no de construcción):** `contract_data.json` y `client_register.yaml`
> del cliente concreto. Llegan cuando el motor se *opera*, no ahora. (Para construir y probar el flujo se
> usará el **golden client C1** sintético — ver `D-012`/`D-014` y `T-014`.)

## 5. Artefactos esperados (salida del flujo al operar)

| Artefacto | Propósito |
|-----------|-----------|
| **`map_client_data.json`** | Especificación de mapeo: número exacto de archivos esperados, campos por archivo, jerarquía de producto (familia→clase) y de geografía (región→sede), métrica de demanda y periodicidad. Lo consume **Ingestion** para validar y cargar la información histórica en bronze. |

> Los *paths* exactos, el esquema preciso del `map_client_data.json` y la mecánica se fijan en el
> **diseño del flujo** (paso siguiente).

## 6. Criterios de éxito (Done)

1. Existe un `map_client_data.json` bien formado y **consistente con `contract_data.json`** (lo mapeado
   coincide con lo contratado).
2. El **número de archivos** mapeado es **exactamente** el declarado en el contrato (ni de más ni de
   menos), de modo que el cliente sepa qué enviar.
3. La jerarquía de **producto** (familia → categoría → subcategoría → clase) queda definida y mapeada a
   campos concretos de los archivos.
4. La jerarquía de **geografía** (región → país → ciudad → sede) queda definida y mapeada a campos
   concretos.
5. Quedan mapeadas la **métrica de demanda** y la **periodicidad**, coherentes con el contrato.
6. **Gate humano (obligatorio):** el **científico de datos aprueba explícitamente** el mapeo antes de
   habilitar Ingestion (ver `CLAUDE.md §5`).
7. **Modo Ajuste:** un cambio del contrato queda reflejado en `map_client_data.json` sin borrar lo
   aprobado y con nueva firma.

## 7. Riesgos / advertencias

- **Confusión de planos (`D-001`):** Onboarding mapea *los datos del cliente*, no la maquinaria del motor.
  El `map_client_data.json` es **runtime de la instancia** (`fda-*`), no memoria de construcción.
- **Acoplamiento a un dominio concreto:** asumir un esquema de archivos fijo o una jerarquía rígida
  envenena la reutilización. El mapeo debe inferirse del contrato, no hard-codearse.
- **Envenenar aguas abajo (E9):** un mapeo erróneo (archivos mal contados, dimensión mal asociada,
  periodicidad equivocada) hace que Ingestion cargue mal y contamina toda la tubería. La consistencia
  contrato⇄mapeo y el gate humano son la mitigación.
- **Desalineación con el contrato:** divergencias entre `contract_data.json` y `map_client_data.json`
  (p. ej. el contrato declara 5 archivos y el mapeo asume 4). Validar correspondencia exacta.
- **Grain incompleto:** mapear solo niveles superiores (familia/región) y omitir los finos (clase/sede)
  rompe la cardinalidad de series esperada por Modelling (`D-014`).
- **Fixture stale (al construir):** el `contract_data.json` de C1 debe mantenerse consistente con el
  esquema; un C1 desactualizado da falsos verdes (`D-012`, `T-014`).

## 8. El grain se mapea aquí (`D-014`) — sección específica del flujo

Si Discovery **declara** el grain, Onboarding lo **materializa** como estructura operable. Es el punto
donde las jerarquías pasan de "texto en un contrato" a "campos mapeados que Ingestion sabrá leer":

- **Producto:** familia → categoría → subcategoría → clase, cada nivel asociado a un campo de los archivos.
- **Geografía:** región → país → ciudad → sede, cada nivel asociado a un campo de los archivos.
- **Métrica + periodicidad:** qué campo es la demanda y a qué periodicidad se agregará (rige Derivation).

El producto cartesiano **producto × geografía** define la **cardinalidad de series** que el resto del
motor manejará (matriz de complejidad 2×2 de `D-014`). Un mapeo incompleto aquí se propaga como error
sistemático. El diseño del flujo debe tratar el grain como **dato de primera clase del mapeo**.

## 9. Escalera de capacidades (L0 → Ln) — vista vertical del flujo

> Vista vertical de la *ambición completa* de Onboarding (`D-016`). **L0 = lo mínimo** del walking
> skeleton (Tracer Bullet, `D-015`): mapeo de un único archivo plano con columnas básicas, a partir del
> `contract_data.json` de C1. Cada peldaño agrega capacidad.

| Nivel | Capacidad | Qué incluye | Qué difiere de la realidad |
|-------|-----------|-------------|----------------------------|
| **L0** (mínimo / skeleton) | **Mapeo mínimo de 1 archivo a grain básico** | A partir del `contract_data.json` de C1, produce un `map_client_data.json` que mapea **un único archivo** con columnas básicas (1 nivel de producto, 1 nivel de geografía, demanda, fecha) y la periodicidad. Gate humano simple. | Un solo archivo; jerarquías de 1 nivel; sin validación de número de archivos; sin medios de acceso variados; sin modo Ajuste. |
| **L1** | **Conteo exacto de archivos + jerarquía de producto completa** | Mapea el número exacto de archivos declarado; jerarquía de producto familia→categoría→subcategoría→clase asociada a campos. | Geografía aún básica; un solo medio de acceso (CSV); sin reconciliación fina. |
| **L2** | **Jerarquía de geografía completa + medios de acceso múltiples** | Geografía región→país→ciudad→sede mapeada; soporte declarativo a CSV / base de datos / API según el contrato. | Sin detección automática de discrepancias contrato⇄mapeo; nombres de columna asumidos exactos. |
| **L3** | **Validación y normalización del mapeo** | Detecta discrepancias contra el contrato (archivos faltantes/sobrantes, dimensiones sin mapear); normaliza/alias de nombres de columna heterogéneos; maneja archivos con esquemas distintos. | Aún requiere confirmación humana frecuente; inferencia de esquema asistida, no autónoma. |
| **Ln** (ambición completa) | **Onboarding "como un científico de datos senior"** | Inferencia robusta de esquema, emparejamiento difuso de columnas con confirmación, reconciliación de múltiples archivos heterogéneos, **modo Ajuste** robusto ante cambios de grain o de archivos. | Nada: es el objetivo final del flujo. |

> **Nota de ensamblaje:** al cerrar este brief se refleja el estado en `800_persistence/roadmap.md`
> (fila Onboarding: columna *Brief* → `planeado`; peldaño previsto para Tracer Bullet → **L0**).

## 10. Siguiente paso

Tras **aprobar este brief**: **diseñar el flujo `015_onboarding`** (instancias A/B/C según el modelo plano
`D-009`, workers, política de herramientas, checkpoints canónicos, durabilidad, rúbrica del evaluador y
contrato), reutilizando los patrones transversales ya validados del motor. El **plan de implementación**
viene *después* del diseño (orden del método: **brief → diseño → plan → construir**, `D-011`). El diseño
se materializará en `705_design/015_onboarding.md`.
