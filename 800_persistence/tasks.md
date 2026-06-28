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

_(ninguna)_

## Pendientes

| ID | Estado | Tarea |
|----|--------|-------|
| T-002 | `[ ]` | Diseñar el árbol de carpetas del motor FODA siguiendo `D-011`: carpetas de método (brief/diseño/plan/build), carpeta autocontenida por flujo (`agents/`, `skills/`, `schemas/`, `contract/`, `deliverables/`, `evaluation/`), zona de **golden client + snapshots** (`D-012`) y transversales en la raíz. Registrar como `D-013`. |
| T-014 | `[ ]` | Diseñar la infraestructura de **golden client + snapshots por capa/artefacto** (`D-012`): cliente de prueba canónico, congelado de bronze/silver/gold y artefactos, versionado de snapshot ligado al contrato upstream. Incluye el **generador sintético parametrizado** por jerarquía producto/geo y nº de series (`D-014`): instanciar C1 (primario) ya, C4 (estrés) y C2/C3 bajo demanda. |
| T-015 | `[ ]` | Al diseñar Discovery/Onboarding (T-013): los contratos (`client_register.yaml`, `map_client_data.json`) deben capturar el **grain** multinivel de producto (familia→categoría→subcategoría→SKU) y geografía (región→país→ciudad→sede) y propagarlo a la tubería (`D-014`). |
| T-013 | `[ ]` | Decidir por cuál flujo empezar la construcción (probablemente *Discovery*) y redactar su **brief** (1.er paso del método `D-011`). |
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
