---
description: Protocolo de inicio de sesión del motor FODA — lee la persistencia y orienta el siguiente paso
model: haiku
---

# foda-next — Protocolo de inicio de sesión

> **Auto-reporte de modelo:** antes de comenzar, indica explícitamente con qué modelo se está
> ejecutando este comando (ej. "Ejecutando con Sonnet 4.6").

Ejecuta el **inicio de sesión** del proyecto que construye el motor FODA: recupera el estado del
proyecto desde la memoria de construcción para saber qué se hizo, dónde estamos y qué sigue.

## Pasos

### 1. Leer el estado del proyecto (índices primero)
Lee **únicamente el índice** de estos dos archivos para orientarte rápido sin cargar todo el contenido
(estos archivos crecen con el tiempo):

- **`800_persistence/progress.md`** — del índice, ubica y lee: *Estado actual*, *Próximo paso* y la
  última entrada de la *Bitácora*.
- **`800_persistence/tasks.md`** — del índice, ubica y lee: *En progreso* y *Pendientes*.

Con eso deberías saber: lo último realizado, el punto actual y las próximas tareas a realizar.

### 2. Lectura a demanda
**No** leas completos `lessons.md` ni `decisions.md` por defecto. Consulta su **índice** y lee solo la
entrada relevante (`L-XXX` / `D-XXX`) **cuando** la tarea actual lo requiera:

- **`800_persistence/lessons.md`** — para no repetir errores ni redescubrir aprendizajes.
- **`800_persistence/decisions.md`** — para respetar decisiones de diseño/arquitectura ya tomadas.

### 3. Reporte de arranque
Presenta un resumen breve:
- **Dónde estamos** (estado actual + última entrada de bitácora).
- **Qué sigue** (próximo paso de `progress.md` + tareas en progreso/pendientes de `tasks.md`).
- **Recomendación** de por dónde continuar.

Luego espera la indicación del usuario antes de ejecutar trabajo, salvo que él ya haya pedido avanzar.
