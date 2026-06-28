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

**Fase:** Inicialización del motor → definición metodológica (estrategia de construcción cerrada).
**Punto actual:** Se **enmendó la estrategia de construcción** ante el riesgo de un time-to-MVP muy largo:
en vez de construir cada flujo a profundidad uno por uno (`D-011` puro), se adopta un **enfoque por fases /
walking skeleton** (`D-015`): (0) brief ligero de los 14 flujos, (1) rebanada fina end-to-end sobre C1
(simplificando lo caro) que el cliente pueda validar, (2) profundización por valor con `D-011` dentro de
cada slice. El **control** se ejerce con dos vistas (`D-016`): el **brief** de cada flujo lleva una
**"Escalera de capacidades"** (L0→Ln = su futuro), y el nuevo **`roadmap.md`** es la **matriz workflow ×
iteración** que ensambla esas escaleras (qué peldaño entra en cada iteración, con estado por celda).
Lección `L-007`. **Punto abierto (T-016):** nomenclatura de iteraciones (bandas Caden vs. numeración).
Pendiente: plantilla de brief (T-018) → briefs de los 14 (T-019) → definir Iteración 1 (T-017).

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

## Próximo paso

Orden marcado por `D-015`/`D-016` (Fase 0 primero):

1. **T-018 — Crear la plantilla de brief FODA**: estructura de Caden + sección **"Escalera de capacidades"**
   (L0→Ln). Referencia directa: los briefs de Caden en `Temporal/010_discovery.md` y `Temporal/020_architecture.md`.
2. **T-019 — Redactar el brief ligero de los 14 flujos**, empezando por *Discovery*, poblando la columna
   *Brief* de `roadmap.md` (cada uno con su escalera de capacidades).
3. **T-017 — Definir el alcance mínimo (L0) de la Iteración 1 / walking skeleton** sobre C1, poblando la
   columna *Iter 1* de `roadmap.md`.
4. **T-016 — Decidir la nomenclatura de iteraciones** (bandas Caden vs. numeración) — punto abierto que
   fija el encabezado definitivo de la matriz.

Después: **T-002** (árbol de carpetas, ajustado al flujo por fases) y la construcción de la Iteración 1.
Referencia de método: `Caden_Harness/720_build/` y los briefs en `Temporal/` (`L-006`).

## Bitácora

### 2026-06-28
- El usuario planteó que construir flujo por flujo a profundidad (`D-011`) tarda demasiado en llegar a un MVP validable por el cliente. Se analizó y se adoptó un **enfoque por fases / walking skeleton** (`D-015`): brief de los 14 → rebanada fina end-to-end sobre C1 → profundización por valor (`D-011` pasa a ser el método de la Fase 2).
- Para no perder el control, se definió el control en **dos vistas** (`D-016`): la **escalera de capacidades** (L0→Ln) dentro de cada **brief** (vista por workflow / el futuro del flujo) y la **matriz `roadmap.md`** workflow × iteración (vista entre workflows / qué peldaño y cuándo). Vocabulario de estado por celda: `vacío`/`planeado`/`mínimo`/`completo`.
- Creado `800_persistence/roadmap.md` (esqueleto con los 14 flujos). Registradas `D-015`, `D-016` y `L-007`. Nuevas tareas `T-016`..`T-019`. Quedó como **punto abierto** la nomenclatura de iteraciones (bandas Caden vs. numeración, `T-016`).

### 2026-06-27
- Lectura de los documentos base: `current_state.md`, `expected_workflow.md`, `expected_solution.md`.
- Creada la estructura de persistencia del motor en `800_persistence/`.
- Cierre de sesión: al ejecutar `/foda-progress` se detectó el frontmatter roto (`model: model: sonnet`) que hizo correr el comando con Haiku 4.5 en vez de Sonnet 200K; corregido y registrado en `L-005`.
