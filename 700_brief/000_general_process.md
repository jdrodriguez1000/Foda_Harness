# FODA — Mapa de procesos: entradas y salidas por workflow

> **Documento oficial.** Vista de **proceso** de la tubería FODA: para cada workflow, *qué consume*
> (entradas) y *qué entrega* (salidas), con los **nombres canónicos de cada artefacto**. **No** describe
> *cómo* se construyen las salidas (eso vive en cada brief `700_brief/<NN>_*.md`, en el diseño y en el
> plan); aquí importa el **contrato in/out** que conecta un flujo con el siguiente.
>
> **Nombres canónicos.** Todos los artefactos de entrada y salida tienen **nombre definido y en inglés**.
> Este documento es la **fuente de verdad de los nombres**; los briefs individuales deben coincidir con él.
>
> **Alcance actual.** Workflows con brief redactado: `010`–`075` (**14 de 14, completo**).
>
> **Plano.** Todas las entradas/salidas son **artefactos de runtime de la instancia** (`fda-*`): existen
> cuando el motor se *opera* sobre un cliente, no en el repositorio del motor (`D-001`). Las **capas de
> datos** siguen la arquitectura **bronze → silver → gold**.

---

## Convenciones de nombres

- **Capas de datos:** `bronze` (crudo inalterable) · `silver` (limpio) · `gold` (demanda agregada +
  features). Son **capas**, no archivos sueltos; se referencian por su nombre de capa.
- **Artefactos de archivo:** nombre en inglés con extensión explícita (`.yaml`, `.json`, `.md`, `.pkl`).
- **Exportables:** todo artefacto descargable se exporta con el **mismo nombre base** y extensión de
  formato — `<artifact>.csv` y `<artifact>.xlsx` (p. ej. `data_health.csv` / `data_health.xlsx`).
- **Origen de las entradas:** 🔗 *handoff* de un flujo anterior · 👤 *autoría/insumo humano* ·
  🌐 *fuente externa del cliente* (archivos, base de datos, API).

---

## Vista de cadena (resumen)

```
[questionnaires] 👤
      │
      ▼
010 Discovery ──► client_register.yaml · business_hypothesis.md · contract_data.json
      │                    · problem_statement.md · data_structure.md
      ▼
015 Onboarding ──► map_client_data.json
      │
      ▼  (+ client historical data 🌐)
020 Ingestion ──► bronze (layer) · ingestion_report.json
      │
      ▼
025 Profiling ──► data_health.json
      │
      ▼  (+ data_cleaner.yaml 👤)
030 Cleaning ──► silver (layer) · data_cleaning.json
      │
      ▼  (+ periodicity from contract_data.json)
035 Derivation ──► gold (layer) · data_derivation.json
      │
      ▼  (+ business_hypothesis.md)
040 Exploration ──► exploration.json · feature_engineering.yaml (proposal)
      │
      ▼  (feature_engineering.yaml approved 👤)
045 Featuring ──► gold (enriched layer) · feature_engineering.json
      │
      ▼  (+ modelling_config.yaml 👤)
050 Modelling ──► modelling.json · best_model.pkl   [gate humano: selección]
      │
      ▼  (+ horizon/periodicity from contract_data.json)
055 Inferences ──► gold (predictions) · inferences.json (forecast + MAPE/period)
      │
      ▼  (+ simulation_config.yaml 👤)
060 Simulation ──► gold (simulated demand) · simulation.json
      │              (optimistic/moderate/pessimistic + safety stock)
      ▼  (+ scenarios_config.yaml 👤)
065 Scenarios ──► gold (per-scenario demand) · scenarios.json (base vs. what-if)
      │
      ▼  (+ financial params from bronze: unit price/cost, holding cost)
070 Reporting ──► reporting.json (margins · opportunity cost · safety-stock cost)
      │
      ▼  (+ real demand from bronze + alert threshold config)
075 Monitoring ──► monitoring.json (real vs. simulated) · alerting.json (threshold)
      ╰──► señal de re-ejecución → 050/055/060  (cierra el ciclo, gate humano)
```

---

## Detalle por workflow

