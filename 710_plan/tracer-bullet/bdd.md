# BDD — Tracer Bullet (companion del slice contract)

> **Tipo:** BDD de banda (companion del slice contract — paso "Definir" de `D-021`).
> **Proyecto:** FODA — plano de **construcción** del motor.
> **Banda:** `Tracer Bullet` (walking skeleton, `D-017`).
> **Companion de:** `710_plan/tracer-bullet/slice_contract.md`.
> **Cliente golden:** `C1` (`D-012`/`D-014`).
> **Decisiones que lo enmarcan:** `D-015`, `D-020`, `D-021` · **Estado:** `APROBADO` · **Fecha:** `2026-06-28`.

---

## 1. Comportamiento end-to-end (una frase)

Dada la data cruda de C1, la tubería L0 recorre los 14 flujos (010→075) y produce un **reporte mínimo de
demanda** (`reporting.json`) revisable por el científico de datos, más un cierre de ciclo
(`monitoring.json`/`alerting.json`), respetando la inmutabilidad de capas y el gate humano de Modelling.

## 2. Escenario central — recorrido completo sobre C1

```gherkin
Feature: Pronóstico de demanda mínimo end-to-end (walking skeleton)

  Scenario: La tubería Tracer Bullet produce un reporte de demanda para C1
    Given la data cruda de C1 está disponible para ingestión
      And el grain es producto × geografía (1 sede × ~5–10 SKUs, mensual, ~24–36 meses → ~5–10 series)
      And los últimos K períodos de C1 están reservados como hold-out de demanda real
    When la tubería ejecuta Discovery → Onboarding → Ingestion → Profiling → Cleaning → Derivation
      And ejecuta Exploration → Featuring → Modelling → Inferences → Simulation → Scenarios
      And ejecuta Reporting → Monitoring en su peldaño L0
    Then existe el reporte final reporting.json revisable por el científico de datos
      And reporting.json contiene el margen bruto esperado por serie y período
      And monitoring.json reporta la desviación de lo simulado vs. el hold-out reservado
      And cada flujo dejó su artefacto canónico (000_general_process.md) como traza
```

## 3. Escenarios por hito / handoff crítico

```gherkin
  Scenario: La capa bronze es inmutable
    Given Ingestion escribió la capa bronze de C1
    When Cleaning y Derivation necesitan transformar los datos
    Then bronze permanece intacta
      And Cleaning escribe en silver y Derivation escribe en gold

  Scenario: Las capas derivan en orden bronze → silver → gold
    Given existe la capa bronze de C1
    When la tubería avanza
    Then silver deriva de bronze
      And gold deriva de silver
      And ninguna capa posterior reescribe una anterior

  Scenario: Gate humano en la selección de modelo
    Given Modelling entrenó el modelo ingenuo y un modelo simple y propone un best_model
    When se alcanza el punto de decisión de Modelling
    Then el científico de datos debe aprobarlo explícitamente antes de Inferences
      And best_model.pkl queda serializado solo tras esa aprobación

  Scenario: Inferences entrega MAPE por período hacia Simulation
    Given best_model.pkl fue aprobado
    When Inferences genera el pronóstico a horizonte sobre gold
    Then inferences.json incluye la demanda predicha y el MAPE por período
      And Simulation consume ese MAPE para sus bandas optimista/moderada/pesimista

  Scenario: Scenarios recalcula un delta what-if mínimo vs. la base
    Given existe la demanda base de Inferences/Simulation para una serie de C1
      And scenarios_config.yaml stub declara un escenario con un delta (ej. precio -5%)
    When Scenarios recalcula ese escenario
    Then scenarios.json compara la base vs. el escenario para esa serie

  Scenario: El ciclo se cierra con una alerta básica por umbral
    Given Monitoring comparó lo simulado contra el hold-out de C1
    When la desviación supera el umbral fijo configurado
    Then alerting.json registra la alerta básica
      And no se emite señal de re-ejecución a 050/055/060 en esta banda
```

## 4. Escenarios de borde / fallo (mínimos)

```gherkin
  Scenario: Una serie de C1 con datos faltantes no contamina aguas abajo
    Given una serie de C1 tiene períodos faltantes en bronze
    When Cleaning aplica las reglas de data_cleaner.yaml
    Then el tratamiento queda registrado en data_cleaning.json
      And el dato faltante NO se propaga sin marca a silver/gold (E9)
```

