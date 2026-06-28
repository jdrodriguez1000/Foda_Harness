# Brief — Flujo 065 Scenarios (¿Qué pasa si…? → recálculo dirigido por el humano)

> **Tipo:** Brief de enmarque (alto nivel, previo al diseño agéntico). NO es la definición agéntica fina.
> **Proyecto:** FODA (Forecast Optimization Driven Agentic) — plano de **construcción** del motor.
> **Flujo:** `065` de 14 — `065_scenarios` (duodécimo flujo de la tubería; **escenarios de negocio hipotéticos** parametrizados por el humano).
> **Posición en la tubería:** consume `055_inferences` (`inferences.json`) + `060_simulation` (`simulation.json` / demanda simulada en gold) + `scenarios_config.yaml` (👤 humano) → entrega a `070_reporting`.
> **Capa de datos que toca:** `gold` (lectura de predicciones y demanda simulada; **escribe** la demanda por escenario en gold).
> **Fuente de verdad:** `990_documents/expected_workflow.md` (§ Scenarios) + `990_documents/expected_solution.md`.
> **Método de construcción:** `950_guideline/methodology.md` + `950_guideline/principles.md`.
> **Decisiones que lo enmarcan:** `D-001` (dos planos), `D-012` (snapshots), `D-014` (grain producto × geo), `D-015` (walking skeleton), `D-016` (brief + escalera), `D-017` (bandas + numeración) · **Estado:** `APROBADO` · **Fecha:** `2026-06-28` · **Aprobado por:** `usuario`.

---

## 0. Aclaración de planos — leer primero

Este brief describe un **componente del MOTOR FODA que estamos fabricando** (plano de *construcción*).
No describe los escenarios de una empresa concreta: describe la **maquinaria genérica y reutilizable** que,
al *operarse* sobre el pronóstico y la simulación de un cliente arbitrario, **recalcula** la demanda y la
demanda simulada bajo los **supuestos hipotéticos** ("¿qué pasa si…?") que el humano declara en
`scenarios_config.yaml`. El diseño **no debe cablear** los escenarios: qué variables se alteran, en qué
magnitud (delta) y sobre qué producto/serie son **dato de entrada**, y el conjunto de escenarios debe ser
**extensible**.

- **Insumo del flujo al operar:** el **`inferences.json`** (pronóstico + MAPE), la **`simulation.json`** /
  demanda simulada en **gold** y el **`scenarios_config.yaml`** (escenarios "¿qué pasa si…?" con sus deltas).
  Cambia por cliente.
- **Salida de runtime que produce al operar:** la **demanda por escenario en la capa gold** y el
  **`scenarios.json`** (comparativa base vs. escenarios). Pertenecen al **plano instancia** (`fda-*`);
  **nunca** vuelven a la memoria de construcción del motor.
- **Grain del cliente (`D-014`):** el recálculo se hace **por serie** (producto × geografía) y período; un
  delta puede aplicarse a un producto, a un grupo o a todos, según el config, sin mezclar series.

## 1. Objetivo

Responder preguntas de negocio del tipo **"¿qué pasa si…?"** permitiendo al científico de datos
**parametrizar cambios hipotéticos** sobre variables (p. ej. inflación +2%, lead time −1 día, precio de
venta −5% — **solo ejemplos: el conjunto de variables es abierto y crece con el tiempo**, igual que en
`060_simulation`) y **recalcular** la demanda pronosticada y la demanda simulada bajo esos supuestos. A diferencia
de Simulation —que cuantifica la **incertidumbre** del pronóstico (optimista/moderado/pesimista)—, Scenarios
explora **decisiones y supuestos de negocio** controlados por el humano, reutilizando los resultados de
Inferences y Simulation como **línea base**.

> En una frase: transformar **`inferences.json`** + **`simulation.json`** + **`scenarios_config.yaml`** en la
> **demanda recalculada por escenario** (gold + `scenarios.json`), comparada contra la base, lista para
> `070_reporting`.

