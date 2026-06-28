# Brief — Arnés 020 Architecture (Reglas Técnicas Globales / Gobernanza de Arquitectura)

> **Tipo:** Brief de enmarque (alto nivel, previo al diseño agéntico). NO es la definición agéntica fina.
> **Proyecto:** CADEN (Continuous Agentic Development Engine) — plano de **construcción** del motor.
> **Componente:** Arnés 2 de 6 — `020_architecture` (se ejecuta una sola vez al inicio, tras Discovery; reaparece solo como **validación de impacto** en Modo Ajuste).
> **Fuente de verdad:** `900_inputs/statement_vertical_slices.md` (§"The Architecture Harness" y §"Paso a Paso: The Architecture Harness").
> **Insumos de referencia (3 bloques):** `900_inputs/architecture/{stack_tec.md, architecture_style.md, design_system.md}`.
> **Método de construcción:** `905_methodology/methodology.md` + `905_methodology/principles.md`.
> **Estado:** APROBADO · **Fecha:** 2026-06-21 · **Aprobado por:** usuario (dueño del proyecto CADEN) · **Decisión que enmarca:** D-027

---

## 0. Aclaración de planos (L-001) — leer primero

Este brief describe un **componente del motor CADEN que estamos fabricando** (plano de
*construcción*). No describe la arquitectura de un producto concreto: describe la **maquinaria
genérica y reutilizable** que, cuando se *opera* sobre una carpeta de cliente arbitraria, monta el
**laboratorio técnico** (estructura, dependencias, reglas de gobernanza) sobre el que los arneses
aguas abajo programarán.

- **Insumo del componente al operar:** el **`roadmap-manifest.json` + los BDD por slice** que produjo
  y firmó el Arnés 010 (Discovery), más los **tres bloques de referencia del motor** (stack, estilo,
  design system) y las **elecciones/confirmaciones del arquitecto humano** en el gate.
- **Estado de runtime** que produce al operar (scaffold de carpetas, archivos de configuración, reglas
  del "policía", `.clinerules`/instrucciones de agente, tokens del design system, commit base) pertenece
  al **plano de operación** sobre el cliente, **no** a la memoria de construcción `800_persistence/`.

> **Naturaleza de los 3 bloques (D-027):** son la **base por defecto y opinionada** que el motor trae,
> **no** una imposición rígida ni un menú libre. Al ejecutarse, el 020 **verifica aplicabilidad**,
> **sugiere adiciones/complementos** para las necesidades particulares del proyecto y **firma con el
> humano**. El **stack/estilo/identidad efectivos = base aplicable + adiciones aprobadas**.

## 1. Objetivo

Traducir el **plan de negocio rebanado** (el `roadmap-manifest.json` firmado en Discovery) y la
**configuración técnica de referencia** (stack + estilo arquitectónico + design system) en un
**laboratorio de software listo para programar**: un repositorio andamiado según el patrón de diseño
elegido, con las dependencias base instaladas, un **"policía invisible"** (linter arquitectónico) que
impide violar las capas, y un **manual de instrucciones** para los agentes que trabajarán en las fases
siguientes.

El Arnés 020 **no escribe código de negocio, ni specs, ni tareas, ni tests**: produce las **reglas de
gobernanza técnica globales** y la **estructura vacía** del proyecto, firmadas por el humano, listas
para que el Arnés 3 (Contract & Mold) procese la primera slice.

En una frase: *transformar el stack/estilo/identidad de referencia (adaptados al proyecto y firmados)
en un scaffold gobernado — carpetas + dependencias + policía + instrucciones de agente + tokens de
diseño — con un commit base que marca la cancha.*

## 2. Alcance — qué hace

**Modo Inicio (gobernanza global, una sola vez al arranque del proyecto cliente, tras aprobar Discovery):**

- **Lectura de definición y del plan:** lee el `roadmap-manifest.json` + BDD del Arnés 010 y los **tres
  bloques de referencia** (stack, estilo, design system).
