# Brief — Flujo 020 Ingestion (Carga + capa bronze inalterable)

> **Tipo:** Brief de enmarque (alto nivel, previo al diseño agéntico). NO es la definición agéntica fina.
> **Proyecto:** FODA (Forecast Optimization Driven Agentic) — plano de **construcción** del motor.
> **Flujo:** `020` de 14 — `020_ingestion` (tercer flujo de la tubería; primer flujo que **toca capa de datos**; se ejecuta en cada carga histórica + recargas/incrementales).
> **Posición en la tubería:** consume `015_onboarding` (`map_client_data.json`) + `010_discovery` (`contract_data.json`, `client_register.yaml`) → entrega a `025_profiling`.
> **Capa de datos que toca:** `bronze` (la **crea**: copia cruda **inalterable** de la información del cliente).
> **Fuente de verdad:** `990_documents/expected_workflow.md` (§3 Ingestion) + `990_documents/expected_solution.md`.
> **Método de construcción:** `950_guideline/methodology.md` + `950_guideline/principles.md`.
> **Decisiones que lo enmarcan:** `D-001` (dos planos), `D-012` (golden client + snapshots), `D-014` (grain producto × geo), `D-015` (walking skeleton), `D-016` (brief + escalera), `D-017` (bandas + numeración) · **Estado:** `APROBADO` · **Fecha:** `2026-06-28` · **Aprobado por:** `usuario`.

---

## 0. Aclaración de planos — leer primero

Este brief describe un **componente del MOTOR FODA que estamos fabricando** (plano de *construcción*).
No describe la carga de una empresa concreta: describe la **maquinaria genérica y reutilizable** que, al
*operarse* sobre la carpeta de un cliente arbitrario, lee los contratos del cliente, obtiene la
información histórica por el medio declarado, la coteja contra lo registrado y la deposita en una **capa
bronze inalterable**. El diseño no debe acoplarse a un medio de acceso ni a un esquema de archivos fijo.

- **Insumo del flujo al operar:** `map_client_data.json` (de Onboarding), `contract_data.json` y
  `client_register.yaml` (de Discovery), más la **información histórica real** del cliente por el medio
  declarado (CSV, base de datos, API externa). Cambia por cliente.
- **Salida de runtime que produce al operar:** la **capa bronze** (copia cruda inalterable) y un
  **reporte de carga/consistencia**. Pertenecen al **plano instancia** (`fda-*`); **nunca** vuelven a la
  memoria de construcción del motor.
- **Grain del cliente (`D-014`):** Ingestion **materializa** el grain como filas reales: aquí la
  cardinalidad de series (producto × geografía) deja de ser declaración y pasa a ser dato cargado. No
  agrega ni transforma: **preserva** las columnas de grain tal cual para que los flujos aguas abajo
  operen sobre ellas.

## 1. Objetivo

Cargar la información histórica del cliente en el sistema **sin alterarla**, validando que corresponde a
lo contratado, y depositarla en una **capa bronze inalterable** que sirve de fuente de verdad cruda para
toda la tubería. Ingestion **no perfila, no limpia ni transforma**: su valor es la **fidelidad** (lo
cargado es exactamente lo enviado) y la **trazabilidad** (queda registrado qué se cargó, desde qué medio y
si hubo inconsistencias contra lo registrado en Discovery).

> En una frase: transformar la **información histórica del cliente** (por el medio declarado en los
> contratos) en una **capa bronze inalterable** cotejada contra `client_register.yaml`, lista para
> Profiling.

## 2. Alcance — qué hace

**Modo Inicio (carga histórica):**

- **Lectura de los contratos:** lee `map_client_data.json` y `contract_data.json` para saber **qué
  archivos** espera, **cuántos**, y **por qué medio** obtener la información (CSV, base de datos, API
  externa).
- **Obtención de la información histórica:** accede a la fuente por el medio declarado y trae los datos
  crudos (sin modificarlos).
- **Cotejo de consistencia:** compara inmediatamente lo cargado contra lo registrado en
  `client_register.yaml` (número de archivos esperado, cobertura, rango temporal, campos del grain). **De
  existir inconsistencias, informa al científico de datos** para corrección (no continúa "a ciegas").
- **Depósito en bronze inalterable:** si la información es correcta, realiza una **copia** y la guarda en
  la **capa bronze**, que **Sabbia no puede alterar** (inmutable por diseño).
- **Handoff:** informa que la información está disponible para **Profiling** (determinar salud de datos) y
  los flujos posteriores de limpieza/transformación.

**Modo Recarga / incremental:**

- Reabre el flujo ante una nueva entrega de datos del cliente (más historia, nuevo período) y añade a
  bronze **sin alterar** lo ya cargado, versionando la carga y re-cotejando consistencia.

## 3. Alcance — qué NO hace (límites)

