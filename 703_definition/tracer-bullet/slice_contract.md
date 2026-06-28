# Slice Contract — Tracer Bullet (walking skeleton)

> **Tipo:** Slice contract (definición de banda — nivel banda del método `D-021`). NO es la definición
> agéntica fina de un flujo (eso es el **diseño** de cada celda, `705_design/`).
> **Proyecto:** FODA (Forecast Optimization Driven Agentic) — plano de **construcción** del motor.
> **Banda:** `Tracer Bullet` (= walking skeleton, primera ancla, `D-017`).
> **Cliente golden de prueba:** `C1` (`D-012`/`D-014`).
> **Fuente de selección:** los 14 briefs aprobados (escaleras L0→Ln) + `700_brief/000_general_process.md` + `800_persistence/roadmap.md`.
> **Método de construcción:** `D-021` + `950_guideline/methodology.md` + `950_guideline/principles.md`.
> **Decisiones que lo enmarcan:** `D-015`, `D-016`, `D-017`, `D-020`, `D-021`, `D-012`, `D-014` ·
> **Estado:** `APROBADO` · **Fecha:** `2026-06-28` · **Aprobado por:** `Triple S <110043648+jdrodriguez1000@users.noreply.github.com>`.

---

## 0. Aclaración de planos — leer primero

Todo este documento es **construcción del MOTOR** y vive en este repo (`D-001`). Las **bandas son hitos
de madurez del motor, NO estados de la instancia**: una instancia (`fda-*`) no conoce la banda; solo
ejecuta la tubería con las capacidades que el motor tenga al generarla.

- **Qué produce el motor al operar esta banda:** la tubería de los 14 flujos en su peldaño L0, encadenada
  sobre capas inmutables bronze→silver→gold, culminando en un `reporting.json` mínimo (**margen bruto**
  por serie) y `monitoring.json`/`alerting.json` que cierran el ciclo.
- **Lo que NO viaja a la instancia:** este slice contract, los diseños (`705_design/`), los planes
  (`710_plan/`) y los snapshots (`D-012`) — todo del plano construcción. Solo se despliegan las
  **definiciones canónicas** (`foda-*`) que el build produce.

## 1. Objetivo de la banda

Demostrar que **un dato de C1 entra por Discovery y sale como un reporte de demanda revisable**,
recorriendo los **14 flujos en su versión más delgada** (happy-path, sin ramas ni profundidad),
encadenados sobre snapshots inmutables bronze→silver→gold, con el **gate humano de Modelling ejercido**
aunque el torneo sea trivial (ingenuo + 1 modelo simple). El valor de esta banda no es la precisión del
pronóstico, sino **probar que toda la tubería "respira" de punta a punta** y que los contratos in/out
entre flujos (`000_general_process.md`) se sostienen sobre un cliente real.

En una frase: probar que la tubería completa recorre C1 end-to-end y entrega un reporte que el
científico de datos puede leer.

## 2. Selección de peldaños por flujo — el corazón del contrato

| # | Flujo | Peldaño | Qué hace a ese nivel (resumen) | Artefacto(s) que entrega | Estado |
|----|-------|---------|--------------------------------|--------------------------|--------|
| 010 | Discovery | `L0` | A partir de un **cuestionario pre-respondido** de C1 (sin intake en vivo), emite los **3 contratos básicos**: fija periodicidad (mensual), horizonte y el grain producto×geografía; gate humano simple (aprobar/rechazar) | `client_register.yaml`, `business_hypothesis.md`, `contract_data.json` | `planeado` |
| 015 | Onboarding | `L0` | Mapeo 1:1 de las columnas fuente de C1 al esquema canónico (fecha, producto, geografía, cantidad demandada) | `map_client_data.json` | `planeado` |
| 020 | Ingestion (bronze) | `L0` | Carga el histórico de C1 a **bronze** tal cual; conteo de filas/series y cotejo básico | `bronze`, `ingestion_report.json` | `planeado` |
| 025 | Profiling | `L0` | `data_health.json` mínimo: % de completitud, nº de series, pareto básico | `data_health.json` | `planeado` |
| 030 | Cleaning (silver) | `L0` | Reglas triviales (`data_cleaner.yaml`: nulos/duplicados) → escribe **silver** | `silver`, `data_cleaning.json` | `planeado` |
| 035 | Derivation (gold) | `L0` | Agrega silver a **gold** al grain producto×sede×período → serie temporal de demanda | `gold`, `data_derivation.json` | `planeado` |
| 040 | Exploration | `L0` | Estadísticos básicos + propone `feature_engineering.yaml` con 1–2 features triviales (ej. lag-1, mes) | `exploration.json`, `feature_engineering.yaml` | `planeado` |
| 045 | Featuring | `L0` | Aplica el `feature_engineering.yaml` aprobado; **gold** enriquecida con esas 1–2 features | `gold` (enriquecida), `feature_engineering.json` | `planeado` |
| 050 | Modelling | `L0` | Corre el **baseline ingenuo + 1 modelo simple** con validación temporal básica (torneo de un participante → **selección trivial**); el **gate humano** aprueba el ganador, que se serializa tras la aprobación | `modelling.json`, `best_model.pkl` | `planeado` |
| 055 | Inferences | `L0` | Pronóstico a horizonte con el modelo ingenuo + **MAPE por período** | `gold` (predicciones), `inferences.json` | `planeado` |
| 060 | Simulation | `L0` | Montecarlo con semilla fija usando solo el MAPE: optimista/moderado/pesimista + demanda simulada; **sin** variables de influencia (`simulation_config.yaml` stub) y **sin inventario de seguridad formal** | `gold` (simulada), `simulation.json` | `planeado` |
| 065 | Scenarios | `L0` | **1 escenario con 1 delta** (ej. precio −5%) recalculado vs. base reutilizando Inferences/Simulation; ejercita el contrato what-if mínimo | `gold` (por escenario), `scenarios.json` | `planeado` |
| 070 | Reporting | `L0` | Lee precio/costo unitario de **bronze**; calcula el **margen bruto** esperado por período/serie (**sin** costo de oportunidad ni costo de inventario) | `reporting.json` | `planeado` |
| 075 | Monitoring | `L0` | Compara una **ventana de actuals reservada (hold-out)** de C1 vs. simulado; desviación + alerta básica por umbral fijo; **sin señal de re-ejecución** | `monitoring.json`, `alerting.json` | `planeado` |

