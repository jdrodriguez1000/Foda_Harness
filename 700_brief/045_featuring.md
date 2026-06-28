# Brief — Flujo 045 Featuring (Materialización de variables → capa gold)

> **Tipo:** Brief de enmarque (alto nivel, previo al diseño agéntico). NO es la definición agéntica fina.
> **Proyecto:** FODA (Forecast Optimization Driven Agentic) — plano de **construcción** del motor.
> **Flujo:** `045` de 14 — `045_featuring` (octavo flujo de la tubería; **materializa** las variables que Exploration propuso).
> **Posición en la tubería:** consume `040_exploration` (`feature_engineering.yaml`) + capa **gold** (`035_derivation`) → entrega a `050_modelling`.
> **Capa de datos que toca:** `gold` (lectura) → **escribe** `gold` (enriquecida con variables nuevas).
> **Fuente de verdad:** `990_documents/expected_workflow.md` (§8 Featuring) + `990_documents/expected_solution.md`.
> **Método de construcción:** `950_guideline/methodology.md` + `950_guideline/principles.md`.
> **Decisiones que lo enmarcan:** `D-001` (dos planos), `D-012` (snapshots), `D-014` (grain producto × geo), `D-015` (walking skeleton), `D-016` (brief + escalera), `D-017` (bandas + numeración) · **Estado:** `BORRADOR` · **Fecha:** `2026-06-28` · **Aprobado por:** `—`.

---

## 0. Aclaración de planos — leer primero

Este brief describe un **componente del MOTOR FODA que estamos fabricando** (plano de *construcción*).
No describe el feature engineering de una empresa concreta: describe la **maquinaria genérica y
reutilizable** que, al *operarse* sobre la capa gold de un cliente arbitrario, **materializa** las
variables nuevas declaradas en `feature_engineering.yaml` y enriquece gold, documentando cada
transformación. El diseño no debe cablear variables fijas: las variables a crear son **dato de entrada**,
no código.

- **Insumo del flujo al operar:** la capa **gold** (demanda agregada) y el **`feature_engineering.yaml`**
  (variables aprobadas, de Exploration). Cambia por cliente.
- **Salida de runtime que produce al operar:** la capa **gold enriquecida** (con las variables nuevas) y
  el **`feature_engineering.json`** (bitácora de derivación de variables, replicable). Pertenecen al
  **plano instancia** (`fda-*`); **nunca** vuelven a la memoria de construcción del motor.
- **Grain del cliente (`D-014`):** las variables se construyen **por serie** (producto × geografía);
  features como lags o ventanas móviles deben calcularse dentro de cada serie, sin mezclar series.

## 1. Objetivo

Transformar la propuesta de variables (`feature_engineering.yaml`) en **columnas reales** sobre la capa
gold: generar las variables nuevas a partir de las existentes (p. ej. de una fecha → día de la semana,
mes, año; lags y ventanas de demanda) y dejar la **matriz de features lista para Modelling**, documentando
cómo se construyó cada una. Featuring **no propone ni decide** qué variables crear (eso fue Exploration +
aprobación humana): las **ejecuta** y deja trazabilidad.

> En una frase: transformar la capa **gold** + `feature_engineering.yaml` en una capa **gold enriquecida**
> con las variables nuevas, documentada en `feature_engineering.json`, lista para `050_modelling`.

## 2. Alcance — qué hace

**Modo Inicio (materialización de variables):**

- **Toma de la propuesta de variables:** lee el **`feature_engineering.yaml`** (aprobado) que define qué
  variables nuevas crear y cómo.
- **Generación de variables:** crea las variables nuevas a partir de las existentes (p. ej. derivadas de
  fecha — día de semana, mes, año; lags de demanda; ventanas móviles; indicadores de festivo), aplicando
  las reglas del YAML sobre gold.
- **Escritura de gold enriquecida:** deposita las variables nuevas en la capa **gold**, dejando la matriz
  de features lista para Modelling.
- **Bitácora de variables:** registra qué se generó y cómo en **`feature_engineering.json`** (variable,
  fórmula/regla, origen): documenta y **permite replicar** la generación en otros archivos del cliente.
- **Entrega descargable:** permite al científico de datos descargar `feature_engineering.json` en CSV o
  Excel.

## 3. Alcance — qué NO hace (límites)

