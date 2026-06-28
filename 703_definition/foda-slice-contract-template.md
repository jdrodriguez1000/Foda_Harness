# Plantilla — Slice Contract FODA (contrato de banda)

> **Cómo usar esta plantilla.** Copia este archivo a `703_definition/<banda>/slice_contract.md`
> (p. ej. `703_definition/tracer-bullet/slice_contract.md`) y rellena cada sección. Borra estas
> instrucciones y las notas `> _(guía: …)_` antes de cerrar. La **sesión principal (rol Governor / A)**
> orquesta su redacción; el contenido lo produce el subagente **escritor**, lo audita un **revisor**
> independiente y lo **aprueba el humano** (gate P5) — protocolo de "Definir" de `D-021`.
>
> **Qué es un slice contract en FODA (`D-021`).** Es la **vista horizontal congelada de UNA banda**:
> de toda la ambición de cada flujo (su escalera L0→Ln, que vive en el **brief**), selecciona **qué
> peldaño entra en esta banda**, en qué **orden** se construye la tubería, qué **andamiaje transversal**
> (`TR-*`) se toca y cuál es el **Done end-to-end** que el cliente golden (C1) valida. Es la
> **formalización documental de la columna de la banda en `800_persistence/roadmap.md`**.
>
> **Brief vs. slice contract (no confundir).** El **brief** = alcance del *flujo* (el "menú": escalera
> completa, estable). El **slice contract** = alcance de la *banda* (la "orden": un peldaño de cada
> flujo para esta vuelta). El slice contract **se arma seleccionando** de los 14 briefs aprobados; no
> reescribe la escalera.
>
> **Recuerda los dos planos (`D-001`, `D-021`).** Este documento es **construcción del MOTOR** y vive
> en este repo. Las **bandas son hitos de madurez del motor, NO estados de la instancia**: una
> instancia (`fda-*`) no conoce la banda; solo ejecuta la tubería con las capacidades que el motor
> tenga al generarla.

---

## Frontmatter del slice contract (rellenar)

> **Tipo:** Slice contract (definición de banda — nivel banda del método `D-021`). NO es la definición
> agéntica fina de un flujo (eso es el **diseño** de cada celda, `705_design/`).
> **Proyecto:** FODA (Forecast Optimization Driven Agentic) — plano de **construcción** del motor.
> **Banda:** `<Tracer Bullet | Stabilization N | MVP | Evolution N | Final>` (`D-017`).
> **Cliente golden de prueba:** `C1` (`D-012`/`D-014`) _(guía: el fixture sobre el que corre end-to-end esta banda)_.
> **Fuente de selección:** los 14 briefs aprobados (escaleras L0→Ln) + `700_brief/000_general_process.md` + `800_persistence/roadmap.md`.
> **Método de construcción:** `D-021` + `950_guideline/methodology.md` + `950_guideline/principles.md`.
> **Decisiones que lo enmarcan:** `<D-015, D-020, D-021, …>` · **Estado:** `BORRADOR | APROBADO` · **Fecha:** `YYYY-MM-DD` · **Aprobado por:** `<usuario>`.

---

## 0. Aclaración de planos — leer primero

> _(guía: 1 párrafo. Confirmar que lo que sigue es construcción del motor. Identificar:)_

- **Qué produce el motor al operar esta banda:** `<el reporte/artefactos que la instancia generará con
  las capacidades de esta banda; p. ej. en Tracer Bullet un reporting.json mínimo>`.
- **Lo que NO viaja a la instancia:** este slice contract, los diseños/planes/snapshots — son del plano
  construcción. Solo se despliegan las **definiciones canónicas** (`foda-*`) que el build produce.

## 1. Objetivo de la banda

> _(guía: 1–2 párrafos + 1 frase-resumen. Qué demuestra esta banda **de punta a punta** sobre C1.
> Para el Tracer Bullet: el walking skeleton que recorre los 14 flujos en su L0 y produce un reporte
> validable. Empezar por el verbo. Cerrar con: «En una frase: …».)_

## 2. Selección de peldaños por flujo — el corazón del contrato

> _(guía: **la tabla central**. Una fila por cada uno de los 14 flujos. Por cada flujo elige el
> **peldaño L** de su escalera (del brief) que entra en esta banda, resume qué hace a ese nivel y
> nombra el/los artefacto(s) canónicos que entrega — usar nombres de `000_general_process.md`. La
> columna *Estado* usa el vocabulario de `roadmap.md` (`planeado`/`mínimo`/`completo`). Si un flujo NO
> entra en esta banda, márcalo `—` y justifícalo en §4.)_

| # | Flujo | Peldaño | Qué hace a ese nivel (resumen) | Artefacto(s) que entrega | Estado |
|----|-------|---------|--------------------------------|--------------------------|--------|
| 010 | Discovery | `<L0>` | `<…>` | `<problem_statement.md, …>` | `<planeado>` |
| 015 | Onboarding | `<L0>` | `<…>` | `<map_client_data.json>` | `<planeado>` |
| 020 | Ingestion (bronze) | `<L0>` | `<…>` | `<bronze, ingestion_report.json>` | `<planeado>` |
| 025 | Profiling | `<L0>` | `<…>` | `<data_health.json>` | `<planeado>` |
| 030 | Cleaning (silver) | `<L0>` | `<…>` | `<silver, data_cleaning.json>` | `<planeado>` |
| 035 | Derivation (gold) | `<L0>` | `<…>` | `<gold, data_derivation.json>` | `<planeado>` |
| 040 | Exploration | `<L0>` | `<…>` | `<exploration.json>` | `<planeado>` |
| 045 | Featuring | `<L0>` | `<…>` | `<feature_engineering.json>` | `<planeado>` |
| 050 | Modelling | `<L0>` | `<…>` | `<best_model.pkl, modelling.json>` | `<planeado>` |
| 055 | Inferences | `<L0>` | `<…>` | `<inferences.json>` | `<planeado>` |
| 060 | Simulation | `<L0>` | `<…>` | `<simulation.json>` | `<planeado>` |
| 065 | Scenarios | `<L0>` | `<…>` | `<scenarios.json>` | `<planeado>` |
| 070 | Reporting | `<L0>` | `<…>` | `<reporting.json>` | `<planeado>` |
| 075 | Monitoring | `<L0>` | `<…>` | `<monitoring.json, alerting.json>` | `<planeado>` |

