# Roadmap — Motor FODA (matriz workflow × iteración)

> Tablero estratégico de construcción del motor FODA. Vista **horizontal** (entre workflows):
> qué peldaño de cada flujo entra en cada iteración. La vista **vertical** (la ambición completa
> de cada flujo y su escalera de capacidades L0→Ln) vive en el **brief** de cada flujo.
> Decisiones que lo enmarcan: `D-015` (enfoque por fases / walking skeleton) y `D-016`
> (plantilla de brief con escalera + esta matriz).

---

## Índice
- [Cómo se lee esta matriz](#cómo-se-lee-esta-matriz)
- [Vocabulario de estado por celda](#vocabulario-de-estado-por-celda)
- [Matriz workflow × iteración](#matriz-workflow--iteración)
- [Notas y puntos abiertos](#notas-y-puntos-abiertos)

---

## Cómo se lee esta matriz
- **Filas** = los 14 workflows de la tubería FODA (ver `CLAUDE.md §4`).
- **Columnas** = iteraciones, nombradas como **bandas estilo Caden** (`D-017`):
  **Tracer Bullet → [Stabilization 1..n] → MVP → [Evolution 1..n] → Final**. Las 3 anclas
  (Tracer Bullet, MVP, Final) existen siempre; Stabilization y Evolution se insertan según haga falta.
  Una **banda = una vertical slice** que cruza los workflows tomando **un peldaño de la escalera de
  capacidades** (L0→Ln) de cada uno.
- **Tracer Bullet** (= walking skeleton, antes "Iteración 1") = lo mínimo (L0) de cada flujo, encadenado
  end-to-end sobre el golden client **C1**, produciendo un reporte que el cliente pueda validar (`D-015`, Fase 1).
- Las bandas siguientes **profundizan por valor** (Modelling, Inferences, Scenarios, Reporting
  primero), aplicando el método `D-011` (brief→diseño→plan→build) por flujo (`D-015`, Fase 2).
- La matriz se **ensambla** a partir de las escaleras de capacidades de cada brief (`D-016`).

## Vocabulario de estado por celda
- `vacío` — aún no planeado para esa iteración.
- `planeado` — alcance definido para esa iteración, sin construir.
- `mínimo` — construido en su versión mínima (happy-path), validado end-to-end.
- `completo` — construido con la profundidad prevista para ese peldaño (con evaluador C cuando aplique).

---

## Matriz workflow × iteración

> **Nomenclatura — RESUELTA (`D-017`, cierra `T-016`):** columnas = **bandas estilo Caden**
> (Tracer Bullet → [Stab 1..n] → MVP → [Evol 1..n] → Final). Flujos numerados **de 5 en 5**
> (`010`…`075`). La fila *Brief* registra el estado del brief del flujo (`vacío`/`planeado`/`aprobado`).
> **Los 14 briefs están redactados y aprobados** (`010`–`075`).
> Stabilization/Evolution se agregan como columnas adicionales cuando se definan.

| ID | Workflow | Brief | Tracer Bullet (skeleton) | MVP | Final |
|----|----------|-------|--------------------------|-----|-------|
| 010 | Discovery | `aprobado` (L0→Ln) | `planeado` (L0) | — | — |
| 015 | Onboarding | `aprobado` (L0→Ln) | `planeado` (L0) | — | — |
| 020 | Ingestion (bronze) | `aprobado` (L0→Ln) | `planeado` (L0) | — | — |
| 025 | Profiling | `aprobado` (L0→Ln) | `planeado` (L0) | — | — |
| 030 | Cleaning (silver) | `aprobado` (L0→Ln) | `planeado` (L0) | — | — |
| 035 | Derivation (gold) | `aprobado` (L0→Ln) | `planeado` (L0) | — | — |
| 040 | Exploration | `aprobado` (L0→Ln) | `planeado` (L0) | — | — |
| 045 | Featuring | `aprobado` (L0→Ln) | `planeado` (L0) | — | — |
| 050 | Modelling | `aprobado` (L0→Ln) | `planeado` (L0) | — | — |
| 055 | Inferences | `aprobado` (L0→Ln) | `planeado` (L0) | — | — |
| 060 | Simulation (Montecarlo) | `aprobado` (L0→Ln) | `planeado` (L0) | — | — |
| 065 | Scenarios (¿qué pasa si…?) | `aprobado` (L0→Ln) | `planeado` (L0) | — | — |
| 070 | Reporting | `aprobado` (L0→Ln) | `planeado` (L0) | — | — |
| 075 | Monitoring (incl. Alerting) | `aprobado` (L0→Ln) | `planeado` (L0) | — | — |

---

## Notas y puntos abiertos
- **T-016 — Nomenclatura de iteraciones:** ✅ resuelta por `D-017` (bandas estilo Caden + flujos de 5 en 5).
- La matriz se irá poblando a medida que se redacten los **briefs de los 14 flujos** (Fase 0, `D-015`)
  y se defina el alcance mínimo del **Tracer Bullet** (`T-017`).
- Este archivo es **memoria de construcción del motor** (vive en `800_persistence/`); el roadmap de
  runtime de un cliente concreto (estilo `roadmap-manifest.json` de Caden) pertenece al plano
  **instancia** (`fda-*`), no aquí (ver `D-001`, `D-004`).