- **No** define qué archivos ni qué medios se usan, ni el grain → eso lo declaran/mapean los **flujos
  `010_discovery` y `015_onboarding`** (que Ingestion consume).
- **No** mide la salud de los datos, ni calcula pareto, ni indicador de calidad → eso es el **flujo
  `025_profiling`**.
- **No** limpia, imputa, deduplica ni corrige datos → eso es el **flujo `030_cleaning`** (capa silver).
  Bronze guarda el dato **crudo tal cual**, errores incluidos.
- **No** agrega ni deriva la demanda → eso es el **flujo `035_derivation`** (capa gold).
- **No** modifica bronze después de escrito (inmutabilidad); las correcciones de calidad ocurren aguas
  abajo sobre silver/gold, **nunca** sobre bronze.
- **No** diseña la **maquinaria agéntica fina** de este flujo (instancias A/B/C, workers, checkpoints,
  rúbrica del evaluador, contratos de herramientas) → eso es el **diseño del flujo `020_ingestion`**,
  paso siguiente a este brief.

## 4. Insumos disponibles

| ID | Insumo | Origen |
|----|--------|--------|
| I-1 | Definición del flujo Ingestion en la tubería FODA | `990_documents/expected_workflow.md` (§3) |
| I-2 | Arquitectura de capas bronze/silver/gold y visión de planos | `990_documents/expected_solution.md`, `CLAUDE.md §4` |
| I-3 | Metodología y principios de construcción (P*, E*, NC*, patrón A/B/C, modelo plano) | `950_guideline/methodology.md`, `950_guideline/principles.md` |
| I-4 | Memoria de construcción (estado, decisiones, lecciones) | `800_persistence/` (`D-001`, `D-012`, `D-014`, `D-017`) |
| I-5 | Briefs aprobados aguas arriba (forma de los contratos que consume) | `700_brief/010_discovery.md`, `700_brief/015_onboarding.md` |

> **Insumo en tiempo de operación (no de construcción):** los contratos del cliente y su **información
> histórica real** por el medio declarado. Llegan cuando el motor se *opera*, no ahora. (Para construir y
> probar el flujo se usará el **golden client C1** sintético; bronze de C1 se **congela como snapshot**
> reutilizable por los flujos aguas abajo — `D-012`/`T-014`.)

## 5. Artefactos esperados (salida del flujo al operar)

| Artefacto | Propósito |
|-----------|-----------|
| **Capa `bronze`** (copia cruda inalterable) | Fuente de verdad cruda de toda la tubería. La consumen `025_profiling` (salud) y `030_cleaning` (origen de la limpieza hacia silver). Inmutable. |
| **`ingestion_report.json`** (reporte de carga / consistencia) | Trazabilidad: qué archivos/medios se cargaron, conteos, rango temporal y el resultado del **cotejo contra `client_register.yaml`** (inconsistencias detectadas y su estado). Habilita el handoff a Profiling. |

> Los *paths* exactos, el formato de bronze, el esquema del reporte y la mecánica de cada artefacto se
> fijan en el **diseño del flujo** (paso siguiente).

## 6. Criterios de éxito (Done)

1. La **capa bronze** queda escrita con una copia **fiel y completa** de la información cargada (sin
   alteraciones respecto a la fuente).
2. **Inmutabilidad:** bronze es inalterable tras la escritura (ningún flujo posterior lo modifica).
3. El **cotejo de consistencia** contra `client_register.yaml` se ejecutó y su resultado quedó registrado
   (número de archivos esperado vs. cargado, cobertura, rango temporal, campos de grain).
4. **Gate humano (condicional):** si hay inconsistencias, **se informa al científico de datos** y el
   flujo **no habilita Profiling** hasta resolverlas o aprobarlas explícitamente (ver `CLAUDE.md §5`).
5. Las **columnas de grain** (producto × geografía) y la métrica de demanda se preservan tal cual,
   coherentes con `map_client_data.json`.
6. El handoff a `025_profiling` se emite solo cuando la carga es consistente (o las inconsistencias
   fueron aprobadas).
7. **Modo Recarga:** una nueva entrega se añade a bronze sin alterar lo previo, versionada y re-cotejada.

## 7. Riesgos / advertencias

- **Confusión de planos (`D-001`):** la capa bronze es **runtime de la instancia** (`fda-*`), no memoria
  de construcción del motor.
- **Alterar bronze (anti-patrón crítico):** cualquier limpieza/imputación en este flujo viola la
  inmutabilidad y destruye la fuente de verdad cruda. Toda corrección va en silver/gold aguas abajo.
- **Envenenar aguas abajo (E9):** cargar datos incompletos, del medio equivocado, o saltarse el cotejo de
  consistencia contamina Profiling→Reporting con basura. El cotejo contra `client_register.yaml` y el gate
  de inconsistencias son la mitigación.
