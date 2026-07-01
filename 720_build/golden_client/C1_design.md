# C1_design.md — Diseño del golden client C1 (fixture del Tracer Bullet)

> **Alcance:** diseño técnico del **cliente de prueba canónico C1** y de su **generador sintético
> parametrizado**. Es **infraestructura del plano de construcción del MOTOR** (`D-001`): sirve para
> construir y probar la tubería sin re-ejecutar la cadena (`D-012`), **no** es un cliente real de la
> instancia. Cierra el **paso "diseñar" de la tarea `T-014`**; tras la aprobación humana se implementa.
>
> **Decisiones que lo enmarcan:** `D-012` (golden client + snapshots), `D-014` (matriz de complejidad
> producto×geo), `D-015` (walking skeleton), `D-024` (PostgreSQL), `D-027` (schema-per-tenant),
> `D-023` (Python). Fuente de alcance: `703_definition/tracer-bullet/slice_contract.md` (§5) +
> `700_brief/000_general_process.md` + `700_brief/010_discovery.md` (§8, el grain).
>
> **Idioma:** español · **Plataforma:** Python + PostgreSQL · **Estado:** propuesta para aprobación (gate humano).

---

## Índice
- [1. Propósito y encuadre de planos](#1-propósito-y-encuadre-de-planos)
- [2. Frontera del generador (decisión clave)](#2-frontera-del-generador-decisión-clave)
- [3. Grain de C1 (producto × geografía × periodicidad)](#3-grain-de-c1-producto--geografía--periodicidad)
- [4. Esquema de la fuente cruda de C1](#4-esquema-de-la-fuente-cruda-de-c1)
- [5. Modelo generador de la demanda](#5-modelo-generador-de-la-demanda)
- [6. Ruido de calidad de datos (para que Cleaning tenga trabajo)](#6-ruido-de-calidad-de-datos-para-que-cleaning-tenga-trabajo)
- [7. Parámetros del generador](#7-parámetros-del-generador)
- [8. Instanciación concreta de C1](#8-instanciación-concreta-de-c1)
- [9. Hold-out de Monitoring](#9-hold-out-de-monitoring)
- [10. Aterrizaje: archivos y schema en PostgreSQL](#10-aterrizaje-archivos-y-schema-en-postgresql)
- [11. Determinismo y reproducibilidad](#11-determinismo-y-reproducibilidad)
- [12. Snapshots (D-012)](#12-snapshots-d-012)
- [13. Lo que NO hace C1 en esta fase](#13-lo-que-no-hace-c1-en-esta-fase)
- [14. Entregables de T-014 y siguiente paso](#14-entregables-de-t-014-y-siguiente-paso)
- [15. Trazabilidad a decisiones](#15-trazabilidad-a-decisiones)

---

## 1. Propósito y encuadre de planos

C1 es el **input de prueba fiel** que permite construir cada celda del Tracer Bullet **aislada**,
cargando el snapshot del flujo anterior en vez de recomputar toda la cadena (`D-012`). Representa a un
cliente **mínimo** (esquina C1 de la matriz 2×2 de `D-014`): pocas series, para que el skeleton corra
barato e iterativo, pero **suficientes** (~5–10 series) para que la tubería ejercite de verdad el fixture
(desvío de cardinalidad documentado en el slice_contract §4).

**Plano (`D-001`):** todo lo de este documento vive en el **repo del motor** (`720_build/golden_client/`)
como andamiaje de construcción. La *fuente cruda* de C1 **simula** lo que un cliente real entregaría
(su 🌐 *client historical data*); no es un cliente productivo. Los snapshots y este diseño **nunca**
viajan a una instancia.

## 2. Frontera del generador (decisión clave)

**Decisión (aprobada):** el generador produce la **fuente cruda** de C1 — lo que el cliente entrega —,
**no** la capa bronze.

- **Bronze es artefacto del flujo `020_ingestion`** (`000_general_process.md`, tabla maestra; slice_contract
  §2 fila 020: "Carga el histórico de C1 a bronze tal cual"). Nace cuando se construye esa celda y **ahí**
  se congela como snapshot.
- Si el generador escribiera bronze directo, `020` en L0 se quedaría sin nada que ingerir (no-op) y se
  rompería el contrato in/out que el Tracer Bullet debe probar.

**Consecuencia para T-014:** entregamos (a) el generador, (b) la fuente cruda de C1 depositada donde `020`
la pueda leer, (c) el schema `golden_client` en Postgres como contenedor donde bronze/silver/gold nacerán
al construir las celdas, y (d) el hold-out reservado. **No** creamos tablas bronze/silver/gold aquí.

```
[generador T-014]  ──►  fuente cruda C1 (CSV)  ──►  [celda 020_ingestion]  ──►  bronze (Postgres)  ──► …
     (build)              (simula entrega                (se construye                (snapshot D-012)
                           del cliente 🌐)                 después)
```

## 3. Grain de C1 (producto × geografía × periodicidad)

`D-014` define el grain como producto cartesiano de dos jerarquías. C1 es la **esquina mínima**: jerarquías
**superficiales** pero declaradas (para que Discovery/Onboarding las capturen como en la realidad).

| Dimensión | Jerarquía completa (`D-014`) | Profundidad en C1 |
|-----------|------------------------------|-------------------|
| **Producto** | familia → categoría → subcategoría → SKU | 1 familia → 1 categoría → 1 subcategoría → **~5–10 SKUs** |
| **Geografía** | región → país → ciudad → sede | 1 región → 1 país → 1 ciudad → **1 sede** |
| **Periodicidad** | semanal … anual | **mensual** |
| **Historia** | — | **~24–36 meses** |

**Cardinalidad de series** = (nº SKU) × (nº sede) = **~5–10 series de tiempo**. Cada serie = una pareja
`(SKU, sede)` a lo largo del tiempo.

## 4. Esquema de la fuente cruda de C1

Una sola tabla de hechos "ancha" que simula el export de demanda del cliente (una fila = demanda de un
`(SKU, sede)` en un período). Se incluyen los **atributos financieros** porque Reporting (`070`) los lee
de bronze (`D-019`), y bronze proviene de esta fuente.

| Columna | Tipo | Rol | Consumido por |
|---------|------|-----|---------------|
| `periodo` | fecha (primer día del mes) | eje temporal | toda la tubería |
| `familia` | texto | jerarquía producto (nivel 1) | grain (`D-014`) |
| `categoria` | texto | jerarquía producto (nivel 2) | grain |
| `subcategoria` | texto | jerarquía producto (nivel 3) | grain |
| `sku` | texto | jerarquía producto (hoja) | grain / clave de serie |
| `region` | texto | jerarquía geo (nivel 1) | grain |
| `pais` | texto | jerarquía geo (nivel 2) | grain |
| `ciudad` | texto | jerarquía geo (nivel 3) | grain |
| `sede` | texto | jerarquía geo (hoja) | grain / clave de serie |
| `cantidad_demandada` | entero ≥ 0 | **target** (la demanda) | 035→ (agregación), 050 (modelado) |
| `precio_unitario_venta` | decimal | financiero | 070 Reporting (margen) |
| `costo_unitario_venta` | decimal | financiero | 070 Reporting (margen) |
| `costo_inventario` | decimal | financiero (holding) | 070 Reporting (L1+; en L0 solo margen bruto) |

> **Nota:** los nombres de columna de la **fuente** están en español a propósito — simulan las columnas
> "tal como las nombra el cliente". El mapeo al esquema canónico interno lo hace `015_onboarding`
> (`map_client_data.json`), que es justo su razón de ser. Esto le da trabajo real a Onboarding en L0.

## 5. Modelo generador de la demanda

Para que la demanda sea **realista** y **con patrón conocido** (de modo que `040_exploration` pueda
*validar* una hipótesis que `010_discovery` *declaró* como testeable), cada serie `(SKU, sede)` se genera como:

```
cantidad(t) = max(0, round( nivel_base_sku
                            + tendencia · t
                            + estacionalidad_mensual(mes(t))
                            + ruido_gaussiano(σ) ))
```

- **`nivel_base_sku`**: distinto por SKU → magnitudes variadas (habilita el **pareto** de Profiling `025` y
  un contraste de series alto/bajo volumen).
- **`tendencia`**: leve pendiente por serie (creciente/plana/decreciente).
- **`estacionalidad_mensual`**: **pico conocido en diciembre** (temporada navideña) y valle en un mes bajo.
  Este es el patrón que sostiene la **hipótesis testeable** ("la demanda sube en diciembre"), verificable
  aguas abajo (`business_hypothesis.md` → `040_exploration`).
- **`ruido_gaussiano`**: dispersión moderada → el pronóstico no es trivialmente perfecto (MAPE > 0 real en
  `055`, insumo de la simulación Montecarlo de `060`).

Todo con **semilla fija** (§11) → C1 es idéntico en cada regeneración.

## 6. Ruido de calidad de datos (para que Cleaning tenga trabajo)

El slice_contract fija que `030_cleaning` L0 aplica reglas triviales de **nulos/duplicados**. Para que ese
flujo tenga algo real que limpiar (y no un verde falso), el generador inyecta un **poco** de suciedad
**controlada y determinista**:

- un pequeño % de `cantidad_demandada` nulas (huecos de registro),
- unas pocas filas **duplicadas** exactas,
- (opcional, diferible) algún outlier evidente.

Cantidad y ubicación fijas por la semilla; documentadas en el reporte del generador para poder afirmar que
Cleaning las resolvió. Es **poco** a propósito (E4): lo justo para ejercitar `030`, no un dataset sucio.

## 7. Parámetros del generador

El generador es **parametrizado por la matriz de `D-014`** (aunque en T-014 solo instanciemos C1), para que
C2/C3/C4 sean el mismo código con otros parámetros:

| Parámetro | Significado | Valor en C1 |
|-----------|-------------|-------------|
| `profundidad_producto` | niveles vivos de la jerarquía de producto | superficial (1/1/1/N SKU) |
| `n_sku` | nº de SKUs (hojas de producto) | ~5–10 |
| `profundidad_geo` | niveles vivos de la jerarquía geo | superficial (1/1/1/1 sede) |
| `n_sede` | nº de sedes | 1 |
| `periodicidad` | grano temporal | mensual |
| `n_periodos` | longitud de la historia | 24–36 |
| `hold_out_k` | períodos reservados para Monitoring | ver §9 |
| `semilla` | reproducibilidad | fija (p. ej. 42) |
| `nivel_base_rango` | rango de `nivel_base_sku` | por definir al implementar |
| `sigma_ruido` | dispersión del ruido | por definir al implementar |
| `pct_nulos`, `n_duplicados` | ruido de calidad (§6) | pequeños |

## 8. Instanciación concreta de C1

- **Empresa simulada:** una familia de producto única (p. ej. *"Bebidas"*), 1 categoría, 1 subcategoría,
  **~6–8 SKUs** concretos con nombres legibles.
- **Geografía:** 1 región / 1 país / 1 ciudad / **1 sede**.
- **Tiempo:** **36 meses** mensuales (historia cómoda para validación temporal en `050`).
- **Series resultantes:** ~6–8 (una por SKU en la única sede).
- **Financieros:** `precio_unitario_venta` > `costo_unitario_venta` por SKU (margen positivo, para que
  Reporting entregue un margen bruto sensato); `costo_inventario` pequeño por unidad/período.

> Los valores numéricos exactos (rangos de nivel base, precios/costos por SKU, σ) se fijan al implementar
> y se congelan por la semilla; se listan en el reporte del generador.

## 9. Hold-out de Monitoring

`075_monitoring` L0 compara una **ventana de actuals reservada** contra lo simulado (proxy del flujo
recurrente real, que se difiere). El generador produce la serie **completa** y la **parte** en dos:

- **Historia visible (train):** períodos `1 .. n_periodos − K` → alimentan la tubería (Ingestion → … → Simulation).
- **Hold-out (actuals):** últimos **`K` períodos** → **NO** entran a la tubería; se reservan como "demanda
  real" que `075` cotejará contra el pronóstico/simulación de esos mismos períodos.

Propuesta: **K = 6** (semestre) con `n_periodos = 36` → 30 de historia + 6 de hold-out. Ambos salen del
mismo generador (misma semilla), por lo que el hold-out es coherente con la historia.

## 10. Aterrizaje: archivos y schema en PostgreSQL

**Fuente cruda (lo que entrega el "cliente"):** archivos **CSV** bajo `720_build/golden_client/C1/source/`
—simulan el export del cliente que `020_ingestion` leerá (medio de acceso "CSV" del `contract_data.json`)—:

```
720_build/golden_client/
├── C1_design.md                  ← este documento
├── generator/                    ← código Python del generador (T-014)
├── C1/
│   ├── source/
│   │   ├── demanda_historica.csv ← historia visible (train) — fuente para 020
│   │   └── demanda_holdout.csv   ← hold-out de actuals — solo para 075
│   ├── questionnaires/           ← cuestionarios pre-respondidos de C1 (insumo de 010, L0)
│   └── generation_report.json    ← qué se generó (semilla, params, nulos/dups inyectados)
└── snapshots/                    ← congelado bronze/silver/gold + artefactos (D-012), por celda
```

**Schema en PostgreSQL:** T-014 crea el schema **`golden_client`** (el tenant de prueba, `D-027`) como
**contenedor vacío**. Las tablas `bronze_*` / `silver_*` / `gold_*` **no** se crean aquí: nacen con el DDL
de cada celda (020 crea bronze, 030 silver, 035 gold…). Así se respeta que cada capa es artefacto de su flujo.

**Hosting del Postgres — Docker (decidido 2026-07-01).** El servidor Postgres corre **localmente en un
contenedor Docker** (`docker-compose.yml` en esta carpeta), no como instalación nativa. Es infra de
construcción **desechable y reproducible**: casa con el golden client como fixture reseteable (`down -v`
borra el volumen y regenera limpio, `D-012`). Detalles: imagen `postgres:17-alpine`, contenedor
`foda_golden_db`, base `foda`, puerto host **`55432`** (el 5432 estaba ocupado por otros contenedores),
credenciales en `.env` **gitignored** (los secretos no viven en el motor, `D-001`). El schema
`golden_client` lo crea el script de init `db/init/01_golden_client_schema.sql` en la primera corrida.
Esto **no altera `D-024`** (el motor sigue siendo PostgreSQL); es solo la forma de hospedarlo en desarrollo.
Añade al árbol: `docker-compose.yml`, `.env(.example)`, `db/init/`.

> **Cuestionarios de C1 (`questionnaires/`):** Discovery L0 parte de un **cuestionario ya respondido**
> (sin intake en vivo, brief `010` §9). Ese fixture textual también es parte de C1 y lo produce/uraliza
> T-014 (puede ser redactado a mano, no requiere el generador numérico). Declara el grain, la periodicidad
> mensual, el medio CSV y la hipótesis de estacionalidad de diciembre — coherentes con lo que el generador
> numérico realmente incrustó.

## 11. Determinismo y reproducibilidad

- **Semilla fija** en todo el muestreo aleatorio (numpy `default_rng(semilla)`), incluida la inyección de
  ruido de calidad (§6). Regenerar C1 produce **bytes equivalentes**.
- El `generation_report.json` registra semilla, parámetros y las filas exactas ensuciadas → auditable.
- Es la base de los snapshots (`D-012`): si nada cambia en el contrato upstream, C1 no cambia y los
  snapshots siguen válidos.

## 12. Snapshots (D-012)

- Al construir cada celda, su salida (capa y/o artefacto) se **congela** en `snapshots/` para que la celda
  siguiente parta de ahí sin recomputar.
- El snapshot se **versiona ligado al contrato upstream**; se **invalida por cambio de entrada**, no por TTL.
- La mecánica concreta de versionado (nombres de carpeta, manifiesto) se detalla al construir la **primera
  celda que produzca un snapshot** (020); aquí solo se reserva la zona y el principio.

## 13. Lo que NO hace C1 en esta fase

- **No** instancia C2/C3/C4 (solo el generador queda parametrizado para ellas; se instancian bajo demanda / estrés, `D-014`).
- **No** crea tablas bronze/silver/gold (nacen en las celdas).
- **No** modela jerarquías profundas ni reconciliación jerárquica (eso activa C3/C4 en bandas posteriores).
- **No** incluye variables de influencia (lead time, TRM, inflación) — `060`/`065` van en stub en L0.
- **No** simula entrega recurrente real de Monitoring — se usa el hold-out como proxy.

## 14. Entregables de T-014 y siguiente paso

Al aprobarse este diseño, la **implementación** de T-014 entrega:

1. **Generador** Python parametrizado (`generator/`) — modelo de demanda (§5) + ruido de calidad (§6) + split hold-out (§9), determinista (§11).
2. **Fuente cruda de C1** materializada: `demanda_historica.csv`, `demanda_holdout.csv`, `generation_report.json`.
3. **Cuestionarios pre-respondidos de C1** (`questionnaires/`), coherentes con lo generado.
4. **Schema `golden_client`** creado en PostgreSQL (contenedor vacío) + scaffolding de conexión (`D-024`/`D-027`).
5. Actualización del `README.md` del carril y de la persistencia (`progress`, `tasks`, `lessons`/`decisions` si aplica).

**Siguiente paso tras T-014:** construir la **primera celda** del Tracer Bullet, `010_discovery`
(diseñar → ejecutar → probar → verificar), que consume los cuestionarios de C1 y emite los tres contratos.

## 15. Trazabilidad a decisiones

| Tema | Fuente |
|------|--------|
| Golden client + snapshots (caché por inmutabilidad) | `D-012` |
| Matriz de complejidad producto×geo; C1 esquina mínima; generador parametrizado | `D-014` |
| Walking skeleton (por qué C1 mínimo y barato) | `D-015` |
| PostgreSQL como motor de datos; schema-per-tenant (`golden_client` = tenant de prueba) | `D-024`, `D-027` |
| Python + numpy/pandas para el generador | `D-023` |
| Parámetros financieros leídos de bronze (por eso van en la fuente) | `D-019` |
| Peldaños L0 por flujo que C1 debe alimentar | `703_definition/tracer-bullet/slice_contract.md` §2 |
| El grain nace en Discovery (cuestionarios + `contract_data.json`) | `700_brief/010_discovery.md` §8 |
| Frontera del generador = fuente cruda, no bronze | este documento §2 (decisión aprobada 2026-07-01) |

> **Gate humano:** este diseño no habilita la implementación hasta la aprobación explícita del científico
> de datos (`CLAUDE.md §5`, `D-021`).
