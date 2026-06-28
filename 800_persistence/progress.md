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

**Fase:** Fase 0 de `D-015` — **redacción de los briefs de los 14 flujos** (T-019), en curso.
**Punto actual:** **8 de 14 briefs redactados** en `700_brief/`: `010_discovery`, `015_onboarding`,
`020_ingestion`, `025_profiling` (**aprobados**) y `030_cleaning`, `035_derivation`, `040_exploration`,
`045_featuring` (borrador, avanzando en cadena). Cada brief lleva su **escalera de capacidades L0→Ln**
(`D-016`); el `roadmap.md` registra el peldaño previsto para la banda **Tracer Bullet** (= L0).
**Cerrado en esta sesión:** la nomenclatura de iteraciones — **bandas estilo Caden** (Tracer Bullet →
Stab → MVP → Evol → Final) + flujos numerados **de 5 en 5** (`D-017`, resuelve `T-016`). Creado el
**documento oficial de procesos** `700_brief/000_general_process.md` con los **nombres canónicos en
inglés** de todas las entradas/salidas (`D-018`).
**Pendiente inmediato:** continuar T-019 con `050_modelling` y los flujos `055`–`075`, manteniendo
`000_general_process.md` al día → luego definir el alcance del Tracer Bullet (T-017).

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

## Próximo paso

Orden marcado por `D-015`/`D-016`/`D-017` (Fase 0):

1. **T-019 — Terminar los briefs restantes (`050`–`075`)**: `050_modelling` (torneo de campeones →
   `best_model.pkl`, gate humano de selección), `055_inferences` (→ `inferences.json`, MAPE por período),
   `060_simulation`, `065_scenarios`, `070_reporting`, `075_monitoring_alerting`. Cada uno con su escalera
   L0→Ln, poblando `roadmap.md` y **registrando sus artefactos en `000_general_process.md`** (`T-020`).
2. **T-017 — Definir el alcance del Tracer Bullet** (L0 de cada flujo sobre C1), poblando la columna
   *Tracer Bullet* de `roadmap.md`.

Después: **T-002** (árbol de carpetas, ajustado al flujo por fases) y la construcción del Tracer Bullet.
Referencia de método: `Caden_Harness/720_build/` (`L-006`).

## Bitácora

### 2026-06-28
- El usuario planteó que construir flujo por flujo a profundidad (`D-011`) tarda demasiado en llegar a un MVP validable por el cliente. Se analizó y se adoptó un **enfoque por fases / walking skeleton** (`D-015`): brief de los 14 → rebanada fina end-to-end sobre C1 → profundización por valor (`D-011` pasa a ser el método de la Fase 2).
- Para no perder el control, se definió el control en **dos vistas** (`D-016`): la **escalera de capacidades** (L0→Ln) dentro de cada **brief** (vista por workflow / el futuro del flujo) y la **matriz `roadmap.md`** workflow × iteración (vista entre workflows / qué peldaño y cuándo). Vocabulario de estado por celda: `vacío`/`planeado`/`mínimo`/`completo`.
- Creado `800_persistence/roadmap.md` (esqueleto con los 14 flujos). Registradas `D-015`, `D-016` y `L-007`. Nuevas tareas `T-016`..`T-019`. Quedó como **punto abierto** la nomenclatura de iteraciones (bandas Caden vs. numeración, `T-016`).
- **T-018 completada:** creada la plantilla de brief FODA en `700_brief/foda-brief-template.md` (nueva carpeta `700_brief/`, espejo de Caden). Se estudiaron los briefs de referencia de Caden (`700_brief/010_discovery.md`, `020_architecture.md`) y se adaptó su estructura a FODA: aclaración de planos (`D-001`), tubería de 14 flujos con capas bronze/silver/gold, grain producto×geo (`D-014`), gate del científico de datos, y la **§9 "Escalera de capacidades" (L0→Ln)** distintiva de FODA (`D-016`) que se ensambla en `roadmap.md`. Siguiente: T-019 (briefs de los 14, empezando por Discovery).
- **Sesión de briefs (T-019):** redactados 8 de 14 briefs con la plantilla — `010_discovery` (revisado y **aprobado** por el usuario), `015_onboarding`, `020_ingestion`, `025_profiling` (aprobados en lote), `030_cleaning`, `035_derivation`, `040_exploration`, `045_featuring` (borrador). Se siguió la fuente `expected_workflow.md` flujo por flujo; cada brief cierra con su escalera L0→Ln y se reflejó en `roadmap.md`.
- **Aclaración de método (L-008):** el usuario preguntó si el brief era solo L0; se aclaró que el **brief = escalera completa (vista vertical)** y el **roadmap = slicing por banda (vista horizontal)**. Confirmó además el cambio a **bandas estilo Caden** → `D-017` (cierra `T-016`): bandas + numeración de flujos **de 5 en 5**. Se reescribió `roadmap.md` y se corrigieron referencias en los briefs.
- **Mapa de procesos oficial (`D-018`):** a pedido del usuario se elevó la vista de entradas/salidas a documento oficial `700_brief/000_general_process.md` (movido desde `Template/`), con **nombres canónicos en inglés** de todos los artefactos y sin nombres "a definir": se fijaron `data_health.json`, `ingestion_report.json`, `problem_statement.md`, `data_structure.md`. Es la **fuente de verdad de nombres**; los briefs `010`/`020`/`025` se actualizaron para coincidir. Nueva tarea `T-020` (mantenerlo al día con cada brief). Cierre de sesión: `/foda-progress`. Siguiente: `050_modelling`.

### 2026-06-27
- Lectura de los documentos base: `current_state.md`, `expected_workflow.md`, `expected_solution.md`.
- Creada la estructura de persistencia del motor en `800_persistence/`.
- Cierre de sesión: al ejecutar `/foda-progress` se detectó el frontmatter roto (`model: model: sonnet`) que hizo correr el comando con Haiku 4.5 en vez de Sonnet 200K; corregido y registrado en `L-005`.
