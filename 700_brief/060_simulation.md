# Brief — Flujo 060 Simulation (Montecarlo + variables de influencia → demanda simulada)

> **Tipo:** Brief de enmarque (alto nivel, previo al diseño agéntico). NO es la definición agéntica fina.
> **Proyecto:** FODA (Forecast Optimization Driven Agentic) — plano de **construcción** del motor.
> **Flujo:** `060` de 14 — `060_simulation` (undécimo flujo de la tubería; **simula** la demanda pronosticada bajo incertidumbre).
> **Posición en la tubería:** consume `055_inferences` (`inferences.json` + predicciones en gold) + `simulation_config.yaml` (👤 humano) → entrega a `065_scenarios` y `070_reporting`.
> **Capa de datos que toca:** `gold` (lectura de predicciones; **escribe** la demanda simulada en gold).
> **Fuente de verdad:** `990_documents/expected_workflow.md` (§10 Simulation) + `990_documents/expected_solution.md`.
> **Método de construcción:** `950_guideline/methodology.md` + `950_guideline/principles.md`.
> **Decisiones que lo enmarcan:** `D-001` (dos planos), `D-012` (snapshots), `D-014` (grain producto × geo), `D-015` (walking skeleton), `D-016` (brief + escalera), `D-017` (bandas + numeración) · **Estado:** `APROBADO` · **Fecha:** `2026-06-28` · **Aprobado por:** `usuario`.

---

## 0. Aclaración de planos — leer primero

Este brief describe un **componente del MOTOR FODA que estamos fabricando** (plano de *construcción*).
No describe la simulación de una empresa concreta: describe la **maquinaria genérica y reutilizable** que,
al *operarse* sobre el pronóstico de un cliente arbitrario, aplica una **simulación Montecarlo** usando el
**MAPE por período** (de Inferences) como desviación y, opcionalmente, las **variables de influencia**
declaradas en `simulation_config.yaml`. El diseño **no debe cablear** las variables: cuáles se usan, con qué
parámetros y por qué producto/serie son **dato de entrada** (`simulation_config.yaml`), y el catálogo de
variables debe ser **extensible** sin tocar el motor.

- **Insumo del flujo al operar:** el **`inferences.json`** (demanda pronosticada + MAPE por período) / las
  predicciones en **gold**, y el **`simulation_config.yaml`** (variables de influencia y sus parámetros).
  Cambia por cliente.
- **Salida de runtime que produce al operar:** la **demanda simulada en la capa gold** (escenarios
  optimista/moderado/pesimista + inventario de seguridad) y el **`simulation.json`**. Pertenecen al **plano
  instancia** (`fda-*`); **nunca** vuelven a la memoria de construcción del motor.
- **Grain del cliente (`D-014`):** la simulación corre **por serie** (producto × geografía) y por período;
  los parámetros de cada variable (p. ej. lead time medio/desviación) se aplican **por producto/serie** según
  el config, sin mezclar series.

## 1. Objetivo

Convertir la **demanda pronosticada** (puntual, de Inferences) en una **demanda simulada bajo incertidumbre**
mediante **simulación Montecarlo**. La fuente primaria de incertidumbre es el **MAPE por período** que
entregó Inferences (la desviación de cada predicción); sobre esa base, el flujo incorpora —**si el
`simulation_config.yaml` lo indica**— variables de influencia como **lead time, TRM e inflación**, con sus
parámetros por producto/serie. El resultado son los escenarios **optimista / moderado / pesimista**, la
**demanda simulada** y el **inventario de seguridad**, listos para Scenarios y Reporting.

> En una frase: transformar **`inferences.json`** (pronóstico + MAPE) + **`simulation_config.yaml`** en la
> **demanda simulada** (optimista/moderado/pesimista + inventario de seguridad) en gold y en `simulation.json`,
> lista para `065_scenarios` y `070_reporting`.

## 2. Alcance — qué hace

