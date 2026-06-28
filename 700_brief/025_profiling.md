# Brief — Flujo 025 Profiling (Salud de los datos + pareto)

> **Tipo:** Brief de enmarque (alto nivel, previo al diseño agéntico). NO es la definición agéntica fina.
> **Proyecto:** FODA (Forecast Optimization Driven Agentic) — plano de **construcción** del motor.
> **Flujo:** `025` de 14 — `025_profiling` (cuarto flujo de la tubería; flujo de **diagnóstico**, no de transformación).
> **Posición en la tubería:** consume `020_ingestion` (capa **bronze**) → entrega a `030_cleaning`.
> **Capa de datos que toca:** `bronze` (lectura) — **no escribe** capa nueva: produce un **diagnóstico**, no transforma datos.
> **Fuente de verdad:** `990_documents/expected_workflow.md` (§4 Profiling) + `990_documents/expected_solution.md`.
> **Método de construcción:** `950_guideline/methodology.md` + `950_guideline/principles.md`.
> **Decisiones que lo enmarcan:** `D-001` (dos planos), `D-012` (snapshots), `D-014` (grain producto × geo), `D-015` (walking skeleton), `D-016` (brief + escalera), `D-017` (bandas + numeración) · **Estado:** `APROBADO` · **Fecha:** `2026-06-28` · **Aprobado por:** `usuario`.

---

## 0. Aclaración de planos — leer primero

Este brief describe un **componente del MOTOR FODA que estamos fabricando** (plano de *construcción*).
No describe el perfilado de una empresa concreta: describe la **maquinaria genérica y reutilizable** que,
al *operarse* sobre la capa bronze de un cliente arbitrario, mide la **salud de los datos** y la comunica
como un **índice + pareto** que orienta la limpieza. El diseño no debe acoplarse a un dominio ni asumir
qué problemas tendrá un cliente concreto.

- **Insumo del flujo al operar:** la capa **bronze** del cliente (de Ingestion) + los contratos
  (`map_client_data.json`, `contract_data.json`) para conocer el grain y la periodicidad esperada. Cambia
  por cliente.
- **Salida de runtime que produce al operar:** el **informe de salud de datos** (índice %, desglose por
  tipo de problema, pareto) y su versión **descargable** (CSV/Excel). Pertenece al **plano instancia**
  (`fda-*`); **nunca** vuelve a la memoria de construcción del motor.
- **Grain del cliente (`D-014`):** la salud se mide y reporta **por serie/nivel** (producto × geografía):
  qué productos/sedes están sanos y cuáles no. Caso especial: productos con **periodicidad de entrega
  menor a la mínima permitida** (series demasiado ralas para predecir con precisión).

## 1. Objetivo

Determinar la **salud de los datos** del cliente sobre la capa bronze y comunicarla de forma accionable:
un **índice de salud** (porcentaje), un **desglose por tipo de problema** y un **pareto** que prioriza qué
corregir para que el modelo prediga con precisión. Profiling **no corrige nada**: diagnostica y prioriza;
la corrección se decide y ejecuta en Cleaning. Su valor es dar al cliente y al científico de datos una
**foto honesta y priorizada** del estado de la información antes de invertir en limpieza y modelado.

> En una frase: transformar la capa **bronze** en un **informe de salud de datos** (índice % + desglose +
> pareto, descargable) que orienta la limpieza en `030_cleaning`.

## 2. Alcance — qué hace

**Modo Inicio (diagnóstico de la carga):**

- **Detección de problemas de calidad:** identifica sobre bronze:
  - **Productos bajo periodicidad mínima:** series con periodicidad de entrega menor a la mínima
    permitida (no permiten predicciones precisas).
  - **Información faltante**, **duplicada**, **inconsistente**, **desactualizada** e **incompleta**.
- **Cálculo del índice de salud:** un **porcentaje** global (p. ej. 85% sano / 15% a corregir).
- **Desglose por tipo de problema:** porcentaje de afectación de cada tipo (p. ej. 15% incompletos, 10%
  duplicados, 5% inconsistentes…).
- **Pareto de prioridades:** ordena los problemas por afectación e indica **cuáles** resolver primero para
  el mayor impacto en la calidad de las predicciones.
- **Entrega descargable:** permite al científico de datos descargar el informe en **CSV o Excel**.
- **Handoff:** deja el diagnóstico disponible para que Cleaning construya el `data_cleaner.yaml`.

