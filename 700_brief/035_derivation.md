# Brief — Flujo 035 Derivation (Demanda agregada → capa gold)

> **Tipo:** Brief de enmarque (alto nivel, previo al diseño agéntico). NO es la definición agéntica fina.
> **Proyecto:** FODA (Forecast Optimization Driven Agentic) — plano de **construcción** del motor.
> **Flujo:** `035` de 14 — `035_derivation` (sexto flujo de la tubería; forma la **serie de tiempo objetivo** en la capa gold).
> **Posición en la tubería:** consume `030_cleaning` (capa **silver** + `data_cleaning.json`) + `contract_data.json` (periodicidad) → entrega a `040_exploration`.
> **Capa de datos que toca:** `silver` (lectura) → **escribe** `gold` (demanda histórica agregada).
> **Fuente de verdad:** `990_documents/expected_workflow.md` (§6 Derivation) + `990_documents/expected_solution.md`.
> **Método de construcción:** `950_guideline/methodology.md` + `950_guideline/principles.md`.
> **Decisiones que lo enmarcan:** `D-001` (dos planos), `D-012` (snapshots), `D-014` (grain producto × geo), `D-015` (walking skeleton), `D-016` (brief + escalera), `D-017` (bandas + numeración) · **Estado:** `APROBADO` · **Fecha:** `2026-06-28` · **Aprobado por:** `usuario`.

---

## 0. Aclaración de planos — leer primero

Este brief describe un **componente del MOTOR FODA que estamos fabricando** (plano de *construcción*).
No describe la derivación de una empresa concreta: describe la **maquinaria genérica y reutilizable** que,
al *operarse* sobre la capa silver de un cliente arbitrario, agrega la demanda a la **periodicidad
contratada** y produce una capa **gold** con la **serie de tiempo de demanda** lista para ML. El diseño no
debe acoplarse a un dominio ni asumir una periodicidad fija: la periodicidad es **dato del contrato**.

- **Insumo del flujo al operar:** la capa **silver** (datos limpios), el **`contract_data.json`** (la
  periodicidad de agregación) y el grain de `map_client_data.json`. Cambia por cliente.
- **Salida de runtime que produce al operar:** la capa **gold** (demanda histórica agregada por producto
  × sede × período) y el **`data_derivation.json`** (bitácora de derivación, replicable). Pertenecen al
  **plano instancia** (`fda-*`); **nunca** vuelven a la memoria de construcción del motor.
- **Grain del cliente (`D-014`):** Derivation es donde el **grain se cruza con el tiempo**: cada par
  **producto × geografía** agregado a la periodicidad contratada es **una serie de tiempo**. Aquí queda
  fijada la **cardinalidad de series** que Modelling deberá pronosticar.

## 1. Objetivo

Transformar la capa **silver** (registros limpios, granulares) en la capa **gold**: la **demanda
histórica agregada** de cada producto en cada sede, a la **periodicidad** definida en el contrato
(semanal, quincenal, mensual, bimestral, trimestral, semestral o anual). Derivation **construye la
variable objetivo** del forecasting — la **demanda** (no las ventas) — como serie de tiempo, y documenta
la agregación para que sea reproducible. Es el flujo que convierte "datos limpios" en "series listas para
explorar y modelar".

> En una frase: transformar **silver** en una capa **gold** de demanda agregada (producto × sede ×
> período, a la periodicidad del contrato), documentada en `data_derivation.json` para Exploration.

## 2. Alcance — qué hace

**Modo Inicio (derivación de la demanda):**

- **Lectura de la periodicidad:** toma de `contract_data.json` la **periodicidad** de agregación acordada
  (semanal…anual).
- **Agregación de la demanda:** sobre la capa silver, calcula la **demanda histórica agregada** por
  **producto × sede × período**, formando las series de tiempo.
- **Escritura de gold:** deposita la demanda agregada en la capa **gold**, lista para Exploration,
  Featuring y Modelling.
- **Bitácora de derivación:** registra las transformaciones de agregación en **`data_derivation.json`**
  (qué se agregó, a qué periodicidad, con qué regla): documenta y **permite replicar** la derivación en
  otros archivos del cliente.
- **Entrega descargable:** permite al científico de datos descargar `data_derivation.json` en CSV o Excel.

## 3. Alcance — qué NO hace (límites)

- **No** limpia, imputa ni deduplica → eso es el **flujo `030_cleaning`** (capa silver) que Derivation
  consume.