- **Adaptación al proyecto (D-027):** verifica **qué partes del stack/estilo/identidad aplican** a las
  necesidades reales del proyecto, **propone adiciones/complementos** justificados contra necesidades
  concretas y descarta lo que no aporta valor. El resultado es la **configuración efectiva**.
- **Gate del humano-arquitecto (P5):** presenta la configuración efectiva (stack aplicable + adiciones +
  estilo + identidad/marca) y **cierra las decisiones abiertas** (notablemente **autenticación, D-A**, y
  cualquier escape firmado del estilo, p. ej. D-G/D-I). El humano firma.
- **Creación del scaffold (The Scaffold):** genera el **árbol de carpetas exacto** que exige el estilo
  elegido (backend Clean/Hexagonal en 4 capas `domain`/`application`/`infrastructure`/`interface`;
  frontend modular por features con Next.js App Router).
- **Inicialización del proyecto y dependencias core:** configura los archivos base (gestor `uv`,
  `pyproject`, `package.json`, `tsconfig`, `docker-compose`, etc.) e instala las librerías del stack
  efectivo, **dejándolas limpias de código de negocio**.
- **Configuración del "policía invisible":** instala y configura el análisis estático que materializa la
  **regla de dependencia** (import-linter/deptry en Python · dependency-cruiser en TS), con reglas
  rígidas (p. ej. `domain` no importa de `infrastructure`). Las reglas provienen del bloque B (§2.2).
- **Línea base de seguridad (gobernanza global):** establece los **defaults seguros y las reglas
  verificables** que el policía y el manual de agente hacen cumplir en todo el repo, para prevenir clases
  enteras de vulnerabilidad por construcción (detalle en §8). No es seguridad por funcionalidad (eso es
  aguas abajo): es la línea base transversal del proyecto.
- **Design system base:** instala la capa de **tokens** (primitivas OKLCH `:root`/`.dark`, mapeo
  Tailwind v4 `@theme`, shadcn/ui) según el bloque C, aplicando la **marca del cliente** si la aportó
  (`900_documents/brand.md`) o el **default sobrio** si no, con **accesibilidad WCAG AA** como piso.
- **Manual de instrucciones para la IA (`.clinerules`/instrucciones de agente):** redacta las directrices
  de diseño obligatorias que los agentes programadores de los arneses 3–6 deben respetar.
- **Commit base y cierre de fase (luz verde):** commitea la estructura limpia + reglas activas, persiste
  el **estado técnico global** y emite el reporte de cierre. **El arnés se apaga** y no vuelve a
  ejecutarse salvo el rol de validación del Modo Ajuste.

**Modo Ajuste (Validación de Impacto Arquitectónico, reapertura puntual):**

- Cuando Discovery (Modo Ajuste) muta el `roadmap-manifest.json` con una feature nueva, el 020 **lee el
  roadmap mutado** y valida si la feature **viola alguna regla global de gobernanza** o **requiere un
  molde base nuevo** (p. ej. una tabla, una extensión de DB, una librería externa o un adaptador nuevo).
- Si todo está en orden, **da luz verde** sin re-andamiar; si requiere un molde nuevo, lo provisiona y
  re-firma. No reconstruye el scaffold existente.

## 3. Alcance — qué NO hace (límites)

- **No** descubre ni rebanada el negocio, ni produce BDD, ni clasifica slices → eso es el **Arnés 010
  (Discovery)**; el 020 **consume** su salida firmada.
- **No** genera tipos, esquemas concretos de dominio, contratos de API ni mocks de cada slice → eso es el
  **Arnés 030 (Contract & Mold)**. El 020 fija las **reglas y moldes base**, no los contratos por slice.
- **No** descompone tareas atómicas RED/GREEN/REFACTOR ni asigna feature branch → **Arnés 040 (Tactical
  Planning)**.
- **No** escribe código de negocio ni ejecuta TDD → **Arnés 050 (Execution)**. El 020 deja el laboratorio
  **vacío de lógica de negocio**.