### 010 · Discovery
| | |
|---|---|
| **Entradas** | 👤 Respuestas al **business questionnaire** (≥3 stakeholders de áreas distintas) · 👤 Respuestas al **systems/technical questionnaire** (área de sistemas) |
| **Salidas** | `client_register.yaml` · `business_hypothesis.md` · `contract_data.json` · `problem_statement.md` · `data_structure.md` |
| **Capa de datos** | — (pre-ingestión) |

### 015 · Onboarding
| | |
|---|---|
| **Entradas** | 🔗 `contract_data.json` · 🔗 `client_register.yaml` |
| **Salidas** | `map_client_data.json` |
| **Capa de datos** | — (pre-ingestión) |

### 020 · Ingestion
| | |
|---|---|
| **Entradas** | 🔗 `map_client_data.json` · 🔗 `contract_data.json` · 🔗 `client_register.yaml` · 🌐 **client historical data** (CSV / database / API) |
| **Salidas** | **`bronze`** (capa cruda inalterable) · `ingestion_report.json` (carga + cotejo de consistencia) |
| **Capa de datos** | escribe **bronze** |

### 025 · Profiling
| | |
|---|---|
| **Entradas** | 🔗 capa **`bronze`** · 🔗 `map_client_data.json` · 🔗 `contract_data.json` |
| **Salidas** | `data_health.json` (índice de salud % + desglose por tipo + pareto + productos bajo periodicidad mínima) · exportable `data_health.csv` / `data_health.xlsx` |
| **Capa de datos** | lee **bronze** · **no escribe** capa (diagnóstico) |

### 030 · Cleaning
| | |
|---|---|
| **Entradas** | 🔗 capa **`bronze`** · 🔗 `data_health.json` · 👤 `data_cleaner.yaml` (reglas de limpieza, autoría humana) |
| **Salidas** | **`silver`** (capa limpia) · `data_cleaning.json` · exportable `data_cleaning.csv` / `data_cleaning.xlsx` |
| **Capa de datos** | lee **bronze** · escribe **silver** |

### 035 · Derivation
| | |
|---|---|
| **Entradas** | 🔗 capa **`silver`** · 🔗 `data_cleaning.json` · 🔗 **periodicidad** de `contract_data.json` |
| **Salidas** | **`gold`** (demanda histórica agregada: producto × sede × período) · `data_derivation.json` · exportable `data_derivation.csv` / `data_derivation.xlsx` |
| **Capa de datos** | lee **silver** · escribe **gold** |

### 040 · Exploration
| | |
|---|---|
| **Entradas** | 🔗 capa **`gold`** · 🔗 `business_hypothesis.md` |
| **Salidas** | `exploration.json` (resumen histórico + patrones/tendencias + anomalías + veredicto de hipótesis) · `feature_engineering.yaml` (propuesta de variables) · exportable `exploration.csv` / `exploration.xlsx` |
| **Capa de datos** | lee **gold** · **no escribe** capa (informe + propuesta) |

### 045 · Featuring
| | |
|---|---|
| **Entradas** | 🔗 capa **`gold`** · 👤🔗 `feature_engineering.yaml` (propuesto por Exploration, **aprobado** por el humano) |
| **Salidas** | **`gold`** (enriquecida con variables nuevas; matriz de features lista para modelar) · `feature_engineering.json` · exportable `feature_engineering.csv` / `feature_engineering.xlsx` |
| **Capa de datos** | lee **gold** · escribe **gold** (enriquecida) |

### 050 · Modelling
| | |
|---|---|
| **Entradas** | 🔗 capa **`gold`** enriquecida (matriz de features) · 👤 `modelling_config.yaml` (catálogo de modelos, hiperparámetros, baseline ingenuo, métrica y reglas de selección) |
| **Salidas** | `modelling.json` (modelos + hiperparámetros + ranking por métrica con el ingenuo como referencia + importancia de variables) · `best_model.pkl` (modelo ganador **seleccionado por el humano**, serializado) · exportable `modelling.csv` / `modelling.xlsx` |
| **Capa de datos** | lee **gold** · **no escribe** capa (produce artefacto de modelo) |
| **Gate humano** | el científico de datos **selecciona** el modelo final (el flujo recomienda) |

