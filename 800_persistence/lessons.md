# Lessons — Motor FODA

> Lecciones aprendidas durante la construcción del motor FODA.
> Cada lección documenta qué pasó, qué se aprendió y cómo aplicarlo en adelante.

---

## Índice
- [L-001 — El `model:` del comando solo aplica al invocarlo el usuario, no al ejecutarlo el agente inline](#l-001--el-model-del-comando-solo-aplica-al-invocarlo-el-usuario-no-al-ejecutarlo-el-agente-inline)
- [L-002 — Los subagentes anidados tienen límite de profundidad fijo (5), no configurable](#l-002--los-subagentes-anidados-tienen-límite-de-profundidad-fijo-5-no-configurable)
- [L-003 — `sonnet` ya es 200K; la variante 1M lleva sufijo `[1m]` y se desactiva con `CLAUDE_CODE_DISABLE_1M_CONTEXT`](#l-003--sonnet-ya-es-200k-la-variante-1m-lleva-sufijo-1m-y-se-desactiva-con-claude_code_disable_1m_context)
- [L-004 — El 1M se gobierna por alias vía `ANTHROPIC_DEFAULT_<MODELO>_MODEL`, no solo con el interruptor global](#l-004--el-1m-se-gobierna-por-alias-vía-anthropic_default_modelo_model-no-solo-con-el-interruptor-global)

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

### L-003 — `sonnet` ya es 200K; la variante 1M lleva sufijo `[1m]` y se desactiva con `CLAUDE_CODE_DISABLE_1M_CONTEXT`
- **Contexto:** El comando `foda-progress` consumía créditos al correr Sonnet; se había intentado `model: sonnet` y `model: claude-sonnet-4-6` sin resolverlo.
- **Qué pasó:** Los aliases/IDs `sonnet` y `claude-sonnet-4-6` **ya son la ventana de 200K**. La variante de 1M es explícita: `sonnet[1m]` / `claude-sonnet-4-6[1m]`. El frontmatter nunca fue el problema; el 1M venía del modelo por defecto de la cuenta (un default `sonnet[1m]` hace que **incluso el alias `sonnet` resuelva a 1M**) o de un contexto de sesión > 200K que auto-escala a 1M. En planes Max/Team/Enterprise, **Sonnet 1M consume créditos** (Opus 1M va incluido).
- **Lección:** Para garantizar 200K, no basta con elegir el ID; hay que **desactivar la variante 1M** con la variable `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`, que la quita del selector de modelos.
- **Cómo aplicar:** Se agregó `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` al `env` de `.claude/settings.json` del proyecto (ver `D-006`). Para auditar el modelo real de un comando, invocarlo tecleando `/comando` (no inline) y leer el auto-reporte.
- **Fecha:** 2026-06-27

### L-004 — El 1M se gobierna por alias vía `ANTHROPIC_DEFAULT_<MODELO>_MODEL`, no solo con el interruptor global
- **Contexto:** Queríamos Opus en 1M (sesión principal) pero Sonnet en 200K (comandos como `foda-progress`), sin pagar créditos por Sonnet 1M. El único lever que conocíamos (`CLAUDE_CODE_DISABLE_1M_CONTEXT`) es global y mataría también el 1M de Opus.
- **Qué pasó:** La doc oficial (`model-config`, sección *Environment variables*) aclara que el sufijo `[1m]` **se lee por variable, no global**: `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL` controlan a qué modelo (y con/ sin `[1m]`) resuelve **cada alias** por separado. Fijando `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-4-6` (sin `[1m]`), el alias `sonnet` queda en 200K sin tocar Opus.
- **Lección:** El 1M no es todo-o-nada. Se puede tener **Opus 1M + Sonnet 200K** simultáneamente anclando cada alias por su variable. Esto **supera** a `CLAUDE_CODE_DISABLE_1M_CONTEXT` (D-006), que era el martillo global.
- **Cómo aplicar:** Para cualquier comando/agente del motor, elige el modelo por **alias** (`haiku`/`sonnet`/`opus`) en el frontmatter, y gobierna su ventana con `ANTHROPIC_DEFAULT_<MODELO>_MODEL` en `.claude/settings.json`. Para forzar 1M, añade `[1m]` a esa variable; para 200K, omítelo. Ver `D-008`.
- **Fecha:** 2026-06-27

<!--
### L-001 — <título corto>
- **Contexto:** qué estábamos haciendo.
- **Qué pasó:** el hecho o problema.
- **Lección:** qué aprendimos.
- **Cómo aplicar:** acción concreta para el futuro.
- **Fecha:** YYYY-MM-DD
-->
