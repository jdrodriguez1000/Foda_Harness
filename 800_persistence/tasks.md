# Tasks — Motor FODA

> Tareas del proyecto que construye el motor FODA. Incluye realizadas y pendientes.
> Cada tarea tiene un estado: `[ ]` pendiente · `[~]` en progreso · `[x]` completada · `[!]` bloqueada.

---

## Índice
- [Convención de estados](#convención-de-estados)
- [En progreso](#en-progreso)
- [Pendientes](#pendientes)
- [Completadas](#completadas)

---

## Convención de estados
- `[ ]` Pendiente
- `[~]` En progreso
- `[x]` Completada
- `[!]` Bloqueada (ver nota)

---

## En progreso

| ID | Estado | Tarea |
|----|--------|-------|
| — | — | _(ninguna en progreso; **próxima tarea: T-023** — decidir el stack tecnológico de la instancia, BLOQUEA T-014 y todo vertical slice)_ |

## Pendientes

> **Orden de trabajo actualizado por `D-015`/`D-016` (enfoque por fases / walking skeleton):**
> primero la plantilla de brief y los briefs de los 14 flujos (Fase 0), luego definir la Iteración 1
> (skeleton), y recién entonces el árbol de carpetas y la construcción.

| ID | Estado | Tarea |
|----|--------|-------|
| T-023 | `[ ]` | **(PRÓXIMA — BLOQUEANTE) Decidir el stack tecnológico de la instancia** (`D-022`): resolver como ADRs (`D-023+`), **antes de iniciar cualquier vertical slice**, al menos (1) **lenguaje + librerías de ML**; (2) **motor de datos** de las capas bronze/silver/gold (formato físico + mecanismo de consulta: archivos/Parquet/DuckDB/SQLite/Postgres…); (3) **forma de la app** (batch CLI con gate humano vs. servicio con API); (4) **patrones de diseño base** (cómo un agente invoca código determinista y dónde vive ese código en la instancia). **Precede a T-014** (el golden client necesita el formato de bronze) y a toda celda del Tracer Bullet. Posible conexión con las transversales `TR-*` (`D-020`). Lección `L-011`. |
| T-014 | `[ ]` | Diseñar la infraestructura de **golden client + snapshots por capa/artefacto** (`D-012`): cliente de prueba canónico, congelado de bronze/silver/gold y artefactos, versionado de snapshot ligado al contrato upstream. Incluye el **generador sintético parametrizado** por jerarquía producto/geo y nº de series (`D-014`): instanciar C1 (primario) ya, C4 (estrés) y C2/C3 bajo demanda. |
| T-015 | `[ ]` | Al redactar el brief de Discovery/Onboarding (T-019): los contratos (`client_register.yaml`, `map_client_data.json`) deben capturar el **grain** multinivel de producto (familia→categoría→subcategoría→SKU) y geografía (región→país→ciudad→sede) y propagarlo a la tubería (`D-014`). |
| T-021 | `[ ]` | **Detallar el protocolo agéntico de los pasos restantes del ciclo `D-021`** (Diseñar, Planear, Ejecutar, Probar, Verificar) con el mismo nivel del paso "Definir" (escritor/revisor independiente/gate, encadenamiento por la sesión principal, tope de iteraciones E5). El paso "Definir" ya quedó especificado en `D-021`. |
| T-003 | `[ ]` | Diseñar el instalador `install.sh` (copia de definiciones del flujo + transversales, init de git, esqueleto de instancia). Inspirarse en `caden-setup` (ver `L-006`). |

## Completadas

| ID | Estado | Tarea | Fecha |
|----|--------|-------|-------|
| T-001 | `[x]` | Crear `800_persistence/` con los 4 archivos de memoria (progress, tasks, lessons, decisions). | 2026-06-27 |
| T-004 | `[x]` | Crear `CLAUDE.md` con instrucciones para todos los agentes de Claude Code. | 2026-06-27 |
| T-005 | `[x]` | Crear `.claude/` con `commands/` y los settings `settings.json` (proyecto) y `settings.local.json` (local). | 2026-06-27 |
| T-006 | `[x]` | Crear los comandos de proyecto `foda-progress` (cierre de sesión) y `foda-next` (inicio de sesión). | 2026-06-27 |
| T-007 | `[x]` | Inicializar git, agregar `.gitignore`, conectar remoto y hacer primer commit + push. | 2026-06-27 |
| T-008 | `[x]` | Agregar `.gitattributes` (normalización de fines de línea LF/CRLF y binarios). | 2026-06-27 |
| T-009 | `[x]` | Fijar `model: sonnet` en los comandos `foda-progress` y `foda-next`. | 2026-06-27 |
| T-010 | `[x]` | Agregar línea de auto-reporte de modelo en `foda-progress` y `foda-next` para verificar el modelo en ejecución. | 2026-06-27 |
| T-011 | `[x]` | Adaptar `950_guideline/methodology.md` a la estructura FODA (13 flujos = fases; planos `foda-/fda-`; bronze/silver/gold; subagentes anidados D-005/L-002; renombre `claude-progress.txt`→`project-progress.txt` y estado `fda-*`). | 2026-06-27 |
| T-012 | `[x]` | Estudiar el harness de referencia **Caden** y decidir arquitectura de FODA: modelo plano (`D-009`), B/C por flujo (`D-010`), método de construcción brief→diseño→plan→build (`D-011`). Adaptada `methodology.md` (§3, §3.1, §4.1, §4.2, §12.2, §12.3); lección `L-006`. | 2026-06-27 |
| T-016 | `[x]` | Decidir la nomenclatura de iteraciones del roadmap. Resuelta: **bandas estilo Caden** (Tracer Bullet → Stab → MVP → Evol → Final) + flujos numerados **de 5 en 5** (`D-017`). | 2026-06-28 |
| T-018 | `[x]` | Crear la plantilla de brief FODA (`D-016`): estructura de Caden + sección **"Escalera de capacidades"** (L0→Ln). Creada en `700_brief/foda-brief-template.md`. | 2026-06-28 |
| T-019 | `[x]` | **Redactar los 14 briefs** (`010`–`075`) con la plantilla, cada uno con su escalera L0→Ln. **Todos aprobados.** Configs humanas fijadas: `modelling_config.yaml`, `simulation_config.yaml`, `scenarios_config.yaml` (`D-019`). | 2026-06-28 |
| T-020 | `[x]` | **Mantener `700_brief/000_general_process.md` al día** (`D-018`): registradas las entradas/salidas (nombres canónicos en inglés) de los 14 workflows; mapa de procesos completo (14/14). | 2026-06-28 |
| T-022 | `[x]` | **Crear las plantillas del paso "Definir"** (`D-021`): `703_definition/foda-slice-contract-template.md` (contrato de banda) y `703_definition/foda-bdd-template.md` (BDD end-to-end + checklist scope↔bdd del revisor). **Aprobadas por el usuario.** | 2026-06-28 |
| T-017 | `[x]` | **Escribir el `slice_contract` + `bdd.md` del Tracer Bullet** (`D-021` nivel banda; `D-015` Fase 1) en `703_definition/tracer-bullet/`: 14 flujos en L0 (alineados a la letra de cada brief) + transversales TR-1/TR-2, orden de tubería, Done end-to-end, hold-out de Monitoring. Revisado en contexto fresco (veredicto `REQUIERE SUBSANACIÓN` → subsanado alineando L0 slice↔briefs) y **APROBADO** por el usuario (gate P5). | 2026-06-28 |
| T-002 | `[x]` | **Crear el árbol de carpetas** del motor FODA (`D-021 §4`): `705_design/tracer-bullet/`, `710_plan/tracer-bullet/`, `720_build/tracer-bullet/<flujo>/{agents,skills,schemas,contract,deliverables,evaluation}` para los 14 flujos, `720_build/_transversal/{TR-1..TR-4}` y `720_build/golden_client/snapshots/`. README por carril. `.gitkeep` en hojas vacías. | 2026-06-28 |