## 3. Alcance — qué NO hace (límites)

- **No** carga datos ni crea bronze → eso es el **flujo `020_ingestion`** (que Profiling consume).
- **No** corrige, imputa, deduplica ni elimina registros → eso es el **flujo `030_cleaning`** (capa
  silver). Profiling **solo diagnostica**.
- **No** define las **reglas** de limpieza (`data_cleaner.yaml`) → eso lo construye Cleaning con el
  cliente (Profiling las **informa/prioriza**, no las decide).
- **No** agrega ni deriva la demanda → eso es el **flujo `035_derivation`** (gold).
- **No** modifica bronze (lo lee; bronze es inmutable, `020_ingestion`).
- **No** valida hipótesis de negocio ni explora correlaciones → eso es el **flujo `040_exploration`**.
- **No** diseña la **maquinaria agéntica fina** de este flujo (instancias A/B/C, workers, checkpoints,
  rúbrica del evaluador, contratos de herramientas) → eso es el **diseño del flujo `025_profiling`**,
  paso siguiente a este brief.

## 4. Insumos disponibles

| ID | Insumo | Origen |
|----|--------|--------|
| I-1 | Definición del flujo Profiling en la tubería FODA | `990_documents/expected_workflow.md` (§4) |
| I-2 | Arquitectura de capas bronze/silver/gold y visión de planos | `990_documents/expected_solution.md`, `CLAUDE.md §4` |
| I-3 | Metodología y principios de construcción (P*, E*, NC*, patrón A/B/C, modelo plano) | `950_guideline/methodology.md`, `950_guideline/principles.md` |
| I-4 | Memoria de construcción (estado, decisiones, lecciones) | `800_persistence/` (`D-001`, `D-012`, `D-014`, `D-017`) |
| I-5 | Briefs aprobados aguas arriba (forma de bronze y del grain/periodicidad) | `700_brief/020_ingestion.md`, `700_brief/015_onboarding.md`, `700_brief/010_discovery.md` |

> **Insumo en tiempo de operación (no de construcción):** la capa **bronze real** del cliente. Llega
> cuando el motor se *opera*, no ahora. (Para construir y probar el flujo se usa el **snapshot bronze de
> C1** congelado por Ingestion — `D-012`/`T-014`.)

## 5. Artefactos esperados (salida del flujo al operar)

| Artefacto | Propósito |
|-----------|-----------|
| **`data_health.json`** (informe de salud: índice % + desglose por tipo de problema + pareto) | Foto priorizada del estado de los datos. Lo consume `030_cleaning` para orientar el `data_cleaner.yaml`; lo revisa el científico de datos. |
| **Exportable `data_health.csv` / `data_health.xlsx`** | Permite al científico de datos descargar y compartir el diagnóstico. |

> El nombre canónico del artefacto es **`data_health.json`** (fijado en `700_brief/000_general_process.md`,
> ya que la fuente no lo nombraba). El **esquema exacto**, los *paths* y la mecánica de la exportación se
> fijan en el **diseño del flujo** (paso siguiente).

## 6. Criterios de éxito (Done)

1. Se calcula un **índice de salud** (porcentaje global) sobre la capa bronze.
2. Existe un **desglose por tipo de problema** (faltante, duplicada, inconsistente, desactualizada,
   incompleta) con su porcentaje de afectación.
3. Se identifican los **productos bajo periodicidad mínima** (series no predecibles con precisión).
4. Se entrega un **pareto** que prioriza los problemas por impacto.
5. El informe es **descargable en CSV o Excel**.
6. El diagnóstico se reporta **por grain** donde aplique (qué series/niveles están afectados), coherente
   con `map_client_data.json` (`D-014`).
7. **Gate humano:** el **científico de datos revisa** el informe de salud antes de habilitar Cleaning
   (decide si la calidad amerita corrección y con qué prioridad; ver `CLAUDE.md §5`).

## 7. Riesgos / advertencias

- **Confusión de planos (`D-001`):** el informe de salud es **runtime de la instancia** (`fda-*`), no
  memoria de construcción.
- **Cruzar a corregir (anti-patrón):** Profiling **diagnostica, no limpia**. Imputar/eliminar aquí
  invade Cleaning y rompe la trazabilidad bronze→silver.
