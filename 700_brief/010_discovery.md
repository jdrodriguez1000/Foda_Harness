# Brief — Flujo 010 Discovery (Definición del problema + contrato de datos)

> **Tipo:** Brief de enmarque (alto nivel, previo al diseño agéntico). NO es la definición agéntica fina.
> **Proyecto:** FODA (Forecast Optimization Driven Agentic) — plano de **construcción** del motor.
> **Flujo:** `010` de 14 — `010_discovery` (primer flujo de la tubería; se ejecuta una sola vez al inicio del proyecto cliente + en modo Ajuste cuando cambia el negocio).
> **Posición en la tubería:** abre la cadena → entrega a `015_onboarding`.
> **Capa de datos que toca:** `—` (pre-ingestión: no produce bronze/silver/gold; produce contratos e hipótesis que rigen las capas posteriores).
> **Fuente de verdad:** `990_documents/expected_workflow.md` (§1 Discovery) + `990_documents/expected_solution.md`.
> **Método de construcción:** `950_guideline/methodology.md` + `950_guideline/principles.md`.
> **Decisiones que lo enmarcan:** `D-001` (dos planos), `D-014` (grain producto × geo), `D-015` (walking skeleton), `D-016` (brief + escalera) · **Estado:** `APROBADO` · **Fecha:** `2026-06-28` · **Aprobado por:** `usuario`.

---

## 0. Aclaración de planos — leer primero

Este brief describe un **componente del MOTOR FODA que estamos fabricando** (plano de *construcción*).
No describe el descubrimiento de una empresa concreta: describe la **maquinaria genérica y reutilizable**
que, al *operarse* sobre la carpeta de un cliente arbitrario, transforma el conocimiento disperso del
negocio (entrevistas a stakeholders + entrevista al área de sistemas) en los **tres contratos
fundacionales** que rigen toda la tubería aguas abajo. El diseño no debe acoplarse a un dominio de
negocio concreto (no asumir retail vs. farma vs. manufactura): el flujo opera sobre cualquier empresa ABC.

- **Insumo del flujo al operar:** las **respuestas a dos cuestionarios estandarizados** — (a) el de
  *negocio* a ≥3 stakeholders de áreas distintas (p. ej. planeación, comercialización, logística) y
  (b) el *técnico* al área de sistemas (desde cuándo hay datos, confiabilidad, medios de acceso). Cambia
  por cliente; el flujo no debe asumir un contenido fijo.
- **Salida de runtime que produce al operar:** `client_register.yaml`, `business_hypothesis.md` y
  `contract_data.json` (más los dos documentos legibles de problemática y de estructura de datos).
  Pertenecen al **plano instancia** (`fda-*`); **nunca** vuelven a la memoria de construcción del motor.
- **Grain del cliente (`D-014`):** Discovery es donde **nace** el grain. `contract_data.json` debe
  capturar, al menos de forma declarativa, la jerarquía de **producto** (familia→categoría→subcategoría→
  clase/SKU) y de **geografía** (región→país→ciudad→sede) y la **periodicidad** de la demanda
  (semanal…anual). Onboarding (`015`) lo *mapea* a la estructura interna; Discovery lo *declara* en el
  contrato (`T-015`).

## 1. Objetivo

Transformar el **conocimiento disperso y tácito del negocio del cliente** — repartido entre las áreas
operativas y el área de sistemas — en **comprensión documentada, verificable y firmada**: qué problema
de planeación de demanda se busca resolver, cómo se comporta la demanda del cliente (hipótesis), y bajo
qué **contrato de datos** se intercambiará la información histórica. Discovery **no toca datos, no perfila
ni limpia, no modela**: produce el marco de negocio y el contrato que permiten que `015_onboarding` en
adelante arranquen sin ambigüedad.

> En una frase: transformar las **entrevistas a stakeholders y al área de sistemas** en
> `client_register.yaml` + `business_hypothesis.md` + `contract_data.json`, validados y aprobados por el
> científico de datos.

## 2. Alcance — qué hace

**Modo Inicio (descubrimiento, una sola vez al arranque del proyecto cliente):**