## 5. Restricciones no funcionales (ligadas a esta banda)

| Tipo | Restricción | Criterio verificable |
|------|-------------|----------------------|
| `trazabilidad (P8)` | Cada transformación queda registrada en su artefacto | Existen los `*.json` de los 14 flujos y documentan su transformación |
| `capas de datos` | bronze/silver/gold inmutables y en orden | bronze no se reescribe; silver deriva de bronze; gold deriva de silver |
| `calidad` | MAPE por período presente en el contrato hacia Simulation | `inferences.json` incluye MAPE por período |
| `gate humano` | Selección de modelo aprobada por el científico de datos | Registro de aprobación del `best_model.pkl` antes de Inferences |
| `persistencia (E1/TR-1)` | Estado mínimo de runtime + git en la instancia | `project-progress.txt` existe y la instancia está versionada con git |
| `verificación (TR-2)` | Recorrido validado en contexto fresco | El end-to-end se reproduce/verifica en una sesión separada de la que lo construyó |

## 6. Trazabilidad scope ↔ bdd (checklist del revisor)

| Flujo (slice contract §2) | Peldaño | Cubierto por (escenario/`Then`) |
|---------------------------|---------|----------------------------------|
| `010 Discovery` | `L0` | §2 `When … Discovery …` (artefactos sembrados habilitan el recorrido) |
| `015 Onboarding` | `L0` | §2 `When … Onboarding …` (mapeo habilita Ingestion) |
| `020 Ingestion` | `L0` | §2 `When … Ingestion …` + §3 "bronze inmutable" |
| `025 Profiling` | `L0` | §2 `Then … cada flujo dejó su artefacto` (`data_health.json`) |
| `030 Cleaning` | `L0` | §3 "capas derivan en orden" + §4 "datos faltantes no contaminan" |
| `035 Derivation` | `L0` | §3 "capas derivan en orden" (gold deriva de silver) |
| `040 Exploration` | `L0` | §2 `When … Exploration …` (propone `feature_engineering.yaml`) |
| `045 Featuring` | `L0` | §2 `When … Featuring …` (gold enriquecida) |
| `050 Modelling` | `L0` | §3 "gate humano en la selección de modelo" |
| `055 Inferences` | `L0` | §3 "Inferences entrega MAPE por período" |
| `060 Simulation` | `L0` | §3 "Inferences entrega MAPE… Simulation consume" |
| `065 Scenarios` | `L0` | §3 "Scenarios recalcula un delta what-if mínimo vs. la base" |
| `070 Reporting` | `L0` | §2 `Then … reporting.json contiene el margen bruto … por serie y período` |
| `075 Monitoring` | `L0` | §2 `Then … monitoring.json …` + §3 "el ciclo se cierra con una alerta básica por umbral" |

## 7. Notas / decisiones abiertas

- **Discovery L0** emite los 3 contratos básicos desde un cuestionario pre-respondido (sin intake en
  vivo); los documentos legibles `problem_statement.md` (L1) y `data_structure.md` (L2) se difieren.
- **Modelling L0 = ingenuo + 1 modelo simple** (selección trivial): el gate humano elige entre dos
  candidatos; el torneo real con filtro del ingenuo entra en L1+. `best_model.pkl` se serializa tras la
  aprobación.
- **Scenarios L0 = 1 escenario con 1 delta** (ej. precio −5%): ejercita el recálculo what-if mínimo de
  `065`; la combinación de variables y múltiples escenarios entran en L1+.
- **Reporting L0 = solo margen bruto:** costo de oportunidad y costo de inventario de seguridad se
  difieren a L1+ de `070` (y, en consecuencia, Simulation L0 no produce inventario de seguridad formal).
- **Monitoring vía hold-out:** proxy del flujo recurrente real; sin señal de re-ejecución en esta banda.
  El comportamiento recurrente de producción se difiere a L1+ de `075`.
- **Cardinalidad:** la banda corre C1 completo (~5–10 series) aunque varios briefs definan su L0 sobre 1
  serie; es un desvío deliberado documentado en el slice contract §4.
- **K del hold-out:** número de períodos reservados de C1 para Monitoring — a fijar al construir el golden
  client (`T-014`); debe ser coherente con el horizonte declarado en Discovery.
