# FODA — Mapa de procesos: entradas y salidas por workflow

> **Documento oficial.** Vista de **proceso** de la tubería FODA: para cada workflow, *qué consume*
> (entradas) y *qué entrega* (salidas), con los **nombres canónicos de cada artefacto**. **No** describe
> *cómo* se construyen las salidas (eso vive en cada brief `700_brief/<NN>_*.md`, en el diseño y en el
> plan); aquí importa el **contrato in/out** que conecta un flujo con el siguiente.
>
> **Nombres canónicos.** Todos los artefactos de entrada y salida tienen **nombre definido y en inglés**.
> Este documento es la **fuente de verdad de los nombres**; los briefs individuales deben coincidir con él.
>
> **Alcance actual.** Workflows con brief redactado hasta este punto: `010`–`045` (8 de 14). Se ampliará
> al avanzar los briefs restantes (`050`–`075`).
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
      ▼
050 Modelling … (brief pendiente)
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
| `bronze` | capa de datos | 020 Ingestion | 025, 030 | IA |
| `ingestion_report.json` | archivo | 020 Ingestion | (revisión humana) | IA |
| `data_health.json` | archivo | 025 Profiling | 030 (guía) + revisión humana | IA |
| `data_cleaner.yaml` | archivo (entrada) | 👤 humano + cliente | 030 Cleaning | autoría humana |
| `silver` | capa de datos | 030 Cleaning | 035 | IA |
| `data_cleaning.json` | archivo | 030 Cleaning | (auditoría / replay) | IA |
| `gold` | capa de datos | 035 Derivation (+ 045 enriquece) | 040, 045, 050 | IA |
| `data_derivation.json` | archivo | 035 Derivation | (auditoría / replay) | IA |
| `exploration.json` | archivo | 040 Exploration | revisión humana + cliente | IA |
| `feature_engineering.yaml` | archivo (puente) | 040 Exploration (propone) + 👤 aprueba | 045 Featuring | IA + gate humano |
| `feature_engineering.json` | archivo | 045 Featuring | (auditoría / replay) | IA |

---

## Notas

- Los `.yaml` que entran como **autoría humana** (`data_cleaner.yaml`) o como **propuesta IA + aprobación
  humana** (`feature_engineering.yaml`) marcan los **gates de decisión** de la tubería.
- Las **capas** son acumulativas e inmutables hacia atrás: **bronze** nunca se altera; **silver** deriva
  de bronze; **gold** deriva de silver. Esto habilita auditar/reconstruir el proceso y los *snapshots* de
  prueba (`D-012`).
- Pendiente de incorporar a esta vista al redactar sus briefs: `050_modelling` (→ `best_model.pkl`),
  `055_inferences` (→ `inferences.json`, con MAPE por período), `060_simulation`, `065_scenarios`,
  `070_reporting`, `075_monitoring_alerting`.