- **Definición del problema (cuestionario de negocio):** conduce/asiste un **cuestionario estandarizado**
  a **≥3 stakeholders de áreas diferentes** (p. ej. planeación, comercialización, logística) para
  capturar la situación actual del problema de planeación de demanda. Verifica la **cobertura de áreas**
  (no aceptar 3 stakeholders del mismo silo).
- **Documento de problemática:** a partir de las respuestas, el agente redacta un **documento de la
  situación actual** del negocio: sirve de contexto al científico de datos y es **compartible** por el
  cliente con otros stakeholders.
- **Entendimiento de la estructura de datos (cuestionario técnico):** asiste la entrevista al **área de
  sistemas** para entender la estructura de datos: **desde cuándo** hay información, **estado/confiabilidad**,
  **medios de acceso** (CSV, base de datos, API externa), volumen y cobertura.
- **Documento de estructura de datos:** redacta el **documento legible** de la estructura de datos de la
  empresa (contexto para el científico de datos y compartible con el cliente).
- **Captura de hipótesis de comportamiento:** identifica y formaliza cómo se comporta la demanda según
  factores (días festivos, temporadas como Navidad, clima, promociones, pandemia, etc.) como **hipótesis
  testeables** que el flujo `040_exploration` validará más adelante.
- **Emisión de los tres contratos fundacionales (entregable central):**
  - **`client_register.yaml`** — registro estructurado de la situación actual de la empresa.
  - **`business_hypothesis.md`** — hipótesis de comportamiento de la demanda.
  - **`contract_data.json`** — **contrato de datos** Sabbia ⇄ empresa ABC: qué archivos enviará el
    cliente (número y naturaleza), medio de acceso, periodicidad de la demanda y el **grain** declarado
    (producto × geografía, `D-014`).
- **Validación y firma humana:** presenta los artefactos; el **científico de datos** los revisa, pide
  reescrituras si el agente malinterpretó, y **aprueba explícitamente** antes de pasar a Onboarding.

**Modo Ajuste (re-discovery cuando cambia el negocio):**

- Reabre el flujo ante un cambio material (nueva línea de producto, nueva geografía, cambio de
  periodicidad, nueva hipótesis de negocio) y actualiza los tres contratos **sin destruir** lo aprobado,
  re-firmando el resultado para que la tubería aguas abajo se reanude de forma consistente.

## 3. Alcance — qué NO hace (límites)

- **No** mapea la estructura de datos a la representación interna del sistema ni fija el número exacto de
  archivos a recibir contra el sistema → eso es el **flujo `015_onboarding`** (que consume
  `contract_data.json`).
- **No** carga, copia ni versiona datos del cliente, ni crea la capa **bronze** → eso es el **flujo
  `020_ingestion`**.
- **No** mide la salud de los datos ni calcula pareto/indicadores → eso es el **flujo `025_profiling`**.
- **No** **valida** las hipótesis de comportamiento (solo las **declara**) → la validación contra los
  datos es del **flujo `040_exploration`**.
- **No** define reglas de limpieza, derivación ni feature engineering → eso es de los flujos `030`–`045`.
- **No** diseña la **maquinaria agéntica fina** de este flujo (instancias A/B/C, workers, checkpoints,
  rúbrica del evaluador, contratos de herramientas) → eso es el **diseño del flujo `010_discovery`**,
  paso siguiente a este brief.

## 4. Insumos disponibles

| ID | Insumo | Origen |
|----|--------|--------|
| I-1 | Definición del flujo Discovery en la tubería FODA | `990_documents/expected_workflow.md` (§1) |
| I-2 | Visión de solución y dos planos motor/instancia | `990_documents/expected_solution.md` |
| I-3 | Metodología y principios de construcción (P*, E*, NC*, patrón A/B/C, modelo plano) | `950_guideline/methodology.md`, `950_guideline/principles.md` |
| I-4 | Memoria de construcción (estado, decisiones, lecciones) | `800_persistence/` (`D-001`, `D-014`, `D-015`, `D-016`) |
| I-5 | Brief de referencia (tono y estructura de enmarque) | `Caden_Harness/700_brief/010_discovery.md` (externo, solo referencia) |