- **Envenenar aguas abajo (E9):** un diagnóstico erróneo (subestimar problemas, pareto mal priorizado)
  hace que Cleaning corrija lo que no es y deje pasar lo que importa, degradando el modelo. Métricas
  verificables y revisión humana son la mitigación.
- **Índice engañoso:** un % de salud global puede ocultar que **series críticas** (alta rotación) están
  enfermas mientras el promedio luce sano. Reportar por grain/nivel mitiga el promedio engañoso.
- **Periodicidad mínima mal fijada:** si el umbral de periodicidad no se toma del contrato, se marcan
  como "no predecibles" series que sí lo son (o viceversa).
- **Snapshot stale (al construir):** el perfil de C1 depende de su snapshot bronze; si cambia el contrato
  upstream hay que regenerarlo (`D-012`).

## 8. Índice de salud, pareto y periodicidad mínima — sección específica del flujo

El valor diferencial de Profiling está en **cuantificar y priorizar**, no solo en listar problemas:

- **Índice de salud (%):** una métrica única y comprensible para el cliente ("85% sano"). Debe ser
  **reproducible** (misma carga → mismo índice) y **descomponible** en el desglose por tipo de problema.
- **Pareto:** la regla 80/20 aplicada a la calidad de datos — concentrar el esfuerzo de limpieza donde
  está el mayor impacto. Es lo que convierte el diagnóstico en **plan de acción** para Cleaning.
- **Periodicidad mínima permitida:** concepto propio del forecasting. Series con entregas demasiado
  espaciadas frente al umbral (tomado del contrato/periodicidad) **no son predecibles con precisión** y
  deben señalarse explícitamente: no es "dato sucio", es "dato insuficiente para el objetivo".

## 9. Escalera de capacidades (L0 → Ln) — vista vertical del flujo

> Vista vertical de la *ambición completa* de Profiling (`D-016`). **L0 = lo mínimo** del walking
> skeleton (banda **Tracer Bullet**, `D-017`): índice de salud básico sobre el snapshot bronze de C1.
> Cada peldaño agrega capacidad.

| Nivel | Capacidad | Qué incluye | Qué difiere de la realidad |
|-------|-----------|-------------|----------------------------|
| **L0** (mínimo / skeleton) | **Índice de salud básico + handoff** | Sobre el snapshot bronze de C1, calcula un índice de salud simple (p. ej. % de faltantes/duplicados) y emite el informe + handoff a Cleaning. | Pocos tipos de problema; sin pareto; sin periodicidad mínima; sin exportación; índice global (no por grain). |
| **L1** | **Desglose completo de tipos de problema + índice descomponible** | Cubre los tipos: faltante, duplicada, inconsistente, desactualizada, incompleta; índice global descomponible en el desglose por tipo. | Aún sin pareto ni exportación; sin periodicidad mínima. |
| **L2** | **Pareto + productos bajo periodicidad mínima + exportable** | Pareto de prioridades por impacto; detección de series bajo periodicidad mínima; exportación a CSV/Excel. | Diagnóstico global/poco segmentado por jerarquía. |
| **L3** | **Salud por grain/nivel + recomendaciones priorizadas** | Salud por serie y por nivel jerárquico (familia/categoría/sede); recomendaciones priorizadas que alimentan directamente el `data_cleaner.yaml` de Cleaning. | Sin detección estadística avanzada de anomalías; sin comparabilidad entre cargas. |
| **Ln** (ambición completa) | **Profiling "como un científico de datos senior"** | Detección estadística de anomalías y outliers, perfilado por nivel jerárquico, recomendaciones accionables ligadas a reglas de limpieza, comparabilidad entre cargas/versiones, alertas tempranas de degradación de calidad. | Nada: es el objetivo final del flujo. |

> **Nota de ensamblaje:** al cerrar este brief se refleja el estado en `800_persistence/roadmap.md`
> (fila Profiling: columna *Brief* → `planeado`; peldaño previsto para Tracer Bullet → **L0**).

## 10. Siguiente paso

Tras **aprobar este brief**: **diseñar el flujo `025_profiling`** (instancias A/B/C según el modelo plano
`D-009`, workers, política de herramientas, checkpoints canónicos, durabilidad, rúbrica del evaluador y
contrato), reutilizando los patrones transversales ya validados del motor. El **plan de implementación**
viene *después* del diseño (orden del método: **brief → diseño → plan → construir**, `D-011`). El diseño
se materializará en `705_design/025_profiling.md`.