- **No** valida en Sandbox, no corre regresión/E2E ni hace merge a `main` → **Arnés 060 (Validation)**.
- **No** elige el dominio de negocio ni acopla el scaffold a un producto concreto: parte de una **base
  adaptable** que se ajusta y firma por proyecto (D-027).
- **No** diseña la **maquinaria agéntica fina** de este propio arnés (instancias A/B/C, workers,
  checkpoints, rúbrica, contratos) → eso es el **diseño del harness**, paso siguiente a este brief.

## 4. Insumos disponibles

| ID | Insumo | Origen |
|----|--------|--------|
| I-1 | Definición de CADEN y de los 6 arneses (fuente de verdad) | `900_inputs/statement_vertical_slices.md` |
| I-2 | Paso a paso del Architecture Harness + Validación de Impacto del Modo Ajuste | `900_inputs/statement_vertical_slices.md` (§"Paso a Paso: The Architecture Harness" y §"Inyección de Features → Paso 4") |
| I-3 | **Bloque A — Stack tecnológico de referencia** (base adaptable; D-A auth abierta) | `900_inputs/architecture/stack_tec.md` |
| I-4 | **Bloque B — Estilo arquitectónico de referencia** (Clean/Hexagonal 4 capas + contratos del policía; D-F..D-I FIRMES locales) | `900_inputs/architecture/architecture_style.md` |
| I-5 | **Bloque C — Identidad visual / Design System de referencia** (tokens, L0–L4, a11y AA; D-J..D-M FIRMES locales) | `900_inputs/architecture/design_system.md` |
| I-6 | Metodología y principios de construcción del harness (P1–P8, E1–E12, patrón A/B/C) | `905_methodology/methodology.md`, `905_methodology/principles.md` |
| I-7 | Memoria de construcción del proyecto (estado, decisiones, lecciones) | `800_persistence/` |
| I-8 | Patrón de los arneses ya construidos (010): comandos del motor, modelo mixto de persistencia, gates, durabilidad | `720_build/` (010_discovery + transversales) |

> **Insumo en tiempo de operación (no de construcción):** el **`roadmap-manifest.json` + BDD por slice**
> firmados por Discovery (en la carpeta del proyecto cliente), el insumo de marca opcional
> `900_documents/brand.md`, y las **elecciones del arquitecto humano** en el gate. Llegan cuando el motor
> se *opera*, no ahora.

## 5. Artefactos esperados (salida del componente al operar)

El Arnés 020 entrega el laboratorio gobernado que el Arnés 030 (Contract & Mold) y el bucle necesitan:

| Artefacto | Propósito |
|-----------|-----------|
| **Scaffold del repositorio** | Árbol de carpetas exacto del estilo elegido (backend 4 capas; frontend por features), vacío de lógica de negocio. |
| **Configuración base del proyecto** | Gestores y manifiestos (`uv`/`pyproject`, `package.json`, `tsconfig`, `docker-compose`, etc.) con las dependencias del **stack efectivo** instaladas. |
| **Reglas del "policía invisible"** | Configuración del análisis estático (import-linter/deptry · dependency-cruiser) que **bloquea** imports que violen las capas; verificable ejecutándola. |
| **Manual de instrucciones de agente** | `.clinerules`/`ai-instructions` con las directrices de diseño obligatorias para los agentes de los arneses 3–6. |
| **Capa de design system** | Tokens (primitivas OKLCH + mapeo Tailwind/shadcn), claro+oscuro, marca aplicada o default, baseline WCAG AA. |
| **Estado técnico global + commit base** | Reglas de gobernanza y configuración efectiva persistidas; commit "laboratorio listo" con luz verde de cierre. |
| **Registro de firma del gate** | Evidencia de la validación y aprobación humana de la configuración efectiva (incluye el cierre de D-A). |

> Los *paths* exactos, el esquema preciso del estado técnico global y la mecánica de cada artefacto se
> fijan en el **diseño del harness** (paso siguiente).