> **Insumo en tiempo de operación (no de construcción):** los **cuestionarios respondidos** por los ≥3
> stakeholders de negocio y por el área de sistemas del cliente concreto. Llegan cuando el motor se
> *opera*, no ahora. (Para construir y probar el flujo se usará el **golden client C1** sintético — ver
> `D-012`/`D-014` y `T-014`.)

## 5. Artefactos esperados (salida del flujo al operar)

| Artefacto | Propósito |
|-----------|-----------|
| **`client_register.yaml`** | Registro estructurado de la situación actual de la empresa. Lo consumen `015_onboarding` e `020_ingestion` (cotejo de consistencia de la carga). |
| **`business_hypothesis.md`** | Hipótesis de comportamiento de la demanda (festivos, temporadas, clima, promociones…). Lo consume `040_exploration` para validarlas contra los datos. |
| **`contract_data.json`** | Contrato de datos Sabbia ⇄ ABC: archivos esperados, medios de acceso, periodicidad de la demanda y grain producto × geografía (`D-014`). Lo consumen `015_onboarding`, `020_ingestion` y `035_derivation` (periodicidad de agregación). |
| **`problem_statement.md`** (documento legible de problemática) | Contexto de negocio para el científico de datos; compartible por el cliente. |
| **`data_structure.md`** (documento legible de estructura de datos) | Contexto técnico para el científico de datos; compartible por el cliente. |

> Los *paths* exactos, el esquema preciso de cada artefacto y la mecánica se fijan en el **diseño del
> flujo** (paso siguiente).

## 6. Criterios de éxito (Done)

1. Existen los **tres contratos fundacionales** (`client_register.yaml`, `business_hypothesis.md`,
   `contract_data.json`) bien formados y mutuamente consistentes (lo declarado en el registro coincide
   con el contrato de datos).
2. La **cobertura de stakeholders** es válida: ≥3 entrevistas de **áreas diferentes** quedaron reflejadas
   en el documento de problemática.
3. El `contract_data.json` declara de forma **inequívoca**: número/naturaleza de archivos a recibir,
   medio(s) de acceso, **periodicidad** de la demanda y el **grain** producto × geografía (`D-014`).
4. `business_hypothesis.md` contiene **≥1 hipótesis** de comportamiento formulada de forma **testeable**
   (verificable aguas abajo en `040_exploration`).
5. **Gate humano (obligatorio):** el **científico de datos aprueba explícitamente** los tres artefactos
   antes de habilitar `015_onboarding` (ver `CLAUDE.md §5`).
6. **Modo Ajuste:** un cambio de negocio queda reflejado en los tres contratos sin borrar lo aprobado y
   con nueva firma.

## 7. Riesgos / advertencias

- **Confusión de planos (`D-001`):** Discovery descubre *el negocio del cliente*, no la maquinaria que lo
  fabrica. Los tres contratos son **runtime de la instancia** (`fda-*`), no memoria de construcción.
- **Acoplamiento a un dominio concreto:** asumir un tipo de empresa, un set fijo de archivos o una
  jerarquía rígida envenena la reutilización del motor. El contrato debe ser **declarativo y genérico**.
- **Envenenar aguas abajo (E9):** un contrato de datos ambiguo o un grain mal declarado contamina
  Onboarding→Reporting (flujos `015`–`070`): archivos incompletos, agregación errónea, series mal
  formadas. El gate humano y la consistencia registro⇄contrato son la mitigación.
- **Hipótesis no testeables:** hipótesis vagas ("la demanda sube a veces") que `040_exploration` no podrá
  validar. Exigir formulación verificable.
- **Compromiso prematuro (E11):** fijar el problema a la primera respuesta de un solo stakeholder, ciego
  a las visiones de otras áreas. Explorar amplio (varias áreas) antes de profundizar.
- **Fixture stale (al construir):** el golden client C1 debe mantenerse consistente con el esquema del
  contrato; un C1 desactualizado da falsos verdes (`D-012`, `T-014`).

## 8. El grain nace aquí (`D-014`) — sección específica del flujo

Discovery es el **origen del grain** de toda la tubería. Aunque `015_onboarding` lo *mapea* a la
representación interna, es el `contract_data.json` de Discovery el que lo **declara** por primera vez:

- **Jerarquía de producto:** familia → categoría → subcategoría → clase/SKU.
- **Jerarquía de geografía:** región → país → ciudad → sede (sucursal/oficina/centro de despacho).
- **Periodicidad de la demanda:** semanal / quincenal / mensual / bimestral / trimestral / semestral /
  anual (rige la agregación en `035_derivation`).

El **producto cartesiano grain × periodicidad** determina la **cardinalidad de series** que el resto del
motor deberá manejar (matriz de complejidad 2×2 de `D-014`). Declararlo mal o de forma incompleta aquí se
propaga como error sistemático aguas abajo. El diseño del flujo debe tratar el grain como **dato de
primera clase del contrato**, no como detalle opcional.

## 9. Escalera de capacidades (L0 → Ln) — vista vertical del flujo

> Vista vertical de la *ambición completa* de Discovery (`D-016`). **L0 = lo mínimo** del walking
> skeleton (Tracer Bullet, `D-015`): sin entrevistas en vivo, se parte de cuestionarios **ya respondidos**
> del golden client **C1** y se emiten los tres contratos en forma mínima. Cada peldaño agrega capacidad.

| Nivel | Capacidad | Qué incluye | Qué difiere de la realidad |
|-------|-----------|-------------|----------------------------|
| **L0** (mínimo / skeleton) | **Emisión mínima de los 3 contratos desde cuestionarios pre-respondidos** | A partir de un cuestionario ya respondido (fixture de C1), el agente genera `client_register.yaml` (campos básicos), `business_hypothesis.md` (1 hipótesis), `contract_data.json` (archivos, medio, periodicidad y grain básico de C1). Gate humano simple (aprobar/rechazar). | No hay entrevistas en vivo ni protocolo dinámico; un solo "stakeholder" simulado; grain básico (pocos niveles); sin documentos legibles ricos; sin modo Ajuste. |
| **L1** | **Cuestionario de negocio multi-stakeholder + documento de problemática** | Cuestionario estandarizado a ≥3 stakeholders de áreas distintas; verificación de cobertura de áreas; síntesis del **documento de problemática** legible. | Aún sin entrevista técnica formal; hipótesis y contrato todavía simples. |
| **L2** | **Entrevista técnica al área de sistemas + documento de estructura de datos + hipótesis ricas** | Cuestionario técnico (desde cuándo, confiabilidad, medios de acceso); **documento de estructura de datos**; hipótesis de comportamiento por factores (festivos, clima, promociones…) formuladas como testeables. | Cuestionarios aún guionados (no dinámicos); grain declarado pero no exhaustivo; sin conciliación de visiones contradictorias. |
| **L3** | **Grain multinivel completo + cuestionario dinámico + detección de contradicciones** | Captura completa del grain producto × geo y periodicidad en el contrato (`D-014`); cuestionario **dinámico** (amplio→estrecho, E11); detección de contradicciones entre áreas y re-preguntas. | Aún no concilia automáticamente visiones en conflicto ni negocia el contrato; modo Ajuste básico. |
| **Ln** (ambición completa) | **Discovery "como un científico de datos senior"** | Conduce/transcribe entrevistas reales, concilia visiones contradictorias entre áreas, **negocia** el contrato de datos, prioriza hipótesis y las enlaza a variables candidatas, **modo Ajuste** (re-discovery) robusto ante cambios de negocio. | Nada: es el objetivo final del flujo. |

> **Nota de ensamblaje:** al cerrar este brief se refleja el estado en `800_persistence/roadmap.md`
> (fila Discovery: columna *Brief* → `planeado`; peldaño previsto para Tracer Bullet → **L0**).

## 10. Siguiente paso

Tras **aprobar este brief**: **diseñar el flujo `010_discovery`** (instancias A/B/C según el modelo plano
`D-009`, workers, política de herramientas, checkpoints canónicos, durabilidad, rúbrica del evaluador y
contrato), reutilizando los patrones transversales ya validados del motor. El **plan de implementación**
viene *después* del diseño (orden del método: **brief → diseño → plan → construir**, `D-011`). El diseño
se materializará en `705_design/010_discovery.md`.
