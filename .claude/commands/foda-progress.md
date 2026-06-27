---
description: Protocolo de cierre de sesión del motor FODA — actualiza la persistencia, hace commit y push
---

# foda-progress — Protocolo de cierre de sesión

Ejecuta el **cierre de sesión** del proyecto que construye el motor FODA: deja la memoria de
construcción al día y sincroniza el repositorio remoto.

Repositorio remoto: `https://github.com/jdrodriguez1000/Foda_Harness.git`

## Pasos

### 1. Actualizar los 4 archivos de persistencia (`800_persistence/`)
Revisa lo realizado en esta sesión y actualiza **cada uno** según corresponda. Mantén siempre el
**índice** de cada archivo al día cuando agregues entradas.

- **`progress.md`** — Actualiza *Estado actual*, *Hitos completados*, *Próximo paso* y agrega una
  entrada a la *Bitácora* con fecha de hoy resumiendo lo realizado.
- **`tasks.md`** — Marca como completadas (`[x]`) las tareas terminadas, mueve a *En progreso* (`[~]`)
  o *Pendientes* lo que aplique, y agrega las tareas nuevas detectadas (IDs `T-XXX`).
- **`lessons.md`** — Registra cualquier lección aprendida en esta sesión (IDs `L-XXX`). Si no hay, omite.
- **`decisions.md`** — Registra cualquier decisión de diseño/arquitectura tomada (IDs `D-XXX`,
  formato ADR). Si no hay, omite.

> Si no hubo cambios reales en la sesión, dilo explícitamente y **no** inventes entradas.

### 2. Commit
1. Verifica el estado: `git status` y `git diff` para confirmar qué se va a commitear.
2. Si el repositorio no está inicializado o el remoto `origin` no existe, configúralo:
   - `git init` (si hace falta)
   - `git remote add origin https://github.com/jdrodriguez1000/Foda_Harness.git` (si falta `origin`)
3. Añade los cambios: `git add -A`
4. Crea el commit con un mensaje claro en español que resuma lo realizado en la sesión. Termina el
   mensaje con:

   ```
   Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
   ```

### 3. Push
1. Empuja al remoto: `git push -u origin <rama-actual>`.
2. Si el push falla (rama remota adelantada, autenticación, etc.), **reporta el error tal cual** y
   sugiere la corrección. No fuerces el push (`--force`) salvo que el usuario lo pida explícitamente.

### 4. Confirmación
Reporta brevemente: archivos de persistencia actualizados, hash del commit y resultado del push.