**Modo Inicio (simulación Montecarlo):**

- **Lectura del pronóstico:** toma la demanda pronosticada y su **MAPE por período** (de `inferences.json` /
  gold) como base de la simulación.
- **Lectura de la configuración humana:** lee el **`simulation_config.yaml`** que declara **qué variables de
  influencia** usar (lead time, TRM, inflación; subconjunto variable) y sus **parámetros por producto/serie**
  (p. ej. lead time medio 15 días, desviación 3 días).
- **Simulación Montecarlo:** genera múltiples realizaciones de la demanda aplicando la **desviación derivada
  del MAPE** por período y la influencia de las variables activas del config.
- **Escenarios + demanda simulada:** deriva, por serie/período, los escenarios **optimista**, **moderado** y
  **pesimista**, la **demanda simulada** y el **inventario de seguridad**.
- **Escritura en gold:** deposita la demanda simulada en la capa **gold**, lista para Scenarios y Reporting.
- **Bitácora de simulación:** registra supuestos, variables activas, parámetros y resultados en
  **`simulation.json`** (documenta y **permite replicar** la simulación).
- **Entrega descargable:** permite al científico de datos descargar `simulation.json` en CSV o Excel.

## 3. Alcance — qué NO hace (límites)

- **No** genera el pronóstico puntual ni el MAPE → eso es el **flujo `055_inferences`** (Simulation **consume**
  el MAPE como desviación).
- **No** entrena ni selecciona modelos → flujo `050_modelling`.
- **No** responde preguntas "¿qué pasa si…?" abiertas del usuario → eso es el **flujo `065_scenarios`**
  (que **reutiliza** Inferences + Simulation). Simulation produce los escenarios **estadísticos**
  (optimista/moderado/pesimista) por incertidumbre, no los escenarios de negocio hipotéticos.
- **No** calcula márgenes, precios, costos ni costo de oportunidad → eso es el **flujo `070_reporting`**
  (aunque el **inventario de seguridad** sí se deriva aquí, por ser parte de la simulación de demanda).
- **No** define el catálogo de variables de influencia ni sus parámetros (son **dato** del
  `simulation_config.yaml`, autoría humana) → no se cablean en el agente; el catálogo debe ser **extensible**.
- **No** diseña la **maquinaria agéntica fina** de este flujo (instancias A/B/C, workers, checkpoints,
  rúbrica del evaluador, contratos de herramientas) → eso es el **diseño del flujo `060_simulation`**, paso
  siguiente a este brief.

## 4. Insumos disponibles

| ID | Insumo | Origen |
|----|--------|--------|
| I-1 | Definición del flujo Simulation en la tubería FODA | `990_documents/expected_workflow.md` (§10 Simulation) |
| I-2 | Arquitectura de capas bronze/silver/gold y visión de planos | `990_documents/expected_solution.md`, `CLAUDE.md §4` |
| I-3 | Metodología y principios de construcción (P*, E*, NC*, patrón A/B/C, modelo plano) | `950_guideline/methodology.md`, `950_guideline/principles.md` |
| I-4 | Memoria de construcción (estado, decisiones, lecciones) | `800_persistence/` (`D-001`, `D-012`, `D-014`, `D-017`) |
| I-5 | Briefs aprobados aguas arriba (forma del `inferences.json` y del MAPE por período) | `700_brief/055_inferences.md`, `700_brief/050_modelling.md` |

> **Insumo en tiempo de operación (no de construcción):** el **`inferences.json`** real (pronóstico + MAPE) y
> el **`simulation_config.yaml`** (autoría humana: variables activas y parámetros por producto/serie). Llegan
> cuando el motor se *opera*, no ahora. (Para construir y probar el flujo se usa el **snapshot gold de C1** +
> un `inferences.json` y un `simulation_config.yaml` fixture — `D-012`/`T-014`.)

## 5. Artefactos esperados (salida del flujo al operar)

