# Metodología del Harness FODA

Este documento define el estándar y el proceso para construir y operar **FODA** (*Forecast Optimization
Driven Agentic*): el motor (harness) reutilizable que replica el trabajo de los científicos de datos de
Sabbia Solutions & Services para la **planeación de demanda** con machine learning, ejecutándolo de
forma autónoma y controlada, garantizando la calidad y la reducción de la varianza en los resultados.

> **Dos planos (ver `D-001`).** El **MOTOR** (`foda-*`) contiene las definiciones canónicas reutilizables
> de esta metodología. La **INSTANCIA** (`fda-*`) es la solución concreta de un cliente: una carpeta
> externa por empresa donde corre el runtime y se generan los artefactos. El runtime de la instancia
> nunca vuelve al motor; el puente entre planos es el instalador de terminal (`install.sh`).

---

## 1. Fundamentos y Propósito
El objetivo del harness FODA es reducir el espacio de decisiones probabilísticas de los LLMs,
encuadrando su comportamiento mediante contratos, herramientas específicas y evaluación independiente,
para automatizar el 85–95% del trabajo de planeación de demanda y dejar al científico de datos como
revisor/aprobador del 5–15% restante.

### Principios de Ingeniería (P1-P8)
*   **P1: Separación de Roles**: Orquestador, Trabajador y Evaluador deben ser entidades distintas.
*   **P2: Artefactos de Handoff**: La comunicación entre fases se realiza exclusivamente mediante archivos persistentes.
*   **P3: Evaluador Externo Independiente**: Ningún agente evalúa su propio trabajo.
*   **P4: Context Resets**: Se prefiere el reinicio de contexto sobre la compactación para evitar la "ansiedad contextual".
*   **P5: Contratos Explícitos**: Definición de "terminado" antes de iniciar la ejecución.
*   **P6: Escalamiento Proporcional**: Ajuste del esfuerzo (workers, reasoning) según la complejidad.
*   **P7: Herramientas Críticas**: Las herramientas disponibles son tan importantes como el prompt.
*   **P8: Observabilidad**: Trazabilidad total de cada decisión en el filesystem.

### Estándares de Comportamiento (E1-E12)
*   **E1: Persistencia de estado**: El sistema debe poder reanudar el trabajo entre sesiones sin pérdida de contexto.
*   **E2: Context Anxiety**: Protocolo proactivo de reinicio de contexto al alcanzar umbrales de tokens.
*   **E3: Calibración del Evaluador**: Uso de rúbricas y ejemplos few-shot para evitar la lenidad del evaluador.
*   **E4: Mínima Complejidad**: Evolución continua del sistema, evitando sobre-ingeniería inicial.
*   **E5: Ejecución Durable**: Capacidad de reanudar la ejecución desde checkpoints canónicos tras un fallo.
*   **E6: Outputs al Filesystem**: Los agentes escriben resultados directamente al disco, no al orquestador.
*   **E7: Paralelización Explícita**: Ejecución simultánea de tareas independientes para reducir tiempos.
*   **E8: Extended Thinking**: Uso de razonamiento profundo (reasoning) para decisiones críticas y complejas.
*   **E9: Evaluación Temprana**: Validación con muestras pequeñas y representativas en etapas iniciales.
*   **E10: Inicio de Sesión Estructurado**: Ritual obligatorio de lectura de estado y orientación al arrancar.
*   **E11: Búsqueda de Amplio a Estrecho**: Entendimiento del dominio y el problema antes de entrar en detalles técnicos.
*   **E12: Arquitectura Orquestador-Trabajador**: El orquestador planifica y delega; los trabajadores ejecutan.

---

## 2. Arquitectura de Capas
El sistema no es un programa único, sino un "sistema de sistemas" dividido en dos capas para separar el **valor de negocio** de la **ejecución técnica**.

### ¿Por qué dos capas?
1.  **Eliminación de Sesgo**: El ejecutor (Capa 2) no debe ser el mismo que aprueba el alcance (Capa 1).
2.  **Gestión de Contexto**: La Capa 1 mantiene la visión global del proyecto, mientras que la Capa 2 opera con "Contexto Estricto" (E2) para evitar alucinaciones.
3.  **Seguridad**: La Capa 1 actúa como el "GateKeeper" humano-IA (el **científico de datos**), asegurando que ninguna acción técnica ocurra sin alineación estratégica.

### Las dos capas en FODA
*   **Capa 1: Gobernanza** — *"¿Estamos prediciendo lo correcto?"*. Encuadra el problema de negocio del
    cliente y aprueba los checkpoints clave. La opera la **Instancia A (Governor)**, con el científico de
    datos como GateKeeper humano. Métricas Tipo 2 (valor de negocio, salud del sistema).
*   **Capa 2: Ejecución** — *"¿Lo estamos prediciendo bien?"*. Construye y corre el **pipeline de demanda**.
    La operan la **Instancia B (Orchestrator)** y sus **Workers**, con la **Instancia C (Evaluator)** como
    auditor. Métricas Tipo 1 (calidad de artefactos, MAPE, apego a especificación).

> ⚠️ FODA predice **la demanda** de los productos del cliente, **no las ventas**.

### Los 14 flujos = las fases del harness
En FODA, las fases del ciclo de vida **son los 14 flujos del pipeline de demanda**. Cada flujo es una
"fase" en el sentido del §3 (patrón A/B/C) y produce artefactos canónicos (`*.json`/`*.yaml`) que sirven
de handoff al siguiente. La instancia los ejecuta encadenados sobre una arquitectura de datos
**bronze → silver → gold**:

| # | Flujo | Artefactos canónicos | Capa de datos |
|---|-------|----------------------|---------------|
| 1 | **Discovery** | `client_register.yaml`, `business_hypothesis.md`, `contract_data.json` | — |
| 2 | **Onboarding** | `map_client_data.json` | — |
| 3 | **Ingestion** | (carga inalterable) | **bronze** |
| 4 | **Profiling** | índice de salud de datos + pareto | bronze |
| 5 | **Cleaning** | `data_cleaner.yaml` → `data_cleaning.json` | → **silver** |
| 6 | **Derivation** | `data_derivation.json` | → **gold** |
| 7 | **Exploration** | `exploration.json`, `feature_engineering.yaml` | gold |
| 8 | **Featuring** | `feature_engineering.json` | gold |
| 9 | **Modelling** (torneo de campeones) | `best_model.pkl` | gold · **checkpoint humano** |
| 10 | **Inferences** | `inferences.json` (MAPE por período) | gold |
| 11 | **Simulation** (Montecarlo) | escenarios optimista/moderado/pesimista + demanda simulada | gold |
| 12 | **Scenarios** (¿qué pasa si…?) | `scenarios.json` | gold |
| 13 | **Reporting** | `reporting.json` (márgenes, costo de oportunidad, inventario de seguridad) | gold |
| 14 | **Monitoring / Alerting** | `monitoring.json` · `alerting.json` | — |

*   **Scenarios (#12)**: responde preguntas **"¿qué pasa si…?"**. Un agente de IA simula distintos
    escenarios de negocio combinando la información de *Inferences* (#10) y *Simulation* (#11) como insumo.

*   **Capa de datos**: **bronze** (crudo inalterable) → **silver** (limpio) → **gold** (derivado/listo para ML).
*   **Checkpoint humano obligatorio**: la selección del modelo en *Modelling* (#9) la confirma el
    científico de datos antes de continuar a *Inferences* (ver §3 y §8.1).

---

## 3. El Patrón Universal de Fase
En FODA, una **Fase** es un bloque lógico de trabajo que representa un hito del proyecto: cada uno de los
**14 flujos del pipeline de demanda** (§2). Ninguna fase puede considerarse terminada hasta que supere su
gate de aprobación correspondiente.

Toda fase, sin excepción, debe implementar la colaboración de **tres instancias independientes** (sesiones de IA con contexto separado) para garantizar la calidad:

### Las Tres Instancias del Patrón
1.  **Instancia A: Gobernanza (`foda-governor`)**
    *   **Rol**: Director del Proyecto. En la práctica, es la **sesión principal de Claude Code** (nivel 0
        del árbol de subagentes) operada junto al científico de datos.
    *   **Responsabilidad**: Define el contrato de la fase, gestiona las señales de bloqueo y toma la decisión final de "Avanzar o Repetir" (GateKeeper). Es el único que escribe el estado global (`fda-harness-state.json`).
2.  **Instancia B: Orquestación/Planificación (`foda-<flujo>-orchestrator`)**
    *   **Rol**: Capataz Técnico **planificador**. Es un **subagente** spawneado por A; **solo planifica**,
        **no ejecuta ni spawnea** (`tools: Read`; ver modelo plano §3.1 y `D-009`). Es **específico por flujo**
        (`D-010`): su cadena de workers va embebida en su definición.
    *   **Responsabilidad**: Recibe la referencia al contrato y a los insumos, descompone el trabajo en
        micro-tareas y devuelve a A el **`orchestration_plan`** (qué Workers ejecutar, en qué orden y con qué
        inputs/outputs). **A** ejecuta ese plan invocando a los Workers. B no produce artefactos ni escribe al
        filesystem (salvo que el modelo plano delegue en A la persistencia del estado técnico).
    *   **Regla crítica (E12)**: El `orchestration_plan` que B devuelve se persiste en la sección
        `orchestration_plan` de `fda-execution-state.json` (la escribe **A**, único orquestador). Si el contexto
        crece durante la ejecución, A puede releer el plan desde el filesystem sin reconstruirlo. Ningún Worker
        se activa sin que este plan esté guardado.
3.  **Instancia C: Evaluación (`foda-<flujo>-evaluator`)**
    *   **Rol**: Auditor Independiente. Es un **subagente** spawneado por A; **no** lleva la herramienta
        `Agent` (no puede spawnear a nadie), lo que garantiza P3. Es **específico por flujo** (`D-010`): su
        rúbrica (dimensiones, vetos, anclas) va embebida en su definición.
    *   **Responsabilidad**: Actúa con un cerebro fresco (sin contexto de la ejecución). Lee el contrato y los artefactos finales, aplica una rúbrica objetiva y emite un veredicto de aprobación o rechazo con feedback técnico.

### Jerarquía de Control y Llamadas entre Instancias
Las tres instancias no operan como pares; tienen una jerarquía de control estricta que debe respetarse para preservar P1 (Separación de Roles) y P3 (Evaluador Independiente).

```
A (Governor) ── única instancia que spawnea (modelo plano, D-009)
│
├──▶ spawea B (Phase Orchestrator)   ← B PLANIFICA y devuelve el orchestration_plan (no ejecuta)
│
├──▶ ejecuta el plan: spawea Workers (1..N, en paralelo si son independientes)
│         │
│         └──▶ escriben artefactos al filesystem; reportan a A solo la referencia (path)
│
└──▶ spawea C (Phase Evaluator)      ← solo después de que los Workers terminan
          │
          └──▶ lee artefactos del filesystem → emite veredicto
```

**Reglas que no pueden violarse (modelo plano, `D-009`):**

*   **A es la única instancia que spawnea.** B, Workers y C **no se invocan entre sí**: todo pasa por A. Esto hace el motor robusto a la versión de Claude Code (no depende de subagentes anidados).
*   **B planifica, no ejecuta.** B recibe el contrato + insumos y devuelve a A el `orchestration_plan` (qué Workers, en qué orden, con qué inputs/outputs). No spawnea ni escribe artefactos. A persiste el plan en `fda-execution-state.json` antes de ejecutar (E12).
*   **A ejecuta el plan llamando a los Workers.** A invoca cada Worker según el `orchestration_plan` de B (en paralelo los independientes). El secuencial es: B planifica → A ejecuta Workers → C audita. A decide cuándo avanzar de una etapa a la siguiente.
*   **C no llama a nadie.** C solo lee artefactos del filesystem. Si C contactara a A o a Workers para "aclarar" algo, perdería la independencia que garantiza P3. Toda la información que C necesita debe estar en los artefactos y en el Sprint Contract.
*   **Cada "llamada" es un agente con contexto fresco.** En la práctica con Claude Code, spawear una instancia significa lanzar un nuevo agente (`Agent` tool) con contexto limpio. Esto implementa P4 (Context Resets) y garantiza que ninguna instancia herede sesgos de las anteriores.

### 3.1 Implementación con modelo plano de Claude Code (D-009)
El patrón A/B/C se implementa con un **modelo plano**: la **sesión principal (A) es la única que
spawnea**. No se usan subagentes anidados (B no spawnea a los Workers). Esto hace el motor **robusto a
la versión de Claude Code**: no depende de la feature de anidamiento (v2.1.172+) y está validado en el
harness de referencia Caden (ver `L-006`). Reemplaza el diseño anidado original de `D-005`.

*   **Mapa de spawneo** (la conversación principal es nivel 0; todo lo demás cuelga de A, nivel 1):
    ```
    nivel 0 ── foda-governor (A)  = sesión principal de Claude Code (ÚNICA que spawnea)
                 ├──▶ nivel 1 ── foda-<flujo>-orchestrator (B)  → devuelve orchestration_plan a A
                 ├──▶ nivel 1 ── foda-<flujo>-<rol> (Workers)   → A los ejecuta según el plan de B
                 └──▶ nivel 1 ── foda-<flujo>-evaluator (C)     → audita y emite veredicto
    ```
*   **Política de `tools` por instancia** (es lo que hace cumplir P1 y P3 a nivel de herramienta):
    *   **A (Governor)**: es la sesión principal; **única** con capacidad de invocar subagentes (`Agent`).
    *   **B (`foda-<flujo>-orchestrator`)**: `tools: Read` (solo planifica). **No** incluye `Agent`.
    *   **C (`foda-<flujo>-evaluator`)**: `tools: Read, Write`. **No** incluye `Agent` (C no llama a nadie).
    *   **Workers (`foda-<flujo>-<rol>`)**: las herramientas de su dominio + `Write`. **No** incluyen `Agent`.
*   **Sin límite de profundidad relevante**: el árbol es plano (A → {B | Workers | C}, todos a nivel 1),
    así que el límite de 5 niveles de `L-002` deja de ser una restricción de diseño. Si en el futuro se
    necesitara paralelismo más rico, evaluar *agent teams* (contexto propio por worker), nunca reintroducir
    anidamiento sin revisar `D-009`.

### Los 4 Elementos Internos de la Fase
Para que estas instancias operen, deben existir:
1.  **Sprint Contract**: El acuerdo de lo que significa "terminado", propuesto por A y ratificado por B y C.
2.  **Workers**: Agentes especializados activados por B para el trabajo de dominio.
3.  **Rúbrica de Evaluación**: Los criterios de puntuación (0.0–1.0) que usará la Instancia C. Para evitar lenidad sistémica, toda rúbrica debe incluir obligatoriamente tres elementos:
    *   **a) Dimensiones definidas**: Cada dimensión evaluada debe tener nombre, descripción y peso relativo. Las dimensiones estándar son: *Precisión Factual*, *Completitud*, *Calidad de Fuentes/Referencias* y *Eficiencia de Herramientas*. Un harness puede agregar dimensiones específicas de dominio.
    *   **b) Ejemplos few-shot calibrados**: Al menos 2 ejemplos con desglose de puntaje detallado por dimensión — uno de output aceptable (score global ≥ 0.7) y uno de output rechazado (score global < 0.5). Sin estos ejemplos, el evaluador opera sin referencia y tiende a la aprobación indiscriminada.
    *   **c) Anclas de calibración por nivel**: Definición explícita de qué constituye cada extremo de la escala para cada dimensión:
        *   **1.0** — Criterio cumplido sin observaciones.
        *   **0.5** — Criterio cumplido parcialmente; requiere corrección menor.
        *   **0.0** — Criterio ausente o incumplido; causa de rechazo directo.
