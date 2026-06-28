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
- **Columnas** = iteraciones. Una **iteración = una vertical slice** que cruza los workflows
  tomando **un peldaño de la escalera de capacidades** (L0→Ln) de cada uno.
- **Iteración 1** = *walking skeleton*: lo mínimo (L0) de cada flujo, encadenado end-to-end sobre
  el golden client **C1**, produciendo un reporte que el cliente pueda validar (`D-015`, Fase 1).
- Las iteraciones siguientes **profundizan por valor** (Modelling, Inferences, Scenarios, Reporting
  primero), aplicando el método `D-011` (brief→diseño→plan→build) por flujo (`D-015`, Fase 2).
- La matriz se **ensambla** a partir de las escaleras de capacidades de cada brief (`D-016`).

## Vocabulario de estado por celda
- `vacío` — aún no planeado para esa iteración.
- `planeado` — alcance definido para esa iteración, sin construir.
- `mínimo` — construido en su versión mínima (happy-path), validado end-to-end.
- `completo` — construido con la profundidad prevista para ese peldaño (con evaluador C cuando aplique).

---

## Matriz workflow × iteración

> **Nomenclatura de iteraciones — PENDIENTE (`T-016`):** falta decidir entre **bandas estilo Caden**
> (Tracer Bullet → Stabilization → MVP → Evolution → Final) o **numeración simple** (Iteración 1..n).
> Mientras se decide, se usan columnas numéricas. La fila *Brief* registra si el brief del flujo existe.

| # | Workflow | Brief | Iter 1 (skeleton) | Iter 2 | Iter 3 | … |
|---|----------|-------|-------------------|--------|--------|---|
| 1 | Discovery | `vacío` | `vacío` | — | — | |
| 2 | Onboarding | `vacío` | `vacío` | — | — | |
| 3 | Ingestion (bronze) | `vacío` | `vacío` | — | — | |
| 4 | Profiling | `vacío` | `vacío` | — | — | |
| 5 | Cleaning (silver) | `vacío` | `vacío` | — | — | |
| 6 | Derivation (gold) | `vacío` | `vacío` | — | — | |
| 7 | Exploration | `vacío` | `vacío` | — | — | |
| 8 | Featuring | `vacío` | `vacío` | — | — | |
| 9 | Modelling | `vacío` | `vacío` | — | — | |
| 10 | Inferences | `vacío` | `vacío` | — | — | |
| 11 | Simulation (Montecarlo) | `vacío` | `vacío` | — | — | |
| 12 | Scenarios (¿qué pasa si…?) | `vacío` | `vacío` | — | — | |
| 13 | Reporting | `vacío` | `vacío` | — | — | |
| 14 | Monitoring · Alerting | `vacío` | `vacío` | — | — | |

---

## Notas y puntos abiertos
- **T-016 — Nomenclatura de iteraciones:** bandas Caden vs. numeración simple. Bloquea el encabezado
  definitivo de las columnas.
- La matriz se irá poblando a medida que se redacten los **briefs de los 14 flujos** (Fase 0, `D-015`)
  y se defina el alcance mínimo de la **Iteración 1** (`T-017`).
- Este archivo es **memoria de construcción del motor** (vive en `800_persistence/`); el roadmap de
  runtime de un cliente concreto (estilo `roadmap-manifest.json` de Caden) pertenece al plano
  **instancia** (`fda-*`), no aquí (ver `D-001`, `D-004`).
