# Brief — Flujo 040 Exploration (EDA + validación de hipótesis + propuesta de variables)

> **Tipo:** Brief de enmarque (alto nivel, previo al diseño agéntico). NO es la definición agéntica fina.
> **Proyecto:** FODA (Forecast Optimization Driven Agentic) — plano de **construcción** del motor.
> **Flujo:** `040` de 14 — `040_exploration` (séptimo flujo de la tubería; flujo de **análisis/insight**, no de transformación de datos).
> **Posición en la tubería:** consume `035_derivation` (capa **gold**) + `business_hypothesis.md` (`010_discovery`) → entrega a `045_featuring`.
> **Capa de datos que toca:** `gold` (lectura) — **no escribe** capa nueva: produce un **informe + una propuesta de variables**.
> **Fuente de verdad:** `990_documents/expected_workflow.md` (§7 Exploration) + `990_documents/expected_solution.md`.
> **Método de construcción:** `950_guideline/methodology.md` + `950_guideline/principles.md`.
> **Decisiones que lo enmarcan:** `D-001` (dos planos), `D-012` (snapshots), `D-014` (grain producto × geo), `D-015` (walking skeleton), `D-016` (brief + escalera), `D-017` (bandas + numeración) · **Estado:** `BORRADOR` · **Fecha:** `2026-06-28` · **Aprobado por:** `—`.

---

## 0. Aclaración de planos — leer primero

Este brief describe un **componente del MOTOR FODA que estamos fabricando** (plano de *construcción*).
No describe la exploración de una empresa concreta: describe la **maquinaria genérica y reutilizable** que,
al *operarse* sobre la capa gold de un cliente arbitrario, hace análisis exploratorio, **valida las
hipótesis de negocio** declaradas en Discovery y **propone variables nuevas** para mejorar el pronóstico.
El diseño no debe acoplarse a un dominio ni asumir qué patrones o hipótesis tendrá un cliente concreto.

- **Insumo del flujo al operar:** la capa **gold** (demanda histórica agregada) y el
  **`business_hypothesis.md`** (hipótesis de comportamiento, de Discovery). Cambia por cliente.
- **Salida de runtime que produce al operar:** el **`exploration.json`** (informe exploratorio +
  veredicto de hipótesis) y el **`feature_engineering.yaml`** (propuesta de variables nuevas). Pertenecen
  al **plano instancia** (`fda-*`); **nunca** vuelven a la memoria de construcción del motor.
- **Grain del cliente (`D-014`):** los patrones, tendencias y correlaciones se analizan **por serie/nivel**
  (producto × geografía); una hipótesis puede cumplirse en una familia/sede y no en otra.

## 1. Objetivo

Entender la demanda histórica **antes de modelar**: identificar patrones, tendencias y anomalías;
**contrastar las hipótesis de negocio** que el cliente declaró en Discovery contra los datos reales; y
**proponer variables nuevas** (respaldadas por correlación con la demanda) que mejoren la calidad del
pronóstico. Exploration **no crea las variables ni entrena modelos**: produce **insight documentado** y una
**propuesta de feature engineering** que Featuring ejecutará. Su valor es convertir datos limpios en
**conocimiento accionable** y dirigir el esfuerzo de modelado.

> En una frase: transformar la capa **gold** + `business_hypothesis.md` en un `exploration.json` (patrones,
> tendencias, anomalías y veredicto de hipótesis) y un `feature_engineering.yaml` (variables propuestas)
> para Featuring.

## 2. Alcance — qué hace

**Modo Inicio (exploración de la demanda):**

- **Análisis exploratorio (EDA):** explora la demanda histórica de gold para identificar **patrones,
  tendencias y anomalías**.
- **Informe exploratorio (`exploration.json`):** documenta como mínimo: un **resumen de la información
  histórica**, un **resumen de patrones y tendencias**, y un **resumen de anomalías**.
- **Validación de hipótesis de negocio:** contrasta cada hipótesis del **`business_hypothesis.md`** contra
  los datos (p. ej. "la demanda sube en festivos", "las ventas subieron durante la pandemia") y emite un
  **veredicto** (se cumple / no se cumple / parcial) con evidencia.
- **Estudio de correlación + propuesta de variables:** estudia la correlación entre las variables
  existentes y la **variable objetivo (demanda)** y **sugiere variables nuevas** que podrían mejorar el
  pronóstico (p. ej. día de la semana, mes, festivo, lag de demanda).
