# Brief — Flujo 050 Modelling (Torneo de campeones → mejor modelo)

> **Tipo:** Brief de enmarque (alto nivel, previo al diseño agéntico). NO es la definición agéntica fina.
> **Proyecto:** FODA (Forecast Optimization Driven Agentic) — plano de **construcción** del motor.
> **Flujo:** `050` de 14 — `050_modelling` (noveno flujo de la tubería; **entrena, compara y selecciona** el modelo de pronóstico).
> **Posición en la tubería:** consume `045_featuring` (capa **gold** enriquecida) + `modelling_config.yaml` (👤 humano) → entrega a `055_inferences`.
> **Capa de datos que toca:** `gold` (lectura de la matriz de features; **no** escribe capa — produce un artefacto de modelo).
> **Fuente de verdad:** `990_documents/expected_workflow.md` (§9 Modelling) + `990_documents/expected_solution.md`.
> **Método de construcción:** `950_guideline/methodology.md` + `950_guideline/principles.md`.
> **Decisiones que lo enmarcan:** `D-001` (dos planos), `D-012` (snapshots), `D-014` (grain producto × geo), `D-015` (walking skeleton), `D-016` (brief + escalera), `D-017` (bandas + numeración) · **Estado:** `APROBADO` · **Fecha:** `2026-06-28` · **Aprobado por:** `usuario`.

---

## 0. Aclaración de planos — leer primero

Este brief describe un **componente del MOTOR FODA que estamos fabricando** (plano de *construcción*).
No describe el modelado de una empresa concreta: describe la **maquinaria genérica y reutilizable** que,
al *operarse* sobre la capa gold de un cliente arbitrario, corre un **modelo ingenuo** como línea base,
ejecuta un **torneo de campeones** entre los modelos declarados en `modelling_config.yaml`, y entrega el
**mejor modelo** que el científico de datos selecciona. El diseño **no debe cablear modelos ni
hiperparámetros**: el catálogo de modelos, sus hiperparámetros y los criterios del torneo son **dato de
entrada** (`modelling_config.yaml`), no código.

- **Insumo del flujo al operar:** la capa **gold enriquecida** (matriz de features, de Featuring) y el
  **`modelling_config.yaml`** (modelos, hiperparámetros, baseline ingenuo, métrica y reglas de selección).
  Cambia por cliente.
- **Salida de runtime que produce al operar:** el **`modelling.json`** (informe del torneo) y el
  **`best_model.pkl`** (modelo ganador serializado). Pertenecen al **plano instancia** (`fda-*`); **nunca**
  vuelven a la memoria de construcción del motor.
- **Grain del cliente (`D-014`):** el modelado respeta la cardinalidad de series (producto × geografía);
  según el `modelling_config.yaml`, el torneo puede correr **por serie**, por grupo o global. La validación
  temporal (train/test por fecha) se hace **dentro** de cada serie, sin mezclarlas.

## 1. Objetivo

Determinar el **mejor modelo de machine learning** para pronosticar la demanda de los productos del
cliente. El flujo arranca calculando un **modelo ingenuo** (baseline) que fija el piso de desempeño;
luego ejecuta un **torneo de campeones** entre los modelos declarados en `modelling_config.yaml`, donde el
**primer filtro obligatorio es superar al modelo ingenuo** y el segundo es competir entre sí por la
métrica objetivo. El flujo **presenta los resultados** y **recomienda**, pero la **selección final la hace
el científico de datos** (gate humano); una vez elegido, serializa el ganador en `best_model.pkl`.

> En una frase: transformar la capa **gold** enriquecida + `modelling_config.yaml` en un **`best_model.pkl`**
> seleccionado por el humano y un **`modelling.json`** que documenta el torneo, listo para `055_inferences`.

## 2. Alcance — qué hace

**Modo Inicio (torneo y selección):**

- **Línea base ingenua (baseline):** entrena/aplica primero un **modelo ingenuo** (p. ej. naive estacional,
  media móvil, último valor) según `modelling_config.yaml`, y mide su desempeño. Es el **umbral mínimo** que
  cualquier modelo candidato debe superar para seguir en competencia.
