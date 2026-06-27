# CLAUDE.md — Proyecto Motor FODA

> Instrucciones para todos los agentes de Claude Code que trabajen en este repositorio.
> **Este repo construye el MOTOR, no la solución de un cliente.** Leer esto antes de actuar.

---

## 1. Qué es este proyecto

Construimos **FODA** (*Forecast Optimization Driven Agentic*): un **motor (harness) reutilizable
e instalable** que replica el trabajo de los científicos de datos de **Sabbia Solutions & Services**
para **planeación de demanda** con machine learning.

Objetivo de negocio: pasar de un modelo de **servicio** (un científico de datos atiende ≤4 clientes)
a **Service-as-a-Software (SaaSw)**, automatizando el **85–95%** del trabajo con agentes de IA y
dejando al científico de datos como **revisor/aprobador** del 5–15% restante.

> ⚠️ Predecimos **la demanda** de los productos del cliente, **no las ventas**.

Documentos fuente (leer si falta contexto): `990_documents/current_state.md`,
`990_documents/expected_workflow.md`, `990_documents/expected_solution.md`.

## 2. Los dos planos (regla de oro)

**Nunca se mezclan.** Ver decisión `D-001` en `800_persistence/decisions.md`.

| Plano | Qué es | Nomenclatura | Vive en |
|-------|--------|--------------|---------|
| **MOTOR** | Definiciones canónicas reutilizables (agentes, comandos, skills, plantillas, esquemas de estado) + memoria de construcción | `foda-*` | **Este repositorio** |
| **INSTANCIA** | La solución concreta para una empresa ABC. Una **carpeta externa por cliente**. Código, iteraciones, artefactos y runtime | `fda-*` | Carpeta destino del cliente (fuera de este repo) |

- El **runtime de la instancia NUNCA vuelve** al repositorio del motor.
- El **puente** entre planos es un instalador de terminal (`./install.sh`) que copia definiciones,
  inicializa git en la instancia y deja el esqueleto de entrada.
- Como Claude Code solo auto-carga `.claude/`, lo privado del motor en la instancia vive en un
  **namespace aparte** y se promueve *just-in-time*.

**Al nombrar artefactos:** si es del motor → prefijo `foda-`. Si es algo que la instancia usará/creará
para un cliente → prefijo `fda-` (ej. un comando sería `fda-comando`).

## 3. Memoria de construcción — `800_persistence/`

**SIEMPRE consultar y mantener actualizada** la memoria del proyecto. Cada archivo tiene un **índice**
al inicio: úsalo para ubicar lo que necesitas **sin leer el archivo completo** (van a crecer).

| Archivo | Para qué | Cuándo actualizarlo |
|---------|----------|---------------------|
| `progress.md` | Estado general: qué se hizo, dónde estamos, qué sigue | Al cerrar un hito o cambiar de fase |
| `tasks.md` | Tareas con estado `[ ] [~] [x] [!]` e ID `T-XXX` | Al iniciar (`[~]`) y completar (`[x]`) una tarea |
| `lessons.md` | Lecciones aprendidas (`L-XXX`) | Cuando algo enseñe a hacer/no hacer algo en adelante |
| `decisions.md` | Decisiones tipo ADR (`D-XXX`) | Al tomar una decisión de diseño/arquitectura |

**Flujo de trabajo obligatorio para cada cambio significativo:**
1. **Antes:** revisar el índice de `tasks.md` y `progress.md` para saber dónde estamos.
2. **Durante:** marcar la tarea en progreso (`[~]`) en `tasks.md`.
3. **Después:** marcar la tarea completada (`[x]`), actualizar `progress.md`, y registrar cualquier
   lección (`lessons.md`) o decisión (`decisions.md`) que aplique.

Convención de IDs: tareas `T-XXX`, lecciones `L-XXX`, decisiones `D-XXX`. Mantener actualizado el
índice de cada archivo al agregar entradas.

## 4. El flujo objetivo (la tubería)

La instancia ejecuta ~13 flujos encadenados, cada uno operado por un agente de IA con artefactos
canónicos (ver detalle en `990_documents/expected_workflow.md`):

1. **Discovery** → `client_register.yaml`, `business_hypothesis.md`, `contract_data.json`
2. **Onboarding** → `map_client_data.json`
3. **Ingestion** → capa **bronze** (inalterable)
4. **Profiling** → índice de salud de datos + pareto
5. **Cleaning** (`data_cleaner.yaml`) → `data_cleaning.json` → capa **silver**
6. **Derivation** → `data_derivation.json` → capa **gold**
7. **Exploration** → `exploration.json`, `feature_engineering.yaml`
8. **Featuring** → `feature_engineering.json`
9. **Modelling** (torneo de campeones) → `best_model.pkl`
10. **Inferences** → `inferences.json` (con MAPE por período)
11. **Simulation** (Montecarlo) → optimista / moderado / pesimista + demanda simulada
12. **Reporting** → `reporting.json` (márgenes, costo de oportunidad, inventario de seguridad)
13. **Monitoring** → `monitoring.json` · **Alerting** → `alerting.json`

Arquitectura de datos en la instancia: **bronze** (crudo inalterable) → **silver** (limpio) →
**gold** (derivado/listo para ML).

## 5. Convenciones de trabajo

- **Idioma:** documentación y artefactos en **español** (es el idioma del proyecto y del cliente).
- **Plataforma:** Windows. Shell primario **PowerShell**; el instalador de la instancia es `install.sh`
  (Git Bash / entorno POSIX).
- **No mezclar planos:** no escribir runtime de cliente en este repo; no asumir que el motor conoce
  datos de un cliente concreto.
- **Cada flujo deja trazabilidad:** sus artefactos (`*.json`/`*.yaml`) documentan las transformaciones
  y permiten **replicar** el proceso en otros archivos del cliente.
- **El humano aprueba:** los puntos de decisión clave (ej. selección del modelo en *Modelling*) los
  confirma el científico de datos. Diseñar los flujos con ese checkpoint en mente.
- **Antes de crear algo nuevo,** revisar si ya existe una definición canónica reutilizable en el motor.

## 6. Estructura del repositorio

```
Foda_Harness/
├── CLAUDE.md              ← este archivo
├── 800_persistence/       ← memoria de construcción del motor
│   ├── progress.md
│   ├── tasks.md
│   ├── lessons.md
│   └── decisions.md
└── 990_documents/         ← documentos fuente (estado actual, flujo y solución esperada)
```

_(La estructura crecerá a medida que se construyan las definiciones canónicas del motor y el
instalador. Mantener esta sección y `progress.md` al día.)_
