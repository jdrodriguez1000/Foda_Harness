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
- [D-008 — Anclar el alias `sonnet` a 200K por variable de entorno, conservando Opus 1M](#d-008--anclar-el-alias-sonnet-a-200k-por-variable-de-entorno-conservando-opus-1m)
- [D-009 — Modelo de ejecución plano: A es la única instancia que spawnea (reemplaza el anidamiento de D-005)](#d-009--modelo-de-ejecución-plano-a-es-la-única-instancia-que-spawnea-reemplaza-el-anidamiento-de-d-005)
- [D-010 — Orchestrator (B) y Evaluator (C) por flujo, no genéricos](#d-010--orchestrator-b-y-evaluator-c-por-flujo-no-genéricos)
- [D-011 — Método de construcción flujo por flujo: brief → diseño → plan → build, con gate humano](#d-011--método-de-construcción-flujo-por-flujo-brief--diseño--plan--build-con-gate-humano)
- [D-012 — Inputs de prueba por workflow: golden client + snapshots cacheados (híbrido), no re-ejecución acumulativa](#d-012--inputs-de-prueba-por-workflow-golden-client--snapshots-cacheados-híbrido-no-re-ejecución-acumulativa)
- [D-014 — Complejidad del cliente como matriz 2×2 (producto × geografía): generador parametrizado, fixtures escalonados, jerarquías en el contrato de Discovery/Onboarding](#d-014--complejidad-del-cliente-como-matriz-2x2-producto--geografía-generador-parametrizado-fixtures-escalonados-jerarquías-en-el-contrato-de-discoveryonboarding)
- [D-015 — Enfoque por fases (walking skeleton): brief de los 14 → slice mínima end-to-end → profundización (enmienda D-011)](#d-015--enfoque-por-fases-walking-skeleton-brief-de-los-14--slice-mínima-end-to-end--profundización-enmienda-d-011)
- [D-016 — Plantilla de brief con "Escalera de capacidades" (L0→Ln) y `roadmap.md` como matriz de control (workflow × iteración)](#d-016--plantilla-de-brief-con-escalera-de-capacidades-l0ln-y-roadmapmd-como-matriz-de-control-workflow--iteración)
- [D-017 — Nomenclatura de iteraciones: bandas estilo Caden (Tracer Bullet → Stabilization → MVP → Evolution → Final) y numeración de los 14 flujos de 5 en 5](#d-017--nomenclatura-de-iteraciones-bandas-estilo-caden-tracer-bullet--stabilization--mvp--evolution--final-y-numeración-de-los-14-flujos-de-5-en-5)
- [D-018 — Mapa de procesos oficial (`700_brief/000_general_process.md`) como fuente de verdad de los nombres canónicos de artefactos (en inglés)](#d-018--mapa-de-procesos-oficial-700_brief000_general_processmd-como-fuente-de-verdad-de-los-nombres-canónicos-de-artefactos-en-inglés)

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
- **Estado:** Reemplazada parcialmente por D-009 (se abandona el anidamiento B→Workers; se conserva la política de `tools` que impide a C y a los Workers spawnear)
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

### D-008 — Anclar el alias `sonnet` a 200K por variable de entorno, conservando Opus 1M
- **Estado:** Aceptada (complementa D-007)
- **Fecha:** 2026-06-27
- **Contexto:** Tras `D-007` la sesión principal corre en **Opus 1M** (deseado, sin costo). Pero al invocar `/foda-progress` (`model: sonnet`) el alias `sonnet` resolvía a **Sonnet 1M** y pedía créditos (`API Error: Usage credits required for 1M context`). El default global de `sonnet` del usuario lleva la variante 1M. Se necesita que **solo** Sonnet quede en 200K **sin** desactivar el 1M de Opus.
- **Decisión:** Agregar `"ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-6"` (sin sufijo `[1m]`) al `env` de `.claude/settings.json`. La doc oficial confirma que el `[1m]` se lee **por variable, no global**: cada alias controla su propia ventana. Así el alias `sonnet` queda anclado a 200K y Opus conserva su 1M (vía picker / auto-upgrade, su propia variable). Se mantiene `model: sonnet` (alias) en `foda-progress` y `model: haiku` en `foda-next`.
- **Alternativas consideradas:** (a) Reintroducir `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` (D-006) — descartada: es global y mataría también el 1M de Opus, que el usuario quiere conservar. (b) Usar el ID con fecha `claude-sonnet-4-6` directo en el frontmatter — insuficiente: como override no anclaba la ventana y heredaba el 1M de la sesión.
- **Consecuencias:** Requiere reiniciar para tomar efecto. Opus 1M intacto; `foda-progress` corre Sonnet 200K sin créditos. Patrón reutilizable para cualquier comando/agente del motor: el modelo se elige por alias y su ventana se gobierna por la variable `ANTHROPIC_DEFAULT_<MODELO>_MODEL`. Opcional: anclar también `ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-4-8[1m]` si se quiere el 1M de Opus explícito (no necesario para la sesión principal). Ver `L-004`.

### D-009 — Modelo de ejecución plano: A es la única instancia que spawnea (reemplaza el anidamiento de D-005)
- **Estado:** Aceptada (reemplaza parcialmente D-005)
- **Fecha:** 2026-06-27
- **Contexto:** `D-005`/§3.1 de `methodology.md` apostaban por **subagentes anidados** (B lleva la herramienta `Agent` y spawnea a los Workers), lo que **depende de Claude Code v2.1.172+**. Al estudiar el harness de referencia **Caden** (`C:\Users\USUARIO\Documents\TripleS\Caden_Harness`), comprobamos que eligió deliberadamente un **modelo plano** "robusto a la versión de Claude Code", ya validado en seco en 2 de sus 6 arneses.
- **Decisión:** Adoptar el **modelo plano**: la **sesión principal (Instancia A / Governor) es la única que spawnea**. Roles:
  - **A (Governor):** orquesta, persiste estado, gestiona checkpoints y el gate humano; **única que invoca subagentes** (tiene `Agent`).
  - **B (Orchestrator):** **solo planifica** — lee el contrato + insumos y devuelve el `orchestration_plan` (qué workers, en qué orden, con qué inputs/outputs). **No ejecuta ni spawnea** (`tools: Read`).
  - **Workers:** producen los entregables (cada uno su artefacto al filesystem). No spawnean.
  - **C (Evaluator):** audita con la rúbrica del flujo y emite veredicto (`tools: Read, Write`). No spawnea.
  - B, Workers y C **no se invocan entre sí**: todo pasa por A.
- **Alternativas consideradas:** Mantener el anidamiento de `D-005` — descartada por acoplar el motor a una versión específica de Claude Code y no estar validada por nosotros; el modelo plano cumple igual `P1` (separación de roles) y `P3` (C independiente) sólo con la política de `tools`.
- **Consecuencias:** Se conserva de `D-005` la política de herramientas (C y Workers **sin** `Agent`). Se invierte quién ejecuta el plan: ya **no** es B sino A. Hay que adaptar §3, §3.1 y §12.2 de `methodology.md`. El límite de profundidad de `L-002` deja de ser una restricción de diseño (el árbol es plano: A → {B | Workers | C}, todos a nivel 1).

### D-010 — Orchestrator (B) y Evaluator (C) por flujo, no genéricos
- **Estado:** Aceptada
- **Fecha:** 2026-06-27
- **Contexto:** Quedaba abierto si el motor tendría **un** `foda-orchestrator` y **un** `foda-evaluator` genéricos (parametrizados por contrato/rúbrica como datos) o **uno por flujo**. Caden resuelve con **uno por flujo** (`discovery-orchestrator`/`architecture-orchestrator`, `discovery-evaluator`/`architecture-evaluator`).
- **Decisión:** **B y C son específicos por flujo.** La razón: en la práctica la **cadena de workers va embebida en B** y la **rúbrica (dimensiones, vetos, anclas few-shot) va embebida en C**; no son datos parametrizables limpios sino el "cerebro" del agente. Nomenclatura del motor: `foda-<flujo>-orchestrator`, `foda-<flujo>-evaluator`, y workers `foda-<flujo>-<rol>`.
- **Alternativas consideradas:** B/C genéricos parametrizados — descartada: más DRY pero más difícil de afinar por dominio y no validada; la rúbrica/cadena cambian tanto entre *Cleaning* y *Modelling* que un prompt genérico se vuelve frágil.
- **Consecuencias:** Cada carpeta de flujo del motor contiene sus propios `agents/` (B + workers + C). Lo **transversal** (esquema de `fda-harness-state.json`, knowledge, comandos de gate, `CLAUDE.md`) se construye una sola vez. Habilita la construcción **flujo por flujo** (`D-011`).

### D-011 — Método de construcción flujo por flujo: brief → diseño → plan → build, con gate humano
- **Estado:** Aceptada
- **Fecha:** 2026-06-27
- **Contexto:** El motor tiene 14 flujos; construirlos todos a la vez es inviable. Caden construye **arnés por arnés** con un método de 4 pasos secuenciales (`700_brief/` → `705_design/` → `710_plan/` → `720_build/`), aprobando cada paso con el humano, y hoy tiene 2 de 6 arneses construidos.
- **Decisión:** Adoptar el mismo método: construir **un workflow a la vez** pasando por **brief → diseño → plan → build**, con **gate humano entre pasos**. Cada flujo del motor vive en una **carpeta autocontenida** con la anatomía: `agents/`, `skills/`, `schemas/` (estado por flujo `fda-execution-state` + `project-progress`), `contract/`, `deliverables/` (moldes), `evaluation/` (verdict + metrics + testbank E9). Lo transversal vive en la raíz del plano de construcción.
- **Alternativas consideradas:** Construir todos los flujos en paralelo o un genérico que sirva a todos — descartadas por `E4` (mínima complejidad) y por riesgo de envenenar aguas abajo sin validación temprana (`E9`).
- **Consecuencias:** Define la estructura de carpetas del motor (cierra el diseño pendiente de T-002) y el orden de trabajo. Falta decidir **por cuál flujo empezar** (probablemente *Discovery*, primero de la tubería). El instalador (T-003) copiará la carpeta del flujo + lo transversal a la instancia. Detalle de nombres de carpeta y numeración: a definir al diseñar el árbol.

### D-012 — Inputs de prueba por workflow: golden client + snapshots cacheados (híbrido), no re-ejecución acumulativa
- **Estado:** Aceptada
- **Fecha:** 2026-06-27
- **Contexto:** Al construir el motor **flujo por flujo** (`D-011`), la tubería FODA es **acumulativa**: cada workflow consume el handoff y la capa de datos del anterior (*Cleaning*←bronze, *Modelling*←gold, *Inferences*←`best_model.pkl`). Para construir/validar el workflow N se necesita un input que represente la salida de 1..N‑1. La duda: ¿hay que re-ejecutar toda la cadena hasta N cada vez? Caden lo evita con **fixtures fabricados** en el testbank (`020_architecture/.../roadmap-manifest.sample.json`), pero en FODA los artefactos son **pesados** (datasets, modelo entrenado) y fabricarlos a mano es inviable y arriesgado.
- **Decisión:** Adoptar un **híbrido**: mantener **un cliente de prueba canónico (golden client)** en el plano de construcción; correr la cadena **una vez** y **congelar la salida de cada capa/artefacto como snapshot** (fixture *real*, no fabricado). Para construir el workflow N se **carga el snapshot del upstream** en vez de recomputar. La inmutabilidad **bronze/silver/gold** habilita reusar cada capa congelada tal cual. Un snapshot upstream se **regenera solo si cambia su contrato**.
- **Alternativas consideradas:** (a) **Fixtures fabricados por workflow** (como Caden) — descartada: para datos/ML un fixture irreal valida contra basura. (b) **Re-ejecución acumulativa** (correr 1..N‑1 cada vez) — descartada por costo en tokens/tiempo (torneo de modelos), justo el problema que motivó la pregunta.
- **Consecuencias:** Se construye cada workflow **aislado** (sin re-correr la cadena) con fixtures fieles. Costo: **mantener los snapshots** y regenerarlos cuando un contrato upstream cambie (riesgo de fixture stale → registrar versión del contrato junto al snapshot). Implica diseñar en el plano de construcción una zona de **golden client + snapshots por capa/artefacto** (nueva tarea de infraestructura). El testbank E9 de cada workflow apunta a su snapshot upstream en vez de a una muestra inventada. Encaja con la durabilidad/checkpoints de la metodología (§6).

### D-014 — Complejidad del cliente como matriz 2×2 (producto × geografía): generador parametrizado, fixtures escalonados, jerarquías en el contrato de Discovery/Onboarding
- **Estado:** Aceptada (complementa D-012)
- **Fecha:** 2026-06-27
- **Contexto:** Los clientes reales varían en dos dimensiones ortogonales que definen la **granularidad y cardinalidad de series** del forecasting: jerarquía de **producto** (familia→categoría→subcategoría→SKU) y jerarquía de **geografía** (región→país→ciudad→sede). Sus combinaciones dan 4 casos: **C1** mínimo (1 producto, 1 sede) · **C2** (1 producto, geo jerárquica) · **C3** (producto jerárquico, 1 sede) · **C4** mayor (ambas jerárquicas). Cada par `producto × ubicación` es una **serie de tiempo**. Esto activa capacidades reales: escala (1 vs miles de series), **reconciliación jerárquica** (bottom-up/top-down/middle-out), agregación y MAPE por nivel, features jerárquicas, cold-start de series ralas.
- **Decisión:**
  1. **Modelado de pruebas:** un **generador sintético parametrizado** por `(profundidad jerarquía producto, profundidad jerarquía geo, nº series, longitud histórica)`. Las 4 esquinas se instancian como **snapshots** del golden client (D-012), de forma **escalonada** (E4/E9): **C1 = golden client primario** (walking skeleton, corre la cadena barato e iterativo); **C4 = fixture de estrés** (se corre poco, en el gate "Done"/E9 amplio: escala + ambas jerarquías + reconciliación); **C2/C3 = diagnóstico bajo demanda** (aíslan un eje cuando un workflow falla). No construir las 4 desde el inicio.
  2. **Modelado del motor:** las dos jerarquías se **capturan en el contrato de Discovery/Onboarding** (`client_register.yaml`, `map_client_data.json`) como el **grain** del cliente, y se propagan a toda la tubería. No son solo una variable de pruebas: son concepto de primera clase de los contratos del motor.
- **Alternativas consideradas:** (a) Construir las 4 fixtures fijas ya — descartada por sobre-ingeniería temprana (E4) y costo de mantenimiento. (b) Solo C1 y posponer jerarquías — descartada: arriesga diseñar workflows que no soporten jerarquía/escala real (la mayoría de clientes reales son C3/C4); deuda que aflora tarde. (c) Jerarquías solo en pruebas — descartada por desacoplar las pruebas del diseño real de los contratos.
- **Consecuencias:** El testbank de cada workflow apunta al **snapshot del caso relevante para él** (Discovery basta con el esquema; Modelling necesita C4). Amplía T-014 (el generador debe parametrizar ambas jerarquías). Impone un requisito de diseño a Discovery/Onboarding (T-013): sus contratos deben representar grain multinivel de producto y geografía. La reconciliación jerárquica se vuelve una capacidad esperada de Modelling/Inferences/Reporting.

### D-015 — Enfoque por fases (walking skeleton): brief de los 14 → slice mínima end-to-end → profundización (enmienda D-011)
- **Estado:** Aceptada (enmienda D-011; no lo reemplaza)
- **Fecha:** 2026-06-28
- **Contexto:** `D-011` es **profundidad-primero**: construir cada flujo *completo* (brief→diseño→plan→build, con B+workers+C+rúbricas+testbank) antes de pasar al siguiente. Aplicado a los 14 flujos de FODA, el **time-to-MVP es muy largo**: solo hay algo demostrable tras construir todo. Y un cliente **no valida el código de *Cleaning***; valida el **resultado** (pronóstico, escenarios, reporte — flujos 10–13), que con depth-first llega al final. `D-014` ya nombraba a **C1 como "walking skeleton"**: faltaba elevarlo de táctica de pruebas a **método de construcción**.
- **Decisión:** Adoptar un **híbrido por fases**:
  - **Fase 0 — Contratos + briefs de los 14 flujos** (barato, alto valor): define la *ambición completa* y el contrato in/out de cada flujo; fuerza la integración y propaga el grain de `D-014`. No construye agentes.
  - **Fase 1 — Walking skeleton** (rebanada vertical fina): implementación mínima *happy-path* de cada flujo sobre **C1**, encadenada de punta a punta, produciendo un reporte. Se **simplifica deliberadamente lo caro** (*Modelling* = 1 modelo simple, no el torneo; *Simulation* = Montecarlo básico; Discovery/Onboarding casi stub). **Esto es lo que el cliente valida.**
  - **Fase 2 — Profundización flujo por flujo** (`D-011` tal cual), **priorizando por valor** (Modelling, Inferences, Scenarios, Reporting primero; Discovery/Onboarding delgados más tiempo).
  - **Control:** matriz **workflow × iteración** en `roadmap.md` (ver `D-016`). Una **iteración = una vertical slice = una columna** que toma un peldaño de la *escalera de capacidades* de cada flujo.
- **Alternativas consideradas:** (a) Mantener `D-011` puro (depth-first) — descartada por time-to-MVP largo y por dejar la validación con cliente al final. (b) Construir todo en paralelo sin orden — descartada por `E4`/`E9`.
- **Consecuencias:** `D-011` **no se reemplaza**, se reubica como el **método de la Fase 2** (profundización dentro de una slice). Cambia el próximo paso: **brief de los 14 + definir Slice 1** antes que T-002 a profundidad. El riesgo `E9` (envenenar aguas abajo sin validación) se mitiga: el skeleton se valida **end-to-end contra C1** y los evaluadores (C) llegan en la Fase 2; se acepta validación más ligera en Fase 1 **a cambio de velocidad**, conscientemente. **Punto abierto:** nomenclatura de iteraciones (bandas estilo Caden — Tracer Bullet → Stab → MVP → Evol → Final — vs. numeración simple Slice 1..n) — **pendiente de decidir** (ver T-016).

### D-016 — Plantilla de brief con "Escalera de capacidades" (L0→Ln) y `roadmap.md` como matriz de control (workflow × iteración)
- **Estado:** Aceptada (complementa D-015)
- **Fecha:** 2026-06-28
- **Contexto:** El usuario quiere **no perder el control**: saber siempre qué se implementó de cada workflow, qué falta y cuándo se implementará, además de poder ver el futuro. Mezclar el "mínimo vs. siguiente" en un solo lugar oculta una de las dos vistas necesarias: la **vertical** (por workflow) y la **horizontal** (entre workflows / por iteración).
- **Decisión:** Separar en **dos artefactos** con responsabilidades distintas:
  1. **Brief (vista vertical, por workflow):** plantilla = estructura de los briefs de Caden (objetivo, alcance *qué hace* / *qué NO hace*, insumos, artefactos esperados, criterios Done, riesgos, siguiente paso) **+ sección nueva "Escalera de capacidades"**: tabla **L0 (mínimo) → L1 → … → Ln** que ordena la *ambición completa* del flujo por madurez. El brief describe **el futuro** del flujo, no solo el mínimo.
  2. **`roadmap.md` (vista horizontal, entre workflows):** matriz **workflow × iteración** en `800_persistence/`. Una **iteración = vertical slice = columna** que toma **un peldaño de la escalera de cada flujo**. La matriz se **ensambla** a partir de las escaleras de los briefs. Vocabulario de estado por celda: **`vacío` / `planeado` / `mínimo` / `completo`**.
- **Alternativas consideradas:** (a) Meter el slicing **dentro** del brief — descartada: mezcla niveles y se pierde la vista de tubería completa. (b) Solo `roadmap.md` sin escalera en el brief — descartada: se pierde la vista del *futuro por workflow*.
- **Consecuencias:** Se crea una **plantilla de brief FODA** (nueva tarea) y el archivo **`roadmap.md`** (memoria de construcción del motor → vive en `800_persistence/`, no es runtime de cliente). `tasks.md` sigue rastreando tareas granulares de la slice en curso; `roadmap.md` es el tablero estratégico. **Pendiente:** la nomenclatura de las columnas depende de `D-015` (punto abierto, T-016).

### D-017 — Nomenclatura de iteraciones: bandas estilo Caden (Tracer Bullet → Stabilization → MVP → Evolution → Final) y numeración de los 14 flujos de 5 en 5
- **Estado:** Aceptada (cierra el punto abierto de D-015 / resuelve T-016; complementa D-016)
- **Fecha:** 2026-06-28
- **Contexto:** `D-015` dejó **abierta** la nomenclatura de las columnas de iteración del `roadmap.md`: bandas estilo Caden vs. numeración simple (Slice 1..n). El usuario indicó que **siempre ha trabajado con las bandas de Caden** y prefiere ese vocabulario. Paralelamente, al numerar los flujos surgió `015_onboarding` (entre `010` y `020`), rompiendo el incremento de 10 heredado de Caden.
- **Decisión:**
  1. **Iteraciones = bandas estilo Caden:** **Tracer Bullet → [Stabilization 1..n] → MVP → [Evolution 1..n] → Final**. Las 3 anclas (Tracer Bullet, MVP, Final) existen siempre; Stabilization y Evolution son bandas opcionales (0..n) que se insertan según haga falta. La **Iteración 1 / walking skeleton = Tracer Bullet** (L0 de los 14 flujos encadenados sobre C1). Las columnas del `roadmap.md` pasan de numéricas a estas bandas.
  2. **Numeración de flujos de 5 en 5:** los 14 flujos se numeran `010, 015, 020, …, 075` (Monitoring · Alerting juntos en `075`, como `CLAUDE.md §4`). El paso de 5 deja hueco para insertar flujos intermedios sin renumerar. Lista canónica: `010_discovery, 015_onboarding, 020_ingestion, 025_profiling, 030_cleaning, 035_derivation, 040_exploration, 045_featuring, 050_modelling, 055_inferences, 060_simulation, 065_scenarios, 070_reporting, 075_monitoring_alerting`.
- **Alternativas consideradas:** (a) Numeración simple de iteraciones (Slice 1..n) — descartada por preferencia explícita del usuario y por alineación con su experiencia previa (Caden). (b) Incrementos de 10 en los flujos — descartada: ya se introdujo `015`, y el paso de 5 da más holgura para inserciones.
- **Consecuencias:** Se reescribe el encabezado y el texto explicativo de `roadmap.md` (columnas = bandas). Los briefs nombran la primera iteración como **Tracer Bullet** (no "Iteración 1") en su §9. Las referencias cruzadas de numeración en los briefs ya escritos (Discovery, Onboarding) se corrigen al esquema de 5 en 5. La relación brief↔roadmap de `D-016` no cambia: el brief sigue siendo la vista vertical (escalera completa) y el roadmap la horizontal (qué peldaño entra en cada banda).

### D-018 — Mapa de procesos oficial (`700_brief/000_general_process.md`) como fuente de verdad de los nombres canónicos de artefactos (en inglés)
- **Estado:** Aceptada (complementa D-016)
- **Fecha:** 2026-06-28
- **Contexto:** Al revisar la vista de entradas/salidas de la tubería, el usuario pidió (a) elevarla a documento oficial dentro de `700_brief/`, (b) que **todos** los artefactos de entrada/salida tengan **nombre definido** (sin "a definir"; p. ej. el informe de salud de Profiling no tenía nombre) y (c) que los nombres de archivo estén **en inglés**.
- **Decisión:** Crear **`700_brief/000_general_process.md`** como **documento oficial** y **fuente de verdad de los nombres canónicos** de los artefactos de la tubería (entradas/salidas por workflow + tabla maestra). Reglas: nombres de archivo **en inglés** con extensión explícita; **capas** `bronze`/`silver`/`gold`; **exportables** con el mismo nombre base (`<artifact>.csv`/`.xlsx`). Se nombran los artefactos que la fuente no nombraba: **`data_health.json`** (Profiling), **`ingestion_report.json`** (Ingestion) y los documentos legibles de Discovery **`problem_statement.md`** y **`data_structure.md`**. El documento describe **solo el contrato in/out** (qué entra/qué sale), no el "cómo". Los briefs individuales deben **coincidir** con este documento.
- **Alternativas consideradas:** (a) Dejar los nombres "a definir en el diseño" — descartada por la petición explícita de cerrar nombres ya. (b) Mantener el doc en `Template/` — descartada: se movió a `700_brief/` (se eliminó la copia de `Template/`). (c) Conservar el nombre con typo `general_processs.md` — descartada: se renombró a `000_general_process.md` (prefijo `000_` para que ordene primero como índice de procesos).
- **Consecuencias:** Al redactar cada brief nuevo (`050`–`075`) hay que **registrar sus artefactos en `000_general_process.md`** (sección de pendientes ya los lista) y mantener la coincidencia de nombres. Se actualizaron los briefs `010`, `020` y `025` para reflejar los nombres recién fijados. La tabla maestra de artefactos queda como referencia rápida de quién produce/consume cada uno.

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