- **Torneo de campeones:** toma la matriz de features de **gold** y entrena/evalúa los modelos declarados en
  `modelling_config.yaml` con sus **hiperparámetros**, bajo una validación temporal consistente.
  - **Filtro 1 — superar al ingenuo:** descarta (o marca como no aptos) los modelos que **no superan** el
    baseline ingenuo.
  - **Filtro 2 — competir entre sí:** entre los que sí lo superan, los ordena por la **métrica objetivo**
    (p. ej. MAPE) definida en el config.
- **Informe del torneo:** genera **`modelling.json`** con (i) modelos aplicados e hiperparámetros, (ii)
  resultados/ranking por métrica (incluido el baseline ingenuo como referencia), (iii) variables que mejor
  explicaron la demanda (importancia de features).
- **Recomendación al humano:** presenta el ranking y **recomienda** un modelo, con el razonamiento, para
  habilitar la decisión.
- **Selección humana (gate):** el científico de datos **elige** el modelo a usar para inferencias.
- **Serialización del ganador:** una vez elegido, produce **`best_model.pkl`** (modelo entrenado listo para
  `055_inferences`).
- **Entrega descargable:** permite al científico de datos descargar `modelling.json` en CSV o Excel.

## 3. Alcance — qué NO hace (límites)

- **No** crea ni materializa variables → eso es el **flujo `045_featuring`** (gold enriquecida es insumo).
- **No** deriva ni agrega la demanda → eso es el **flujo `035_derivation`**.
- **No** realiza las predicciones del horizonte futuro ni calcula el MAPE por período de pronóstico → eso es
  el **flujo `055_inferences`** (que consume `best_model.pkl`). Modelling mide desempeño **en validación**
  para comparar, no produce el pronóstico de negocio.
- **No** corre simulación Montecarlo ni escenarios → flujos `060_simulation` / `065_scenarios`.
- **No** decide por su cuenta el modelo final: **recomienda**; **selecciona el humano** (`CLAUDE.md §5`).
- **No** define el catálogo de modelos ni los hiperparámetros (son **dato** del `modelling_config.yaml`,
  autoría humana) → no se cablean en el agente.
- **No** diseña la **maquinaria agéntica fina** de este flujo (instancias A/B/C, workers, checkpoints,
  rúbrica del evaluador, contratos de herramientas) → eso es el **diseño del flujo `050_modelling`**, paso
  siguiente a este brief.

## 4. Insumos disponibles

| ID | Insumo | Origen |
|----|--------|--------|
| I-1 | Definición del flujo Modelling en la tubería FODA | `990_documents/expected_workflow.md` (§9) |
| I-2 | Arquitectura de capas bronze/silver/gold y visión de planos | `990_documents/expected_solution.md`, `CLAUDE.md §4` |
| I-3 | Metodología y principios de construcción (P*, E*, NC*, patrón A/B/C, modelo plano) | `950_guideline/methodology.md`, `950_guideline/principles.md` |
| I-4 | Memoria de construcción (estado, decisiones, lecciones) | `800_persistence/` (`D-001`, `D-012`, `D-014`, `D-017`) |
| I-5 | Briefs aprobados aguas arriba (forma de la gold enriquecida y de la matriz de features) | `700_brief/045_featuring.md`, `700_brief/035_derivation.md` |

> **Insumo en tiempo de operación (no de construcción):** la capa **gold enriquecida real** y el
> **`modelling_config.yaml`** (autoría humana: catálogo de modelos, hiperparámetros, baseline, métrica y
> reglas de selección). Llegan cuando el motor se *opera*, no ahora. (Para construir y probar el flujo se
> usa el **snapshot gold de C1** + un `modelling_config.yaml` fixture — `D-012`/`T-014`.)

## 5. Artefactos esperados (salida del flujo al operar)

| Artefacto | Propósito |
|-----------|-----------|
| **`modelling.json`** (informe del torneo) | Documenta modelos aplicados, hiperparámetros, ranking por métrica (con el ingenuo como referencia) e importancia de variables. Soporta la **decisión humana** y la auditoría/replay. |
| **`best_model.pkl`** (modelo ganador serializado) | El modelo **seleccionado por el humano**, entrenado y listo para producir pronósticos. Lo consume `055_inferences`. |
| **Exportable CSV/Excel** de `modelling.json` | Permite al científico de datos descargar y compartir los resultados del torneo. |