- **No** modifica **bronze** ni **silver** → los lee; gold es una capa nueva.
- **No** crea variables explicativas nuevas (día de semana, lags, clima…) → eso son los flujos
  `040_exploration` / `045_featuring`.
- **No** explora patrones ni valida hipótesis → eso es el **flujo `040_exploration`**.
- **No** entrena ni selecciona modelos → eso es el **flujo `050_modelling`**.
- **No** predice la demanda futura → eso es el **flujo `055_inferences`**; Derivation produce demanda
  **histórica** (observada), no pronosticada.
- **No** diseña la **maquinaria agéntica fina** de este flujo (instancias A/B/C, workers, checkpoints,
  rúbrica del evaluador, contratos de herramientas) → eso es el **diseño del flujo `035_derivation`**,
  paso siguiente a este brief.

## 4. Insumos disponibles

| ID | Insumo | Origen |
|----|--------|--------|
| I-1 | Definición del flujo Derivation en la tubería FODA | `990_documents/expected_workflow.md` (§6) |
| I-2 | Arquitectura de capas bronze/silver/gold y visión de planos | `990_documents/expected_solution.md`, `CLAUDE.md §4` |
| I-3 | Metodología y principios de construcción (P*, E*, NC*, patrón A/B/C, modelo plano) | `950_guideline/methodology.md`, `950_guideline/principles.md` |
| I-4 | Memoria de construcción (estado, decisiones, lecciones) | `800_persistence/` (`D-001`, `D-012`, `D-014`, `D-017`) |
| I-5 | Briefs aprobados aguas arriba (forma de silver y de la periodicidad del contrato) | `700_brief/030_cleaning.md`, `700_brief/010_discovery.md` |

> **Insumo en tiempo de operación (no de construcción):** la capa **silver real** y la **periodicidad**
> del `contract_data.json`. Llegan cuando el motor se *opera*, no ahora. (Para construir y probar el flujo
> se usa el **snapshot silver de C1** congelado por Cleaning — `D-012`/`T-014`.)

## 5. Artefactos esperados (salida del flujo al operar)

| Artefacto | Propósito |
|-----------|-----------|
| **Capa `gold`** (demanda histórica agregada) | Series de tiempo de demanda por producto × sede × período, a la periodicidad del contrato. La consumen `040_exploration`, `045_featuring` y `050_modelling`. |
| **`data_derivation.json`** (bitácora de derivación) | Documenta la agregación aplicada; habilita **reproducir** la derivación en otros archivos del cliente y auditar silver→gold. |
| **Exportable CSV/Excel** de `data_derivation.json` | Permite al científico de datos descargar y compartir el detalle de la derivación. |

> Los *paths*, el esquema exacto de `data_derivation.json` y la mecánica se fijan en el **diseño del
> flujo** (paso siguiente).

## 6. Criterios de éxito (Done)

1. La capa **gold** queda escrita con la **demanda agregada** por **producto × sede × período**, a la
   periodicidad declarada en `contract_data.json`.
2. La agregación es **correcta y reproducible** (misma silver + misma periodicidad → misma gold).
3. Cada transformación de agregación queda registrada en **`data_derivation.json`**, de forma que la
   derivación se pueda **replicar** sobre otros archivos del cliente.
4. El **grain** (producto × geografía) se respeta: cada par genera su serie; la cardinalidad coincide con
   lo mapeado (`D-014`).
5. `data_derivation.json` es **descargable en CSV o Excel**.
6. **Gate humano:** el científico de datos **revisa** la periodicidad y la lógica de agregación antes de
   habilitar Exploration (ver `CLAUDE.md §5`).

## 7. Riesgos / advertencias

- **Confusión de planos (`D-001`):** gold y `data_derivation.json` son **runtime de la instancia**
  (`fda-*`), no memoria de construcción.
- **Demanda ≠ ventas:** el motor predice **demanda**, no ventas (`CLAUDE.md §1`). Si la derivación toma
  ventas crudas sin ajustar (devoluciones, quiebres de stock, períodos sin oferta), la serie objetivo
  queda sesgada. Las reglas de derivación deben reflejar **demanda**.
- **Periodicidad equivocada (E9):** agregar a una periodicidad distinta de la contratada produce series
  inservibles para el resto de la tubería; tomar la periodicidad del contrato es obligatorio.
