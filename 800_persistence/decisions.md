# Decisions — Motor FODA

> Decisiones de diseño y arquitectura tomadas durante la construcción del motor FODA.
> Registro tipo ADR (Architecture Decision Record) resumido.

---

## Índice
- [D-001 — Dos planos: Motor (FODA) e Instancia (fda)](#d-001--dos-planos-motor-foda-e-instancia-fda)
- [D-002 — Memoria de construcción en 800_persistence/](#d-002--memoria-de-construcción-en-800_persistence)
- [D-003 — Comandos de sesión ejecutan con Sonnet](#d-003--comandos-de-sesión-ejecutan-con-sonnet)
- [D-004 — Archivos de estado de runtime viven en la instancia (fda-)](#d-004--archivos-de-estado-de-runtime-viven-en-la-instancia-fda)
- [D-005 — Subagentes anidados y política de `tools` por instancia A/B/C/Workers](#d-005--subagentes-anidados-y-política-de-tools-por-instancia-abcworkers)
- [D-006 — Desactivar la ventana de 1M en el proyecto (`CLAUDE_CODE_DISABLE_1M_CONTEXT`)](#d-006--desactivar-la-ventana-de-1m-en-el-proyecto-claude_code_disable_1m_context)
- [D-007 — Reactivar la ventana de 1M al volver a Opus por defecto](#d-007--reactivar-la-ventana-de-1m-al-volver-a-opus-por-defecto)

---

## Decisiones

### D-001 — Dos planos: Motor (FODA) e Instancia (fda)
- **Estado:** Aceptada
- **Fecha:** 2026-06-27
- **Contexto:** El producto debe escalar a muchas empresas sin mezclar el código del harness con el de cada cliente.
- **Decisión:** Separar en dos planos que nunca se mezclan: el **MOTOR** (`foda-*`, definiciones canónicas reutilizables) y la **INSTANCIA** (`fda-*`, una carpeta externa por cliente). El runtime de la instancia nunca vuelve al motor. El puente es un instalador de terminal.
- **Origen:** `990_documents/expected_solution.md`.

### D-002 — Memoria de construcción en 800_persistence/
- **Estado:** Aceptada
- **Fecha:** 2026-06-27
- **Contexto:** Los archivos de memoria crecerán y no se quiere leerlos completos cada vez.
- **Decisión:** Mantener 4 archivos (`progress.md`, `tasks.md`, `lessons.md`, `decisions.md`), cada uno con un **índice** al inicio para búsqueda rápida.

### D-003 — Comandos de sesión ejecutan con Sonnet
- **Estado:** Aceptada
- **Fecha:** 2026-06-27
- **Contexto:** La sesión de trabajo corre con Opus, pero los comandos `foda-progress` y `foda-next` son tareas mecánicas (leer estado, actualizar persistencia, commit/push) que no requieren el modelo más potente.
- **Decisión:** Fijar `model: sonnet` en el frontmatter de ambos comandos. Cada slash-command puede declarar su propio modelo sin alterar el modelo de la sesión.
- **Consecuencias:** Ejecución más rápida y económica de los protocolos de inicio/cierre. Si se requiere más capacidad de razonamiento en un comando futuro, se ajusta su frontmatter individualmente.

### D-004 — Archivos de estado de runtime viven en la instancia (fda-)
- **Estado:** Aceptada
- **Fecha:** 2026-06-27
- **Contexto:** `methodology.md` define archivos de estado (`harness-state.json`, `execution-state.json`, `claude-progress.txt`). Hay que ubicarlos respecto a los dos planos de `D-001` y al `800_persistence/` del motor.
- **Decisión:** Los archivos de estado son artefactos de **runtime** de un cliente concreto, por lo que pertenecen al plano **INSTANCIA** y se renombran con prefijo `fda-`:
  - `fda-harness-state.json` — escrito solo por la Instancia A (Governor); fuente de verdad estratégica.
  - `fda-execution-state.json` — escrito solo por la Instancia B (Orchestrator); control de micro-tareas y Workers.
  - `project-progress.txt` — bitácora narrativa (renombre de `claude-progress.txt`); conserva nombre genérico por indicación explícita del usuario.
  Viven en la carpeta de la instancia (fuera de este repo), **no** en `800_persistence/`. El `800_persistence/` del motor (`progress.md`, `tasks.md`, `lessons.md`, `decisions.md`) sigue siendo exclusivamente **memoria de construcción del motor** (ver `D-002`).
- **Alternativas consideradas:** (a) Renombrar a `foda-*` y colocarlos en `800_persistence/` — descartada por mezclar planos (viola `D-001`). (b) Dejar nombres genéricos sin prefijo — descartada por ambigüedad sobre a qué plano pertenecen.
- **Consecuencias:** Refuerza la separación de planos. La regla "single writer" de `methodology.md` se mantiene con los nuevos nombres. El instalador (`install.sh`) deberá generar estos archivos en el esqueleto de la instancia.

### D-005 — Subagentes anidados y política de `tools` por instancia A/B/C/Workers
- **Estado:** Aceptada
- **Fecha:** 2026-06-27
- **Contexto:** El patrón A→B→Workers de `methodology.md` requiere que un subagente (B) spawnee otros subagentes (Workers). Había que confirmar que Claude Code lo soporta y fijar cómo se controla.
- **Decisión:** Apoyarse en los **subagentes anidados** (Claude Code v2.1.172+): la sesión principal actúa como Instancia A y spawnea B y C; B spawnea los Workers. Política de herramientas:
  - **B (Orchestrator):** incluye `Agent` en `tools` → puede spawnear Workers.
  - **C (Evaluator) y Workers:** **no** incluyen `Agent` (omitido o en `disallowedTools`) → no pueden spawnear a nadie, reforzando `P1` (separación de roles) y `P3` (evaluador independiente, "C no llama a nadie").
- **Alternativas consideradas:** Aplanar todo a la sesión principal (A llama directo a Workers) — descartada por violar `P1` y contaminar el contexto estratégico de A.
- **Consecuencias:** El árbol queda dentro del límite de profundidad de subagentes (5 niveles, ver `L-002`). El allowlist `Agent(tipo)` solo aplica al hilo principal (`claude --agent`); dentro de una definición de subagente la lista de tipos en el paréntesis se ignora (basta con incluir/omitir `Agent`).

### D-006 — Desactivar la ventana de 1M en el proyecto (`CLAUDE_CODE_DISABLE_1M_CONTEXT`)
- **Estado:** Reemplazada por D-007
- **Fecha:** 2026-06-27
- **Contexto:** Se busca trabajar con Sonnet de 200K tokens y evitar el consumo de créditos que implica la variante de 1M (premium en planes Max/Team/Enterprise). Ver `L-003`.
- **Decisión:** Agregar `"CLAUDE_CODE_DISABLE_1M_CONTEXT": "1"` al `env` de `.claude/settings.json` (alcance de proyecto). Esto elimina las variantes 1M del selector de modelos para cualquiera que trabaje en este repo. El comando `foda-progress` queda fijado en `model: claude-sonnet-4-6` (200K).
- **Alternativas consideradas:** (a) Solo cambiar el frontmatter del comando — insuficiente, porque el default global `sonnet[1m]` haría que el alias resolviera a 1M igual. (b) Aplicarlo global en `~/.claude/settings.json` — descartado por afectar todos los proyectos del usuario (incluido Opus 1M); se prefirió alcance de proyecto.
- **Consecuencias:** Requiere reiniciar la sesión para tomar efecto. Con 1M desactivado, ante un contexto > 200K Claude Code compacta en vez de escalar a 1M. `foda-next` se mantuvo sin cambios por decisión del usuario.

### D-007 — Reactivar la ventana de 1M al volver a Opus por defecto
- **Estado:** Aceptada
- **Fecha:** 2026-06-27
- **Contexto:** El modelo por defecto de la sesión volvió a **Opus 4.8**, cuya variante de 1M va **incluida** (no consume créditos premium, a diferencia de Sonnet 1M; ver `L-003`). Con `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` (de `D-006`) la sesión Opus quedaba atrapada en 200K, porque esa variable es un interruptor **global del proyecto** que desactiva el 1M de **todos** los modelos sin posibilidad de distinguir por modelo.
- **Decisión:** Quitar `CLAUDE_CODE_DISABLE_1M_CONTEXT` del `env` de `.claude/settings.json` (queda `"env": {}`), reactivando la ventana de 1M en el proyecto. Esto restituye Opus 1M (deseado y sin costo extra).
- **Alternativas consideradas:** (a) Desactivar solo el 1M de Sonnet — no existe tal granularidad; la variable es global. (b) Mantener `D-006` y aceptar Opus a 200K — descartada por contradecir el objetivo del usuario (aprovechar la ventana de 1M de Opus).
- **Consecuencias:** Requiere reiniciar la sesión para tomar efecto. La protección de `D-006` contra el consumo de créditos por **Sonnet 1M** se pierde a nivel de selector: el riesgo solo se materializa si alguien **selecciona manualmente** `sonnet[1m]`. Los comandos de sesión siguen protegidos porque están fijados al ID explícito `claude-sonnet-4-6` (200K), que no escala a 1M. Si en el futuro se vuelve a trabajar con Sonnet por defecto, reconsiderar reintroducir `D-006`.

---

<!--
Plantilla para nuevas decisiones:
### D-XXX — <título>
- **Estado:** Propuesta | Aceptada | Reemplazada por D-YYY
- **Fecha:** YYYY-MM-DD
- **Contexto:** por qué surge la decisión.
- **Decisión:** qué se decidió.
- **Alternativas consideradas:** opciones descartadas y por qué.
- **Consecuencias:** implicaciones.
-->