## 6. Criterios de éxito (Done)

1. El humano **aprueba explícitamente** la **configuración efectiva** del proyecto (stack aplicable +
   adiciones + estilo + identidad), con las **decisiones abiertas cerradas** (D-A auth y cualquier escape
   firmado). Gate humano obligatorio (P5).
2. El **scaffold** generado **corresponde exactamente** al estilo arquitectónico elegido (4 capas backend
   + frontend por features), y está **vacío de lógica de negocio**.
3. El **"policía invisible" funciona**: una violación de la regla de dependencia (p. ej. `domain`
   importando de `infrastructure`) es **detectada y bloqueada** por el análisis estático (verificación
   demostrable, no declarativa).
4. Las **dependencias base del stack efectivo** quedan instaladas y el entorno **arranca/compila** limpio
   (sanidad del ambiente).
5. Existe un **manual de instrucciones de agente** con las directrices de diseño obligatorias para las
   fases siguientes.
6. La **capa de design system** queda instalada con tokens (claro+oscuro), marca o default, y cumple el
   piso de **accesibilidad WCAG AA**.
7. Hay un **commit base** con la estructura limpia y las reglas activas, y el **estado técnico global**
   queda persistido y trazable (P8).
8. La **línea base de seguridad (§8)** queda establecida y es **verificable**: al menos la regla anti-SQLi
   se demuestra (una consulta de SQL crudo/concatenado fuera del punto autorizado es bloqueada por el
   policía), y los defaults de secretos, validación de entrada, AuthN/Z, XSS/headers/CORS e higiene de
   dependencias están activos (no solo declarados).
9. **Modo Ajuste:** una feature inyectada por Discovery queda **validada** contra la gobernanza global; si
   exige un molde base nuevo, se provisiona y re-firma, sin re-andamiar lo existente.

## 7. Riesgos / advertencias

- **Confusión de planos (L-001):** el 020 monta *el laboratorio del producto del cliente*, no la
  maquinaria que lo fabrica. El scaffold y las reglas son estado de operación, no memoria de construcción.
- **Base adaptable mal aplicada (D-027):** imponer el stack/estilo a ciegas (sin verificar aplicabilidad
  ni firmar adiciones) reintroduce la varianza que el harness busca reducir; arrastrar piezas inútiles
  infla el proyecto. La adaptación + firma humana es la mitigación.
- **Decisiones abiertas sin cerrar:** **D-A (autenticación)** condiciona scaffold, contratos y pruebas;
  dejarla difusa contamina los arneses aguas abajo. Debe cerrarse en este gate (ver §8).
- **Policía declarativo pero inerte:** configurar el linter arquitectónico sin **verificar que realmente
  bloquea** una violación deja una falsa sensación de gobernanza. El Done exige verificación demostrable
  (criterio 3), eco de L-008 (un molde no usado es código muerto) y L-009 (dar la herramienta y
  comprobar, no asumir).
- **Versiones del stack — piso estable (D-C, bloque A §0.1):** la base shippea la **última estable madura**
  (Python 3.13, Next 15.x, TS 5.9; Tailwind 4 y PG18 se mantienen por load-bearing), con **0 CVEs** en el
  lockfile; el **filo es opt-in firmado** en el gate. El 020 verifica versiones contra documentación vigente
  y aplica fallback de compatibilidad, sin fijar a ciegas.
- **Andamiar de más:** generar carpetas/dependencias para features que el proyecto no tiene viola E4
  (mínima complejidad). El scaffold se ajusta al `roadmap-manifest.json` real, no a la base completa.
- **Seguridad declarativa pero inerte:** una regla de seguridad configurada que no se *verifica* (igual
  que el policía, criterio 3/8) da falsa confianza. El default seguro debe estar **activo y demostrable**,
  no solo escrito en el `.clinerules`.

## 8. Línea base de seguridad (gobernanza global del 020)

