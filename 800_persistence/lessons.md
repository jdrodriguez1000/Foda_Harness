# Lessons — Motor FODA

> Lecciones aprendidas durante la construcción del motor FODA.
> Cada lección documenta qué pasó, qué se aprendió y cómo aplicarlo en adelante.

---

## Índice
- [L-001 — El `model:` del comando solo aplica al invocarlo el usuario, no al ejecutarlo el agente inline](#l-001--el-model-del-comando-solo-aplica-al-invocarlo-el-usuario-no-al-ejecutarlo-el-agente-inline)

---

## Lecciones

### L-001 — El `model:` del comando solo aplica al invocarlo el usuario, no al ejecutarlo el agente inline
- **Contexto:** Fijamos `model: sonnet` en `foda-progress`/`foda-next` (ver `D-003`) y queríamos verificar qué modelo realmente los ejecuta.
- **Qué pasó:** Cuando el agente de la sesión (Opus) ejecuta el protocolo inline, corre con el modelo de la sesión (Opus), no con el `model:` del frontmatter. El `model:` del frontmatter toma efecto cuando **el usuario teclea** el slash-command y el harness lo lanza.
- **Lección:** Para auditar el modelo de un comando, la prueba válida es invocarlo escribiendo `/comando` directamente; un auto-reporte de modelo dentro del comando lo confirma de forma inequívoca.
- **Cómo aplicar:** No asumir que el `model:` se respeta cuando otro agente reusa los pasos del comando; verificar con el auto-reporte tras invocarlo manualmente.
- **Fecha:** 2026-06-27

<!--
### L-001 — <título corto>
- **Contexto:** qué estábamos haciendo.
- **Qué pasó:** el hecho o problema.
- **Lección:** qué aprendimos.
- **Cómo aplicar:** acción concreta para el futuro.
- **Fecha:** YYYY-MM-DD
-->
