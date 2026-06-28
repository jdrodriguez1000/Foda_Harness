# Brief — Flujo 055 Inferences (Predicciones del mejor modelo + MAPE por período)

> **Tipo:** Brief de enmarque (alto nivel, previo al diseño agéntico). NO es la definición agéntica fina.
> **Proyecto:** FODA (Forecast Optimization Driven Agentic) — plano de **construcción** del motor.
> **Flujo:** `055` de 14 — `055_inferences` (décimo flujo de la tubería; **genera el pronóstico** con el modelo seleccionado).
> **Posición en la tubería:** consume `050_modelling` (`best_model.pkl`) + capa **gold** (features) → entrega a `060_simulation`.
> **Capa de datos que toca:** `gold` (lectura de features; **escribe** las predicciones en gold).
> **Fuente de verdad:** `990_documents/expected_workflow.md` (§10 Inferences) + `990_documents/expected_solution.md`.
> **Método de construcción:** `950_guideline/methodology.md` + `950_guideline/principles.md`.
> **Decisiones que lo enmarcan:** `D-001` (dos planos), `D-012` (snapshots), `D-014` (grain producto × geo), `D-015` (walking skeleton), `D-016` (brief + escalera), `D-017` (bandas + numeración) · **Estado:** `APROBADO` · **Fecha:** `2026-06-28` · **Aprobado por:** `usuario`.

---

## 0. Aclaración de planos — leer primero

Este brief describe un **componente del MOTOR FODA que estamos fabricando** (plano de *construcción*).
No describe el pronóstico de una empresa concreta: describe la **maquinaria genérica y reutilizable** que,
al *operarse* sobre la capa gold y el `best_model.pkl` de un cliente arbitrario, produce las **predicciones
de demanda** para el horizonte contratado, **cada una con su MAPE** por período. El diseño **no debe
cablear** el modelo ni el horizonte: el modelo llega serializado (`best_model.pkl`) y el horizonte/períodos
provienen del contrato (`contract_data.json`).

- **Insumo del flujo al operar:** el **`best_model.pkl`** (modelo seleccionado, de Modelling), la capa
  **gold** (features para el período a predecir) y el **horizonte/periodicidad** del contrato. Cambia por
  cliente.
- **Salida de runtime que produce al operar:** las **predicciones en la capa gold** y el
  **`inferences.json`** (pronóstico + **MAPE por período**). Pertenecen al **plano instancia** (`fda-*`);
  **nunca** vuelven a la memoria de construcción del motor.
- **Grain del cliente (`D-014`):** las predicciones se generan **por serie** (producto × geografía) y por
  período del horizonte; el MAPE se reporta al nivel/período correspondiente sin mezclar series.

## 1. Objetivo

Generar las **predicciones de demanda** para el horizonte contratado aplicando el **`best_model.pkl`**
sobre las features de la capa gold. Cada predicción se entrega **acompañada de su métrica de desviación
(MAPE)** por período, porque ese MAPE es el **insumo central del flujo siguiente** (`060_simulation`, que
aplica la desviación para los escenarios optimista/moderado/pesimista). El flujo deja las predicciones en
gold y documenta el resultado en `inferences.json`, descargable y replicable.

> En una frase: transformar **`best_model.pkl`** + features de **gold** en las **predicciones de demanda con
> MAPE por período** (`inferences.json` + predicciones en gold), listas para `060_simulation`.

## 2. Alcance — qué hace

**Modo Inicio (generación del pronóstico):**

- **Carga del modelo:** lee el **`best_model.pkl`** seleccionado en Modelling (sin re-entrenar ni
  re-seleccionar).
- **Predicción del horizonte:** aplica el modelo a las features de **gold** para producir la demanda
  pronosticada por **período** del horizonte (según la periodicidad del `contract_data.json`) y por **serie**
  (producto × sede).
- **Métrica de desviación (MAPE) por período:** acompaña cada predicción con su **MAPE** (p. ej. mes 1:
  10,20%; mes 2: 10,90%; mes 3: 11,87%). Es la base cuantitativa del flujo de simulación.
- **Escritura en gold:** deposita las predicciones en la capa **gold** (demanda pronosticada por
  serie/período), lista para Simulation.
- **Bitácora de inferencias:** registra el pronóstico y su MAPE en **`inferences.json`**, documentando el
  proceso para **replicarlo** sobre otros archivos del cliente.
- **Entrega descargable:** permite al científico de datos descargar `inferences.json` en CSV o Excel.

## 3. Alcance — qué NO hace (límites)

- **No** entrena, compara ni selecciona modelos → eso es el **flujo `050_modelling`** (Inferences solo
  **aplica** el `best_model.pkl`).