> El **`modelling_config.yaml`** es **insumo** (autoría humana), no salida de este flujo. Los *paths*, el
> esquema exacto de `modelling.json`, el formato de serialización de `best_model.pkl` y la mecánica del
> torneo (validación temporal, búsqueda de hiperparámetros) se fijan en el **diseño del flujo** (paso
> siguiente).

## 6. Criterios de éxito (Done)

1. Se calcula un **modelo ingenuo** como baseline y queda registrado como **umbral** de comparación.
2. El **torneo** entrena/evalúa los modelos del `modelling_config.yaml` bajo una **validación temporal**
   consistente (sin fuga de datos futuros), respetando el grain (`D-014`).
3. **Filtro del ingenuo aplicado:** los modelos que no superan el baseline quedan marcados/descartados; el
   ranking final solo compite entre los que sí lo superan.
4. **`modelling.json`** documenta modelos, hiperparámetros, ranking por métrica (incluido el ingenuo) e
   importancia de variables, de forma **reproducible**.
5. **Gate humano (obligatorio):** el agente **presenta el ranking y recomienda**; el científico de datos
   **selecciona explícitamente** el modelo final (`CLAUDE.md §5`).
6. Tras la selección, se produce **`best_model.pkl`** entrenado y listo para `055_inferences`.
7. `modelling.json` es **descargable en CSV o Excel**.

## 7. Riesgos / advertencias

- **Confusión de planos (`D-001`):** `modelling.json` y `best_model.pkl` son **runtime de la instancia**
  (`fda-*`), no memoria de construcción.
- **Modelos/hiperparámetros cableados (anti-patrón):** hard-codear el catálogo o los hiperparámetros en el
  agente rompe la reutilización entre clientes. Son **dato** (`modelling_config.yaml`), no código.
- **Fuga de datos futuros (data leakage) — riesgo crítico:** una partición train/test mal hecha (no
  temporal, o que mezcla series) infla el desempeño del torneo y elige un modelo que fallará en producción.
  La validación debe ser **temporal y por serie**.
- **Métrica engañosa:** comparar por una métrica inadecuada (o sin el baseline ingenuo como referencia)
  puede coronar un modelo peor que "no hacer nada". El **filtro del ingenuo** es la salvaguarda; documentar
  siempre el baseline en `modelling.json`.
- **Saltarse el gate humano (E-/NC):** auto-seleccionar el modelo sin aprobación viola el checkpoint de
  diseño (`CLAUDE.md §5`). El flujo **recomienda**, el humano **decide**.
- **Envenenar aguas abajo (E9):** un `best_model.pkl` débil o con leakage contamina `055_inferences` y todo
  lo que sigue (simulación, escenarios, reporting). El filtro del ingenuo + validación temporal + gate
  humano mitigan.
- **Sobre-ingeniería temprana (E4):** en el skeleton, no montar búsqueda exhaustiva de hiperparámetros ni
  decenas de modelos; L0 corre el ingenuo + un modelo simple.
- **Snapshot stale (al construir):** el torneo de C1 depende del snapshot gold enriquecida y del config
  fixture; si cambian, regenerar (`D-012`).

## 8. Modelo ingenuo + torneo de campeones + gate de selección — sección específica del flujo

Modelling es el **corazón de decisión** de la tubería y tiene tres piezas distintivas:

- **El baseline ingenuo va primero, y es un filtro, no un adorno.** Antes de cualquier modelo sofisticado,
  el flujo calcula un **modelo ingenuo** (p. ej. naive estacional / último período / media móvil) y mide su
  desempeño. Ese número es el **umbral mínimo**: un candidato que no lo supera **no merece selección**. Esto
  protege al cliente de "modelos" que rinden peor que una heurística trivial y da una referencia honesta al
  comparar.
