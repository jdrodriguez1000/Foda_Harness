# Progress — Motor FODA

> Estado general del proyecto que construye el motor FODA (Forecast Optimization Driven Agentic).
> Aquí se registra, a grandes rasgos, lo realizado, el punto actual y lo que sigue.

---

## Índice
- [Resumen ejecutivo](#resumen-ejecutivo)
- [Estado actual](#estado-actual)
- [Hitos completados](#hitos-completados)
- [Próximo paso](#próximo-paso)
- [Bitácora](#bitácora)

---

## Resumen ejecutivo

El proyecto construye **FODA**, un motor (harness) reutilizable e instalable que replica el
trabajo de los científicos de datos de Sabbia Solutions & Services para la planeación de demanda
con ML. El motor se instala en carpetas externas (una **instancia por cliente**) donde se construye
la solución concreta. El objetivo es automatizar el 85–95% del trabajo con agentes de IA y dejar al
científico de datos como revisor/aprobador.

- **Motor:** nomenclatura `foda-*`. Memoria de construcción en `800_persistence/`.
- **Instancia:** nomenclatura `fda-*`. Una por cliente, carpeta externa, runtime aislado.
- **Puente:** instalador de terminal (`./install.sh`).

## Estado actual

**Fase:** Fase 1 de `D-015` — **T-014 CERRADA**: la infraestructura del **golden client C1** está construida y
verificada. Postgres 17 corre en **Docker** (`foda_golden_db`, `localhost:55432`, schema `golden_client`, `D-028`);
el **generador** determinista emite la **fuente cruda** de C1 (7 SKUs × 36 meses, pico de diciembre, ruido de
calidad, hold-out K=6); los **cuestionarios** pre-respondidos alimentan Discovery L0. **Próxima tarea: T-021**
(protocolo agéntico de los pasos restantes de `D-021`) y luego la **primera celda `010_discovery`**.
(Fase 0 cerrada: 14 briefs aprobados. T-023 cerrada: stack decidido `D-023..D-027`.)
**Punto actual:** los 14 briefs (`010`–`075`) viven en `700_brief/`, todos en estado **APROBADO**, cada
uno con su **escalera de capacidades L0→Ln** (`D-016`). El **mapa de procesos oficial**
`700_brief/000_general_process.md` está **completo (14/14)**: entradas/salidas por workflow + tabla
maestra de artefactos con nombres canónicos en inglés (`D-018`). El `roadmap.md` tiene la columna *Brief*
en `aprobado (L0→Ln)` para los 14 flujos y la columna *Tracer Bullet* marcada como `planeado (L0)`.
**Cerrado en esta sesión:** redactados los briefs `050`–`075` (Modelling, Inferences, Simulation,
Scenarios, Reporting, Monitoring); fijadas las **configs de autoría humana** `modelling_config.yaml`,
`simulation_config.yaml`, `scenarios_config.yaml` con la convención `<flujo>_config.yaml` y el principio
"reglas como dato" (`D-019`); resuelto que los **parámetros financieros** de Reporting se **leen de
bronze** (`D-019`); `075` agrupa **Monitoring + Alerting** y cierra el ciclo. Todos los briefs aprobados.
**Cerrado en esta sesión:** **T-017 completada** — escritos y **APROBADOS** el `slice_contract.md` + `bdd.md`
del **Tracer Bullet** en `703_definition/tracer-bullet/`. Definen los **14 flujos en su peldaño L0 alineado a la
letra de cada brief** (010→075), las transversales **TR-1/TR-2** (TR-3/TR-4 diferidas), el orden de la
tubería, el **Done end-to-end** (margen bruto por serie + cierre de ciclo) y el **hold-out de Monitoring**.
Se ejecutó el **protocolo agéntico de "Definir"** (`D-021`): la sesión principal orquestó, se escribieron
los borradores y un **revisor en contexto fresco** los auditó (veredicto inicial `REQUIERE SUBSANACIÓN`:
varias filas etiquetaban "L0" un alcance mayor/menor que el L0 del brief). **Subsanado** bajando el slice a
la letra del brief en 010/050/060/065/070/075 y documentando el único desvío deliberado (cardinalidad: la
banda corre C1 completo ~5–10 series aunque varios briefs definen L0 sobre 1 serie). Gate P5 cerrado con la
identidad de git. Lección `L-009`.
**Cerrado en sesiones recientes:** definido el **método de construcción por vertical slice** (`D-021`):
dos niveles (banda → `slice_contract`; celda flujo×banda → diseñar/ejecutar/probar/verificar), estructura
de carpetas `705_design/`/`710_plan/`/`720_build/<banda>/<flujo>/` espejo de Caden, y el **protocolo
agéntico del paso "Definir"** (sesión principal A + escritor + revisor independiente + gate humano).
Aclarado que las **bandas son madurez del motor, no estado de la instancia**. Creadas y aprobadas las
dos plantillas del paso "Definir" (`703_definition/foda-slice-contract-template.md` y `…/foda-bdd-template.md`).
**Cerrado en esta sesión:** **T-002 completada** — creado el **árbol de carpetas** del motor (`D-021 §4`):
carriles `705_design/tracer-bullet/`, `710_plan/tracer-bullet/`, `720_build/tracer-bullet/<flujo>/` con las
6 subcarpetas (`agents`/`skills`/`schemas`/`contract`/`deliverables`/`evaluation`) para los 14 flujos,
`720_build/_transversal/{TR-1..TR-4}` y `720_build/golden_client/snapshots/`. README por carril explicando
su paso del ciclo, convención de nombres y notas. `CLAUDE.md §6` actualizado con la estructura completa.
**Próximo paso (REPRIORIZADO):** **T-023** — **decidir el stack tecnológico de la instancia** (`D-022`, lección
`L-011`) **antes de iniciar cualquier vertical slice**. Se detectó que lo definido hasta ahora es la
arquitectura **agéntica** y el **contrato de datos**, pero **nunca el stack** (lenguaje/ML, motor de datos
físico de bronze/silver/gold, forma de la app, patrones). T-023 es **bloqueante** y **precede a T-014**
(el golden client necesita el formato de bronze) y a toda celda del Tracer Bullet.

## Hitos completados

| Fecha | Hito |
|-------|------|
| 2026-06-27 | Creada la carpeta `800_persistence/` con los 4 archivos de memoria (progress, tasks, lessons, decisions). |
| 2026-06-27 | Creado `CLAUDE.md` con las instrucciones para todos los agentes de Claude Code. |
| 2026-06-27 | Creada la carpeta `.claude/` con `commands/` y los settings de proyecto y local. |
| 2026-06-27 | Creados los comandos `foda-progress` (cierre de sesión) y `foda-next` (inicio de sesión). |
| 2026-06-27 | Inicializado git (rama `main`), agregado `.gitignore`, conectado remoto y primer commit + push (`8df2967`). |
| 2026-06-27 | Agregado `.gitattributes` y fijado `model: sonnet` en los comandos de sesión. |
| 2026-06-27 | Agregada línea de auto-reporte de modelo en los comandos para verificar qué modelo ejecuta. |
| 2026-06-27 | Adaptado `950_guideline/methodology.md` a FODA (T-011): 13 flujos como fases, planos `foda-/fda-`, bronze/silver/gold, subagentes anidados. Decisiones `D-004`/`D-005`, lección `L-002`. |
| 2026-06-27 | Agregado el flujo **Scenarios** (¿qué pasa si…?) tras *Simulation*: pipeline ahora de **14 flujos**. Actualizados `methodology.md` (§2 tabla + referencias) y `expected_workflow.md`. Detalle del flujo pendiente. |
| 2026-06-27 | Agregadas **Normas de Comportamiento** (NC-1 a NC-6) a `950_guideline/principles.md` tras los estándares E1–E12. Actualizado `CLAUDE.md` (§4 ahora con 14 flujos en lugar de 13). |
| 2026-06-27 | Resuelto el consumo de créditos por Sonnet 1M: `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` en `.claude/settings.json` y `foda-progress` fijado en `model: claude-sonnet-4-6` (200K). Decisión `D-006`, lección `L-003`. `foda-next` sin cambios. |
| 2026-06-27 | Reactivada la ventana de 1M al volver el default a Opus 4.8 (1M incluido): se quitó `CLAUDE_CODE_DISABLE_1M_CONTEXT` de `.claude/settings.json` (`"env": {}`). Decisión `D-007` (reemplaza `D-006`). |
| 2026-06-27 | Resuelto el conflicto Opus-1M vs Sonnet-200K sin desactivar el 1M global: se ancló el alias `sonnet` a 200K con `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-4-6` en `.claude/settings.json`. `foda-progress` usa `model: sonnet` (alias), `foda-next` `model: haiku`. Corregido el frontmatter roto de `foda-progress.md` (`yo ---`→`---`). Decisión `D-008`, lección `L-004`. |
| 2026-06-27 | Detectado y corregido (de nuevo) el frontmatter roto de `foda-progress.md`: `model: model: sonnet`→`model: sonnet`. Por la línea inválida el comando se ejecutó con Haiku 4.5 en vez de Sonnet 200K. Lección `L-005`. |
| 2026-06-27 | Estudiado el harness de referencia **Caden** (`Caden_Harness/`) y cerrada la arquitectura de FODA: **modelo plano** (`D-009`, reemplaza el anidamiento de `D-005`), **B/C por flujo** (`D-010`) y **método brief→diseño→plan→build flujo por flujo** (`D-011`). Adaptada `methodology.md` (§3, §3.1, §4.1, §4.2, §12.2, §12.3). Lección `L-006`. Tarea `T-012`. |
| 2026-06-27 | Resuelto el reto de la tubería acumulativa al construir flujo por flujo: se adopta **golden client + snapshots cacheados** (`D-012`, híbrido) en vez de re-ejecutar la cadena; aprovecha la inmutabilidad bronze/silver/gold. Nueva tarea de infraestructura `T-014`. |
| 2026-06-27 | Definida la **complejidad del cliente como matriz 2×2** (jerarquía producto × geografía = grain/cardinalidad de series): generador sintético parametrizado, fixtures escalonados (C1 ya, C4 estrés, C2/C3 bajo demanda) y jerarquías capturadas en el contrato de Discovery/Onboarding (`D-014`). Amplía `T-014`; nueva `T-015`. |
| 2026-06-28 | **Enmendada la estrategia de construcción** para acortar el time-to-MVP: enfoque por fases / **walking skeleton** (`D-015`, enmienda `D-011`) — brief de los 14 → slice fina end-to-end sobre C1 → profundización por valor. **Control en dos vistas** (`D-016`): escalera de capacidades L0→Ln en cada brief + nueva **matriz `roadmap.md`** (workflow × iteración). Lección `L-007`. Nuevas tareas `T-016`/`T-017`/`T-018`/`T-019`; reordenadas las pendientes. Creado `800_persistence/roadmap.md`. |
| 2026-06-28 | **Creada la plantilla de brief FODA** (`T-018`, `D-016`): `700_brief/foda-brief-template.md`. Estructura de Caden (objetivo, alcance qué hace/qué NO, insumos, artefactos, Done, riesgos, siguiente paso) adaptada a FODA (dos planos `D-001`, tubería de 14 flujos, capas bronze/silver/gold, grain `D-014`, gate del científico de datos) **+ sección distintiva §9 "Escalera de capacidades" L0→Ln** que se ensambla en `roadmap.md`. Nueva carpeta `700_brief/` (espejo de Caden). |
| 2026-06-28 | **Resuelta la nomenclatura de iteraciones** (`D-017`, cierra `T-016`): **bandas estilo Caden** (Tracer Bullet → [Stab] → MVP → [Evol] → Final) + flujos numerados **de 5 en 5** (`010`…`075`). Reescrito el encabezado de `roadmap.md` a bandas; corregidas las referencias de numeración y "Iteración 1"→"Tracer Bullet" en los briefs y la plantilla. Lección `L-008` (brief = escalera completa; roadmap = slicing). |
| 2026-06-28 | **Redactados 8 de 14 briefs** (T-019) en `700_brief/`: `010_discovery` (aprobado por el usuario), `015_onboarding`, `020_ingestion`, `025_profiling` (aprobados) y `030_cleaning`, `035_derivation`, `040_exploration`, `045_featuring` (borrador). Cada uno con su escalera L0→Ln; `roadmap.md` poblado hasta la fila Featuring. |
| 2026-06-28 | **Creado el mapa de procesos oficial** `700_brief/000_general_process.md` (`D-018`): entradas/salidas por workflow (`010`–`045`) + tabla maestra, con **nombres canónicos en inglés** de todos los artefactos. Se fijaron los que faltaban: `data_health.json` (Profiling), `ingestion_report.json` (Ingestion), `problem_statement.md` / `data_structure.md` (Discovery). Movido desde `Template/` y actualizados los briefs `010`/`020`/`025` para coincidir. |
| 2026-06-28 | **Completados los 14 briefs (Fase 0 cerrada)**: redactados `050_modelling`, `055_inferences`, `060_simulation`, `065_scenarios`, `070_reporting`, `075_monitoring`. **Los 14 briefs aprobados** (`010`–`075`). Configs humanas `<flujo>_config.yaml` (`modelling`/`simulation`/`scenarios`) y parámetros financieros de Reporting desde bronze (`D-019`). Mapa de procesos `000_general_process.md` completo (14/14); `roadmap.md` con *Brief* = `aprobado` en las 14 filas. |
| 2026-06-28 | **Definido el método de construcción por vertical slice** (`D-021`) tras estudiar el método de Caden (`700_brief→705_design→710_plan→720_build` + ciclo A/B/C). **Dos niveles**: banda (`slice_contract`) y celda flujo×banda (diseñar/ejecutar/probar/verificar sobre golden client C1). Estructura de carpetas espejo de Caden con eje banda. **Protocolo agéntico del paso "Definir"** (escritor/revisor independiente/gate humano) como plantilla. Aclarado: **bandas = madurez del motor, no estado de la instancia**; el `slice_contract` = formalización de la columna de la banda en `roadmap.md` (= entregable de `T-017`). |
| 2026-06-28 | **Creadas y aprobadas las dos plantillas del paso "Definir"** (`D-021`): `710_plan/foda-slice-contract-template.md` (contrato de banda — tabla de peldaño L por los 14 flujos, andamiaje transversal `TR-1..TR-4`, golden client C1, BDD companion, Done end-to-end, gate P5) y `710_plan/foda-bdd-template.md` (BDD end-to-end de banda en Gherkin: escenario central de recorrido completo + hitos críticos atados a invariantes `D-020` + **checklist de trazabilidad scope↔bdd** que usa el revisor). Aprobadas por el usuario. Carril `710_plan/` sembrado. |
| 2026-06-28 | **T-017 — `slice_contract.md` + `bdd.md` del Tracer Bullet escritos y APROBADOS**: 14 flujos en L0 alineados a la letra de cada brief + TR-1/TR-2, orden de tubería, Done end-to-end (margen bruto + cierre de ciclo), hold-out de Monitoring. Ejecutado el protocolo agéntico de "Definir" (`D-021`) con **revisor en contexto fresco**: veredicto inicial `REQUIERE SUBSANACIÓN` (filas con "L0" desalineado del L0 del brief) → **subsanado** alineando 010/050/060/065/070/075 a los briefs y documentando el único desvío (cardinalidad C1). Gate P5 cerrado. Lección `L-009`. |
| 2026-06-28 | **Enmienda de carriles (`D-021` §4):** creado el carril dedicado **`703_definition/`** para el output del paso **Definir** (banda). Movidos `slice_contract.md` + `bdd.md` del Tracer Bullet y las dos plantillas desde `710_plan/` → `703_definition/` (vía `git mv`). Motivo: `710_plan/` debe guardar el output del paso **Planear** (planes por celda); ubicar ahí el `slice_contract` conflactaba Definir con Planear y lo separaba de su hermano el brief. Un carril por paso del ciclo. Lección `L-010`. |
| 2026-06-28 | **T-002 — Árbol de carpetas creado (`D-021 §4`):** sembrados los carriles `705_design/tracer-bullet/` y `710_plan/tracer-bullet/` (archivos `<flujo>.md` por celda, a crear al diseñar/planear) y `720_build/tracer-bullet/<flujo>/{agents,skills,schemas,contract,deliverables,evaluation}` para los 14 flujos (010→075). Más `720_build/_transversal/{TR-1..TR-4}` (D-020) y `720_build/golden_client/snapshots/` (D-012/D-014). `README.md` por carril (paso del ciclo, convención, notas) y `.gitkeep` en hojas vacías. `CLAUDE.md §6` actualizado. |
| 2026-07-01 | **T-023 — Stack tecnológico de la instancia decidido (`D-023..D-027`):** (1) Python + pandas/polars/scikit-learn/numpy/SQLAlchemy (`D-023`); (2) PostgreSQL para bronze/silver/gold (`D-024`); (3) app batch multi-cliente, 1 DS para N clientes, gate humano (`D-025`); (4) monolito modular por capas + hexagonal ligero (`D-026`); (5) schema-per-tenant (`D-027`). Cuestionario de diseño de sistemas completado (`985_inputs/questionnaire_DS.md`). Documento de diseño del sistema creado: `955_architecture/design_system.md`. **T-014 desbloqueada.** |
| 2026-07-01 | **T-014 — Infraestructura de golden client C1 construida y verificada.** Diseño `720_build/golden_client/C1_design.md` (aprobado); frontera decidida: el generador emite **fuente cruda** (CSV), no bronze (nace en la celda `020`). **Postgres 17 en Docker** (`docker-compose.yml`, `foda_golden_db`, `localhost:55432`, DB `foda`, schema `golden_client`; `D-028`, `.env` gitignored). **Generador** `generator/generate_c1.py` determinista (semilla 42): 7 SKUs × 36 meses mensuales, estacionalidad con pico en diciembre (hipótesis testeable), ruido de calidad (nulos+duplicados) y split hold-out K=6. Fuente cruda C1 (`demanda_historica.csv` 214 filas + `demanda_holdout.csv` 42 + `generation_report.json`) y **cuestionarios** pre-respondidos (insumo de `010` L0). Verificado: pico dic. (711→1302), determinismo (hash igual al regenerar), conexión host→contenedor por psycopg. Lección `L-012` (verificar presencia de herramientas). |

## Próximo paso

**T-014 cerrada:** infraestructura del golden client C1 lista (Postgres en Docker + generador + fuente cruda
+ cuestionarios). Sigue la construcción de la banda (Fase 1 de `D-015`):

1. **T-021 — (PRÓXIMA) Detallar el protocolo agéntico de los pasos restantes** del ciclo `D-021` (Diseñar,
   Planear, Ejecutar, Probar, Verificar) con el mismo nivel del paso "Definir" ya especificado.
2. **Primera celda `010_discovery`** del Tracer Bullet: diseñar → ejecutar → probar → verificar contra C1
   (consume los cuestionarios de C1, emite los 3 contratos). El diseño en `705_design/tracer-bullet/010_discovery.md`.
3. Después: continuar celda por celda (015→075) aplicando el ciclo de `D-021`, acumulando snapshots (`D-012`).

## Bitácora

### 2026-06-28
- El usuario planteó que construir flujo por flujo a profundidad (`D-011`) tarda demasiado en llegar a un MVP validable por el cliente. Se analizó y se adoptó un **enfoque por fases / walking skeleton** (`D-015`): brief de los 14 → rebanada fina end-to-end sobre C1 → profundización por valor (`D-011` pasa a ser el método de la Fase 2).
- Para no perder el control, se definió el control en **dos vistas** (`D-016`): la **escalera de capacidades** (L0→Ln) dentro de cada **brief** (vista por workflow / el futuro del flujo) y la **matriz `roadmap.md`** workflow × iteración (vista entre workflows / qué peldaño y cuándo). Vocabulario de estado por celda: `vacío`/`planeado`/`mínimo`/`completo`.
- Creado `800_persistence/roadmap.md` (esqueleto con los 14 flujos). Registradas `D-015`, `D-016` y `L-007`. Nuevas tareas `T-016`..`T-019`. Quedó como **punto abierto** la nomenclatura de iteraciones (bandas Caden vs. numeración, `T-016`).
- **T-018 completada:** creada la plantilla de brief FODA en `700_brief/foda-brief-template.md` (nueva carpeta `700_brief/`, espejo de Caden). Se estudiaron los briefs de referencia de Caden (`700_brief/010_discovery.md`, `020_architecture.md`) y se adaptó su estructura a FODA: aclaración de planos (`D-001`), tubería de 14 flujos con capas bronze/silver/gold, grain producto×geo (`D-014`), gate del científico de datos, y la **§9 "Escalera de capacidades" (L0→Ln)** distintiva de FODA (`D-016`) que se ensambla en `roadmap.md`. Siguiente: T-019 (briefs de los 14, empezando por Discovery).
- **Sesión de briefs (T-019):** redactados 8 de 14 briefs con la plantilla — `010_discovery` (revisado y **aprobado** por el usuario), `015_onboarding`, `020_ingestion`, `025_profiling` (aprobados en lote), `030_cleaning`, `035_derivation`, `040_exploration`, `045_featuring` (borrador). Se siguió la fuente `expected_workflow.md` flujo por flujo; cada brief cierra con su escalera L0→Ln y se reflejó en `roadmap.md`.
- **Aclaración de método (L-008):** el usuario preguntó si el brief era solo L0; se aclaró que el **brief = escalera completa (vista vertical)** y el **roadmap = slicing por banda (vista horizontal)**. Confirmó además el cambio a **bandas estilo Caden** → `D-017` (cierra `T-016`): bandas + numeración de flujos **de 5 en 5**. Se reescribió `roadmap.md` y se corrigieron referencias en los briefs.
- **Mapa de procesos oficial (`D-018`):** a pedido del usuario se elevó la vista de entradas/salidas a documento oficial `700_brief/000_general_process.md` (movido desde `Template/`), con **nombres canónicos en inglés** de todos los artefactos y sin nombres "a definir": se fijaron `data_health.json`, `ingestion_report.json`, `problem_statement.md`, `data_structure.md`. Es la **fuente de verdad de nombres**; los briefs `010`/`020`/`025` se actualizaron para coincidir. Nueva tarea `T-020` (mantenerlo al día con cada brief). Cierre de sesión: `/foda-progress`. Siguiente: `050_modelling`.
- **Cierre de la Fase 0 — los 14 briefs (T-019/T-020):** en una segunda corrida se redactaron los 6 briefs restantes guiados por el usuario flujo por flujo: `050_modelling` (modelo ingenuo como baseline → torneo → selección humana del `best_model.pkl`), `055_inferences` (pronóstico + **MAPE por período** como contrato hacia Simulation), `060_simulation` (Montecarlo con MAPE + variables de influencia **opcionales/extensibles**), `065_scenarios` ("¿qué pasa si…?" como **deltas** dirigidos), `070_reporting` (márgenes/costo de oportunidad/inventario de seguridad) y `075_monitoring` (Monitoring + Alerting, cierra el ciclo). El usuario aportó la semántica de cada input humano.
- **Decisión `D-019`:** convención **`<flujo>_config.yaml`** para los inputs de configuración de autoría humana (`modelling_config.yaml`, `simulation_config.yaml`, `scenarios_config.yaml`) con el principio **"reglas como dato"** (variables/catálogos extensibles editando el YAML, no el motor). El usuario precisó dos veces que las variables de `060`/`065` (lead time, TRM, inflación, precio…) son **ejemplos**, no lista cerrada. Resuelto también que los **parámetros financieros** de `070_reporting` se **leen de la capa bronze** (datos del cliente, mapeados en Onboarding), no de un insumo nuevo. `075` se nombró `075_monitoring` (agrupa Alerting).
- **Aprobación y cierre:** el usuario **aprobó los 14 briefs** (estado `APROBADO`, `Aprobado por: usuario`); `000_general_process.md` quedó completo (14/14) y `roadmap.md` con la columna *Brief* en `aprobado` para los 14 flujos. T-019 y T-020 completadas. **Próxima tarea: `T-017`** (alcance del Tracer Bullet). Cierre con `/foda-progress`.
- **Método de construcción por vertical slice (`D-021`):** el usuario pidió revisar el método de Caden (`700_brief→705_design→710_plan→720_build` por arnés + ciclo SDD+TDD con instancias A/B/C) y definir cómo construir cada vertical slice de FODA con los pasos **definir→diseñar→planear→ejecutar→probar→verificar**. Se resolvieron tres puntos en conversación: (1) **granularidad** → el usuario eligió **dos niveles** (banda = `slice_contract`; celda flujo×banda = diseñar/ejecutar/probar/verificar acumulando sobre snapshots `D-012`); (2) **terminología** → el **brief** es el alcance del flujo (escalera L0→Ln, "el menú") y el **`slice_contract`** es el alcance de la banda (qué peldaño entra, "la orden"); el paso "Definir" se materializa en el `slice_contract`; (3) **planos** → todo el ciclo es **construcción del motor**; las **bandas son madurez del motor, no estado de la instancia** (la instancia solo ejecuta el motor vigente).
- **Protocolo agéntico del paso "Definir":** el usuario propuso un flujo detallado (escritor de `scope.md`+`bdd.md` → revisor de consistencia independiente → gate humano, con loop de subsanación y escalamiento). Se **validó** como el patrón harness de Caden (A=sesión principal/Governor, escritor=Worker, revisor=Evaluador C) y se aportaron **dos correcciones**: (a) un subagente no lanza a su "hermano" — termina y devuelve el control a la sesión principal, que encadena el siguiente (modelo plano `D-009`, ver `L-002`); (b) poner un **tope de iteraciones** (~2, E5) antes de escalar al humano. Todo quedó registrado en **`D-021`** (enmienda/precisa `D-011`).
- **Andamiaje transversal (`D-020`):** ante la pregunta del usuario sobre cómo se trabajarán los temas de `methodology.md`/`principles.md` (persistencia de estado, A/B/C, evaluador, ejecución durable…), se aclaró que (1) hay **dos persistencias** —construcción (`800_persistence/`, ya operativa) vs. runtime de instancia (`fda-*`, por construir)— y (2) la metodología es la **ambición Ln**; el andamiaje se construye **mínimo en el Tracer Bullet y se afina por bandas** (E4/NC-2/`D-015`). Se fijaron los **invariantes no deferibles** (P2, P8, bronze/silver/gold, gate humano, persistencia mínima+git) y los **diferibles** (A/B/C completo, evaluador calibrado, durabilidad, context resets, CR, knowledge base). Se agregaron **filas transversales `TR-1..TR-4`** a `roadmap.md` con su propia escalera y se amplió `T-017` para que también las defina. Decisión `D-020`.
- **T-017 — slice_contract + bdd del Tracer Bullet (escritos, revisados y APROBADOS):** se redactó por pantalla la propuesta del `slice_contract` (14 flujos en L0 + TR-1..TR-4 + orden + Done end-to-end + fixture C1), el usuario la aprobó y se escribieron los documentos definitivos en `710_plan/tracer-bullet/` (`slice_contract.md` + `bdd.md`, usando las plantillas de T-022). A pedido del usuario se renombró `000_slice_contract.md` → `slice_contract.md`. Se lanzó un **revisor independiente en contexto fresco** (`general-purpose`) que auditó scope↔bdd, nombres canónicos, invariantes `D-020`, planos y conformidad con plantillas: veredicto `REQUIERE SUBSANACIÓN` por **un solo eje** (el "L0" de varias filas no coincidía con el L0 de la letra del brief). Se **subsanó** alineando 010 (3 contratos), 050 (ingenuo+1 modelo), 060 (sin safety stock), 065 (1 delta), 070 (solo margen bruto) y 075 (sin señal) a los briefs, y se documentó el **único desvío deliberado** (cardinalidad: C1 completo ~5–10 series). Gate P5 cerrado con la identidad de git (`Triple S`); ambos documentos en `APROBADO`. Lección `L-009` (corolario operativo de `L-008`). T-017 completada.
- **Hueco detectado — stack tecnológico de la instancia (`D-022`, `L-011`):** el usuario preguntó qué **stack, base de datos, arquitectura y patrones de diseño** usará la instancia. Al verificar contra documentos fuente, briefs y decisiones se confirmó que **nunca se decidió**: lo definido es arquitectura **agéntica** (planos, A/B/C, vertical slice `D-021`) y **contrato de datos** (nombres canónicos `D-018`), pero no la capa de **implementación**. Solo había señales *implícitas* (Python por `best_model.pkl`; exportables `.csv`/`.xlsx`; los "medios de acceso CSV/BD/API" son la **fuente del cliente**, no la BD de la solución). Se decidió (`D-022`) que el stack es **transversal** y debe fijarse como ADRs **antes del primer vertical slice**, no descubrirse celda por celda. Se creó **T-023** (bloqueante, **precede a T-014**) para resolver: (1) lenguaje + librerías de ML, (2) motor de datos físico de bronze/silver/gold, (3) forma de la app (batch CLI vs. servicio), (4) patrones de diseño base. Lección `L-011`. Cierre con `/foda-progress`.

### 2026-06-27
- Lectura de los documentos base: `current_state.md`, `expected_workflow.md`, `expected_solution.md`.
- Creada la estructura de persistencia del motor en `800_persistence/`.
- Cierre de sesión: al ejecutar `/foda-progress` se detectó el frontmatter roto (`model: model: sonnet`) que hizo correr el comando con Haiku 4.5 en vez de Sonnet 200K; corregido y registrado en `L-005`.