4.  **Handoff Artifact**: El resultado tangible que C audita y A aprueba.

---

## 4. Estrategia de Persistencia y Trazabilidad
La "fuente de verdad" reside en el filesystem, no en la memoria de los agentes. Esta arquitectura garantiza que el sistema nunca pierda contexto, incluso entre sesiones o ante fallos.

### 4.1 Los Archivos de Estado (Single Writer Rule)
Para evitar condiciones de carrera, cada archivo tiene un único responsable de escritura:

*   **Harness State (`fda-harness-state.json`)**: 
    *   **Responsable**: **Instancia A (Gobernanza)**.
    *   **Propósito**: Fuente de verdad estratégica, fases y aprobaciones.
*   **Execution State (`fda-execution-state.json`)**:
    *   **Responsable**: **Instancia A (Governor)** — en el modelo plano (`D-009`) A es la única que escribe;
        persiste el `orchestration_plan` que B devuelve y el avance de los Workers que A ejecuta.
    *   **Propósito**: Control de micro-tareas, uso de workers y estado técnico (táctico, por flujo).
*   **Progress Log (`project-progress.txt`)**:
    *   **Responsable**: **Orquestador activo** (la instancia que esté ejecutando la tarea en ese momento, ya sea A, B o C).
    *   **Propósito**: Bitácora narrativa de avance.

### 4.2 Regla de Referencias Ligeras (E6)
Cuando un Worker completa su tarea, **reporta al Orquestador (Instancia B) únicamente la referencia** al artefacto producido — el path del archivo o el ID del recurso — nunca el contenido completo.

