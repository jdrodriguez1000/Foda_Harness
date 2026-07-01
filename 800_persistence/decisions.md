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
- [D-019 — Convención `<flujo>_config.yaml` para inputs de configuración de autoría humana, y parámetros financieros de Reporting leídos de bronze](#d-019--convención-flujo_configyaml-para-inputs-de-configuración-de-autoría-humana-y-parámetros-financieros-de-reporting-leídos-de-bronze)
- [D-020 — La metodología es la ambición (Ln); el andamiaje transversal (estado, A/B/C, evaluador) se construye por bandas con su propia escalera en el roadmap](#d-020--la-metodología-es-la-ambición-ln-el-andamiaje-transversal-estado-abc-evaluador-se-construye-por-bandas-con-su-propia-escalera-en-el-roadmap)
- [D-021 — Método de construcción por vertical slice en dos niveles (banda/celda) y protocolo agéntico escritor/revisor/gate; las bandas son madurez del motor, no estado de la instancia](#d-021--método-de-construcción-por-vertical-slice-en-dos-niveles-bandacelda-y-protocolo-agéntico-escritorrevisorgate-las-bandas-son-madurez-del-motor-no-estado-de-la-instancia)
- [D-022 — El stack tecnológico de la instancia (lenguaje/ML, motor de datos bronze/silver/gold, forma de la app, patrones) se decide ANTES de cualquier vertical slice](#d-022--el-stack-tecnológico-de-la-instancia-lenguajeml-motor-de-datos-bronzesilvergold-forma-de-la-app-patrones-se-decide-antes-de-cualquier-vertical-slice)
- [D-023 — Lenguaje de la instancia: Python con pandas/polars, scikit-learn, numpy, SQLAlchemy/psycopg](#d-023--lenguaje-de-la-instancia-python-con-pandaspolars-scikit-learn-numpy-sqlalchemypsycopg)
- [D-024 — Motor de datos de bronze/silver/gold: PostgreSQL](#d-024--motor-de-datos-de-bronzesilvergold-postgresql)
- [D-025 — Forma de la app: batch multi-cliente operado por 1 DS para N clientes, con gate humano. Sin API web en esta fase](#d-025--forma-de-la-app-batch-multi-cliente-operado-por-1-ds-para-n-clientes-con-gate-humano-sin-api-web-en-esta-fase)
- [D-026 — Patrones de diseño base: monolito modular por capas + hexagonal ligero (puerto/adaptador para acceso a datos)](#d-026--patrones-de-diseño-base-monolito-modular-por-capas--hexagonal-ligero-puertoadaptador-para-acceso-a-datos)
- [D-027 — Aislamiento multi-tenant en PostgreSQL: esquema por cliente (schema-per-tenant)](#d-027--aislamiento-multi-tenant-en-postgresql-esquema-por-cliente-schema-per-tenant)
- [D-028 — Hosting del Postgres de construcción (golden client) en Docker local, puerto 55432](#d-028--hosting-del-postgres-de-construcción-golden-client-en-docker-local-puerto-55432)
- [D-029 — Protocolo de construcción por celda (Diseñar/Planear/Ejecutar/Probar/Verificar) dimensionado a E4: carriles separados, peso mínimo por artefacto, independencia creciente (3 contextos frescos)](#d-029--protocolo-de-construcción-por-celda-diseñarplanearejecutarprobarverificar-dimensionado-a-e4-carriles-separados-peso-mínimo-por-artefacto-independencia-creciente-3-contextos-frescos)

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

### D-019 — Convención `<flujo>_config.yaml` para inputs de configuración de autoría humana, y parámetros financieros de Reporting leídos de bronze
- **Estado:** Aceptada (complementa D-018)
- **Fecha:** 2026-06-28
- **Contexto:** Al redactar los briefs `050`–`075` aparecieron varios **inputs de configuración que el humano construye** para dirigir un flujo (torneo de modelos, simulación, escenarios). Había que fijar sus nombres canónicos de forma consistente con los ya existentes (`data_cleaner.yaml`, `feature_engineering.yaml`). Además, Reporting (`070`) necesita **parámetros financieros** (precio/costo unitario, costo de inventario) que la tubería no produce.
- **Decisión:** (a) Los inputs de **configuración de autoría humana** que parametrizan un flujo se nombran **`<flujo>_config.yaml`**: **`modelling_config.yaml`** (catálogo de modelos, hiperparámetros, baseline ingenuo, métrica y reglas de selección), **`simulation_config.yaml`** (variables de influencia —lead time, TRM, inflación— **opcionales y extensibles**, por producto/serie) y **`scenarios_config.yaml`** (escenarios "¿qué pasa si…?" como **deltas** dirigidos sobre variables, lista abierta y extensible). Principio común: **"reglas como dato"** — el catálogo/variables son entrada declarativa, nunca cableadas en el agente; agregar una variable = editar el YAML, no el motor. (b) Los **parámetros financieros** de `070_reporting` se **leen de la capa bronze** (las tablas que el cliente entrega), con su mapeo declarado en Onboarding/`map_client_data.json`; **no** se crea un insumo/YAML nuevo para ellos. (c) Modelling corre primero un **modelo ingenuo** como baseline: superar al ingenuo es el **primer filtro** del torneo antes de la selección humana. (d) `075` se nombra **`075_monitoring`** y **agrupa Monitoring + Alerting** (es recurrente y cierra el ciclo realimentando `050`/`055`/`060` con gate humano).
- **Alternativas consideradas:** Para los nombres de config se consideró `modelling.json`/`simulation.json` como input (lo que sugería la fuente), descartado por chocar con el artefacto de **salida**; y nombres evocadores (`champions_tournament.yaml`), descartados por menos neutrales. Para los parámetros financieros se consideró ampliar `contract_data.json` o crear un insumo dedicado; descartados a favor de leerlos de **bronze** (mantiene la trazabilidad al dato crudo del cliente).
- **Consecuencias:** `000_general_process.md` registra los tres `*_config.yaml` como entradas de autoría humana y los nuevos artefactos de salida (`modelling.json`, `best_model.pkl`, `inferences.json`, `simulation.json`, `scenarios.json`, `reporting.json`, `monitoring.json`, `alerting.json`). Profiling/Onboarding deberían verificar la presencia de los campos financieros en bronze. Los flujos `060`/`065` deben tratar las variables como entradas extensibles (no ramas cableadas).

### D-020 — La metodología es la ambición (Ln); el andamiaje transversal (estado, A/B/C, evaluador) se construye por bandas con su propia escalera en el roadmap
- **Estado:** Aceptada (complementa D-015, D-016; ancla E4 / NC-2)
- **Fecha:** 2026-06-28
- **Contexto:** El usuario preguntó cómo se trabajarán los temas que describen `950_guideline/methodology.md` y `principles.md` —persistencia de estado por iteración, patrón A/B/C, evaluador calibrado, ejecución durable, context resets, CR, knowledge base— y si se crean en el Tracer Bullet y se afinan después. Surgió un hueco: esos temas son **transversales** (no son un workflow), pero el `roadmap.md` es *workflow × banda* y la escalera L0→Ln vive **por brief de flujo**; no había dónde ubicarlos.
- **Decisión:** (a) **Distinguir dos persistencias:** la de **construcción del motor** (`800_persistence/`, ya operativa) vs. la de **runtime de instancia** (`fda-harness-state.json`, `fda-execution-state.json`, `project-progress.txt`, `/eval/`, `/knowledge/` — `fda-*`, aún por construir). La pregunta aplica a la segunda. (b) `methodology.md`/`principles.md` describen la **ambición completa (Ln)**, **no** el L0: por **E4 / NC-2 / D-015** se construye el andamiaje **mínimo** en el Tracer Bullet y se profundiza **banda por banda**, agregando un componente solo cuando se demuestre que su ausencia degrada la calidad (E4 §10). (c) **Invariantes desde el Tracer Bullet** (no deferibles): handoff de artefactos en filesystem (P2), trazabilidad (P8), capas bronze/silver/gold inmutables, gate humano de Modelling, y persistencia mínima + git (E1). (d) **Diferibles a bandas posteriores:** separación A/B/C completa (en L0 puede ser una sola sesión sin evaluador independiente), evaluador C calibrado (rúbrica/few-shot/anclas), ejecución durable/resume, context resets orquestados, CR management y re-evaluación de la knowledge base. (e) El **andamiaje transversal tiene su propia escalera**: se modela como **filas transversales (`TR-x`)** en `roadmap.md`, separadas de los 14 workflows, cada una con su progresión por banda.
- **Alternativas consideradas:** (1) Meter el andamiaje dentro de la escalera de cada brief de flujo — descartado: es transversal, lo duplicaría en 14 lugares. (2) Construir A/B/C + estado completo desde el Tracer Bullet — descartado por violar E4/NC-2 (sobre-ingeniería temprana) y retrasar el time-to-MVP (`D-015`). (3) Dejarlo implícito y resolverlo ad hoc en cada flujo — descartado: sin una escalera explícita se pierde el control del "cuándo".
- **Consecuencias:** `roadmap.md` gana filas transversales `TR-1` (estado & persistencia `fda-*`), `TR-2` (patrón A/B/C), `TR-3` (evaluador + rúbrica), `TR-4` (ejecución durable / checkpoints / context resets). **T-017** debe definir el L0 de cada una de esas filas además del L0 de los 14 flujos. La metodología no se reescribe: se reinterpreta su lectura (es Ln, se aterriza por bandas). Conecta con `T-002` (árbol de carpetas) y `T-014` (golden client/snapshots).

### D-021 — Método de construcción por vertical slice en dos niveles (banda/celda) y protocolo agéntico escritor/revisor/gate; las bandas son madurez del motor, no estado de la instancia
- **Estado:** Aceptada (enmienda/precisa D-011; complementa D-015, D-009, D-012, D-020)
- **Fecha:** 2026-06-28
- **Contexto:** Tras estudiar el método de Caden (`700_brief → 705_design → 710_plan → 720_build` por arnés + ciclo SDD+TDD con instancias A/B/C), el usuario pidió definir **cómo se construye cada vertical slice** de FODA con los pasos **definir → diseñar → planear → ejecutar → probar → verificar**. Surgieron tres preguntas a cerrar: (1) la **granularidad** (FODA tiene dos ejes: 14 flujos × bandas, mientras Caden tiene un solo eje por arnés); (2) la relación entre "definir el alcance" y el `slice_contract`; (3) si una sola sesión de Claude Code hace todo el ciclo o se descompone en agentes especializados, y a qué plano pertenece todo esto.
- **Decisión:**
  1. **Plano:** todo este ciclo (slice_contract, diseño, plan, build, pruebas) es **construcción del MOTOR** (este repo, `foda-*`). Las **bandas (Tracer Bullet → Stabilization → MVP → Evolution → Final) son hitos de madurez del motor, NO estados de la instancia.** Una instancia (`fda-*`) **no conoce la banda**: solo ejecuta la tubería (Discovery→…→Monitoring) con las capacidades que el motor tenga al momento de generarla. La banda es una foto de la capacidad; la instancia siempre corre el motor vigente. (Precisa D-001/D-015.)
  2. **Dos niveles de granularidad** (elección del usuario):
     - **Nivel banda (vertical slice):** se corre **una vez por banda**. Entregable nuevo = **`slice_contract`**: qué peldaño L de cada uno de los 14 flujos entra, el **orden de la tubería**, qué transversales `TR-1..TR-4` se tocan y el **Done end-to-end** (reporte que C1 valida). Es la **formalización documental de la columna de esa banda en `roadmap.md`** (cierra el sentido de **T-017** para el Tracer Bullet).
     - **Nivel celda (flujo × banda):** se corre **por flujo, en orden de tubería**, acumulando sobre snapshots (D-012): cada flujo pasa por `diseñar → ejecutar → probar → verificar` contra el golden client C1.
  3. **Dos "alcances" distintos** (aclaración terminológica): el **brief** = alcance del *flujo* (escalera completa L0→Ln, estable; el "menú"). El **`slice_contract`** = alcance de la *banda* (qué peldaño de cada flujo entra en esta vuelta; la "orden"). El paso "Definir" se materializa en el `slice_contract`, **armado seleccionando** de los briefs ya aprobados.
  4. **Estructura de carpetas (un carril por paso del ciclo; eje banda) — ENMENDADA 2026-06-28:** `700_brief/` (brief por flujo — el "menú", estable; pre-ciclo) · **`703_definition/<banda>/{slice_contract.md, bdd.md}` (DEFINIR — por banda)** · `705_design/<banda>/<flujo>.md` (diseñar — por celda) · `710_plan/<banda>/<flujo>.md` (planear — por celda) · `720_build/<banda>/<flujo>/{agents,skills,schemas,contract,deliverables,evaluation}` (ejecutar+probar+verificar) · `720_build/_transversal/` (TR-1..TR-4) · `720_build/golden_client/` (C1 + snapshots, D-012/D-014). En el Tracer Bullet, diseño/plan por celda son **ligeros** (E4); el peso está en el `slice_contract`. **Enmienda:** originalmente el `slice_contract` + `bdd` se ubicaron en `710_plan/` (tratados como "planeación"), pero eso conflactaba el paso **Definir** (banda) con el paso **Planear** (celda) y separaba el `slice_contract` de su hermano conceptual el brief. Se creó el carril dedicado **`703_definition/`** para el output del paso Definir. El nombre canónico del archivo es `slice_contract.md` (no `000_slice_contract.md`). Ver L-010.
  5. **Mapeo de los 6 pasos a instancias:** Definir = A (sesión principal) escribe/coordina el `slice_contract` + gate humano. Diseñar/Planear/Ejecutar = B + Workers (contexto fresco). Probar/Verificar = C independiente (E9) + gate humano. **Regla dura:** quien ejecuta ≠ quien verifica (P1, P3); nunca autoaprobación.
  6. **Protocolo agéntico del paso "Definir"** (plantilla replicable a Diseñar/Planear/Ejecutar): la **sesión principal (A)** y el humano discuten el alcance → al acuerdo, A invoca un **subagente escritor** que produce `scope.md` (= slice_contract) + `bdd.md` → A invoca un **subagente revisor** (independiente, fresco) que audita consistencia scope↔bdd (vacíos/ambigüedades/sobrantes) → si OK, A presenta al humano para **aprobación** (P5); si hay problemas, A reinvoca al escritor para subsanar, y si el escritor no puede (falta info del humano), **escala** a A para que pregunte al humano. Si el humano rechaza, A pide motivos y reinvoca al escritor.
  7. **Dos correcciones de mecánica** sobre la propuesta del usuario: (a) **un subagente NO lanza a su "hermano"**: termina y **devuelve el control a la sesión principal**, que es quien encadena el siguiente agente (coherente con el modelo plano D-009; ver L-002). (b) **Tope de iteraciones** en el loop escritor↔revisor (~2, E5): tras N rondas sin converger, **escalar al humano** en vez de iterar indefinidamente.
- **Alternativas consideradas (granularidad):** (a) **Por flujo como Caden** (cada flujo = unidad con su brief→design→plan→build; la banda solo marca el L) — descartada: ignora que el valor de FODA es la rebanada end-to-end (D-015) y no captura el `slice_contract`. (b) **Por slice monolítico** (los 14 flujos a un nivel L como una sola unidad de los 6 pasos, sin sub-ciclo por flujo) — descartada: pierde trazabilidad por flujo y el gate por flujo. (c) **Dos niveles** — elegida.
- **Consecuencias:** Habilita **T-002** (crear el árbol `705_design/`, `710_plan/`, `720_build/` con la rama `tracer-bullet/`) y precisa **T-017** (el `slice_contract` del Tracer Bullet es su entregable). El protocolo agéntico de "Definir" queda como plantilla para los demás pasos (pendiente detallar Diseñar/Planear/Ejecutar/Probar/Verificar con el mismo nivel). Los subagentes de construcción (escritor/revisor) son **herramientas de construcción del motor**, distintas de los agentes runtime `foda-*` que se despliegan a la instancia. Conecta con D-020 (en Tracer Bullet, A+B+ejecución pueden colapsar en una sesión por E4, pero **verificar** se mantiene en contexto fresco).

---

### D-022 — El stack tecnológico de la instancia (lenguaje/ML, motor de datos bronze/silver/gold, forma de la app, patrones) se decide ANTES de cualquier vertical slice
- **Estado:** Propuesta (a resolver antes de iniciar el Tracer Bullet; bloquea T-014 y la primera celda)
- **Fecha:** 2026-06-28
- **Contexto:** Todo el trabajo hasta ahora definió la **arquitectura agéntica** (planos `foda-`/`fda-`, modelo A/B/C, método de construcción por vertical slice `D-021`) y el **contrato de datos** (qué artefacto produce cada flujo y con qué nombre canónico, `D-018`). Pero **nunca se decidió sobre qué tecnología corre la instancia**: lenguaje de implementación, librerías de ML, qué son *físicamente* las capas bronze/silver/gold (¿archivos en disco?, ¿Parquet?, ¿DuckDB/SQLite/Postgres?), la forma de la aplicación (batch CLI con gate humano vs. servicio con API/frontend) y los patrones de diseño base. Lo único *implícito* en los documentos fuente y briefs: Python está sugerido por `best_model.pkl` (pickle); los exportables son `.csv`/`.xlsx`; los medios de acceso `CSV / base de datos / API` se refieren a la **fuente del cliente** (lo que Ingestion lee), **no** a la BD de la solución. Nada de esto está formalizado como decisión.
- **Decisión (de proceso):** El stack tecnológico de la instancia es **transversal** y debe fijarse como ADRs **antes de ejecutar la primera celda del Tracer Bullet** — no descubrirse celda por celda (eso produciría implementaciones divergentes, lo contrario a un motor reutilizable). Se antepone una nueva tarea **T-023** que debe resolver, como mínimo: (1) **lenguaje + librerías de ML**; (2) **motor de datos** de las capas bronze/silver/gold (formato físico + mecanismo de consulta); (3) **forma de la app** (batch CLI con gate humano vs. servicio); (4) **patrones de diseño base** (cómo un agente invoca código determinista y dónde vive ese código en la instancia). El resultado se registra como decisiones `D-023+`. Esta T-023 **precede a T-014** (el generador del golden client ya necesita saber en qué formato vive bronze) y a toda celda del Tracer Bullet.
- **Alternativas consideradas:** (a) **Descubrir el stack al construir la primera celda** (estilo walking-skeleton puro, `D-015`) — descartada: el stack es transversal a los 14 flujos; improvisarlo por celda rompe la reutilización. (b) **Dejarlo implícito** (Python + archivos porque "se sobreentiende") — descartada: el usuario detectó que motor de datos, forma de la app y patrones no son deducibles y deben ser explícitos. (c) **ADRs transversales antes del slice** — elegida.
- **Consecuencias:** Nueva tarea **T-023** se vuelve la **próxima** del proyecto, por delante de T-014 y T-021. Hasta cerrarla, **no se inicia ningún vertical slice**. Probablemente genere varios ADRs (`D-023+`) y pueda conectarse con las filas transversales `TR-*` (`D-020`). Lección `L-011`.

---

### D-023 — Lenguaje de la instancia: Python con pandas/polars, scikit-learn, numpy, SQLAlchemy/psycopg
- **Estado:** Aceptada (cierra T-023 punto 1; deriva de `D-022`)
- **Fecha:** 2026-07-01
- **Contexto:** T-023 requería decidir el lenguaje + librerías antes del primer vertical slice. Python estaba implícito por `best_model.pkl` (pickle de scikit-learn) pero nunca formalizado.
- **Decisión:** La instancia se implementa en **Python**. Stack mínimo: `pandas` o `polars` (datos tabulares), `scikit-learn` + librerías de series de tiempo (torneo de Modelling), `numpy` (Montecarlo de Simulation), `SQLAlchemy` + `psycopg` (acceso a PostgreSQL).
- **Alternativas consideradas:** R — descartado (ecosistema ML más estrecho y el DS opera desde Python). Julia — descartado (madurez de ecosistema y familiaridad del equipo).
- **Consecuencias:** Todo el código determinista de las `skills/` de cada celda (`D-021 §4`) se escribe en Python. El acceso a Postgres va vía SQLAlchemy (ORM/Core) para mantener el hexagonal ligero de `D-026`.

---

### D-024 — Motor de datos de bronze/silver/gold: PostgreSQL
- **Estado:** Aceptada (cierra T-023 punto 2; deriva de `D-022`)
- **Fecha:** 2026-07-01
- **Contexto:** El motor de datos físico de las capas bronze/silver/gold nunca se había decidido. Candidatos evaluados: archivos Parquet + DuckDB (sin servidor, inmutabilidad natural), SQLite (embebido, mínimo), **PostgreSQL** (servidor, SQL completo, multi-tenant real).
- **Decisión:** Las capas **bronze/silver/gold** viven como **tablas en PostgreSQL** dentro del schema del cliente (ver `D-027`). bronze es **inmutable** (solo-inserción / versionado; nunca `UPDATE`/`DELETE` sobre lo ingerido). silver/gold son regenerables desde bronze. PostgreSQL habilita Profiling/Exploration con SQL estándar y soporta el aislamiento multi-tenant por schema.
- **Alternativas consideradas:** Parquet + DuckDB — descartado para esta fase porque el usuario optó por Postgres al confirmarse el requisito de N clientes con un motor relacional único. CSV + SQLite — descartado (escala insuficiente para N clientes). Postgres sigue siendo válido también para volumen por-cliente moderado (planeación de demanda mensual, pocas decenas de SKUs).
- **Consecuencias:** El generador del golden client (T-014) emite bronze directamente a Postgres en el schema del cliente de prueba. Las migraciones de esquema usan Alembic (o similar) aplicadas por-schema. El acceso desde la lógica ML pasa por el puerto de repositorio (`D-026`).

---

### D-025 — Forma de la app: batch multi-cliente operado por 1 DS para N clientes, con gate humano. Sin API web en esta fase
- **Estado:** Aceptada (cierra T-023 punto 3; deriva de `D-022`)
- **Fecha:** 2026-07-01
- **Contexto:** La tesis SaaSw de FODA es pasar de "1 DS ≤4 clientes" a "1 DS → N clientes", automatizando el 85–95% del trabajo. T-023 debía precisar si esto implica un servicio web/API o un batch CLI multi-tenant.
- **Decisión:** La instancia es una **app Python batch multi-cliente**: el **DS selecciona el cliente** (tenant) al inicio de una corrida y ejecuta el pipeline de 14 flujos para ese cliente, con **gate humano** en los puntos de decisión clave (selección del `best_model.pkl`, aprobación de artefactos). **Sin API web ni frontend en esta fase** — la multi-clienteidad se logra por **selección de tenant en CLI**, no por concurrencia. El DS puede cambiar de cliente entre corridas.
- **Alternativas consideradas:** Servicio REST/API — diferido: es la dirección natural del SaaSw final, pero añade complejidad (auth, multi-usuario concurrente, despliegue) antes de validar el pipeline. Aplicación de escritorio — descartado.
- **Consecuencias:** La **capa de transporte** es CLI/orquestador batch (ver `D-026`). La **notificación** de fin de flujo es revisión de artefactos (polling manual); webhook/email se difiere. La concurrencia de operación ≈ 1 (el DS), eliminando la necesidad de caché externa, colas distribuidas, réplicas de lectura o CDN.

---

### D-026 — Patrones de diseño base: monolito modular por capas + hexagonal ligero (puerto/adaptador para acceso a datos)
- **Estado:** Aceptada (cierra T-023 punto 4; deriva de `D-022`)
- **Fecha:** 2026-07-01
- **Contexto:** El cuestionario de diseño de sistemas (`985_inputs/questionnaire_DS.md`) confirmó: equipo pequeño → monolito; MVP → por capas; requisitos estables en el contorno → hexagonal ligero viable; dominio modular → 14 módulos independientes.
- **Decisión:** **Monolito modular por capas + hexagonal ligero**: (1) **Transporte** — CLI/orquestador batch (selección de tenant, disparo de flujos, gate humano). (2) **Dominio** — 14 módulos, uno por flujo, con lógica ML determinista + agente del flujo; cada módulo tiene su celda canónica `agents/skills/schemas/contract/deliverables/evaluation` (`D-021 §4`). (3) **Datos** — repositorio/puerto con `tenant` como parámetro transversal; adaptador PostgreSQL (SQLAlchemy/psycopg) implementa el puerto. La **lógica ML no importa** psycopg ni conoce el schema físico; habla solo con la interfaz del repositorio. El **agente orquesta**; el trabajo pesado y reproducible vive en **código determinista** (`skills/`), invocado por el agente.
- **Alternativas consideradas:** Microservicios — descartados (`D-021` warning; equipo pequeño, sin fricción entre equipos). Hexagonal completo (puertos para todo) — descartado como sobreingeniería para esta fase; "ligero" = solo el borde de datos necesita el puerto para habilitar el cambio a object storage en SaaSw.
- **Consecuencias:** La puerta a **BD-por-cliente** (si un contrato lo exige) o a **object storage** (fase SaaSw) se deja abierta sin trabajo extra: cambiar el adaptador de conexión en el puerto no toca la lógica ML. Ver también `D-027`.

---

### D-027 — Aislamiento multi-tenant en PostgreSQL: esquema por cliente (schema-per-tenant)
- **Estado:** Aceptada (complementa D-024/D-025; cierra el punto 5 de T-023)
- **Fecha:** 2026-07-01
- **Contexto:** Con PostgreSQL como motor (`D-024`) y N clientes en la misma app (`D-025`), se necesita decidir cómo aislar los datos de cada cliente. Tres opciones evaluadas: (a) esquema por cliente, (b) BD por cliente, (c) `tenant_id` en tablas compartidas.
- **Decisión:** **Esquema por cliente (schema-per-tenant):** un solo servidor PostgreSQL; un `schema` por cliente (ej. `cliente_abc`) que contiene sus tablas `bronze_*`, `silver_*`, `gold_*`. La app fija el schema activo al inicio de cada corrida (`SET search_path` o calificando el schema). Elegida por el usuario.
  ```
  postgres://servidor/foda
  ├── cliente_abc (schema) → bronze_* / silver_* / gold_*
  ├── cliente_xyz (schema) → bronze_* / silver_* / gold_*
  └── ...
  ```
- **Alternativas consideradas:** (a) BD por cliente — aislamiento máximo pero N cadenas de conexión y N backups; overhead innecesario para 1 DS con N moderado. Se reserva si un contrato exige separación física. (b) `tenant_id` en tablas compartidas — operación más simple pero riesgo de fuga entre clientes por filtro olvidado; descartado por seguridad de datos.
- **Consecuencias:** Migraciones se aplican por-schema en un loop (Alembic con `search_path`). La carpeta-por-cliente (`fda-*`, `D-001`) guarda config/artefactos y apunta al schema de su cliente. Reconcilia limpio con `D-001`: los **datos** viven en Postgres; el **runtime** vive en la carpeta del cliente. La puerta a **BD-por-cliente** sigue abierta sin tocar la lógica ML (via el puerto de `D-026`).

### D-028 — Hosting del Postgres de construcción (golden client) en Docker local, puerto 55432
- **Estado:** Aceptada (refina `D-024`; no lo altera)
- **Fecha:** 2026-07-01
- **Contexto:** Al arrancar `T-014` se necesitaba un PostgreSQL corriendo para el golden client C1. No había instalación nativa, pero **sí Docker Desktop operativo** (engine 29.5.3, WSL2). Se evaluó instalar Postgres nativo (winget) vs. contenedor.
- **Decisión:** Hospedar el Postgres de **construcción** en un **contenedor Docker local** (`docker-compose.yml` en `720_build/golden_client/`): imagen `postgres:17-alpine`, contenedor `foda_golden_db`, base `foda`, **puerto host `55432`** (el 5432 estaba ocupado por otros contenedores del usuario), credenciales en `.env` **gitignored**, schema `golden_client` creado por script de init. Es infra **desechable y reproducible** (`docker compose down -v` = reset del fixture), que casa con el golden client como fixture reseteable (`D-012`).
- **Alternativas consideradas:** (a) Instalación nativa con winget — permanente, ocupa el 5432, menos alineada con un fixture desechable; descartada al haber Docker listo. (b) SQLite — contradice `D-024`; descartada.
- **Consecuencias:** **No cambia `D-024`** (el motor sigue siendo PostgreSQL 17); es solo la forma de hospedarlo en desarrollo. El mismo `docker-compose.yml` puede alojar más schemas de prueba (schema-per-tenant, `D-027`). Los secretos (`.env`) no viven en el motor (`D-001`). Nota operativa: `psql` no queda en el PATH del host; se accede vía `docker exec` o psycopg (host→`localhost:55432`).

---

### D-029 — Protocolo de construcción por celda (Diseñar/Planear/Ejecutar/Probar/Verificar) dimensionado a E4: carriles separados, peso mínimo por artefacto, independencia creciente (3 contextos frescos)
- **Estado:** Aceptada (cierra **T-021**; extiende `D-021 §6` a los 5 pasos restantes; complementa `D-020`)
- **Fecha:** 2026-07-01
- **Contexto:** `D-021 §6` solo especificó el protocolo agéntico del paso **"Definir"** (nivel banda). Faltaba detallar los 5 pasos del **nivel celda** (flujo × banda): **Diseñar → Planear → Ejecutar → Probar → Verificar**. El usuario pidió el protocolo **proporcional a E4** (Mínima Complejidad) para el Tracer Bullet, y resolvió dos preguntas de forma: (1) los pasos ligeros se mantienen como **carriles separados** (no se fusionan en una sola sesión); (2) **Probar** y **Verificar** corren en **dos sesiones frescas separadas** (no una sola C que haga ambos).
- **Decisión:**
  1. **Invariante que nunca se relaja** (toda banda): **quien ejecuta ≠ quien verifica** (`P1`, `P3`); **gate humano** al cierre de celda (`P5`). Nunca autoaprobación.
  2. **La proporcionalidad (`P6`/`E4`) se expresa como PESO del artefacto, no como fusión de pasos.** Los 6 pasos conservan su carril propio; en Tracer Bullet, **Diseñar y Planear son ligeros** (≤1 página / checklist). Si el diseño de una celda excede una página, es señal de que el L0 está mal recortado → volver a Definir (`L-009`).
  3. **La independencia crece hacia el final:** **Ejecutar** (Instancia B, contexto propio), **Probar** (Instancia C-test, **contexto fresco**), **Verificar** (Instancia C-verify, **contexto fresco e independiente del tester**) → **tres contextos frescos distintos**. Reconcilia con `D-020` (en Tracer Bullet A+B pueden colapsar, pero la garantía no).
  4. **Mapa por paso** (nivel celda, en orden de tubería del `slice_contract`):

     | Paso | Instancia | Contexto | Artefacto / carril | Rigor E4 |
     |------|-----------|----------|--------------------|----------|
     | Diseñar | B | propio | `705_design/<banda>/<flujo>.md` | ≤1 pág: qué hace el agente `foda-*`, qué skill invoca, qué schema produce, qué lee/escribe (bronze/silver/gold) |
     | Planear | B | propio | `710_plan/<banda>/<flujo>.md` | checklist de construcción (crear agente, skill, schema, contract) |
     | Ejecutar | B (+workers `E7`) | propio | `720_build/<banda>/<flujo>/{agents,skills,schemas,contract}` | escribe las definiciones + código determinista (`D-023`/`D-026`) |
     | Probar | **C-test** | **fresco** | `.../deliverables/` + `.../evaluation/` | corre la celda contra C1 (`E9`: 7 SKUs×36m); valida schema, contract, determinismo (semilla 42) |
     | Verificar | **C-verify** + humano | **fresco** | `.../evaluation/` (veredicto) + gate `P5` | audita deliverable vs `slice_contract` (Done) y brief L0; emite `APROBADO`/`REQUIERE SUBSANACIÓN` |

  5. **Mecánica de encadenamiento (`D-021 §7`):** un subagente **termina y devuelve control** a la sesión principal (A), que encadena el siguiente; un subagente no lanza a su hermano (modelo plano `D-009`, `L-002`).
  6. **Loop y tope (`P6`):** si `REQUIERE SUBSANACIÓN`, A reinvoca el bloque de construcción; **tope ~2 rondas**; si no converge, **escala al humano** en vez de iterar.
  7. **Disciplina de snapshots (`D-012`):** cada celda consume el snapshot de la celda anterior y **congela** el suyo al aprobar; ese snapshot es la entrada del siguiente flujo. Demuestra el end-to-end acumulando estado sobre C1, no probando flujos aislados.
  8. **Mapeo al ciclo SDD+TDD (§7):** Diseñar≈SPEC, Planear≈plan, Ejecutar≈GREEN, Probar≈RED+corrida, Verificar≈EVAL. La §7 es la ambición (Ln); este protocolo es su realización proporcional a E4 para la banda Tracer Bullet.
- **Alternativas consideradas:** (a) **Colapsar Diseñar+Planear+Ejecutar en una sola sesión** (propuesta inicial por E4) — descartada por el usuario: se mantienen carriles separados aunque ligeros, para trazabilidad por paso (`P8`). (b) **Una sola sesión fresca C para Probar+Verificar** — descartada por el usuario: dos sesiones frescas separadas dan mayor independencia (`P3`; el tester tampoco es el verificador). (c) Detallar los 5 pasos con el mismo peso que "Definir" — descartada: rompería E4 para un esqueleto.
- **Consecuencias:** Cierra **T-021** y **desbloquea la construcción de la primera celda `010_discovery`** (nivel L0) con este protocolo. Queda como plantilla dimensionable: en bandas superiores (Stabilization→Final) el mismo protocolo sube de peso (diseño/plan dejan de ser ≤1 pág) sin cambiar el invariante ni el mapa de instancias. Sección operativa registrada en `950_guideline/methodology.md §7`. Lección `L-013`.

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