## 3. Andamiaje transversal en esta banda (`TR-1..TR-4`, `D-020`)

| TR | Transversal | Peldaño | Qué andamiaje mínimo entra en esta banda |
|----|-------------|---------|------------------------------------------|
| TR-1 | Estado & persistencia runtime (`fda-*`) | `L0` | `project-progress.txt` mínimo + `git init` en la instancia: handoff en filesystem (P2) y trazabilidad por artefacto (P8). Es la persistencia de **runtime de instancia**, distinta de `800_persistence/` (construcción). |
| TR-2 | Patrón de instancias A/B/C | `L0` | **A+B colapsados** en una sesión única (sin instancia B separada); verificación en **contexto fresco** del recorrido end-to-end. Sin evaluador C independiente. |
| TR-3 | Evaluador + rúbrica (C) | `—` | **No entra** → se difiere a Stabilization/MVP. La verificación L0 es por contexto fresco, no por evaluador calibrado. |
| TR-4 | Ejecución durable / checkpoints / context resets | `—` | **No entra** → se difiere. El skeleton corre en el happy-path sin durabilidad ni resets. |

## 4. Alcance de la banda — qué entra / qué NO entra

- **Entra:** los **14 flujos en su peldaño L0** encadenados end-to-end sobre C1; capas
  bronze/silver/gold **inmutables** y en orden; **gate humano** en Modelling (aprobación del
  `best_model.pkl`); persistencia mínima + git (TR-1); verificación en contexto fresco (TR-2); un
  **reporte final revisable** (`reporting.json`) y el cierre de ciclo mínimo (`monitoring.json` /
  `alerting.json`).
- **NO entra (se difiere a la banda siguiente):**
  - intake en vivo multi-stakeholder y los documentos legibles `problem_statement.md` (L1) / `data_structure.md` (L2) de Discovery → L1+ de `010`.
  - torneo real de campeones y filtro del ingenuo en Modelling (en L0 solo ingenuo + 1 modelo) → L1+ de `050`.
  - variables de influencia e inventario de seguridad formal en Simulation (`simulation_config.yaml` stub en L0) → L1+ de `060`.
  - combinación de deltas / múltiples escenarios en Scenarios (en L0 un escenario con un delta) → L1+ de `065`.
  - costo de oportunidad y costo de inventario de seguridad en Reporting (en L0 solo margen bruto) → L1+ de `070`.
  - flujo recurrente real y señal de re-ejecución en Monitoring (en L0 hold-out como proxy, sin señal) → L1+ de `075`.
  - evaluador C independiente (TR-3) y durabilidad/checkpoints/resets (TR-4).
  - exportables `.csv`/`.xlsx` de cada flujo.

> **Nota de cardinalidad (desvío deliberado vs. la letra de los briefs):** seis briefs definen su L0
> sobre **1 serie**; esta banda los **escala al golden client C1 completo (~5–10 series)** para que el
> recorrido ejercite de verdad el fixture (`D-014`). Correr una sola serie no probaría la tubería sobre
> C1. Es el único punto donde el slice **amplía** el L0 del brief; todo lo demás se alinea a la letra del
> brief.

## 5. Insumos de prueba — golden client y snapshots (`D-012`/`D-014`)

- **Fixture:** `C1` — grain **1 región / 1 sede × ~5–10 SKUs (una familia)**, periodicidad **mensual**,
  ~24–36 meses de historia → **~5–10 series** (`D-014`). Generado por el generador sintético
  parametrizado (`T-014`).