## 2. Alcance — qué hace

**Modo Inicio (recálculo por escenario):**

- **Lectura de la línea base:** toma la demanda pronosticada (`inferences.json`) y la demanda simulada
  (`simulation.json` / gold) como **escenario base** de referencia.
- **Lectura de los escenarios humanos:** lee el **`scenarios_config.yaml`** que declara uno o más escenarios
  "¿qué pasa si…?", cada uno con sus **deltas** sobre variables (inflación, lead time, precio de venta, … —
  **lista no cerrada: pueden ser más variables, igual que en `060_simulation`**) y el alcance
  (producto/serie/grupo) al que aplican.
- **Recálculo de demanda y simulación:** por cada escenario, **recalcula** la demanda y la demanda simulada
  aplicando los deltas declarados, reutilizando la mecánica de Inferences/Simulation (no re-entrena modelos).
- **Comparativa base vs. escenarios:** produce la comparación entre el escenario base y cada escenario
  hipotético, por serie/período.
- **Escritura en gold:** deposita la **demanda por escenario** en la capa **gold**.
- **Bitácora de escenarios:** registra los escenarios, sus deltas y resultados en **`scenarios.json`**
  (documenta y **permite replicar** los escenarios).
- **Entrega descargable:** permite al científico de datos descargar `scenarios.json` en CSV o Excel.

## 3. Alcance — qué NO hace (límites)

- **No** genera el pronóstico puntual ni el MAPE → eso es el **flujo `055_inferences`**.
- **No** produce los escenarios **estadísticos** por incertidumbre (optimista/moderado/pesimista) ni el
  inventario de seguridad → eso es el **flujo `060_simulation`** (Scenarios **reutiliza** su salida como base).
- **No** re-entrena ni re-selecciona modelos → flujo `050_modelling`. Scenarios **recalcula** aplicando
  supuestos, no re-optimiza el modelo.
- **No** calcula márgenes, costos ni costo de oportunidad de los escenarios → eso es el **flujo
  `070_reporting`** (que puede reportar sobre la base y/o los escenarios).
- **No** define el conjunto de escenarios ni sus deltas (son **dato** del `scenarios_config.yaml`, autoría
  humana) → no se cablean en el agente; el conjunto debe ser **extensible**.
- **No** diseña la **maquinaria agéntica fina** de este flujo (instancias A/B/C, workers, checkpoints,
  rúbrica del evaluador, contratos de herramientas) → eso es el **diseño del flujo `065_scenarios`**, paso
  siguiente a este brief.

## 4. Insumos disponibles

| ID | Insumo | Origen |
|----|--------|--------|
| I-1 | Definición del flujo Scenarios en la tubería FODA | `990_documents/expected_workflow.md` (§ Scenarios) |
| I-2 | Arquitectura de capas bronze/silver/gold y visión de planos | `990_documents/expected_solution.md`, `CLAUDE.md §4` |
| I-3 | Metodología y principios de construcción (P*, E*, NC*, patrón A/B/C, modelo plano) | `950_guideline/methodology.md`, `950_guideline/principles.md` |
| I-4 | Memoria de construcción (estado, decisiones, lecciones) | `800_persistence/` (`D-001`, `D-012`, `D-014`, `D-017`) |
| I-5 | Briefs aprobados aguas arriba (forma de `inferences.json`, `simulation.json` y de las variables) | `700_brief/055_inferences.md`, `700_brief/060_simulation.md` |

> **Insumo en tiempo de operación (no de construcción):** el **`inferences.json`** y **`simulation.json`**
> reales y el **`scenarios_config.yaml`** (autoría humana: escenarios y deltas). Llegan cuando el motor se
> *opera*, no ahora. (Para construir y probar el flujo se usa el **snapshot gold de C1** + fixtures de
> `inferences.json`, `simulation.json` y `scenarios_config.yaml` — `D-012`/`T-014`.)

