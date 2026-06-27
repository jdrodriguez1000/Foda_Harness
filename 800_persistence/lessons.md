# Lessons — Motor FODA

> Lecciones aprendidas durante la construcción del motor FODA.
> Cada lección documenta qué pasó, qué se aprendió y cómo aplicarlo en adelante.

---

## Índice
- [L-001 — El `model:` del comando solo aplica al invocarlo el usuario, no al ejecutarlo el agente inline](#l-001--el-model-del-comando-solo-aplica-al-invocarlo-el-usuario-no-al-ejecutarlo-el-agente-inline)
- [L-002 — Los subagentes anidados tienen límite de profundidad fijo (5), no configurable](#l-002--los-subagentes-anidados-tienen-límite-de-profundidad-fijo-5-no-configurable)

---

## Lecciones

### L-001 — El `model:` del comando solo aplica al invocarlo el usuario, no al ejecutarlo el agente inline
- **Contexto:** Fijamos `model: sonnet` en `foda-progress`/`foda-next` (ver `D-003`) y queríamos verificar qué modelo realmente los ejecuta.
- **Qué pasó:** Cuando el agente de la sesión (Opus) ejecuta el protocolo inline, corre con el modelo de la sesión (Opus), no con el `model:` del frontmatter. El `model:` del frontmatter toma efecto cuando **el usuario teclea** el slash-command y el harness lo lanza.
- **Lección:** Para auditar el modelo de un comando, la prueba válida es invocarlo escribiendo `/comando` directamente; un auto-reporte de modelo dentro del comando lo confirma de forma inequívoca.
- **Cómo aplicar:** No asumir que el `model:` se respeta cuando otro agente reusa los pasos del comando; verificar con el auto-reporte tras invocarlo manualmente.
- **Fecha:** 2026-06-27

### L-002 — Los subagentes anidados tienen límite de profundidad fijo (5), no configurable
- **Contexto:** Al diseñar el patrón A→B→Workers (ver `D-005`) revisamos la doc oficial de Claude Code sobre subagentes para confirmar el anidamiento.
- **Qué pasó:** Desde Claude Code v2.1.172 un subagente puede spawnear sus propios subagentes. La profundidad se cuenta como niveles bajo la conversación principal; un subagente en **profundidad 5 ya no recibe la herramienta `Agent`** y no puede spawnear más. El límite es **fijo y no configurable**. Solo el resumen del subagente de nivel superior regresa a la conversación principal.
- **Lección:** El árbol de instancias del harness debe caber en ≤5 niveles. El patrón actual (A=nivel 0 → B=1 → Workers=2; C=1) está holgado, pero hay que vigilarlo si en el futuro un Worker necesitara sub-delegar.
- **Cómo aplicar:** Al diseñar nuevas cadenas de delegación, contar la profundidad desde la sesión principal y no superar 5. Si se necesita más paralelismo sostenido, usar *agent teams* (contexto propio por worker) en vez de anidar más niveles.
- **Fecha:** 2026-06-27

<!--
### L-001 — <título corto>
- **Contexto:** qué estábamos haciendo.
- **Qué pasó:** el hecho o problema.
- **Lección:** qué aprendimos.
- **Cómo aplicar:** acción concreta para el futuro.
- **Fecha:** YYYY-MM-DD
-->