*   **Por qué**: Pasar contenido completo entre agentes produce el efecto "teléfono descompuesto": cada traspaso degrada la fidelidad de la información, consume tokens innecesariamente y genera cuellos de botella en el orquestador.
*   **Cómo**: B actualiza `fda-execution-state.json` con la referencia (path/ID) y continúa la coordinación. Cualquier instancia que necesite el contenido lo lee directamente del filesystem usando esa referencia.
*   **Aplica a toda la cadena**: Workers → A (solo paths), B → A (solo el `orchestration_plan`), C → A (solo path a `/eval/verdict.json`). Ningún agente embebe contenido de artefactos en sus mensajes de reporte.

### 4.3 Artefactos de Memoria y Métricas (Responsabilidades de Cierre) (Responsabilidades de Cierre)
*   **Métricas (`/eval/metrics_summary.json`)**:
    *   **Responsable**: **Instancia C (Evaluación)**. Se genera al finalizar la auditoría de cada fase.
*   **Base de Conocimiento (`/knowledge/decisions_library.md`, `lessons_learned.md`)**:
    *   **Responsable**: **Instancia A (Gobernanza)**. Al finalizar el proyecto, el Gobernador consolida las lecciones y decisiones validadas para integrarlas en la memoria a largo plazo.


### 4.4 Otros Artefactos de Persistencia
*   **Handoff Artifacts**: Artefactos canónicos (`*.json`/`*.yaml`) que genera un flujo y sirven de entrada
    al siguiente (ej: `contract_data.json`, `data_cleaning.json`, `feature_engineering.json`,
    `best_model.pkl`, `inferences.json`; ver tabla de los 14 flujos en §2). Cada artefacto documenta las
    transformaciones aplicadas y permite **replicar** el proceso sobre otros archivos del cliente.
*   **Capas de datos (bronze/silver/gold)**: La trazabilidad de datos en la instancia sigue una
    arquitectura de capas inmutable hacia atrás: **bronze** (crudo, inalterable — nunca se sobrescribe),
    **silver** (limpio, salida de *Cleaning*) y **gold** (derivado/listo para ML, salida de *Derivation*
    en adelante). Un flujo nunca modifica una capa anterior; produce la siguiente.
*   **Git History**: Registro inmutable de cambios con una convención de commits estricta para trazabilidad técnica.

---

## 5. Fase 0: Definición Estructural (Contrato del Arnés)
Antes de construir un harness, se debe definir su interfaz:

*   **Entradas (Inputs)**: ¿Qué material "en bruto" recibe?
*   **Propósito (Intent)**: ¿Qué problema específico resuelve?
*   **Procesos**: ¿Qué transformaciones ocurren dentro?
*   **Salidas (Outputs)**: ¿Qué artefactos tangibles produce?