| Artefacto | Propósito |
|-----------|-----------|
| **Demanda simulada en la capa `gold`** | Escenarios optimista/moderado/pesimista + demanda simulada + inventario de seguridad por serie/período. La consumen `065_scenarios` y `070_reporting`. |
| **`simulation.json`** (bitácora de simulación) | Documenta supuestos, variables activas, parámetros y resultados; soporta auditoría y **replay** de la simulación. |
| **Exportable CSV/Excel** de `simulation.json` | Permite al científico de datos descargar y compartir los resultados de la simulación. |

> El **`simulation_config.yaml`** es **insumo** (autoría humana), no salida de este flujo. Los *paths*, el
> esquema exacto de `simulation.json`, el número de realizaciones Montecarlo y la mecánica de cada variable
> se fijan en el **diseño del flujo** (paso siguiente).

## 6. Criterios de éxito (Done)

1. La simulación usa el **MAPE por período** de Inferences como desviación base, por **serie** y **período**
   (`D-014`).
2. Las **variables de influencia activas** del `simulation_config.yaml` se aplican con sus parámetros por
   producto/serie; las **no declaradas se omiten** sin romper el flujo (subconjunto variable: 0, 1, 2 o más).
3. El catálogo de variables es **extensible**: agregar una variable nueva al config no exige cambiar el motor.
4. Se producen, por serie/período, los escenarios **optimista / moderado / pesimista**, la **demanda
   simulada** y el **inventario de seguridad**, escritos en **gold**.
5. **`simulation.json`** documenta supuestos, variables activas, parámetros y resultados de forma
   **reproducible**.
6. `simulation.json` es **descargable en CSV o Excel**.
7. **Gate humano (si aplica):** el científico de datos **revisa** los supuestos y escenarios antes de
   habilitar Reporting (ver `CLAUDE.md §5`).

## 7. Riesgos / advertencias

- **Confusión de planos (`D-001`):** demanda simulada en gold y `simulation.json` son **runtime de la
  instancia** (`fda-*`), no memoria de construcción.
- **MAPE de entrada erróneo:** la simulación hereda la calidad del MAPE de Inferences; un MAPE mal calculado
  produce escenarios sin sustento. (Riesgo aguas arriba; aquí se asume el contrato de `055`.)
- **Variables cableadas (anti-patrón):** hard-codear lead time/TRM/inflación en el agente rompe la
  reutilización y la **extensibilidad**. Las variables y sus parámetros son **dato** (`simulation_config.yaml`).
- **Subconjunto no respetado:** asumir que siempre están las tres variables, o fallar cuando faltan, viola el
  requisito de **opcionalidad** (a veces ninguna, a veces solo una o dos).
- **Parámetros por serie mal aplicados:** usar un lead time global cuando el config lo define por producto, o
  mezclar parámetros entre series, corrompe la simulación (respetar el grain `D-014`).
- **Determinismo/replay:** una simulación Montecarlo sin semilla controlada no es reproducible; `simulation.json`
  debe permitir **replicar** el resultado (semilla/realizaciones documentadas).
- **Envenenar aguas abajo (E9):** escenarios mal calibrados contaminan Scenarios y Reporting (inventario de
  seguridad, costo de oportunidad). Trazabilidad y revisión humana mitigan.
- **Sobre-ingeniería temprana (E4):** en el skeleton, simular solo con el MAPE (sin variables de influencia);
  las variables entran en peldaños superiores.

## 8. `simulation_config.yaml`: variables de influencia opcionales y extensibles — sección específica del flujo

La pieza distintiva de Simulation es que **el humano parametriza la incertidumbre** más allá del MAPE:

- **Dos fuentes de variabilidad.** (1) La **desviación estadística** del pronóstico, derivada del **MAPE por
  período** (siempre presente, viene de Inferences). (2) Las **variables de influencia de negocio**
  declaradas por el humano (opcionales).