## 3. Andamiaje transversal en esta banda (`TR-1..TR-4`, `D-020`)

> _(guía: qué nivel del andamiaje transversal entra en esta banda. Respetar los **invariantes no
> deferibles** de `D-020` (handoff en filesystem P2, trazabilidad P8, capas bronze/silver/gold
> inmutables, gate humano de Modelling, persistencia mínima + git). Lo demás se difiere a bandas
> posteriores con mínima complejidad (E4).)_

| TR | Transversal | Peldaño | Qué andamiaje mínimo entra en esta banda |
|----|-------------|---------|------------------------------------------|
| TR-1 | Estado & persistencia runtime (`fda-*`) | `<L0>` | `<…>` |
| TR-2 | Patrón de instancias A/B/C | `<L0>` | `<p. ej. en Tracer Bullet: A+B colapsados; verificar en contexto fresco>` |
| TR-3 | Evaluador + rúbrica | `<L0>` | `<…>` |
| TR-4 | Ejecución durable / checkpoints / context resets | `<L0>` | `<…>` |

## 4. Alcance de la banda — qué entra / qué NO entra

> _(guía: dos listas. Hacer explícito el recorte respecto a la ambición Ln. "Qué NO entra" justifica
> los `—` de la §2 y lo que se difiere a la banda siguiente. Evita el compromiso prematuro: esta banda
> NO intenta hacer todo.)_

- **Entra:** `<…>`.
- **NO entra (se difiere a `<banda siguiente>`):** `<…>` → eso será L1+ del flujo `<X>`.

## 5. Insumos de prueba — golden client y snapshots (`D-012`/`D-014`)

> _(guía: qué fixture y snapshots usa esta banda para correr/probar end-to-end sin re-ejecutar toda la
> cadena. Declarar el grain producto×geografía y la cardinalidad de series de C1.)_

- **Fixture:** `C1` — grain `<producto × geografía>`, `<nº de series>` (`D-014`).
- **Snapshots disponibles:** `<bronze/silver/gold y artefactos cacheados que evitan re-correr aguas arriba>` (`D-012`).

## 6. BDD end-to-end (companion `bdd.md`)

> _(guía: el slice contract se acompaña de un `bdd.md` que describe el **comportamiento esperado de la
> banda** en Gherkin (Given-When-Then) de punta a punta sobre C1. Aquí solo se referencia y se resume;
> el detalle va en `703_definition/<banda>/bdd.md`. El revisor verifica que **scope (este doc) ↔ bdd estén
> alineados**: nada de más, nada de menos.)_

- **Companion:** `703_definition/<banda>/bdd.md`.
- **Resumen del comportamiento end-to-end:** `<1–3 escenarios clave que esta banda debe satisfacer>`.

## 7. Criterio Done end-to-end de la banda

> _(guía: lista numerada y verificable — lo que un evaluador (C) auditaría. Debe incluir el recorrido
> completo sobre C1, los artefactos de §2 producidos, el **gate humano** donde aplique (científico de
> datos aprueba la selección de modelo en Modelling, `CLAUDE.md §5`) y el reporte final validable.)_

1. La tubería corre **end-to-end sobre C1** en el orden de §2 y produce todos los artefactos marcados.
2. El **reporte final** (`<reporting.json / artefacto>`) existe y es **revisable por el científico de datos**.
3. **Gate humano** (si aplica): el científico de datos **aprueba** `<la decisión clave de esta banda>`.
4. Los **invariantes no deferibles** de `D-020` se respetan (capas inmutables, trazabilidad, persistencia + git).
5. `<criterios propios de la banda>`.

## 8. Riesgos / advertencias

> _(guía: viñetas. Confusión de planos; acoplamiento a un dominio concreto; envenenar aguas abajo sin
> validación (E9); sobre-ingeniería temprana (E4); slicing que deja una celda sin contrato claro.)_

- **Confusión de planos:** `<…>`.
- **Eslabón débil end-to-end:** un flujo en L0 mal definido rompe toda la cadena; mitigación `<…>`.
- …

## 9. Gate de aprobación del contrato (P5)

> _(guía: este contrato no habilita la construcción hasta la aprobación humana explícita. El nombre del
> aprobador se toma de `git config user.name + user.email`; nunca del contexto del agente.)_

- **Propuesto por A:** `<iso8601>`
- **Revisado por (revisor independiente):** `<referencia al reporte de revisión + iso8601>`
- **Aprobado por:** `<Nombre <correo> de git config; "humano" si git sin configurar>`
- **Fecha de aprobación:** `<iso8601>`

## 10. Siguiente paso

> _(guía: fijo. Tras aprobar el slice contract → diseñar las celdas. Orden del método `D-021`.)_

Tras **aprobar este slice contract**: pasar al nivel **celda** — para cada flujo seleccionado en §2, en
el **orden de la tubería**, ejecutar `diseñar → ejecutar → probar → verificar` contra C1, acumulando
sobre snapshots (`D-012`). El **diseño** de cada celda se materializa en
`705_design/<banda>/<NN>_<flujo>.md` y su **plan** en `710_plan/<banda>/<NN>_<flujo>.md`.