- **No** propone ni decide qué variables crear, ni valida hipótesis → eso es el **flujo `040_exploration`**
  (que produce el `feature_engineering.yaml` que Featuring consume).
- **No** deriva ni agrega la demanda (la variable objetivo ya existe en gold) → eso es el **flujo
  `035_derivation`**.
- **No** limpia datos → eso es el **flujo `030_cleaning`** (capa silver).
- **No** modifica bronze ni silver → los predecesores son inmutables aguas arriba; Featuring enriquece gold.
- **No** entrena, compara ni selecciona modelos → eso es el **flujo `050_modelling`**.
- **No** diseña la **maquinaria agéntica fina** de este flujo (instancias A/B/C, workers, checkpoints,
  rúbrica del evaluador, contratos de herramientas) → eso es el **diseño del flujo `045_featuring`**, paso
  siguiente a este brief.

## 4. Insumos disponibles

| ID | Insumo | Origen |
|----|--------|--------|
| I-1 | Definición del flujo Featuring en la tubería FODA | `990_documents/expected_workflow.md` (§8) |
| I-2 | Arquitectura de capas bronze/silver/gold y visión de planos | `990_documents/expected_solution.md`, `CLAUDE.md §4` |
| I-3 | Metodología y principios de construcción (P*, E*, NC*, patrón A/B/C, modelo plano) | `950_guideline/methodology.md`, `950_guideline/principles.md` |
| I-4 | Memoria de construcción (estado, decisiones, lecciones) | `800_persistence/` (`D-001`, `D-012`, `D-014`, `D-017`) |
| I-5 | Briefs aprobados aguas arriba (forma de gold y del `feature_engineering.yaml`) | `700_brief/040_exploration.md`, `700_brief/035_derivation.md` |

> **Insumo en tiempo de operación (no de construcción):** la capa **gold real** y el
> **`feature_engineering.yaml`** aprobado. Llegan cuando el motor se *opera*, no ahora. (Para construir y
> probar el flujo se usa el **snapshot gold de C1** + un `feature_engineering.yaml` fixture —
> `D-012`/`T-014`.)

## 5. Artefactos esperados (salida del flujo al operar)

| Artefacto | Propósito |
|-----------|-----------|
| **Capa `gold` enriquecida** (con variables nuevas) | Matriz de features lista para entrenar. La consume `050_modelling` (torneo de campeones). |
| **`feature_engineering.json`** (bitácora de variables) | Documenta cómo se construyó cada variable; habilita **reproducir** la generación en otros archivos del cliente y auditar la transformación. |
| **Exportable CSV/Excel** de `feature_engineering.json` | Permite al científico de datos descargar y compartir el detalle de las variables. |

> El **`feature_engineering.yaml`** es **insumo** (propuesta aprobada de Exploration), no salida de este
> flujo. Los *paths*, el esquema exacto de `feature_engineering.json` y la mecánica se fijan en el
> **diseño del flujo** (paso siguiente).

## 6. Criterios de éxito (Done)

1. Las variables del **`feature_engineering.yaml`** quedan **materializadas** como columnas sobre gold.
2. La capa **gold enriquecida** queda escrita y lista para Modelling; la **demanda** (objetivo) se
   preserva intacta.
3. Cada variable queda documentada en **`feature_engineering.json`** (definición, regla, origen), de forma
   **reproducible** sobre otros archivos del cliente.
4. Las variables se construyen **por serie** respetando el grain (lags/ventanas no cruzan series, `D-014`).
5. **Sin fuga de datos futuros:** ninguna variable usa información no disponible en tiempo de inferencia.
6. `feature_engineering.json` es **descargable en CSV o Excel**.
7. **Gate humano (si aplica):** el científico de datos **revisa** el conjunto de features materializadas
   antes de habilitar Modelling (ver `CLAUDE.md §5`).

## 7. Riesgos / advertencias

- **Confusión de planos (`D-001`):** gold enriquecida y `feature_engineering.json` son **runtime de la
  instancia** (`fda-*`), no memoria de construcción.
- **Fuga de datos futuros (data leakage) — riesgo crítico:** materializar un lag/ventana que incluya el
  período a predecir, o una variable construida con información futura, infla el desempeño y arruina el
  modelo en producción. La construcción debe ser **temporalmente segura** por serie.
- **Variables cableadas (anti-patrón):** hard-codear features en el agente en vez de leerlas del
  `feature_engineering.yaml` rompe la reutilización entre clientes. Las variables son **dato**, no código.
