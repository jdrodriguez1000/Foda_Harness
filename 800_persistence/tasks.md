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
| T-002 | `[ ]` | Definir la estructura de carpetas del motor FODA (definiciones canónicas, namespace privado, esqueleto de instancia). _(Se reorienta con base en T-011.)_ |
| T-003 | `[ ]` | Diseñar el instalador `install.sh` (copia de definiciones, init de git, esqueleto de entrada). |

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