- **Snapshots disponibles:** congelado de **bronze/silver/gold** y de los artefactos `*.json` por flujo,
  para reanudar la cadena sin re-correr aguas arriba (`D-012`). Las capas son acumulativas e inmutables
  hacia atrás (bronze nunca se altera; silver deriva de bronze; gold de silver).
- **Hold-out de Monitoring:** los **últimos K períodos** de C1 se reservan como "demanda real" para que
  `075` compare real vs. simulado, en lugar del flujo recurrente real (que se difiere).

## 6. BDD end-to-end (companion `bdd.md`)

- **Companion:** `703_definition/tracer-bullet/bdd.md`.
- **Resumen del comportamiento end-to-end:** dada la data cruda de C1, cuando la tubería ejecuta los 14
  flujos en orden (010→075) en su peldaño L0, entonces se produce un `reporting.json` con margen bruto por
  serie y un `monitoring.json` con la desviación vs. el hold-out, respetando la inmutabilidad de capas y
  el gate humano de Modelling. El detalle en Gherkin vive en el companion.

## 7. Criterio Done end-to-end de la banda

1. La tubería corre **end-to-end sobre C1** en el orden de §2 (010→075) y produce **todos los 14
   artefactos** marcados.
2. El **reporte final** (`reporting.json`) existe y es **revisable por el científico de datos** (**margen
   bruto** por serie/período).
3. **Gate humano:** el científico de datos **aprueba** explícitamente el `best_model.pkl` (ganador entre
   el ingenuo y 1 modelo simple) en Modelling antes de Inferences (`CLAUDE.md §5`).
4. Los **invariantes no deferibles** de `D-020` se respetan: bronze/silver/gold inmutables y en orden,
   trazabilidad por artefacto (P8), handoff en filesystem (P2), persistencia mínima + git (E1/TR-1).
5. `inferences.json` incluye **MAPE por período** (contrato hacia Simulation).
6. `monitoring.json` + `alerting.json` cierran el ciclo: la desviación vs. el hold-out se calcula y, al
   superar el umbral fijo, se emite la alerta básica (**sin** señal de re-ejecución en esta banda).
7. El recorrido completo se **verifica en un contexto fresco** (TR-2), separado del que lo construyó.

## 8. Riesgos / advertencias

- **Confusión de planos:** tratar la banda como estado de la instancia. No lo es; es madurez del
  **motor**. La instancia solo ejecuta la tubería con las capacidades vigentes (`D-001`/`D-021`).
- **Eslabón débil end-to-end:** un flujo L0 mal contratado (sobre todo el **grain** en
  Derivation/Onboarding) rompe toda la cadena; mitigación: fijar el grain producto×geografía en
  Discovery/Onboarding y propagarlo (`T-015`/`D-014`).
- **Sobre-ingeniería temprana (E4):** la tentación de meter torneo real (050), variables de influencia o
  inventario de seguridad (060), múltiples deltas/escenarios (065), costo de oportunidad/inventario (070)
  o evaluador C (TR-3) en esta banda. Resistirla: todo eso es L1+.
- **Monitoring sin demanda real:** el hold-out es un **proxy** del flujo recurrente; documentarlo como
  tal para no confundirlo con el comportamiento de producción.
- **Envenenar aguas abajo sin validar (E9):** un L0 que pasa datos malos a un flujo posterior; mitigar
  con la trazabilidad por artefacto y la verificación en contexto fresco.

## 9. Gate de aprobación del contrato (P5)

> Este contrato no habilita la construcción hasta la aprobación humana explícita. El nombre del aprobador
> se toma de `git config user.name + user.email`; nunca del contexto del agente.

- **Propuesto por A (sesión principal):** `2026-06-28`
- **Revisado por (revisor independiente):** revisión en contexto fresco del `2026-06-28` — veredicto
  inicial `REQUIERE SUBSANACIÓN` (desalineación L0 slice↔briefs); **subsanado** alineando la §2 a la letra
  de los briefs y documentando el único desvío (cardinalidad C1, §4). Apto para gate humano.
- **Aprobado por:** `Triple S <110043648+jdrodriguez1000@users.noreply.github.com>`
- **Fecha de aprobación:** `2026-06-28`

## 10. Siguiente paso

Tras **aprobar este slice contract**: pasar al nivel **celda** — para cada flujo seleccionado en §2, en
el **orden de la tubería** (010→075), ejecutar `diseñar → ejecutar → probar → verificar` contra C1,
acumulando sobre snapshots (`D-012`). El **diseño** de cada celda se materializa en
`705_design/tracer-bullet/<NN>_<flujo>.md` y su **plan** en `710_plan/tracer-bullet/<NN>_<flujo>.md`.
Antes de la primera celda hace falta la infraestructura de **golden client C1** (`T-014`).
