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

**Fase:** Inicialización del motor → definición metodológica (arquitectura cerrada).
**Punto actual:** Tras estudiar el harness de referencia **Caden**, se cerró la arquitectura de FODA:
**modelo plano** (A es la única que spawnea, B solo planifica — `D-009`, reemplaza el anidamiento de
`D-005`), **B y C por flujo** (`D-010`) y **método de construcción flujo por flujo** brief→diseño→plan→build
(`D-011`). `methodology.md` adaptada en consecuencia (§3, §3.1, §4.1, §4.2, §12.2, §12.3). Lección `L-006`
(Caden como referencia validada). Pendiente: diseñar el árbol de carpetas (T-002 → `D-012`) y elegir el
primer flujo a construir (T-013).

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

## Próximo paso

**T-002 — Diseñar el árbol de carpetas del motor FODA** según `D-011`/`D-010`/`D-009`: carpetas del
método de construcción (brief → diseño → plan → build), la **carpeta autocontenida por flujo** (`agents/`
con `foda-<flujo>-orchestrator` + workers + `foda-<flujo>-evaluator`, `skills/`, `schemas/`, `contract/`,
`deliverables/`, `evaluation/`) y los **transversales** en la raíz (esquema `fda-harness-state`, knowledge,
comandos de gate, `CLAUDE.md`), más la zona de **golden client + snapshots** (`D-012`, tarea T-014).
Registrar la estructura como `D-013`. Luego **T-013**: elegir el primer flujo (probablemente *Discovery*) y
redactar su **brief**. Referencia: `Caden_Harness/720_build/` (`L-006`).

## Bitácora

### 2026-06-27
- Lectura de los documentos base: `current_state.md`, `expected_workflow.md`, `expected_solution.md`.
- Creada la estructura de persistencia del motor en `800_persistence/`.
- Cierre de sesión: al ejecutar `/foda-progress` se detectó el frontmatter roto (`model: model: sonnet`) que hizo correr el comando con Haiku 4.5 en vez de Sonnet 200K; corregido y registrado en `L-005`.