### 055 · Inferences
| | |
|---|---|
| **Entradas** | 🔗 `best_model.pkl` · 🔗 capa **`gold`** (features) · 🔗 **horizonte/periodicidad** de `contract_data.json` |
| **Salidas** | **`gold`** (predicciones por serie/período) · `inferences.json` (demanda predicha + **MAPE por período**) · exportable `inferences.csv` / `inferences.xlsx` |
| **Capa de datos** | lee **gold** · escribe **gold** (predicciones) |

### 060 · Simulation
| | |
|---|---|
| **Entradas** | 🔗 `inferences.json` (pronóstico + **MAPE** por período) / predicciones en **`gold`** · 👤 `simulation_config.yaml` (variables de influencia —lead time, TRM, inflación— **opcionales y extensibles**, con parámetros por producto/serie) |
| **Salidas** | **`gold`** (demanda simulada: optimista/moderado/pesimista + inventario de seguridad) · `simulation.json` · exportable `simulation.csv` / `simulation.xlsx` |
| **Capa de datos** | lee **gold** · escribe **gold** (demanda simulada) |

### 065 · Scenarios (¿qué pasa si…?)
| | |
|---|---|
| **Entradas** | 🔗 `inferences.json` · 🔗 `simulation.json` / demanda simulada en **`gold`** · 👤 `scenarios_config.yaml` (escenarios "¿qué pasa si…?" con **deltas** sobre variables —inflación, lead time, precio de venta… **solo ejemplos; lista abierta y extensible**, como en `060_simulation`—, con alcance por producto/serie/grupo) |
| **Salidas** | **`gold`** (demanda por escenario) · `scenarios.json` (comparativa base vs. escenarios) · exportable `scenarios.csv` / `scenarios.xlsx` |
| **Capa de datos** | lee **gold** · escribe **gold** (demanda por escenario) |

### 070 · Reporting
| | |
|---|---|
| **Entradas** | 🔗 `simulation.json` / demanda simulada en **`gold`** · 🔗 `scenarios.json` (si se reportan escenarios) · 🔗 **parámetros financieros** leídos de la capa **`bronze`** (precio unitario de venta, costo unitario de venta, costo de inventario, tal como el cliente los entregó; mapeados en Onboarding) |
| **Salidas** | `reporting.json` (márgenes, costo de oportunidad, costo de inventario de seguridad, por serie/período y agregados) · exportable `reporting.csv` / `reporting.xlsx` |
| **Capa de datos** | lee **gold** + **bronze** (parámetros financieros) · **no escribe** capa (informe) |

### 075 · Monitoring (incl. Alerting)
| | |
|---|---|
| **Entradas** | 🔗 **demanda real** del cliente en la capa **`bronze`** (entrega periódica) · 🔗 demanda simulada/pronosticada en **`gold`** (`simulation.json` / `inferences.json`) · 👤 **configuración de alertas** (umbral de desviación, destinatarios) |
| **Salidas** | `monitoring.json` (real vs. simulado, desviación por serie/período) · `alerting.json` (alertas al superar el umbral) · exportable `monitoring.csv` / `monitoring.xlsx` · **señal de re-ejecución** a `050`/`055`/`060` (gate humano) |
| **Capa de datos** | lee **gold** + **bronze** (demanda real) · **no escribe** capa (informes/alertas) |
| **Naturaleza** | **recurrente** (corre periódicamente con la demanda real incremental); cierra el ciclo de la tubería |

---

## Tabla maestra de artefactos (nombres canónicos)

