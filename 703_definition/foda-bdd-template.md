# Plantilla — BDD de banda FODA (companion del slice contract)

> **Cómo usar esta plantilla.** Copia este archivo a `703_definition/<banda>/bdd.md` (junto al
> `slice_contract.md` de la misma banda) y rellena cada sección. Borra estas instrucciones y las
> notas `> _(guía: …)_` antes de cerrar. Lo produce el subagente **escritor** en el paso "Definir"
> (`D-021`), emparejado con el slice contract; el **revisor** independiente verifica que **scope
> (slice contract) ↔ bdd estén alineados**: nada de más, nada de menos.
>
> **Qué es el `bdd.md` en FODA.** Es el **comportamiento esperado de la banda, de punta a punta sobre
> C1**, escrito en Gherkin (Given-When-Then). Mientras el **slice contract** dice *qué peldaño entra y
> qué se entrega* (el alcance), el **bdd** dice *cómo se comporta observablemente* la tubería con ese
> alcance (el contrato de comportamiento). Es la pareja `scope.md` + `bdd.md` del protocolo de "Definir".
>
> **Granularidad.** El escenario central es **end-to-end** (de los datos crudos de C1 al reporte final).
> Añade escenarios en los **hitos/handoffs críticos** de la tubería (capas inmutables, baseline vencido,
> gate humano…) solo donde el comportamiento lo amerite. **No** repliques aquí la maquinaria agéntica
> fina de cada flujo (eso es el **diseño** de cada celda, `705_design/`).
>
> **Dos planos (`D-001`, `D-021`).** Documento de **construcción del motor**. El comportamiento se
> describe sobre el cliente golden **C1**; la instancia real (`fda-*`) reproducirá ese comportamiento
> con otros datos, pero el contrato observable es el mismo.

---

## Frontmatter del bdd (rellenar)

> **Tipo:** BDD de banda (companion del slice contract — paso "Definir" de `D-021`).
> **Proyecto:** FODA — plano de **construcción** del motor.
> **Banda:** `<Tracer Bullet | Stabilization N | MVP | Evolution N | Final>` (`D-017`).
> **Companion de:** `703_definition/<banda>/slice_contract.md`.
> **Cliente golden:** `C1` (`D-012`/`D-014`).
> **Decisiones que lo enmarcan:** `<D-020, D-021, …>` · **Estado:** `BORRADOR | APROBADO` · **Fecha:** `YYYY-MM-DD`.

---

## 1. Comportamiento end-to-end (una frase)

> _(guía: 1 frase. Qué hace observablemente la tubería en esta banda, de datos crudos a reporte.
> Para el Tracer Bullet: «Dada la data cruda de C1, la tubería L0 produce un reporte mínimo de demanda
> revisable por el científico de datos».)_

## 2. Escenario central — recorrido completo sobre C1

> _(guía: **obligatorio**. UN escenario Gherkin que recorra la tubería de punta a punta. El `Given` es
> el estado inicial de C1 (data cruda); los `When` encadenan los flujos seleccionados en el slice
> contract §2; el `Then` es el reporte final observable. Mantén el nivel de comportamiento, no de
> implementación.)_

```gherkin
Feature: <capacidad observable de la banda — p. ej. pronóstico de demanda mínimo end-to-end>

  Scenario: La tubería <banda> produce un reporte de demanda para C1
    Given la data cruda de C1 está disponible para ingestión
      And el grain es <producto × geografía> con <nº de series>
    When la tubería ejecuta <Discovery → … → Reporting → Monitoring> en su peldaño de esta banda
    Then existe el reporte final <reporting.json> revisable por el científico de datos
      And <criterio observable clave de la banda>
```

## 3. Escenarios por hito / handoff crítico

> _(guía: añade escenarios SOLO en los puntos donde el comportamiento debe garantizarse explícitamente.
> Ejemplos típicos en FODA — usa los que apliquen a esta banda y omite el resto:)_

```gherkin
  Scenario: La capa bronze es inmutable
    Given la ingestión escribió la capa bronze de C1
    When un flujo posterior necesita transformar los datos
    Then bronze permanece intacta y la transformación se escribe en silver/gold

  Scenario: El modelo seleccionado vence al baseline ingenuo
    Given Modelling entrenó el modelo ingenuo y los candidatos
    When se evalúa el torneo
    Then ningún modelo peor que el ingenuo pasa el primer filtro

  Scenario: Gate humano en la selección de modelo
    Given Modelling propone un best_model
    When se alcanza el punto de decisión
    Then el científico de datos debe aprobarlo explícitamente antes de Inferences
```

> _(guía: cada escenario aquí debe corresponder a un invariante no deferible de `D-020` o a una
> capacidad declarada en el slice contract. No inventes comportamiento fuera del alcance de la banda.)_

## 4. Escenarios de borde / fallo (mínimos)

> _(guía: en el Tracer Bullet, mantén esto al mínimo (E4); profundiza en bandas posteriores. Incluye
> solo los fallos que la banda debe manejar observablemente; lo demás se difiere.)_

```gherkin
  Scenario: <dato faltante o fuera de rango en una serie de C1>
    Given <...>
    When <...>
    Then <comportamiento esperado — p. ej. se registra y NO se contamina aguas abajo>
```

## 5. Restricciones no funcionales (ligadas a esta banda)

> _(guía: obligatorio. Solo restricciones **atadas a esta banda**, no genéricas. Incluir siempre
> trazabilidad (P8) y la persistencia mínima (E1); añadir MAPE/calidad donde aplique.)_

| Tipo | Restricción | Criterio verificable |
|------|-------------|----------------------|
| `trazabilidad (P8)` | Cada transformación queda registrada en su artefacto | `<los *.json de cada flujo existen y documentan la transformación>` |
| `capas de datos` | bronze/silver/gold inmutables y en orden | `<bronze no se reescribe; gold deriva de silver>` |
| `calidad` | `<p. ej. MAPE por período presente en inferences.json>` | `<…>` |
| `gate humano` | `<decisión clave aprobada por el científico de datos>` | `<registro de aprobación>` |

## 6. Trazabilidad scope ↔ bdd (checklist del revisor)

> _(guía: tabla de control que usa el **revisor independiente** para verificar la alineación. Una fila
> por cada flujo seleccionado en el slice contract §2; marca qué escenario/`Then` de este bdd prueba su
> comportamiento. Si un flujo del scope no tiene comportamiento aquí → **falta algo**; si hay
> comportamiento sin flujo en el scope → **sobra algo**.)_

| Flujo (slice contract §2) | Peldaño | Cubierto por (escenario/`Then`) |
|---------------------------|---------|----------------------------------|
| `010 Discovery` | `<L0>` | `<§2 When … / §3 Scenario …>` |
| `… (las 14 filas seleccionadas)` | `<…>` | `<…>` |

## 7. Notas / decisiones abiertas

> _(guía: supuestos, ambigüedades pendientes, o comportamientos marcados como UNRESOLVED que el humano
> debe aclarar antes de aprobar.)_

- `<…>`