El 020 establece una **línea base de seguridad transversal** como parte de las reglas globales: defaults
seguros + reglas que el **"policía invisible"** y el **manual de agente** hacen cumplir en todo el repo,
de modo que los arneses 3–6 no puedan introducir clases enteras de vulnerabilidad. Es **adaptable por
proyecto (D-027)** y **mínima (E4)**: se ajusta en el gate, no se infla. Buena parte ya está implícita en
los bloques A/B; aquí se vuelve **regla verificable**.

| # | Vector | Default / regla del 020 | Origen |
|---|--------|--------------------------|--------|
| 1 | **SQL Injection** | ORM/consultas parametrizadas obligatorias; SQL crudo (`text()`, concatenación/f-strings) prohibido o restringido a un adaptador firmado. Regla del policía. | Stack §3, Estilo §5.1 |
| 2 | **Validación de entrada** | Invariante: todo input cruza **Pydantic** (backend) / **Zod** (frontend) en la frontera antes de llegar al dominio. | Stack §4/§6 |
| 3 | **Gestión de secretos** | `pydantic-settings` (12-factor), **cero secretos en el código**; **escaneo de secretos** en pre-commit/CI. | Stack §4, §9.5 |
| 4 | **AuthN/Z** | **JWT** (access+refresh) + passlib/bcrypt + autorización por **rol/scope** (D-A); autorización aplicada en la capa de aplicación, no en la UI. | Stack §5 (D-A) |
| 5 | **XSS / headers / CORS** | Auto-escape de React (regla contra `dangerouslySetInnerHTML`); **CORS restrictivo** y **security headers** por default en el backend. | Estilo §3, Stack §6 |
| 6 | **Higiene de dependencias** | `pip-audit` / `npm audit` (o deptry) en CI; lockfiles; sin dependencias con CVE conocidas en el árbol. | Stack §9.2/§9.5 |

> Estas reglas se **materializan** en el policía (import-linter/dependency-cruiser + lint), el `.clinerules`
> y la configuración base (CORS/headers/CI). El **detalle accionable** (qué regla concreta del linter, qué
> headers, qué job de CI) se fija en el **diseño** del 020 y se documenta junto a los contratos del policía
> del **bloque B** (`architecture_style.md §2.2`). La seguridad **por slice** (authz por escenario,
> pruebas de abuso) es de los arneses 030 (contratos) y 060 (validación), no del 020.

## 9. Decisión cerrada en este brief — D-A (Autenticación / Autorización)

**Resuelta (FIRME, local del bloque A):** el default del motor es **autenticación emitida por el
backend con JWT** — access + refresh, hashing con **passlib/bcrypt**, autorización por **rol/scope** vía
dependencias de FastAPI. Es un default **opinionado, sin dependencia externa y con control total**, y
encaja con el resto del stack Python.

Como el 020 es **base adaptable (D-027)**, este default **se verifica y puede sustituirse por proyecto en
el gate**: si un proyecto requiere OAuth/social se añade **Auth.js (NextAuth)** en el frontend (el backend
valida el token), o se adopta un **proveedor gestionado** (Clerk/Auth0/Supabase Auth/Keycloak) cuando se
prioriza time-to-market; cualquiera de estas sustituciones es una **adición aprobada** en el gate, no un
cambio al default. Se actualiza en consecuencia `stack_tec.md §5`.

## 10. Siguiente paso

Tras **aprobar este brief** (y cerrar D-A): **diseñar el Arnés 020** (instancias A/B/C, workers, política
de herramientas y escalamiento, checkpoints canónicos, política de fallback, trigger de context reset,
rúbrica de evaluación y Sprint Contract), reutilizando los patrones ya validados del 010 (modelo mixto de
persistencia D-012, gates D-017, protocolo de rechazo D-021, durabilidad D-024/E5). El **plan de
implementación** viene *después* del diseño (orden del método: **brief → diseño → plan → construir**). El
diseño se materializará en `705_design/020_architecture.md`.