- **Generación de `feature_engineering.yaml`:** deja la propuesta de variables nuevas en un YAML que
  Featuring tomará como base.
- **Entrega descargable:** permite al científico de datos descargar `exploration.json` en CSV o Excel.

## 3. Alcance — qué NO hace (límites)

- **No** deriva ni agrega la demanda → eso es el **flujo `035_derivation`** (capa gold) que Exploration
  consume.
- **No** **crea/materializa** las variables nuevas (solo las **propone** en `feature_engineering.yaml`) →
  eso es el **flujo `045_featuring`**.
- **No** modifica gold, silver ni bronze → los lee; no escribe capa de datos.
- **No** entrena, compara ni selecciona modelos → eso es el **flujo `050_modelling`**.
- **No** **declara** las hipótesis (las **valida**) → la declaración es del **flujo `010_discovery`**
  (`business_hypothesis.md`).
- **No** diseña la **maquinaria agéntica fina** de este flujo (instancias A/B/C, workers, checkpoints,
  rúbrica del evaluador, contratos de herramientas) → eso es el **diseño del flujo `040_exploration`**,
  paso siguiente a este brief.

## 4. Insumos disponibles

| ID | Insumo | Origen |
|----|--------|--------|
| I-1 | Definición del flujo Exploration en la tubería FODA | `990_documents/expected_workflow.md` (§7) |
| I-2 | Arquitectura de capas bronze/silver/gold y visión de planos | `990_documents/expected_solution.md`, `CLAUDE.md §4` |
| I-3 | Metodología y principios de construcción (P*, E*, NC*, patrón A/B/C, modelo plano) | `950_guideline/methodology.md`, `950_guideline/principles.md` |
| I-4 | Memoria de construcción (estado, decisiones, lecciones) | `800_persistence/` (`D-001`, `D-012`, `D-014`, `D-017`) |
| I-5 | Briefs aprobados aguas arriba (forma de gold y del `business_hypothesis.md`) | `700_brief/035_derivation.md`, `700_brief/010_discovery.md` |

> **Insumo en tiempo de operación (no de construcción):** la capa **gold real** y el
> **`business_hypothesis.md`** del cliente. Llegan cuando el motor se *opera*, no ahora. (Para construir y
> probar el flujo se usa el **snapshot gold de C1** congelado por Derivation — `D-012`/`T-014`.)

## 5. Artefactos esperados (salida del flujo al operar)

| Artefacto | Propósito |
|-----------|-----------|
| **`exploration.json`** (informe exploratorio) | Resumen de la información histórica + patrones/tendencias + anomalías + **veredicto de las hipótesis** de negocio. Lo revisa el científico de datos y lo comparte con el cliente. |
| **`feature_engineering.yaml`** (propuesta de variables) | Variables nuevas propuestas (respaldadas por correlación con la demanda). Lo consume `045_featuring` como base para materializarlas. |
| **Exportable CSV/Excel** de `exploration.json` | Permite al científico de datos descargar y compartir el análisis. |

> Los *paths*, el esquema exacto de `exploration.json` / `feature_engineering.yaml` y la mecánica se fijan
> en el **diseño del flujo** (paso siguiente).

## 6. Criterios de éxito (Done)

1. Existe un **`exploration.json`** con los tres resúmenes (información histórica, patrones/tendencias,
   anomalías).
2. Cada hipótesis de **`business_hypothesis.md`** recibe un **veredicto con evidencia** (se cumple / no /
   parcial).
3. Existe un **`feature_engineering.yaml`** con variables propuestas, cada una **respaldada por el estudio
   de correlación** con la demanda.
4. El análisis respeta el **grain** donde aplique (patrones/hipótesis reportados por serie/nivel cuando
   sea relevante, `D-014`).
5. `exploration.json` es **descargable en CSV o Excel**.
6. **Gate humano:** el científico de datos **revisa** el veredicto de hipótesis y **aprueba** las
   variables propuestas antes de habilitar Featuring (ver `CLAUDE.md §5`).

## 7. Riesgos / advertencias

- **Confusión de planos (`D-001`):** `exploration.json` y `feature_engineering.yaml` son **runtime de la
  instancia** (`fda-*`), no memoria de construcción.
- **Fuga de datos futuros (data leakage):** proponer variables que incorporen información del futuro
  (p. ej. usar la demanda del período a predecir) infla artificialmente la correlación y arruina el modelo.
  Las variables propuestas deben ser **construibles en tiempo de inferencia**.