## 5. Artefactos esperados (salida del flujo al operar)

| Artefacto | Propósito |
|-----------|-----------|
| **Demanda por escenario en la capa `gold`** | Demanda recalculada para cada escenario "¿qué pasa si…?", por serie/período. La consume `070_reporting`. |
| **`scenarios.json`** (comparativa base vs. escenarios) | Documenta cada escenario, sus deltas y resultados frente a la base; soporta auditoría y **replay**. |
| **Exportable CSV/Excel** de `scenarios.json` | Permite al científico de datos descargar y compartir los escenarios. |

> El **`scenarios_config.yaml`** es **insumo** (autoría humana), no salida de este flujo. Los *paths*, el
> esquema exacto de `scenarios.json` y la mecánica del recálculo se fijan en el **diseño del flujo** (paso
> siguiente).

## 6. Criterios de éxito (Done)

1. Por cada escenario del **`scenarios_config.yaml`**, la demanda y la demanda simulada se **recalculan**
   aplicando sus deltas, por **serie** y **período** (`D-014`).
2. Se preserva el **escenario base** (Inferences + Simulation) como referencia y se compara contra cada
   escenario.
3. El conjunto de escenarios es **extensible** y de **alcance variable**: agregar un escenario o una variable
   nueva al config no exige cambiar el motor; un delta puede aplicar a un producto, grupo o todos.
4. La **demanda por escenario** queda escrita en **gold**; **`scenarios.json`** documenta deltas y resultados
   de forma **reproducible**.
5. Scenarios **no re-entrena modelos**: reutiliza la mecánica de Inferences/Simulation sobre supuestos.
6. `scenarios.json` es **descargable en CSV o Excel**.
7. **Gate humano (si aplica):** el científico de datos **revisa** los escenarios antes de habilitar Reporting
   (ver `CLAUDE.md §5`).

## 7. Riesgos / advertencias

- **Confusión de planos (`D-001`):** demanda por escenario en gold y `scenarios.json` son **runtime de la
  instancia** (`fda-*`), no memoria de construcción.
- **Confusión con Simulation:** mezclar los escenarios **estadísticos** (incertidumbre, `060`) con los
  escenarios **hipotéticos de negocio** (`065`) confunde al usuario. Mantener la frontera: `060` cuantifica
  incertidumbre; `065` explora supuestos controlados por el humano.
- **Escenarios/deltas cableados (anti-patrón):** hard-codear "inflación +2%" o "lead time −1" en el agente
  rompe la reutilización y la **extensibilidad**. Escenarios y deltas son **dato** (`scenarios_config.yaml`).
- **Recálculo inconsistente con la base:** si el recálculo no parte de la misma línea base ni reutiliza la
  mecánica de Inferences/Simulation, la comparación base vs. escenario pierde validez.
- **Alcance mal aplicado:** aplicar un delta a todas las series cuando el config lo limita a un producto (o
  viceversa) corrompe el escenario (respetar el grain `D-014`).
- **Re-entrenar por error:** Scenarios **no** re-optimiza el modelo; hacerlo invade Modelling y rompe la
  trazabilidad.
- **Envenenar aguas abajo (E9):** escenarios mal calculados contaminan Reporting (márgenes, costo de
  oportunidad). Trazabilidad y revisión humana mitigan.

## 8. `scenarios_config.yaml`: "¿qué pasa si…?" como deltas declarativos — sección específica del flujo

La pieza distintiva de Scenarios es que **el humano explora decisiones**, no incertidumbre estadística:

- **`scenarios_config.yaml` (entrada 👤 humana).** Declara uno o más escenarios; cada escenario define
  **deltas** sobre variables y el **alcance** (producto/serie/grupo). Ejemplos de delta: *inflación +2%*,
  *lead time −1 día*, *precio de venta −5%* — **son solo ejemplos; el catálogo de variables manipulables es
  abierto y puede incluir más** (las mismas tres no son un límite, igual que en `060_simulation`). La demanda
  y la simulación se **recalculan** bajo esos supuestos.