- **`modelling_config.yaml` (entrada 👤 humana) es el guion del torneo.** Igual que `data_cleaner.yaml`
  gobierna Cleaning, este YAML declara: el **modelo ingenuo** (método y parámetros), el **catálogo de
  modelos** candidatos con sus **hiperparámetros** (rejillas o valores), la **métrica objetivo** (p. ej.
  MAPE), el **esquema de validación temporal** y las **reglas de selección** (incl. "debe superar al
  ingenuo"). El agente lo **ejecuta**; no decide el catálogo. Separar la config como dato permite al
  científico de datos afinar el torneo sin tocar el motor.
- **El gate de selección es humano por diseño.** El flujo produce un **ranking + recomendación**, pero la
  **elección del `best_model.pkl` la confirma el científico de datos**. Es el checkpoint clave de toda la
  tubería (`CLAUDE.md §5`): el motor automatiza el 85–95% (correr el torneo, comparar, recomendar) y deja al
  humano el 5–15% de criterio (elegir el modelo que irá a producción).

## 9. Escalera de capacidades (L0 → Ln) — vista vertical del flujo

> Vista vertical de la *ambición completa* de Modelling (`D-016`). **L0 = lo mínimo** del walking skeleton
> (banda **Tracer Bullet**, `D-017`): ingenuo + un modelo simple sobre el snapshot gold de C1, con gate
> humano simulado. Cada peldaño agrega capacidad.

| Nivel | Capacidad | Qué incluye | Qué difiere de la realidad |
|-------|-----------|-------------|----------------------------|
| **L0** (mínimo / skeleton) | **Ingenuo + 1 modelo + selección trivial** | Lee un `modelling_config.yaml` stub; corre un baseline ingenuo y **un** modelo simple sobre el snapshot gold de C1 con validación temporal básica; escribe un `modelling.json` mínimo y serializa `best_model.pkl`; gate humano representado por un paso de aprobación simple. | Un solo modelo candidato; sin búsqueda de hiperparámetros; sin importancia de variables; sin exportación; el "torneo" tiene un participante. |
| **L1** | **Torneo real + filtro del ingenuo + ranking** | Varios modelos del config compiten; se aplica el **filtro de superar al ingenuo** y se rankea por la métrica; `modelling.json` con ranking y baseline. | Hiperparámetros fijos (sin búsqueda); sin importancia de variables formal; sin exportación; modelado global (no por serie). |
| **L2** | **Búsqueda de hiperparámetros + importancia de variables + exportable** | Rejillas/búsqueda de hiperparámetros del config; importancia de features en `modelling.json`; descarga CSV/Excel; recomendación argumentada al humano. | Validación temporal estándar; modelado por grupo, aún no por serie completa. |
| **L3** | **Modelado por serie/grain + validación robusta + gate formal** | Torneo por serie o por grupo según la cardinalidad del grain (`D-014`); validación temporal robusta (walk-forward); gate de selección humano formalizado con trazabilidad de la decisión. | Sin reentrenamiento programado ni versionado de modelos; catálogo acotado. |
| **Ln** (ambición completa) | **Modelling "como un científico de datos senior"** | Catálogo amplio de modelos, búsqueda de hiperparámetros eficiente, validación walk-forward por serie, baseline ingenuo siempre como piso, importancia/explicabilidad, versionado y registro de modelos, reentrenamiento y replay ligados al contrato, recomendación rica para el gate humano. | Nada: es el objetivo final del flujo. |

> **Nota de ensamblaje:** al cerrar este brief se refleja el estado en `800_persistence/roadmap.md`
> (fila Modelling: columna *Brief* → `planeado`; peldaño previsto para Tracer Bullet → **L0**).

## 10. Siguiente paso

Tras **aprobar este brief**: **diseñar el flujo `050_modelling`** (instancias A/B/C según el modelo plano
`D-009`, workers, política de herramientas, checkpoints canónicos —incluido el **gate de selección
humano**—, durabilidad, rúbrica del evaluador y contrato), reutilizando los patrones transversales ya
validados del motor. El **plan de implementación** viene *después* del diseño (orden del método:
**brief → diseño → plan → construir**, `D-011`). El diseño se materializará en `705_design/050_modelling.md`.