### Estrategia de Exploración para la Definición (E11)
Cuando la definición del contrato requiere recopilar o analizar información de dominio — especialmente en los flujos **Discovery** y **Onboarding** (#1–#2), donde el insumo es la intención del cliente y el mapeo de sus datos — se debe aplicar la estrategia de búsqueda **de amplio a estrecho**:

1.  **Exploración amplia**: Comenzar con preguntas o búsquedas cortas y abiertas para mapear el espacio de información disponible. El objetivo es detectar qué fuentes, áreas o ángulos existen, no profundizar en ninguno aún.
2.  **Identificación de densidad**: Determinar qué áreas contienen mayor concentración de información relevante para el problema.
3.  **Profundización selectiva**: Solo entonces dirigir preguntas o búsquedas específicas hacia las áreas de mayor densidad.
4.  **No comprometerse prematuramente**: No fijar el plan, la arquitectura ni el Sprint Contract a una sola fuente o enfoque antes de haber explorado la amplitud del espacio. Un compromiso prematuro ciega al agente ante información más relevante que aparece después.

Este patrón aplica tanto a búsquedas de información externa (documentos, APIs, bases de datos) como al análisis interno de requerimientos con el cliente o stakeholder. La Instancia B es responsable de aplicarlo durante la fase de recopilación de insumos; la Instancia A lo supervisa al revisar el Sprint Contract propuesto.

---

## 6. Fase 1: Diseño Agéntico
Definición de la infraestructura necesaria para ejecutar el arnés. En esta fase se deben cerrar los siguientes puntos antes de construir el primer componente:

*   **Roles de Subagentes**: Especialización de los Workers.
*   **Política de Herramientas**: Qué pueden y qué no pueden usar (P7).
*   **Política de Escalamiento**: Configuración de paralelismo y Reasoning Budget (P6, E8).
*   **Checkpoints Canónicos (E5)**: Definición de puntos de control obligatorios donde el sistema guarda estado. Si el proceso falla, se reanuda desde el último checkpoint, no desde cero.
*   **Política de Fallback de Herramientas (E5)**: Para cada herramienta crítica definida en la Política de Herramientas (P7), el harness debe especificar tres niveles de respuesta ante fallo, en este orden:
    1.  **Reintento**: Volver a intentar la operación hasta 2 veces antes de escalar. Los fallos transitorios (timeout, rate limit) se resuelven en este nivel.
    2.  **Fallback**: Si el reintento falla, activar la herramienta o método alternativo previamente definido para esa función (ej: si la búsqueda web falla, usar la base de conocimiento local).
    3.  **Escalamiento**: Si el fallback también falla, **detener la tarea**, registrar el bloqueo en `project-progress.txt` con el detalle del fallo, y solicitar intervención humana. Nunca improvisar ni continuar con datos parciales o incompletos — un resultado degradado es peor que un bloqueo explícito.
*   **Trigger de Context Reset (E2)**: El Orquestador debe forzar un reinicio de contexto cuando se cumple **cualquiera** de las siguientes condiciones (la que ocurra primero):
    *   **Cuantitativo**: uso de tokens ≥ 70% de la ventana de contexto activa.
    *   **Conductual** (indicador más temprano y confiable): el agente muestra señales de "ansiedad contextual", que se manifiesta como alguno de estos comportamientos — cerrar tareas sin completarlas, omitir pasos del ciclo SDD+TDD, producir respuestas más cortas y superficiales de lo usual, o declarar trabajo como "terminado" sin evidencia de que los criterios de aceptación fueron verificados.
    El criterio conductual es superior al cuantitativo porque emerge antes de alcanzar el umbral de tokens y es una señal directa de degradación de calidad. Ante cualquier duda, priorizar el reset sobre la compactación.

---

## 7. Fase 2: Construcción Iterativa (SDD+TDD)
Este es el motor de ejecución técnica coordinado por la **Instancia B**. Se basa en el principio de que ninguna pieza de trabajo se produce sin una especificación previa y un mecanismo de validación.

### El Ciclo de Vida del Componente
1.  **SPEC (Specifier)**: Define el **Qué**. Transforma el contrato en una especificación técnica o de contenido detallada.
2.  **HUMAN REVIEW**: Punto de control donde el humano aprueba la intención y el alcance de la especificación antes de proceder.
3.  **RED (Tester)**: Define el **Criterio de Éxito**. Escribe las pruebas automáticas o el checklist de aserciones que el resultado debe cumplir.
4.  **GREEN (Executor)**: Define el **Cómo**. Produce el código o contenido mínimo necesario para satisfacer las pruebas/checklist.
5.  **REFACTOR (Optimizer)**: Mejora la estructura, el estilo y la mantenibilidad sin alterar el comportamiento verificado.
6.  **EVAL (Instancia C)**: Auditoría independiente que valida la coherencia entre Spec, Test y Output.

### Adaptación según el tipo de Artefacto
El ciclo SDD+TDD es un modelo mental universal aplicable a cualquier dominio:

| Paso         | Construcción de Código                           | Construcción de Documentos                                         | Construcción de un Flujo FODA (datos/ML)                                            |
| :----------- | :----------------------------------------------- | :----------------------------------------------------------------- | :---------------------------------------------------------------------------------- |
| **SPEC**     | Define interfaces, tipos y lógica de algoritmos. | Define el índice, los temas clave y objetivos de información.      | Define el contrato del flujo: entradas (capa de datos), transformaciones y artefacto de salida (`*.json`/`*.yaml`/`.pkl`). |
| **RED**      | Escribe un Test Unitario/Integración que falla.  | Crea un **Checklist de Aserciones** (ej: "Debe listar 3 riesgos"). | Define las **aserciones de calidad de datos/modelo** (ej: "MAPE ≤ umbral", "0 nulos en clave", "schema silver válido"). |
| **GREEN**    | Escribe código hasta que el test pasa.           | Redacta el contenido hasta cubrir todos los puntos del checklist.  | Ejecuta la transformación hasta producir el artefacto que pasa las aserciones (ej: corre el torneo de modelos). |
| **REFACTOR** | Limpia el código y aplica patrones de diseño.    | Mejora el estilo, la claridad y el uso del Lenguaje Ubicuo.        | Optimiza features/hiperparámetros sin degradar la métrica verificada; consolida el config del flujo. |

### Protocolo de construcción por celda — dimensionado por banda (D-021 §6 / D-029)
El ciclo SDD+TDD anterior es la **ambición (Ln)**. Su realización concreta por **celda** (flujo × banda)
se **dimensiona a la banda** vía Escalamiento Proporcional (`P6`) y Mínima Complejidad (`E4`). En la banda
**Tracer Bullet** el peso ya vive en el `slice_contract` (nivel banda) y en la **verificación**; los pasos
intermedios se dimensionan al mínimo **sin fusionarse**.

**Invariante (toda banda):** quien ejecuta ≠ quien verifica (`P1`, `P3`); gate humano al cierre de celda
(`P5`). La **independencia crece hacia el final**: Ejecutar, Probar y Verificar corren en **tres contextos
frescos distintos** (el tester tampoco es el verificador).

**La proporcionalidad se expresa como PESO del artefacto, no como fusión de pasos.** Los 6 pasos conservan
su carril propio; en Tracer Bullet, Diseñar y Planear son ligeros (≤1 pág / checklist).

| Paso | Instancia | Contexto | Artefacto / carril | Rigor en Tracer Bullet |
| :--- | :--- | :--- | :--- | :--- |
| Definir (banda) | A + humano | — | `703_definition/<banda>/{slice_contract.md, bdd.md}` | el peso de la banda |
| Diseñar | B | propio | `705_design/<banda>/<flujo>.md` | ≤1 pág (agente, skill, schema, I/O de capas) |
| Planear | B | propio | `710_plan/<banda>/<flujo>.md` | checklist de construcción |
| Ejecutar | B (+workers, `E7`) | propio | `720_build/<banda>/<flujo>/{agents,skills,schemas,contract}` | definiciones + código determinista |
| Probar | **C-test** | **fresco** | `.../deliverables/` + `.../evaluation/` | corre la celda contra el golden client (`E9`); valida schema/contract/determinismo |
| Verificar | **C-verify** + humano | **fresco** | `.../evaluation/` (veredicto) + gate | audita vs `slice_contract` y brief L0; `APROBADO`/`REQUIERE SUBSANACIÓN` |

**Mecánica:** un subagente termina y **devuelve control a la sesión principal** (A), que encadena el siguiente
(modelo plano, `D-009`). Loop subsanación con **tope ~2 rondas**; si no converge, **escala al humano**.
**Snapshots (`D-012`):** cada celda consume el snapshot previo y congela el suyo al aprobar; ese snapshot
alimenta el siguiente flujo, demostrando el end-to-end acumulado sobre C1. En bandas superiores el mismo
protocolo sube de peso (diseño/plan dejan de ser ≤1 pág) sin cambiar el invariante ni el mapa de instancias.

### Evaluación Temprana (E9)
No esperar a tener el harness completo para evaluar. La evaluación temprana es la intervención de mayor impacto en el ciclo de vida: los ajustes realizados aquí tienen un efecto de **30%–80% en la calidad final** a un costo mínimo comparado con corregir tarde.

**Cuándo activarla:** Al completar el **primer componente funcional** del ciclo SDD+TDD, antes de continuar con el segundo componente.

**Cómo ejecutarla:**
1.  La **Instancia B** selecciona una muestra de **~20 casos representativos** del dominio cubierto por el componente — no casos triviales ni extremos, sino los más frecuentes y críticos para el negocio.
2.  La **Instancia C** evalúa la muestra contra la rúbrica calibrada y produce un mini-veredicto con score por dimensión.
3.  B registra el resultado en `fda-execution-state.json` bajo la sección `early_eval`.
4.  **Si el score es ≥ 0.7**: continuar al segundo componente sin cambios.
5.  **Si el score es < 0.7**: ajustar el Sprint Contract o la especificación del componente **antes** de seguir. Este ajuste no requiere completar la fase; es un punto de corrección temprana.

**Quién decide:** La Instancia B coordina la ejecución; la Instancia C produce el veredicto; la Instancia A decide si el ajuste al Sprint Contract requiere aprobación humana o puede resolverse internamente.

---

## 8. Gobernanza y Métricas
Control de calidad sistémico basado en indicadores cuantitativos y cualitativos. Toda ejecución de fase debe concluir con la generación de un artefacto de métricas.

### 8.1 Gates de Aprobación
*   **Automáticos**: Criterios técnicos medibles definidos en los contratos (ej: coverage, linting, pasar tests).
*   **Humanos**: Decisiones estratégicas, aprobación de hitos de valor y revisiones de impacto.

### 8.2 Estándar de Persistencia: `metrics_summary.json`
Para asegurar la observabilidad, la **Instancia C (Evaluador)** es responsable de generar un archivo `metrics_summary.json` en la carpeta `/eval` de la fase al finalizar su auditoría. Este archivo debe seguir esta estructura mínima:
*   **Pipeline Data**: Timestamps de completitud y cierre de cambios.
*   **Document/Artifact Status**: Versión final, número de revisiones, estado de aprobación y score detallado por rúbrica.
*   **Timeline Metrics**: Tiempos de ciclo entre hitos clave.
*   **Change Requests (CR)**: Registro de peticiones de cambio gestionadas durante la fase.

### 8.3 Métricas Tipo 1: Desempeño del Agente y Tarea (Micro-nivel)
Miden la eficacia de la ejecución de una tarea específica o el desempeño de un agente trabajador.
*   **Eficiencia**: Latencia de tarea y consumo de tokens vs. complejidad.
*   **Calidad**: Score de rúbrica, tasa de rechazo y apego a especificación.

### 8.4 Métricas Tipo 2: Salud y Eficiencia del Sistema (Macro-nivel)
Miden la salud del harness completo y el progreso hacia los objetivos del proyecto.
*   **Salud del Sistema**: Velocidad de Sprint, estabilidad de construcción y trazabilidad documental.
*   **Eficiencia Estratégica**: Valor de negocio/costo, tiempo total de ciclo de fase y efectividad del Gatekeeper.

---

## 9. Estándares de Ingeniería
*   **Convención de Commits**: `tipo(fase/sprint): descripción`.
*   **Estrategia de Ramas**: Ramas por sprint con merge a `main` tras gate aprobado.
*   **Selección de Modelos**: Asignación del modelo adecuado según la tarea (Opus para specs, Sonnet para ejecución).

---

## 10. Evolución del Harness (E4: Mínima Complejidad)
Los harnesses no son estáticos. Su diseño parte del mínimo viable y evoluciona conforme se validan o invalidan las suposiciones sobre las limitaciones del modelo.

### 10.1 Principio de Construcción Mínima
*   El harness se construye inicialmente con el menor número de componentes que satisfagan los contratos de la fase.
*   Cada componente codifica una suposición explícita sobre una limitación del modelo (ej: "sin este evaluador externo, el agente auto-aprueba su trabajo"). Esa suposición debe documentarse al crear el componente.
*   No se agrega un componente sin antes demostrar, mediante evidencia de una ejecución real, que su ausencia degrada la calidad del output.

### 10.2 Ciclo de Re-evaluación Periódica
Al cierre de cada proyecto, la **Instancia A (Gobernanza)** ejecuta el siguiente ciclo antes de consolidar las lecciones aprendidas:

1.  **Inventario**: Listar todos los componentes activos del harness y la suposición que cada uno cubre.
2.  **Prueba de Remoción**: Remover un componente a la vez (en un entorno de prueba) y medir el impacto en la calidad del output usando la rúbrica de la Instancia C.
3.  **Decisión**:
    *   Si la calidad cae: el componente se mantiene y su suposición se refuerza en `decisions_library.md`.
    *   Si la calidad no cae: el componente se elimina del harness y se registra como lección en `lessons_learned.md` (el modelo ya no requiere ese andamiaje).
4.  **Exploración de Nuevas Capacidades**: Verificar si capacidades nuevas del modelo (razonamiento extendido, herramientas adicionales) justifican agregar componentes que antes no existían.

### 10.3 Responsabilidades y Registro
*   **Responsable**: Instancia A, en coordinación con el análisis de cierre de proyecto (Sección 11.3).
*   **Artefacto de salida**: Una entrada en `decisions_library.md` por cada componente evaluado, con estado `MANTENIDO` o `ELIMINADO` y la evidencia que respalda la decisión.
*   **Frecuencia mínima**: Una re-evaluación por proyecto completado; no es opcional.

---

## 11. Memoria a Largo Plazo (Knowledge Base)
La memoria a largo plazo permite al sistema aprender de éxitos y errores pasados, evitando la repetición de fallos y facilitando la reutilización de soluciones arquitectónicas validadas. Reside en la carpeta `/knowledge`.

### 11.1 Estructura de la Memoria
*   **Decisions Library (`decisions_library.md`)**: Registro de decisiones de arquitectura (DA) tomadas en proyectos anteriores. Cada decisión indica su nivel de reutilización (Alta, Media, Baja), la justificación técnica y el contexto de cuándo NO reutilizarla.
*   **Lessons Learned (`lessons_learned.md`)**: Bitácora de errores operativos, hallazgos de evaluación (major/minor) y bloqueos técnicos. Cada lección incluye una "Regla para escritores futuros", una directriz obligatoria para evitar repetir el fallo.
*   **Índices (`_index.md`, etc.)**: Mapas de navegación para consultar rápidamente el histórico por tipo de proyecto, stack técnico o fecha.

### 11.2 Protocolo de Utilización (Consulta)
Es obligatorio que, antes de iniciar cualquier flujo (especialmente los de preparación de datos y modelado: **Cleaning**, **Derivation**, **Featuring** y **Modelling**), la **Instancia B (Ejecución)** realice los siguientes pasos:
1.  **Consulta de Decisión**: Revisar la biblioteca de decisiones para identificar patrones de arquitectura base (DAs de alta reutilización) aplicables al problema actual.
2.  **Consulta de Lecciones**: Revisar `lessons_learned.md` filtrando por el documento o fase que se está por ejecutar.
3.  **Aplicación de Reglas**: Integrar las "Reglas para escritores futuros" identificadas como restricciones inmutables en el Sprint Contract de la fase.

### 11.3 Protocolo de Actualización (Persistencia)
Al cerrar un proyecto, el Orquestador es responsable de:
1.  **Extracción**: Consolidar las DAs aprobadas y las lecciones aprendidas durante la ejecución (incluyendo hallazgos del Evaluador/Instancia C).
2.  **Indexación**: Actualizar los archivos de índice con los metadatos del proyecto cerrado.
3.  **Integración**: Inyectar el conocimiento nuevo en los archivos de la `/knowledge` base para que esté disponible para el siguiente arnés.

## 12. Flujo del Arnés
El ciclo de vida de un arnés es una coreografía sincronizada entre las tres instancias, asegurando trazabilidad y mejora continua mediante persistencia y memoria.

### 12.1 Inicialización (Instancia A)

*   **Entrada**: Humano envía comando "Iniciemos" o "Continuemos". Instancia A es el agente que recibe este comando directamente en la sesión activa de Claude Code.

*   **Determinación del modo**: A verifica si `fda-harness-state.json` existe en el directorio del proyecto:
    *   **No existe** → modo **Inicio** → ejecutar E10-A.
    *   **Existe y está íntegro** → modo **Continuación** → ejecutar E10-B.
    *   **Existe pero está corrupto** → ejecutar `git restore` o `git checkout` sobre el archivo dañado. Si el fallo persiste, detener el flujo y reportar el error en `project-progress.txt` solicitando intervención humana.

*   **Ritual de arranque**:
    *   *Modo Inicio*: Ejecuta ritual **E10-A** en este orden exacto:
        1. Verificar directorio de trabajo y estado del ambiente (herramientas disponibles, dependencias instaladas).
        2. Crear la jerarquía de carpetas del proyecto.
        3. Inicializar `fda-harness-state.json`, `fda-execution-state.json` y `project-progress.txt` con sus esquemas vacíos.
        4. Ejecutar `git init` y enlazar inmediatamente el repositorio a un remote en GitHub (`git remote add origin <url>`). Sin este enlace, la trazabilidad (P8) queda en riesgo ante fallos locales.
        5. Ejecutar una prueba básica de sanidad del ambiente (ej: verificar que las herramientas críticas responden).
        6. Registrar el arranque en `project-progress.txt` con timestamp y estado inicial.
    *   *Modo Continuación*: Ejecuta ritual **E10-B** en este orden exacto:
        1. Verificar directorio de trabajo y estado del ambiente.
        2. Ejecutar `git log --oneline -10` para orientarse en el historial reciente.
        3. Leer `project-progress.txt` para conocer el estado narrativo de la última sesión.
        4. Cargar `fda-harness-state.json` y revisar el Sprint Contract vigente.
        5. Leer `fda-execution-state.json` para identificar el último checkpoint alcanzado.
        6. Seleccionar la siguiente tarea prioritaria según el backlog registrado en `fda-execution-state.json`.
        7. Ejecutar prueba básica de sanidad del ambiente antes de comenzar a trabajar.

*   **Reporte al humano (obligatorio antes de continuar)**: Al terminar el ritual, A presenta al humano un resumen estructurado con:
    1. **Estado encontrado**: modo detectado (Inicio o Continuación), integridad de archivos, resultado de la prueba de sanidad.
    2. **Sprint Contract propuesto**: en modo Inicio, A redacta el contrato de la fase a ejecutar; en modo Continuación, A muestra el contrato vigente y confirma si sigue siendo válido o requiere ajuste.
    3. **Próxima acción**: qué hará A a continuación una vez aprobado el contrato.
    A no spawea a B hasta recibir aprobación humana explícita del Sprint Contract.

*   **Gate de aprobación humana (P5)**: El humano revisa el Sprint Contract propuesto y responde:
    *   **Aprobado**: A escribe el Sprint Contract en `fda-harness-state.json` y procede a spawear B.
    *   **Ajuste requerido**: A incorpora los cambios, actualiza el contrato y vuelve a presentarlo para aprobación. El ciclo se repite hasta obtener aprobación explícita.
    *   **Cancelación**: A registra la cancelación en `project-progress.txt` y detiene el flujo.

*   **Delegación a B**: Una vez aprobado el Sprint Contract, A lo escribe en `fda-harness-state.json` y **spawea la Instancia B** pasándole únicamente la referencia al archivo. A no inicia la ejecución técnica por sí mismo ni pasa el contenido del contrato de forma inline.

---

### 12.2 Planificación (Instancia B) y Ejecución Técnica (A + Workers)

*   **Planificación (B)**: A spawnea a B pasándole la referencia al Sprint Contract en `fda-harness-state.json`. B lee el contrato y los insumos (`tools: Read`), consulta `knowledge/decisions_library.md` y `knowledge/lessons_learned.md` para ajustar el enfoque, y **devuelve a A el `orchestration_plan`** (qué Workers, en qué orden, con qué inputs/outputs). B no ejecuta ni escribe.
*   **Persistencia del plan (A)**: A escribe el `orchestration_plan` devuelto por B en `fda-execution-state.json` (regla crítica E12). Ningún Worker se activa sin el plan guardado.
*   **Ejecución de Workers (A)**: A spawnea los Workers especializados según el plan. Workers independientes se ejecutan en paralelo (E7). Cada Worker:
    1. Recibe su micro-tarea con objetivo, formato de salida y herramientas disponibles.
    2. Ejecuta el ciclo SDD+TDD correspondiente.
    3. Escribe su artefacto directamente al filesystem.
    4. Reporta a A **únicamente la referencia** al artefacto (path), nunca el contenido completo (E6).
*   **Estado**: A actualiza `fda-execution-state.json` en cada checkpoint de avance, registrando qué Workers completaron y qué artefactos produjeron.
*   **Cierre de la ejecución**: Al finalizar todos los Workers, A marca `fda-execution-state.json` con estado `EXECUTION_COMPLETE` y registra el resumen en `project-progress.txt`, listo para spawnear a C.

---

### 12.3 Auditoría y Gate de Aprobación (Instancia C + Instancia A)

**Paso 1 — Gate intermedio (Instancia A):**
*   A lee `fda-execution-state.json` y verifica que el estado sea `EXECUTION_COMPLETE`.
*   Si algún Worker no ha completado, A investiga el bloqueo antes de continuar.
*   Una vez confirmada la completitud, A **spawea la Instancia C** pasándole las referencias al Sprint Contract y a los artefactos producidos (paths). A no pasa contenido inline.

**Paso 2 — Auditoría independiente (Instancia C):**
*   C lee los artefactos directamente del filesystem usando las referencias recibidas.
*   C evalúa contra la rúbrica calibrada (dimensiones, few-shot, anclas).
*   C escribe sus resultados en dos archivos propios — nunca en `fda-harness-state.json`, que es responsabilidad exclusiva de A:
    *   `/eval/metrics_summary.json` — Métricas Tipo 1 y 2.
    *   `/eval/verdict.json` — Veredicto (`APPROVED` / `REJECTED`) con desglose de hallazgos.
*   C registra el cierre en `project-progress.txt`.

**Paso 3 — Decisión final (Instancia A — GateKeeper):**
*   A lee `/eval/verdict.json`.
*   Toma la decisión **"Avanzar o Repetir"**:
    *   `APPROVED`: A actualiza `fda-harness-state.json` con estado `PHASE_COMPLETE` y notifica al humano que la fase está cerrada.
    *   `REJECTED`: A activa el protocolo de rechazo (ver 12.4).
*   Solo A escribe en `fda-harness-state.json`. C nunca modifica ese archivo.

---

### 12.4 Protocolo de Rechazo y Reintento
Cuando el veredicto de C es `REJECTED`, el flujo entra en estado de **Bloqueo de Fase**:

1.  **Rechazo Técnico (C → filesystem → A → B)**:
    *   **Motivo**: El artefacto no cumple con la rúbrica o los Criterios de Aceptación.
    *   **Flujo correcto**: C escribe el rechazo en `/eval/verdict.json` y `/eval/eval_{artefacto}.json`. A lee el veredicto, actualiza `fda-harness-state.json` a `IN_REWORK` y **spawea B de nuevo** pasándole la referencia al archivo de rechazo. C nunca contacta a B directamente.
    *   **Acción de B**: Lee el informe de rechazo, consulta `lessons_learned.md` para evitar errores previos, y re-ejecuta el ciclo SDD+TDD únicamente para los componentes fallidos.

2.  **Rechazo Estratégico (Humano → A)**:
    *   **Motivo**: El artefacto (o la especificación) no cumple con el objetivo de negocio o requiere un cambio de alcance.
    *   **Acción**: A detiene el flujo, actualiza el `Sprint Contract` y documenta la solicitud de cambio en `fda-harness-state.json` (o abre un nuevo CR). El proyecto no avanza hasta una nueva aprobación humana explícita.
    *   **Estado**: `fda-harness-state.json` se marca como `HOLD`.

3.  **Registro de Aprendizaje**:
    *   Todo rechazo (major/minor) debe ser registrado por la Instancia C en `lessons_learned.md` al finalizar el proyecto, asegurando que el harness "recuerde" por qué falló esta vez.

### 12.4 Protocolo de Gestión de Cambios (CR)
Ante una solicitud de cambio (CR) sobre artefactos ya aprobados, el sistema activa el siguiente protocolo:

1.  **Registro y Notificación**:
    *   El humano o stakeholder envía el cambio.
    *   La **Instancia A (Gobernanza)** registra la solicitud en el `fda-harness-state.json` bajo la sección `change_requests`, asignando un ID (ej: CR_001) y marcándolo como `OPEN`.

2.  **Registro Técnico (Instancia B)**:
    *   La **Instancia B (Ejecución)** crea un nuevo archivo de registro técnico en la carpeta `/changes` con el formato `CR_XXXX_Nombre.md` (ej: `CR_001_CampoVentas.md`).
    *   Este archivo detalla el alcance, los componentes afectados y el análisis de impacto técnico.

3.  **Evaluación de Impacto**:
    *   B evalúa qué fases, artefactos y pruebas existentes se ven afectados y estima el esfuerzo de re-ejecución.

4.  **Aprobación/Rechazo del CR**:
    *   La Instancia A presenta el impacto al humano. Tras la aprobación humana:
        *   El `fda-harness-state.json` se actualiza: el CR cambia a `APPROVED`, se marcan los artefactos afectados como `DEPRECATED` o `PENDING_REWORK`.

5.  **Ejecución del Cambio**:
    *   El sistema reanuda la fase afectada desde el punto de cambio, utilizando el ciclo SDD+TDD para aplicar la actualización.

6.  **Cierre del CR**:
    *   Una vez que la Instancia C evalúa satisfactoriamente los cambios, la Instancia A marca el CR como `CLOSED` en el `fda-harness-state.json` y archiva el registro de cambio y los reportes de evaluación en el histórico.