- **Relación con Simulation.** Las variables que Scenarios altera son, en parte, las mismas que parametriza
  `simulation_config.yaml` (lead time, inflación, …) más variables de negocio como el **precio de venta**. La
  diferencia es el propósito: Simulation muestrea su distribución (incertidumbre); Scenarios fija un **valor
  hipotético dirigido** (decisión) y observa el efecto.
- **Reutiliza, no reinventa.** Scenarios **recicla** la mecánica de Inferences (pronóstico) y Simulation
  (Montecarlo) aplicada sobre los supuestos del escenario; no es un nuevo motor de predicción.
- **Extensibilidad por diseño.** El conjunto de escenarios y de variables manipulables **crecerá**; tratarlos
  como entradas declarativas (no ramas cableadas) permite que el científico de datos "juegue" con nuevas
  preguntas editando el YAML, no el motor. Mismo principio "reglas como dato" de `simulation_config.yaml`.

## 9. Escalera de capacidades (L0 → Ln) — vista vertical del flujo

> Vista vertical de la *ambición completa* de Scenarios (`D-016`). **L0 = lo mínimo** del walking skeleton
> (banda **Tracer Bullet**, `D-017`): un escenario con un delta sobre C1 y comparación contra la base. Cada
> peldaño agrega capacidad.

| Nivel | Capacidad | Qué incluye | Qué difiere de la realidad |
|-------|-----------|-------------|----------------------------|
| **L0** (mínimo / skeleton) | **1 escenario, 1 delta, recálculo vs. base (1 serie)** | Lee un `scenarios_config.yaml` stub con un escenario (p. ej. precio −5%) para una serie de C1, recalcula la demanda reutilizando la base de Inferences/Simulation, escribe el resultado en gold y un `scenarios.json` básico con base vs. escenario; handoff a Reporting. | Una serie; un solo delta; sin combinación de variables; sin exportación. |
| **L1** | **Varios escenarios + multi-variable + bitácora completa** | Múltiples escenarios, cada uno con uno o varios deltas (inflación, lead time, precio); multi-serie; `scenarios.json` documenta deltas y comparativa. | Alcance simple (global o por producto); sin exportación; sin combinación jerárquica fina. |
| **L2** | **Alcance por grain + exportable + comparativa rica** | Deltas con alcance por producto/grupo/serie según el config; descarga CSV/Excel; comparativa base vs. N escenarios por serie/período. | Catálogo de variables acotado; sin replay versionado. |
| **L3** | **Catálogo extensible + replay + gate formal** | Escenarios y variables como entradas declarativas extensibles (sumar uno = editar YAML); replay reproducible; revisión humana formal de los escenarios. | Sin acoplamiento aún a optimización/recomendación automática de escenarios. |
| **Ln** (ambición completa) | **Scenarios "como un científico de datos senior"** | Exploración rica de "¿qué pasa si…?" multi-variable y multi-serie, catálogo extensible de palancas de negocio, comparativas claras contra la base, replay determinista y supuestos auditables ligados al contrato. | Nada: es el objetivo final del flujo. |

> **Nota de ensamblaje:** al cerrar este brief se refleja el estado en `800_persistence/roadmap.md`
> (fila Scenarios: columna *Brief* → `planeado`; peldaño previsto para Tracer Bullet → **L0**).

## 10. Siguiente paso

Tras **aprobar este brief**: **diseñar el flujo `065_scenarios`** (instancias A/B/C según el modelo plano
`D-009`, workers, política de herramientas, checkpoints canónicos, durabilidad, rúbrica del evaluador y
contrato), reutilizando los patrones transversales ya validados del motor —en particular la mecánica de
Inferences/Simulation que Scenarios recicla. El **plan de implementación** viene *después* del diseño (orden
del método: **brief → diseño → plan → construir**, `D-011`). El diseño se materializará en
`705_design/065_scenarios.md`.