- **No** crea ni materializa variables → eso es el **flujo `045_featuring`** (las features ya están en gold).
- **No** aplica simulación Montecarlo ni produce escenarios optimista/moderado/pesimista ni demanda
  simulada → eso es el **flujo `060_simulation`** (que **consume** el MAPE que este flujo entrega).
- **No** calcula márgenes, costos ni inventario de seguridad → flujos `060`/`070`.
- **No** responde "¿qué pasa si…?" → flujo `065_scenarios`.
- **No** diseña la **maquinaria agéntica fina** de este flujo (instancias A/B/C, workers, checkpoints,
  rúbrica del evaluador, contratos de herramientas) → eso es el **diseño del flujo `055_inferences`**, paso
  siguiente a este brief.

## 4. Insumos disponibles

| ID | Insumo | Origen |
|----|--------|--------|
| I-1 | Definición del flujo Inferences en la tubería FODA | `990_documents/expected_workflow.md` (§10) |
| I-2 | Arquitectura de capas bronze/silver/gold y visión de planos | `990_documents/expected_solution.md`, `CLAUDE.md §4` |
| I-3 | Metodología y principios de construcción (P*, E*, NC*, patrón A/B/C, modelo plano) | `950_guideline/methodology.md`, `950_guideline/principles.md` |
| I-4 | Memoria de construcción (estado, decisiones, lecciones) | `800_persistence/` (`D-001`, `D-012`, `D-014`, `D-017`) |
| I-5 | Briefs aprobados aguas arriba (forma de `best_model.pkl`, gold y horizonte del contrato) | `700_brief/050_modelling.md`, `700_brief/045_featuring.md`, `700_brief/010_discovery.md` |

> **Insumo en tiempo de operación (no de construcción):** el **`best_model.pkl`** real, la capa **gold** con
> features y el **horizonte/periodicidad** del `contract_data.json`. Llegan cuando el motor se *opera*, no
> ahora. (Para construir y probar el flujo se usa el **snapshot gold de C1** + un `best_model.pkl` fixture —
> `D-012`/`T-014`.)

## 5. Artefactos esperados (salida del flujo al operar)

| Artefacto | Propósito |
|-----------|-----------|
| **Predicciones en la capa `gold`** | Demanda pronosticada por serie/período. La consume `060_simulation`. |
| **`inferences.json`** (pronóstico + MAPE por período) | Documenta la demanda predicha y su **MAPE** por período; **insumo central** de Simulation y base de auditoría/replay. |
| **Exportable CSV/Excel** de `inferences.json` | Permite al científico de datos descargar y compartir el pronóstico. |

> Los *paths*, el esquema exacto de `inferences.json` (incl. el formato del MAPE por período/serie) y la
> mecánica se fijan en el **diseño del flujo** (paso siguiente).

## 6. Criterios de éxito (Done)

1. Las **predicciones** se generan aplicando `best_model.pkl` sobre las features de gold, por **serie** y por
   **período** del horizonte contratado (`D-014`).
2. **Cada predicción lleva su MAPE** por período, en el formato que Simulation espera consumir.
3. Las predicciones quedan escritas en la capa **gold**, listas para `060_simulation`.
4. **`inferences.json`** documenta el pronóstico y el MAPE de forma **reproducible** sobre otros archivos del
   cliente.
5. **Sin fuga de datos futuros:** la predicción usa solo información disponible en tiempo de inferencia
   (coherente con el modelo y las features).
6. `inferences.json` es **descargable en CSV o Excel**.
7. **Gate humano (si aplica):** el científico de datos **revisa** el pronóstico y su MAPE antes de habilitar
   Simulation (ver `CLAUDE.md §5`).

## 7. Riesgos / advertencias

- **Confusión de planos (`D-001`):** predicciones en gold e `inferences.json` son **runtime de la instancia**
  (`fda-*`), no memoria de construcción.
- **MAPE ausente o mal calculado — riesgo crítico:** el MAPE por período es el **insumo** de Simulation; si
  falta, está mal escalado o no corresponde al período, **rompe `060_simulation`** (escenarios sin sustento).
  Es un requisito de primera clase, no un adorno del informe.
- **Fuga de datos futuros (data leakage):** generar features del horizonte con información no disponible en
  inferencia infla el pronóstico; la construcción debe ser temporalmente segura por serie.
- **Re-entrenar/re-seleccionar por error:** Inferences **aplica** el modelo, no lo re-optimiza; hacerlo aquí
  invade Modelling y rompe la trazabilidad de la selección humana.
