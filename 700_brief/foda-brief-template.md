# Plantilla — Brief de flujo FODA

> **Cómo usar esta plantilla.** Copia este archivo a `700_brief/<NN>_<flujo>.md` (p. ej.
> `700_brief/010_discovery.md`) y rellena cada sección. Borra estas instrucciones y las notas
> `> _(guía: …)_` antes de cerrar. Mantén el tono de **enmarque** (alto nivel): el brief describe
> *qué hace y hasta dónde llega* un flujo del motor, **no** su maquinaria agéntica fina (esa se
> define en el **diseño**, paso siguiente del método `D-011`).
>
> **Qué es un brief en FODA (`D-016`).** Es la **vista vertical** de un flujo: su ambición completa
> ordenada por madurez en la **Escalera de capacidades** (§9, L0→Ln). La **vista horizontal**
> (qué peldaño entra en cada iteración) vive en `800_persistence/roadmap.md`, que se **ensambla** a
> partir de las escaleras de todos los briefs. No mezcles el slicing por iteración dentro del brief:
> aquí va el *futuro del flujo*; el *cuándo* va en el roadmap.
>
> **Recuerda los dos planos (`D-001`).** Este brief describe un **componente del MOTOR** (`foda-*`)
> que estamos fabricando. Cuando ese componente se **opera** sobre la carpeta de un cliente, produce
> artefactos de **runtime de la instancia** (`fda-*`) que **nunca** vuelven a este repo ni a
> `800_persistence/`. Distingue siempre *insumo/salida de construcción* vs. *insumo/salida al operar*.

---

## Frontmatter del brief (rellenar)

> **Tipo:** Brief de enmarque (alto nivel, previo al diseño agéntico). NO es la definición agéntica fina.
> **Proyecto:** FODA (Forecast Optimization Driven Agentic) — plano de **construcción** del motor.
> **Flujo:** `<NN>` de 14 — `<NN>_<flujo>` (_(guía: posición en la tubería de `CLAUDE.md §4`; cuándo se ejecuta)_).
> **Posición en la tubería:** consume `<flujo anterior>` → entrega a `<flujo siguiente>`.
> **Capa de datos que toca:** `<bronze | silver | gold | —>` (_(guía: según la arquitectura bronze→silver→gold)_).
> **Fuente de verdad:** `990_documents/expected_workflow.md` (§`<flujo>`) + `990_documents/expected_solution.md`.
> **Método de construcción:** `950_guideline/methodology.md` + `950_guideline/principles.md`.
> **Decisiones que lo enmarcan:** `<D-XXX, …>` · **Estado:** `BORRADOR | APROBADO` · **Fecha:** `YYYY-MM-DD` · **Aprobado por:** `<usuario>`.

---

## 0. Aclaración de planos — leer primero

> _(guía: 1 párrafo. Recordar que este brief describe la **maquinaria genérica y reutilizable** del
> motor, no la solución de un cliente concreto. Identificar explícitamente:)_

- **Insumo del flujo al operar:** `<qué artefacto/capa consume de la instancia del cliente>` (cambia
  por cliente; el diseño no debe acoplarse a un dominio de negocio concreto).
- **Salida de runtime que produce al operar:** `<artefactos fda-*, capa de datos>` — pertenece al
  **plano instancia**, **no** a la memoria de construcción del motor.
- **Grain del cliente (`D-014`):** `<cómo afecta a este flujo la jerarquía producto × geografía y la
  cardinalidad de series; o "no aplica directamente">`.

## 1. Objetivo

> _(guía: 1–2 párrafos + 1 frase-resumen. Qué transforma este flujo y para qué. Empezar por el verbo.
> Cerrar con: «En una frase: transformar `<insumo>` en `<salida>` …».)_

## 2. Alcance — qué hace

> _(guía: viñetas con las responsabilidades concretas del flujo al operar. Si el flujo tiene modos —
> p. ej. inicio vs. ajuste/re-ejecución— subdivídelo. Nombrar los artefactos canónicos que produce
> según `CLAUDE.md §4`.)_

- **`<Sub-paso>`:** `<descripción>`.
- …

## 3. Alcance — qué NO hace (límites)

> _(guía: viñetas. Delimitar contra los flujos vecinos para evitar solapamiento — «esto es del flujo
> X aguas arriba/abajo». Incluir siempre la frontera con el diseño agéntico:)_

- **No** `<responsabilidad>` → eso es el **flujo `<vecino>`**.
- …
- **No** diseña la **maquinaria agéntica fina** de este flujo (instancias A/B/C, workers, checkpoints,
  rúbrica del evaluador, contratos) → eso es el **diseño del flujo**, paso siguiente a este brief.

## 4. Insumos disponibles

> _(guía: tabla de insumos de **construcción** — lo que existe hoy para diseñar el flujo. Separar al
> final los insumos **al operar**, que llegan en runtime del cliente.)_