| Artefacto | Tipo | Producido por | Consumido por | Origen |
|-----------|------|---------------|---------------|--------|
| `client_register.yaml` | archivo | 010 Discovery | 015, 020 | IA + gate humano |
| `business_hypothesis.md` | archivo | 010 Discovery | 040 | IA + gate humano |
| `contract_data.json` | archivo | 010 Discovery | 015, 020, 035 | IA + gate humano |
| `problem_statement.md` | archivo | 010 Discovery | (lectura humana / cliente) | IA |
| `data_structure.md` | archivo | 010 Discovery | (lectura humana / cliente) | IA |
| `map_client_data.json` | archivo | 015 Onboarding | 020, 025 | IA + gate humano |
| `bronze` | capa de datos | 020 Ingestion (+ demanda real recurrente) | 025, 030, 070 (parámetros financieros), 075 (demanda real) | IA |
| `ingestion_report.json` | archivo | 020 Ingestion | (revisión humana) | IA |
| `data_health.json` | archivo | 025 Profiling | 030 (guía) + revisión humana | IA |
| `data_cleaner.yaml` | archivo (entrada) | 👤 humano + cliente | 030 Cleaning | autoría humana |
| `silver` | capa de datos | 030 Cleaning | 035 | IA |
| `data_cleaning.json` | archivo | 030 Cleaning | (auditoría / replay) | IA |
| `gold` | capa de datos | 035 Derivation (+ 045 enriquece, 055 predicciones, 060 demanda simulada, 065 demanda por escenario) | 040, 045, 050, 055, 060, 065, 070 | IA |
| `data_derivation.json` | archivo | 035 Derivation | (auditoría / replay) | IA |
| `exploration.json` | archivo | 040 Exploration | revisión humana + cliente | IA |
| `feature_engineering.yaml` | archivo (puente) | 040 Exploration (propone) + 👤 aprueba | 045 Featuring | IA + gate humano |
| `feature_engineering.json` | archivo | 045 Featuring | (auditoría / replay) | IA |
| `modelling_config.yaml` | archivo (entrada) | 👤 humano + cliente | 050 Modelling | autoría humana |
| `modelling.json` | archivo | 050 Modelling | (decisión humana + auditoría) | IA |
| `best_model.pkl` | artefacto modelo | 050 Modelling (+ gate humano) | 055 Inferences | IA + gate humano |
| `inferences.json` | archivo | 055 Inferences | 060 Simulation (MAPE) + revisión humana | IA |
| `simulation_config.yaml` | archivo (entrada) | 👤 humano + cliente | 060 Simulation | autoría humana |
| `simulation.json` | archivo | 060 Simulation | 065 Scenarios, 070 Reporting + auditoría | IA |
| `scenarios_config.yaml` | archivo (entrada) | 👤 humano + cliente | 065 Scenarios | autoría humana |
| `scenarios.json` | archivo | 065 Scenarios | 070 Reporting + auditoría | IA |
| `reporting.json` | archivo | 070 Reporting | entregable al cliente + revisión humana | IA |
| `monitoring.json` | archivo | 075 Monitoring | revisión humana + decisión de re-ejecución | IA |
| `alerting.json` | archivo | 075 Monitoring (Alerting) | cliente / científico de datos | IA |

---

## Notas

- Los `.yaml` que entran como **autoría humana** (`data_cleaner.yaml`, `modelling_config.yaml`,
  `simulation_config.yaml`, `scenarios_config.yaml`) o como **propuesta IA + aprobación humana**
  (`feature_engineering.yaml`) marcan los **gates de decisión** de la tubería. En Modelling el gate es además
  de **selección** (el humano elige el `best_model.pkl`). El `simulation_config.yaml` declara variables de
  influencia **opcionales y extensibles** (lead time, TRM, inflación…) por producto/serie; el
  `scenarios_config.yaml` declara escenarios "¿qué pasa si…?" como **deltas** dirigidos (decisión humana) que
  recalculan demanda y simulación.
- Las **capas** son acumulativas e inmutables hacia atrás: **bronze** nunca se altera; **silver** deriva
  de bronze; **gold** deriva de silver. Esto habilita auditar/reconstruir el proceso y los *snapshots* de
  prueba (`D-012`).
- **Vista completa:** los 14 workflows (`010`–`075`) tienen brief y entradas/salidas registradas aquí.
- Los **parámetros financieros** de `070_reporting` (precio/costo unitario, costo de inventario) se **leen de
  la capa bronze** (datos entregados por el cliente, mapeados en Onboarding); no requieren insumo aparte.
- `075_monitoring` agrupa **Monitoring + Alerting** y es **recurrente**: cierra el ciclo realimentando a
  `050`/`055`/`060` (re-modelado/re-inferencia/re-simulación) con **gate humano**.