- **Envenenar aguas abajo (E9):** un pronóstico o un MAPE erróneo contamina Simulation, Scenarios y Reporting.
  Trazabilidad en `inferences.json` y revisión humana mitigan.
- **Horizonte/periodicidad cableados (anti-patrón):** el horizonte viene del `contract_data.json`; cablearlo
  rompe la reutilización entre clientes.
- **Snapshot stale (al construir):** las predicciones de C1 dependen del snapshot gold y del `best_model.pkl`
  fixture; si cambian, regenerar (`D-012`).

## 8. El MAPE por período como contrato hacia Simulation — sección específica del flujo

Inferences es el **puente cuantitativo** hacia la simulación, y su salida más crítica no es solo la
predicción puntual sino la **incertidumbre** que la acompaña:

- **El MAPE es un dato de salida de primera clase.** Cada predicción se entrega como un par (valor esperado,
  **MAPE del período**). Ejemplo del horizonte a 3 períodos:

  | Período | ML Esperado | ML MAPE |
  |---------|-------------|---------|
  | 1 | 1062 | 10,20% |
  | 2 | 1710 | 10,90% |
  | 3 | 1489 | 11,87% |

- **Por qué importa.** `060_simulation` toma ese MAPE como la **desviación** para la simulación Montecarlo y
  derivar los escenarios optimista / moderado / pesimista y la demanda simulada. Sin un MAPE confiable por
  período, la simulación pierde su base. Por eso el contrato de salida de Inferences (predicción **+** MAPE
  por período/serie) es un invariante del diseño.
- **Granularidad coherente con el grain (`D-014`).** El MAPE se reporta al período del horizonte y por serie
  (o nivel agregado acordado), de forma que Simulation pueda aplicarlo serie por serie sin reconciliaciones
  ambiguas.

## 9. Escalera de capacidades (L0 → Ln) — vista vertical del flujo

> Vista vertical de la *ambición completa* de Inferences (`D-016`). **L0 = lo mínimo** del walking skeleton
> (banda **Tracer Bullet**, `D-017`): aplicar el modelo sobre C1 y entregar predicción + MAPE por período.
> Cada peldaño agrega capacidad.

| Nivel | Capacidad | Qué incluye | Qué difiere de la realidad |
|-------|-----------|-------------|----------------------------|
| **L0** (mínimo / skeleton) | **Predicción + MAPE por período (1 serie)** | Carga el `best_model.pkl` fixture, predice el horizonte sobre el snapshot gold de C1 para una serie, escribe las predicciones en gold y un `inferences.json` con la predicción y su **MAPE por período**; handoff a Simulation. | Una sola serie; horizonte corto fijo; sin exportación; sin reconciliación jerárquica. |
| **L1** | **Multi-serie + horizonte del contrato + bitácora completa** | Predice todas las series del grain para el horizonte/periodicidad del `contract_data.json`; `inferences.json` documenta predicción y MAPE por serie/período. | Sin exportación; sin reconciliación entre niveles jerárquicos; MAPE simple. |
| **L2** | **Exportable + intervalos/coherencia de MAPE** | Descarga CSV/Excel; MAPE calculado de forma robusta y coherente con la validación de Modelling; chequeos de sanidad del pronóstico. | Sin reconciliación jerárquica formal; sin re-inferencia incremental. |
| **L3** | **Reconciliación jerárquica + replay + gate formal** | Reconciliación de pronósticos entre niveles del grain (familia/sede); replay idempotente; revisión humana formalizada del pronóstico antes de Simulation. | Sin re-inferencia programada ligada al monitoreo. |
| **Ln** (ambición completa) | **Inferences "como un científico de datos senior"** | Pronóstico multi-serie con MAPE robusto por período/nivel, reconciliación jerárquica, intervalos de incertidumbre, exportación rica, replay y re-inferencia ligados al contrato y al monitoreo. | Nada: es el objetivo final del flujo. |

> **Nota de ensamblaje:** al cerrar este brief se refleja el estado en `800_persistence/roadmap.md`
> (fila Inferences: columna *Brief* → `planeado`; peldaño previsto para Tracer Bullet → **L0**).

## 10. Siguiente paso

Tras **aprobar este brief**: **diseñar el flujo `055_inferences`** (instancias A/B/C según el modelo plano
`D-009`, workers, política de herramientas, checkpoints canónicos, durabilidad, rúbrica del evaluador y
contrato), reutilizando los patrones transversales ya validados del motor. El **plan de implementación**
viene *después* del diseño (orden del método: **brief → diseño → plan → construir**, `D-011`). El diseño se
materializará en `705_design/055_inferences.md`.