- **Mezclar series al calcular features:** un lag/rolling que cruza la frontera entre series (otro
  producto/sede) corrompe la matriz; calcular **dentro** de cada serie del grain.
- **Envenenar aguas abajo (E9):** features irrelevantes o mal construidas degradan el torneo de Modelling
  con ruido y colinealidad. Trazabilidad y revisión humana mitigan.
- **Snapshot stale (al construir):** gold enriquecida de C1 depende del snapshot gold y del yaml fixture;
  si cambian, regenerar (`D-012`).

## 8. Espejo de Cleaning/Derivation: yaml (entrada) → capa + json (salida) — sección específica del flujo

Featuring completa un patrón ya visto en el motor (**reglas como dato + bitácora replicable**), con un
matiz propio de autoría:

- **`feature_engineering.yaml` (entrada):** a diferencia del `data_cleaner.yaml` (autoría 100% humana),
  este YAML lo **propuso la IA** en Exploration y lo **aprobó el humano**. Featuring lo **ejecuta**, no lo
  decide. Separar la propuesta (Exploration) de la materialización (Featuring) permite revisar antes de
  gastar cómputo.
- **`feature_engineering.json` (salida):** bitácora que documenta cómo se construyó cada variable —
  auditable y **replicable** en cargas futuras, igual que `data_cleaning.json` y `data_derivation.json`.
- **Seguridad temporal como invariante:** el feature engineering es donde el **leakage** entra con más
  facilidad; la construcción libre de fuga futura es un requisito de primera clase del diseño, no un
  detalle.

## 9. Escalera de capacidades (L0 → Ln) — vista vertical del flujo

> Vista vertical de la *ambición completa* de Featuring (`D-016`). **L0 = lo mínimo** del walking skeleton
> (banda **Tracer Bullet**, `D-017`): materializar 1 variable de calendario sobre el snapshot gold de C1.
> Cada peldaño agrega capacidad.

| Nivel | Capacidad | Qué incluye | Qué difiere de la realidad |
|-------|-----------|-------------|----------------------------|
| **L0** (mínimo / skeleton) | **Materializar 1 variable → gold enriquecida + bitácora básica** | Lee un `feature_engineering.yaml` stub (p. ej. mes a partir de la fecha), crea la columna sobre el snapshot gold de C1, escribe gold enriquecida y un `feature_engineering.json` básico; handoff a Modelling. | Una sola variable de calendario; sin lags/ventanas; sin exportación; sin chequeo formal de leakage. |
| **L1** | **Conjunto de variables del yaml + bitácora completa** | Materializa todas las variables del `feature_engineering.yaml` (calendario: día de semana, mes, año; indicadores); `feature_engineering.json` documenta cada una. | Sin lags/ventanas móviles; sin exportación; multi-serie básico. |
| **L2** | **Lags / ventanas móviles + multi-serie + exportable** | Variables temporales (lags, medias móviles) calculadas por serie; manejo de la cardinalidad completa del grain; exportación a CSV/Excel. | Sin features por nivel jerárquico; chequeo de leakage manual. |
| **L3** | **Features por grain/nivel + chequeo de leakage + replay** | Variables por nivel jerárquico (familia/sede); validación automática de seguridad temporal (sin fuga futura); replay idempotente entre cargas. | Sin librería de features avanzada ni versionado formal. |
| **Ln** (ambición completa) | **Featuring "como un científico de datos senior"** | Librería rica de features (calendario, clima, precios, promociones, jerárquicas), chequeos automáticos de leakage y colinealidad, conjuntos de features versionados, replay robusto ligado al contrato. | Nada: es el objetivo final del flujo. |

> **Nota de ensamblaje:** al cerrar este brief se refleja el estado en `800_persistence/roadmap.md`
> (fila Featuring: columna *Brief* → `planeado`; peldaño previsto para Tracer Bullet → **L0**).

## 10. Siguiente paso

Tras **aprobar este brief**: **diseñar el flujo `045_featuring`** (instancias A/B/C según el modelo plano
`D-009`, workers, política de herramientas, checkpoints canónicos, durabilidad, rúbrica del evaluador y
contrato), reutilizando los patrones transversales ya validados del motor. El **plan de implementación**
viene *después* del diseño (orden del método: **brief → diseño → plan → construir**, `D-011`). El diseño
se materializará en `705_design/045_featuring.md`.