- **`simulation_config.yaml` (entrada 👤 humana).** Declara, **por producto/serie**, qué variables aplicar y
  con qué parámetros. Variables iniciales: **lead time**, **TRM**, **inflación**. Ejemplo: *producto1 →
  lead time medio 15 días, desviación 3 días* ⇒ la demanda simulada de producto1 se ve afectada por esa
  distribución de lead time.
- **Opcionalidad (subconjunto variable).** Pueden usarse **ninguna, una, dos o las tres** variables, y el
  subconjunto puede diferir por producto. El flujo debe comportarse correctamente con cualquier combinación,
  incluido el caso "solo MAPE, sin variables".
- **Extensibilidad por diseño.** El catálogo de variables **crecerá con el tiempo** (otras variables de
  influencia). El diseño debe tratar las variables como **entradas declarativas** —no como ramas cableadas—
  de modo que sumar una variable sea editar el YAML, no el motor. Es el mismo principio "reglas como dato"
  de `data_cleaner.yaml` / `modelling_config.yaml`.

## 9. Escalera de capacidades (L0 → Ln) — vista vertical del flujo

> Vista vertical de la *ambición completa* de Simulation (`D-016`). **L0 = lo mínimo** del walking skeleton
> (banda **Tracer Bullet**, `D-017`): Montecarlo solo con el MAPE sobre C1, sin variables de influencia.
> Cada peldaño agrega capacidad.

| Nivel | Capacidad | Qué incluye | Qué difiere de la realidad |
|-------|-----------|-------------|----------------------------|
| **L0** (mínimo / skeleton) | **Montecarlo solo con MAPE → 3 escenarios (1 serie)** | Lee el MAPE de `inferences.json` para una serie de C1, corre Montecarlo con semilla fija y deriva optimista/moderado/pesimista + demanda simulada; escribe en gold y un `simulation.json` básico; handoff a Reporting. | Una serie; sin variables de influencia; sin inventario de seguridad formal; sin exportación. |
| **L1** | **Multi-serie + inventario de seguridad + bitácora completa** | Simula todas las series del grain; deriva inventario de seguridad por serie/período; `simulation.json` documenta supuestos y resultados. | Aún sin variables de influencia (solo MAPE); sin exportación. |
| **L2** | **1–N variables de influencia del config + exportable** | Aplica lead time / TRM / inflación según `simulation_config.yaml`, con parámetros por producto/serie y **subconjunto opcional**; descarga CSV/Excel. | Catálogo de variables acotado; sin re-simulación incremental. |
| **L3** | **Catálogo extensible + replay determinista + gate formal** | Variables como entradas declarativas extensibles (sumar una = editar YAML); replay reproducible (semilla/realizaciones versionadas); revisión humana formal de supuestos. | Sin acoplamiento aún a monitoreo/escenarios avanzados. |
| **Ln** (ambición completa) | **Simulation "como un científico de datos senior"** | Montecarlo robusto multi-serie con MAPE + catálogo rico y extensible de variables de influencia (lead time, TRM, inflación, …), inventario de seguridad afinado, replay determinista, supuestos auditables y ligados al contrato. | Nada: es el objetivo final del flujo. |

> **Nota de ensamblaje:** al cerrar este brief se refleja el estado en `800_persistence/roadmap.md`
> (fila Simulation: columna *Brief* → `planeado`; peldaño previsto para Tracer Bullet → **L0**).

## 10. Siguiente paso

Tras **aprobar este brief**: **diseñar el flujo `060_simulation`** (instancias A/B/C según el modelo plano
`D-009`, workers, política de herramientas, checkpoints canónicos, durabilidad, rúbrica del evaluador y
contrato), reutilizando los patrones transversales ya validados del motor. El **plan de implementación**
viene *después* del diseño (orden del método: **brief → diseño → plan → construir**, `D-011`). El diseño se
materializará en `705_design/060_simulation.md`.