- **Acoplamiento a un medio concreto:** hard-codear "siempre CSV" rompe la reutilización; el medio se
  toma del contrato (CSV / base de datos / API).
- **Fidelidad vs. conveniencia:** "corregir de una vez" un encoding o un separador raro es tentador pero
  prohibido en bronze (rompe la trazabilidad). Bronze guarda el crudo; la corrección se documenta en
  Cleaning.
- **Snapshot stale (al construir):** el bronze de C1 se congela como snapshot; si cambia el contrato de
  Onboarding/Discovery hay que regenerarlo (riesgo de fixture desactualizado — `D-012`).

## 8. La capa bronze inalterable + cotejo de consistencia (`D-001`/`D-012`) — sección específica del flujo

Ingestion es el **guardián de la fuente de verdad cruda**. Dos propiedades lo definen y deben tratarse
como de primera clase en el diseño:

- **Inmutabilidad de bronze:** una vez escrita, bronze **no se toca**. Es la base de la trazabilidad
  bronze→silver→gold: cualquier transformación posterior debe poder explicarse contra el crudo original.
  Esto habilita además los **snapshots cacheados** de `D-012` (bronze de C1 congelado y reutilizado por
  los flujos aguas abajo sin recomputar la carga).
- **Cotejo contra `client_register.yaml`:** el flujo **valida antes de confiar**. No basta con cargar:
  hay que verificar que lo cargado **coincide con lo que Discovery registró** (número de archivos,
  cobertura, rango, grain). Una divergencia es una señal temprana que se eleva al humano, no un error que
  se propaga en silencio (`E9`).

> *(Nota: la fuente §3c menciona "client_register.json"; el artefacto canónico es
> `client_register.yaml` —`CLAUDE.md §4`—. Se asume el YAML.)*

## 9. Escalera de capacidades (L0 → Ln) — vista vertical del flujo

> Vista vertical de la *ambición completa* de Ingestion (`D-016`). **L0 = lo mínimo** del walking
> skeleton (banda **Tracer Bullet**, `D-017`): cargar un único CSV de C1 a bronze, cotejo mínimo, handoff.
> Cada peldaño agrega capacidad.

| Nivel | Capacidad | Qué incluye | Qué difiere de la realidad |
|-------|-----------|-------------|----------------------------|
| **L0** (mínimo / skeleton) | **Carga de 1 CSV a bronze + handoff** | Lee un único archivo CSV según `map_client_data.json`, lo copia tal cual a la capa **bronze**, verifica mínimos (existe el archivo, trae las columnas de grain esperadas) y emite el handoff a Profiling. | Un solo archivo CSV; cotejo mínimo (no contra `client_register.yaml` completo); sin medios variados; sin recarga/incremental; inmutabilidad por convención. |
| **L1** | **Cotejo de consistencia + gate de inconsistencias** | Coteja la carga contra `client_register.yaml` (conteo de archivos, cobertura, rango temporal, grain); genera el **reporte de consistencia**; eleva inconsistencias al científico de datos y bloquea el handoff hasta resolución. | Aún un solo medio (CSV); carga completa (no incremental). |
| **L2** | **Medios de acceso múltiples + multi-archivo** | Obtiene la información del medio declarado (CSV / base de datos / API externa) y maneja el **número exacto** de archivos mapeado, ensamblando bronze a partir de varios orígenes. | Sin versionado/idempotencia formal; sin cargas incrementales. |
| **L3** | **Inmutabilidad fuerte + versionado + integridad** | Garantías de inmutabilidad (write-once), versionado de cargas, hashing/checksums de integridad, detección de duplicados de carga, cargas incrementales/append sin alterar lo previo. | Conectores aún básicos; sin reintentos/orquestación de fallos de fuente. |
| **Ln** (ambición completa) | **Ingestion "como un ingeniero de datos senior"** | Conectores robustos con reintentos y manejo de fallos de la fuente, validación de esquema completa contra el grain, snapshots bronze versionados ligados al contrato (`D-012`), auditoría completa de procedencia, recargas incrementales robustas. | Nada: es el objetivo final del flujo. |

> **Nota de ensamblaje:** al cerrar este brief se refleja el estado en `800_persistence/roadmap.md`
> (fila Ingestion: columna *Brief* → `planeado`; peldaño previsto para Tracer Bullet → **L0**).

## 10. Siguiente paso

Tras **aprobar este brief**: **diseñar el flujo `020_ingestion`** (instancias A/B/C según el modelo plano
`D-009`, workers, política de herramientas, checkpoints canónicos, durabilidad, rúbrica del evaluador y
contrato), reutilizando los patrones transversales ya validados del motor. El **plan de implementación**
viene *después* del diseño (orden del método: **brief → diseño → plan → construir**, `D-011`). El diseño
se materializará en `705_design/020_ingestion.md`.
