# design_system.md — Diseño del Sistema de la Instancia FODA

> **Alcance:** define el **diseño técnico de la INSTANCIA** (`fda-*`) — la app que un científico de datos
> de la empresa ejecuta para **N clientes**. No describe el motor (`foda-*`) ni la construcción del harness.
> Deriva de `985_inputs/questionnaire_DS.md` (Cuestionario de Diseño de Sistemas) y cierra la tarea **T-023**
> (`D-022`). Las decisiones aquí se elevan a ADRs `D-023..D-027` en `800_persistence/decisions.md`.
>
> **Idioma:** español · **Plataforma:** Python · **Estado:** propuesta para aprobación (gate humano).

---

## Índice
- [1. Contexto y encuadre](#1-contexto-y-encuadre)
- [2. Perfil arquitectónico (qué es y qué no es)](#2-perfil-arquitectónico-qué-es-y-qué-no-es)
- [3. Decisiones de stack (T-023)](#3-decisiones-de-stack-t-023)
- [4. Multi-tenencia: aislamiento por cliente](#4-multi-tenencia-aislamiento-por-cliente)
- [5. Capas de datos en PostgreSQL (bronze/silver/gold)](#5-capas-de-datos-en-postgresql-bronzesilvergold)
- [6. Arquitectura de la aplicación (capas y patrones)](#6-arquitectura-de-la-aplicación-capas-y-patrones)
- [7. Ejecución: batch, gate humano y orquestación](#7-ejecución-batch-gate-humano-y-orquestación)
- [8. Reconciliación con los dos planos (D-001)](#8-reconciliación-con-los-dos-planos-d-001)
- [9. Observabilidad y resiliencia](#9-observabilidad-y-resiliencia)
- [10. Lo que se difiere (no-metas de esta fase)](#10-lo-que-se-difiere-no-metas-de-esta-fase)
- [11. Trazabilidad a decisiones](#11-trazabilidad-a-decisiones)

---

## 1. Contexto y encuadre

La **instancia** es la solución concreta por cliente del pipeline FODA de **14 flujos**
(Discovery → … → Monitoring) que va de datos crudos del cliente a pronóstico de **demanda** y reportes de
negocio, automatizando el 85–95% del trabajo del DS y dejándolo como **revisor/aprobador**.

**Requisito rector (definido por el usuario en T-023):**
> Un **científico de datos de la empresa** ejecuta esta **aplicación en Python** y puede **trabajar para
> N clientes**, con **PostgreSQL** como motor de datos.

Esto convierte la **multi-tenencia** en requisito **actual** (no futuro): la app es multi-cliente desde el
diseño, operada por un DS que **selecciona el cliente** y corre su pipeline.

---

## 2. Perfil arquitectónico (qué es y qué no es)

Del cuestionario (`985_inputs/questionnaire_DS.md`) se concluye el perfil:

| Es | No es |
|----|-------|
| **Pipeline batch** de procesamiento de datos + ML | Servicio web transaccional de alto tráfico |
| **Monolito modular** por capas (14 módulos = flujos) | Microservicios (`D-021`, warning del cuestionario) |
| **Multi-tenant**: 1 DS opera N clientes | Multi-usuario concurrente (concurrencia ≈ 1: el DS) |
| **Asíncrono por diseño** (gate humano entre flujos) | Request/response interactivo de baja latencia |
| **Stateful** en PostgreSQL (el estado es el producto) | Fan-out/fan-in gobernando el diseño (no hay tráfico) |

**Consecuencias directas:** sin CDN, sin caché externa (Redis), sin colas distribuidas, sin sharding, sin
réplicas de lectura. La "caché" es la **inmutabilidad de bronze + snapshots** (`D-012`); el cold start es
irrelevante (batch).

---

## 3. Decisiones de stack (T-023)

| # | Decisión | Elección | Notas |
|---|----------|----------|-------|
| 1 | **Lenguaje + librerías** | **Python** | pandas/polars (datos), scikit-learn + libs de series de tiempo (torneo de Modelling), numpy (Montecarlo de Simulation), SQLAlchemy + psycopg (acceso a Postgres). |
| 2 | **Motor de datos** | **PostgreSQL** | bronze/silver/gold como esquemas/tablas. bronze **inmutable** (solo-inserción/versionado). SQL habilita Profiling/Exploration. |
| 3 | **Forma de la app** | **App Python batch, multi-cliente, con gate humano** | CLI/orquestador: el DS **selecciona el tenant** y corre el pipeline; aprueba en los checkpoints. Sin API web en esta fase. |
| 4 | **Patrones base** | **Monolito modular por capas + hexagonal ligero** | Acceso a Postgres detrás de un **repositorio/puerto** con `tenant` como parámetro transversal; la lógica ML no conoce el esquema físico. |
| 5 | **Aislamiento multi-tenant** | **Esquema por cliente** (schema-per-tenant) | Ver §4. Recomendado y elegido por el usuario. |

---

## 4. Multi-tenencia: aislamiento por cliente

**Decisión: un solo servidor PostgreSQL con un `schema` por cliente (schema-per-tenant).**

```
postgres://servidor/foda
├── cliente_abc   (schema)
│   ├── bronze_*
│   ├── silver_*
│   └── gold_*
├── cliente_xyz   (schema)
│   ├── bronze_*
│   ├── silver_*
│   └── gold_*
└── ...
```

La app **selecciona el tenant** fijando el `search_path` (o calificando el schema) al inicio de cada corrida.

**Por qué esta opción (frente a BD-por-cliente y a `tenant_id` compartido):**
- **Operación simple para 1 DS ↔ N clientes:** una sola conexión/servidor; cambiar de cliente = `SET search_path`.
- **Aislamiento fuerte por namespace:** imposible "olvidar el `WHERE tenant_id`" que arriesga fuga entre
  clientes (defecto de la opción compartida). Datos de clientes distintos nunca se mezclan por accidente.
- **Migraciones manejables:** el mismo DDL se aplica por schema en un loop (Alembic con `search_path`); con
  N moderado es trivial.
- **Puerta abierta:** al ir el acceso **detrás de un repositorio parametrizado por `tenant`**, migrar a
  **BD-por-cliente** (si un cliente exige separación física por contrato) es cambiar el **adaptador de
  conexión**, no la lógica ML.

**Único costo aceptado:** las migraciones se aplican por-schema (detalle de tooling, no de arquitectura).

**Cuándo reevaluar:** si un cliente exige por contrato backups/permisos/borrado físicamente independientes
→ promover ese tenant a **base de datos propia** (el puerto lo absorbe sin tocar el dominio).

---

## 5. Capas de datos en PostgreSQL (bronze/silver/gold)

La arquitectura medallion se materializa como grupos de tablas dentro del schema del cliente:

| Capa | Semántica | En Postgres |
|------|-----------|-------------|
| **bronze** | Crudo **inalterable** del cliente (invariante `D-020`) | Tablas de **solo-inserción / versionadas**; nunca `UPDATE`/`DELETE` sobre lo ingerido. |
| **silver** | Limpio (Cleaning) | Tablas derivadas de bronze; regenerables. |
| **gold** | Derivado/listo para ML (Derivation/Featuring) | Tablas/vistas materializadas; regenerables. |

- **Inmutabilidad + reanudabilidad:** al ser bronze inmutable y silver/gold regenerables, un flujo se puede
  **re-ejecutar idempotente** desde su entrada sin corromper aguas arriba (soporta el "¿qué pasa si se cae?"
  del cuestionario).
- **Snapshots (`D-012`):** el congelado por capa/artefacto para el golden client se versiona **ligado al
  contrato upstream**; la invalidación es por **cambio de entrada**, no por TTL.
- **Parámetros financieros** de Reporting se **leen de bronze** (datos del cliente mapeados en Onboarding),
  no de un insumo nuevo (`D-019`).

---

## 6. Arquitectura de la aplicación (capas y patrones)

**Monolito modular por capas + hexagonal ligero.**

```
┌─────────────────────────────────────────────────────────┐
│  Transporte  → CLI / orquestador batch (selección de     │
│                tenant, disparo de flujos, gate humano)   │
├─────────────────────────────────────────────────────────┤
│  Dominio     → 1 módulo por flujo (010…075)              │
│                lógica ML determinista + agente del flujo │
│                (celda: agents/skills/schemas/contract/   │
│                 deliverables/evaluation — D-021 §4)      │
├─────────────────────────────────────────────────────────┤
│  Datos       → Repositorio/Puerto (tenant como parámetro)│
│                Adaptador PostgreSQL (SQLAlchemy/psycopg)  │
└─────────────────────────────────────────────────────────┘
```

- **Modularidad por dominio, no por equipo:** cada flujo es un módulo con su celda canónica (`D-021 §4`).
- **Hexagonal ligero:** la lógica ML **no importa** psycopg ni conoce el schema; habla con un **puerto**
  (interfaz de repositorio) que recibe el `tenant`. El **adaptador Postgres** implementa ese puerto.
- **Agente ↔ código determinista:** el agente de cada flujo **orquesta**; el trabajo pesado y reproducible
  vive en **código determinista** (`skills/` de la celda), invocado por el agente. El humano aprueba en los
  puntos de decisión (p. ej. selección del `best_model.pkl` en Modelling).

---

## 7. Ejecución: batch, gate humano y orquestación

- **Modelo de despliegue:** batch que **escala a cero** en reposo (sin servidor 24/7; costo idle nulo).
- **Selección de tenant:** el DS elige el cliente al inicio de la corrida → fija el schema activo.
- **Orquestación:** **secuencia de flujos con checkpoints** (no cola distribuida). 1 worker; el único
  paralelismo con sentido es **intra-Modelling** (entrenar candidatos en paralelo), diferible.
- **Gate humano:** puntos de decisión clave (selección de modelo, aprobación de artefactos) los confirma el
  DS; la app persiste el estado y el DS **revisa los artefactos** para aprobar/continuar.
- **Notificación:** hoy = inspección del estado/artefactos (polling manual); webhook/email a futuro.

---

## 8. Reconciliación con los dos planos (D-001)

La multi-tenencia en Postgres **no rompe** la regla de oro de `D-001`:

| Plano | Qué guarda | Dónde |
|-------|-----------|-------|
| **Motor (`foda-*`)** | Definiciones canónicas reutilizables | Este repo; **no conoce** ningún cliente. |
| **Instancia (`fda-*`) — carpeta por cliente** | Config, artefactos, runtime, credenciales de conexión y **nombre del schema** del cliente | Carpeta externa por cliente. |
| **Instancia (`fda-*`) — datos** | bronze/silver/gold del cliente | **PostgreSQL, schema = `cliente_abc`**. |

- El **runtime de datos vive en Postgres**, nunca vuelve al repo del motor.
- La **carpeta por cliente** sigue existiendo (config/artefactos/estado); apunta a su schema por
  configuración. El motor sigue siendo agnóstico del cliente.

---

## 9. Observabilidad y resiliencia

**Mínimo viable en el Tracer Bullet; se afina por bandas (`D-020`).**

- **Logs:** estructurados, con `tenant` / `flujo` / `run_id`. Los **artefactos `*.json`/`*.yaml`** de cada
  flujo son la traza auditable de las transformaciones.
- **Métricas de negocio (ya en contrato):** MAPE por período (055), márgenes/costo de oportunidad/inventario
  de seguridad (070); **Monitoring + Alerting (075)** son flujos del propio pipeline (`alerting.json`).
- **Trazas:** un **`run_id`** correlaciona la corrida a través de los 14 flujos.
- **Resiliencia:** **reanudabilidad** por checkpoints + idempotencia por capa (no alta disponibilidad).
  **Timeouts/reintentos con backoff/circuit breaker** solo en el borde **LLM/API externa** del cliente;
  diferidos al andamiaje transversal (`TR-*`, `D-020`).

---

## 10. Lo que se difiere (no-metas de esta fase)

- API web / servicio en vivo (la app es batch operada por el DS).
- BD-por-cliente y object storage (S3/GCS) — se habilitan vía el puerto si algún contrato lo exige.
- Caché externa (Redis), colas distribuidas (SQS/Kafka), réplicas de lectura, sharding, CDN.
- Paralelismo multi-máquina; circuit breakers/retries sofisticados; dashboards de salud del *sistema*.

---

## 11. Trazabilidad a decisiones

| Tema | Fuente |
|------|--------|
| Dos planos motor/instancia | `D-001` |
| Estado de runtime en la instancia | `D-004` |
| Golden client + snapshots (caché por inmutabilidad) | `D-012` |
| Grain producto×geografía (jerarquías del cliente) | `D-014` |
| Configs de autoría humana `<flujo>_config.yaml`; financieros desde bronze | `D-019` |
| Invariantes transversales (bronze inmutable, gate humano, persistencia+git) y diferibles | `D-020` |
| Vertical slice, celda flujo×banda, código determinista en `skills/` | `D-021` |
| Stack de la instancia se decide antes del primer slice | `D-022` |
| **Stack: Python / PostgreSQL / batch multi-tenant / hexagonal ligero / schema-per-tenant** | **este documento → `D-023..D-027` (a registrar)** |

> **Siguiente paso:** registrar `D-023..D-027` en `800_persistence/decisions.md`, marcar **T-023** completada
> en `tasks.md`, actualizar `progress.md`, y **desbloquear T-014** (el generador del golden client emite
> bronze directo a Postgres en el schema del cliente de prueba).