- **Períodos incompletos / huecos:** períodos parciales al inicio/fin o sin registros pueden falsear la
  serie; el tratamiento (excluir, marcar, cero-demanda) debe ser explícito y documentado.
- **Agregación que rompe el grain:** colapsar sedes o productos al agregar destruye la cardinalidad que
  Modelling necesita; agregar **en el tiempo**, no en el grain.
- **Snapshot stale (al construir):** gold de C1 depende del snapshot silver y de la periodicidad; si
  cambian, regenerar (`D-012`).

## 8. La demanda como serie de tiempo (grain × periodicidad) — sección específica del flujo

Derivation es el flujo que **fabrica la variable objetivo** del forecasting. Su diseño gira en torno a tres
ideas:

- **Serie = producto × geografía × período:** la agregación cruza el **grain** (`D-014`) con la
  **periodicidad** del contrato. El resultado es el conjunto de **series de tiempo** que Modelling
  pronosticará; su número es la **cardinalidad** que define la escala del problema (C1: 1 serie; C4: miles).
- **Agregar en el tiempo, preservar el grain:** la agregación reduce la resolución **temporal** (de
  transacciones a períodos), pero **no** colapsa producto ni geografía. Confundir ambas agregaciones es el
  error clásico que rompe aguas abajo.
- **Demanda, no ventas:** la regla de derivación define qué cuenta como demanda (con/sin devoluciones,
  ajustes por quiebres). Es una decisión de negocio que debe quedar **documentada** en
  `data_derivation.json` y, en niveles maduros, revisada por el humano.

## 9. Escalera de capacidades (L0 → Ln) — vista vertical del flujo

> Vista vertical de la *ambición completa* de Derivation (`D-016`). **L0 = lo mínimo** del walking
> skeleton (banda **Tracer Bullet**, `D-017`): agregar la silver de C1 a una sola periodicidad para una
> sola serie. Cada peldaño agrega capacidad.

| Nivel | Capacidad | Qué incluye | Qué difiere de la realidad |
|-------|-----------|-------------|----------------------------|
| **L0** (mínimo / skeleton) | **Agregación a 1 periodicidad para 1 serie → gold** | Sobre el snapshot silver de C1, agrega la demanda a una periodicidad fija (p. ej. mensual, por suma simple) para la única serie producto×sede; escribe **gold** y un `data_derivation.json` básico; handoff a Exploration. | Una sola periodicidad y serie; suma simple; sin tratamiento de huecos; sin exportación; sin ajuste demanda-vs-ventas. |
| **L1** | **Periodicidades del contrato + demanda por producto × sede** | Lee la periodicidad de `contract_data.json` (semanal…anual) y agrega la demanda por cada producto × sede; `data_derivation.json` completo. | Sin exportación; sin tratamiento explícito de períodos incompletos; multi-serie básico. |
| **L2** | **Multi-serie (grain producto × geo) + calendario + exportable** | Maneja la cardinalidad completa de series; tratamiento explícito de huecos/períodos incompletos y calendario; exportación a CSV/Excel. | Sin agregados por nivel jerárquico; sin reconciliación. |
| **L3** | **Agregados por nivel jerárquico (listos para reconciliación) + replay** | Demanda agregada también a niveles superiores (familia/categoría, región/país) consistente para reconciliación bottom-up/top-down; replay idempotente entre cargas. | Reglas demanda-vs-ventas aún simples; sin versionado avanzado. |
| **Ln** (ambición completa) | **Derivation "como un científico de datos senior"** | Derivación de demanda consciente de devoluciones/quiebres/ajustes, agregación consciente del calendario (festivos, semanas ISO), agregados jerárquicos coherentes para reconciliación, replay robusto y versionado ligado al contrato. | Nada: es el objetivo final del flujo. |

> **Nota de ensamblaje:** al cerrar este brief se refleja el estado en `800_persistence/roadmap.md`
> (fila Derivation: columna *Brief* → `planeado`; peldaño previsto para Tracer Bullet → **L0**).

## 10. Siguiente paso

Tras **aprobar este brief**: **diseñar el flujo `035_derivation`** (instancias A/B/C según el modelo plano
`D-009`, workers, política de herramientas, checkpoints canónicos, durabilidad, rúbrica del evaluador y
contrato), reutilizando los patrones transversales ya validados del motor. El **plan de implementación**
viene *después* del diseño (orden del método: **brief → diseño → plan → construir**, `D-011`). El diseño
se materializará en `705_design/035_derivation.md`.