- **Correlación ≠ causalidad:** una correlación alta no justifica una variable causal; el veredicto de
  hipótesis y las propuestas deben matizar esto y dejarlo a revisión humana.
- **Envenenar aguas abajo (E9):** un EDA superficial o una propuesta de variables irrelevantes hace que
  Featuring/Modelling trabajen sobre ruido. La revisión humana y el respaldo por correlación mitigan.
- **Promedio engañoso por grain:** un patrón global puede no cumplirse en series concretas; analizar por
  nivel evita conclusiones falsas.
- **Snapshot stale (al construir):** el análisis de C1 depende de su snapshot gold; si cambia el contrato
  upstream, regenerar (`D-012`).

## 8. Validación de hipótesis + propuesta de variables por correlación — sección específica del flujo

Exploration es el **puente entre el negocio y el modelado**. Dos responsabilidades lo distinguen:

- **Validación de hipótesis de negocio:** cierra el ciclo que abrió Discovery. Las hipótesis del
  `business_hypothesis.md` (declaradas como *testeables*) se **contrastan contra los datos** y reciben un
  veredicto con evidencia. Esto da confianza al cliente ("sí, tus festivos sí mueven la demanda") y orienta
  qué variables valen la pena.
- **Propuesta de variables por correlación:** el estudio de correlación entre variables existentes y la
  **demanda** fundamenta qué features proponer en `feature_engineering.yaml`. La propuesta es **insumo**
  para Featuring (que las materializa) y pasa por **aprobación humana**: a diferencia del
  `data_cleaner.yaml` (autoría 100% humana), aquí la IA **propone** y el humano **aprueba**.

## 9. Escalera de capacidades (L0 → Ln) — vista vertical del flujo

> Vista vertical de la *ambición completa* de Exploration (`D-016`). **L0 = lo mínimo** del walking
> skeleton (banda **Tracer Bullet**, `D-017`): EDA básico sobre el snapshot gold de C1. Cada peldaño
> agrega capacidad.

| Nivel | Capacidad | Qué incluye | Qué difiere de la realidad |
|-------|-----------|-------------|----------------------------|
| **L0** (mínimo / skeleton) | **EDA básico + `feature_engineering.yaml` stub** | Sobre el snapshot gold de C1, calcula estadísticos resumidos y una tendencia simple en `exploration.json`; propone 1 variable de calendario en un `feature_engineering.yaml` mínimo; handoff a Featuring. | Sin validación de hipótesis; sin estudio de correlación; sin anomalías; sin exportación; análisis global. |
| **L1** | **Informe exploratorio completo** | `exploration.json` con los tres resúmenes: información histórica, patrones/tendencias y anomalías. | Aún sin validación de hipótesis ni correlación formal. |
| **L2** | **Validación de hipótesis + correlación → propuesta de variables + exportable** | Contrasta `business_hypothesis.md` y emite veredictos; estudio de correlación con la demanda que respalda el `feature_engineering.yaml`; exportación a CSV/Excel. | Análisis poco segmentado por jerarquía; propuestas sin priorización fina. |
| **L3** | **Análisis por grain/nivel + estacionalidad + propuestas priorizadas** | EDA por serie y nivel jerárquico; descomposición de estacionalidad/tendencia; detección de anomalías; propuestas de variables priorizadas por fuerza de correlación y libres de leakage. | Sin pruebas estadísticas formales de hipótesis; sin análisis causal. |
| **Ln** (ambición completa) | **Exploration "como un científico de datos senior"** | EDA rico, pruebas estadísticas de hipótesis, descomposición avanzada, detección robusta de anomalías, propuesta de features justificada y libre de leakage, narrativa de insight lista para el cliente. | Nada: es el objetivo final del flujo. |

> **Nota de ensamblaje:** al cerrar este brief se refleja el estado en `800_persistence/roadmap.md`
> (fila Exploration: columna *Brief* → `planeado`; peldaño previsto para Tracer Bullet → **L0**).

## 10. Siguiente paso

Tras **aprobar este brief**: **diseñar el flujo `040_exploration`** (instancias A/B/C según el modelo plano
`D-009`, workers, política de herramientas, checkpoints canónicos, durabilidad, rúbrica del evaluador y
contrato), reutilizando los patrones transversales ya validados del motor. El **plan de implementación**
viene *después* del diseño (orden del método: **brief → diseño → plan → construir**, `D-011`). El diseño
se materializará en `705_design/040_exploration.md`.