| ID | Insumo | Origen |
|----|--------|--------|
| I-1 | Definición del flujo en la tubería FODA | `990_documents/expected_workflow.md` (§`<flujo>`) |
| I-2 | Metodología y principios de construcción (P*, E*, NC*, patrón A/B/C) | `950_guideline/methodology.md`, `950_guideline/principles.md` |
| I-3 | Memoria de construcción (estado, decisiones, lecciones) | `800_persistence/` |
| I-4 | `<Patrón de flujos ya construidos, si aplica>` | `<carpeta de build>` |

> **Insumo en tiempo de operación (no de construcción):** `<artefacto/capa del cliente + handoff del
> flujo anterior>`. Llega cuando el motor se *opera*, no ahora.

## 5. Artefactos esperados (salida del flujo al operar)

> _(guía: tabla. Los artefactos canónicos `*.json`/`*.yaml`/capas de datos que el flujo entrega para
> que el flujo siguiente arranque. Cada artefacto deja **trazabilidad** de sus transformaciones.)_

| Artefacto | Propósito |
|-----------|-----------|
| **`<artefacto.json>`** | `<para qué sirve y quién lo consume aguas abajo>` |

> Los *paths* exactos, el esquema preciso de cada artefacto y la mecánica se fijan en el **diseño del
> flujo** (paso siguiente).

## 6. Criterios de éxito (Done)

> _(guía: lista numerada y verificable. Incluir el **gate humano** donde aplique (el científico de
> datos aprueba; ver `CLAUDE.md §5`), la calidad mínima de los artefactos y la trazabilidad. Pensar el
> Done como lo que un evaluador (C) auditaría en la Fase 2.)_

1. `<criterio verificable>`.
2. **Gate humano** (si aplica): el científico de datos **aprueba explícitamente** `<la decisión clave>`.
3. …

## 7. Riesgos / advertencias

> _(guía: viñetas. Confusión de planos; acoplamiento a un dominio concreto; envenenar aguas abajo sin
> validación (E9); sobre-ingeniería temprana (E4). Añadir los riesgos propios del dominio del flujo —
> p. ej. fuga de datos futuros, MAPE engañoso, fixture stale.)_

- **Confusión de planos:** `<…>`.
- **Envenenar aguas abajo:** `<un error de este flujo contamina los flujos N+1..14; mitigación>`.
- …

## 8. `<Sección específica del flujo — opcional>`

> _(guía: opcional. Úsala cuando el flujo tenga una dimensión transversal que merezca detalle propio
> — p. ej. en Discovery/Onboarding el **grain multinivel** (`D-014`); en Modelling el **torneo de
> campeones** y el gate de selección; en Inferences/Reporting el **MAPE por período/nivel**. Si no
> aplica, elimina esta sección.)_

## 9. Escalera de capacidades (L0 → Ln) — vista vertical del flujo

> _(guía: **sección distintiva de FODA (`D-016`)**. Ordena la *ambición completa* del flujo por
> madurez. **L0 = lo mínimo** happy-path que entra en el walking skeleton (banda **Tracer Bullet**, `D-015`/`D-017`),
> deliberadamente simplificando lo caro. Cada peldaño siguiente agrega capacidad real. Esta tabla es
> la que se **ensambla** en `roadmap.md`: cada columna-iteración del roadmap toma **un peldaño** de
> esta escalera. Define al menos L0 y L1; añade L2…Ln según la riqueza del flujo.)_

| Nivel | Capacidad | Qué incluye | Qué difiere de la realidad |
|-------|-----------|-------------|----------------------------|
| **L0** (mínimo / skeleton) | `<lo mínimo demostrable>` | `<happy-path, C1, simplificado>` | `<qué se simplifica/omite a propósito>` |
| **L1** | `<siguiente capacidad de valor>` | `<…>` | `<…>` |
| **L2** | `<…>` | `<…>` | `<…>` |
| **Ln** (ambición completa) | `<el flujo "como un científico de datos senior">` | `<…>` | `<nada: es el objetivo final>` |

> **Nota de ensamblaje:** al cerrar este brief, refleja el estado del flujo en
> `800_persistence/roadmap.md` (columna *Brief* → `planeado`; y el peldaño previsto por iteración).

## 10. Siguiente paso

> _(guía: fijo. Tras aprobar el brief → diseñar el flujo. Mantener el orden del método `D-011`.)_

Tras **aprobar este brief**: **diseñar el flujo `<NN>_<flujo>`** (instancias A/B/C según el modelo
plano `D-009`, workers, política de herramientas, checkpoints canónicos, durabilidad, rúbrica del
evaluador y contrato), reutilizando los patrones transversales ya validados del motor. El **plan de
implementación** viene *después* del diseño (orden del método: **brief → diseño → plan → construir**,
`D-011`). El diseño se materializará en `705_design/<NN>_<flujo>.md`.
