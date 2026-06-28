# Brief — Arnés 010 Discovery (Co-Diseño / Engine BDD)

> **Tipo:** Brief de enmarque (alto nivel, previo al diseño agéntico). NO es la definición agéntica fina.
> **Proyecto:** CADEN (Continuous Agentic Development Engine) — plano de **construcción** del motor.
> **Componente:** Arnés 1 de 6 — `010_discovery` (primero del bucle; se ejecuta una sola vez al inicio + en modo Ajuste).
> **Fuente de verdad:** `900_inputs/statement_vertical_slices.md` (§"The Discovery Harness" y §"Paso a Paso Harness Discovery").
> **Método de construcción:** `905_methodology/methodology.md` + `905_methodology/principles.md`.
> **Estado:** APROBADO · **Fecha:** 2026-06-18 · **Aprobado por:** usuario (dueño del proyecto CADEN)

---

## 0. Aclaración de planos (L-001) — leer primero

Este brief describe un **componente del motor CADEN que estamos fabricando** (plano de
*construcción*). No describe el descubrimiento de un producto concreto: describe la **maquinaria
genérica y reutilizable** que, cuando se *opera* sobre una carpeta de cliente arbitraria, traduce una
idea libre en un plan de ingeniería rebanado.

- **Insumo del componente al operar:** un archivo **`scope.md`** ubicado en `900_documents/` en la raíz
  del proyecto cliente, con la **descripción de alto nivel** que el cliente espera del proyecto (p. ej.
  *"Quiero construir una aplicación web para la gestión de mis gastos personales"*). Cambia en cada
  proyecto cliente.
- **Estado de runtime** que produce al operar (`roadmap-manifest.json`, BDD por slice, etc.) pertenece
  al **plano de operación** sobre el cliente, **no** a la memoria de construcción `800_persistence/`.

## 1. Objetivo

Traducir una **idea abstracta o épica del cliente**, expresada en lenguaje natural, en un **plan de
ingeniería perfectamente rebanado y libre de ambigüedades**. El Arnés 010 **no produce código,
arquitectura, specs técnicas ni backlog**: produce **comprensión de negocio documentada como
comportamiento (BDD) y firmada explícitamente por el humano**, lista para que el Arnés 2 (Architecture)
y el Arnés 3 (Contract & Mold) arranquen.

En una frase: *transformar el `scope.md` del cliente en un `roadmap-manifest.json` de Vertical Slices
(MECE) con escenarios BDD y restricciones no funcionales, validado y firmado por el humano.*

## 2. Alcance — qué hace

**Modo Inicio (descubrimiento, una sola vez al arranque del proyecto cliente):**

- **Recepción del insumo bruto:** lee el archivo **`scope.md`** (en `900_documents/`) con la descripción
  de alto nivel del cliente y detecta cuándo una petición es una **Épica** (demasiado grande/densa para
  una sola rebanada) y activa el protocolo de división.
- **Cuestionario de comportamiento (Behavior Filtering):** lanza un cuestionario **dinámico y corto
  (3–8 preguntas)** enfocado en el **comportamiento del usuario y el flujo de datos**, no en
  características técnicas. Aplica búsqueda **de amplio a estrecho** (E11): primero mapea el espacio,
  luego profundiza donde hay mayor densidad de información relevante.
- **Trituración de épicas y diseño de slices (Slice Splitting):** rompe la épica en **Vertical Slices
  mutuamente excluyentes y colectivamente exhaustivas (MECE)**, organizadas en una estructura **ordenada
  por bandas con 3 anclas obligatorias**: **Tracer Bullet** → [**Stabilization**: Stab 1, Stab 2, …
  (0..n)] → **MVP** → [**Evolution**: Evol 1, Evol 2, … (0..n)] → **Final**. Las anclas **Tracer Bullet,
  MVP y Final** existen **siempre** (mínimo 3 slices); Stabilization y Evolution son bandas opcionales.
  Calcula su dependencia lógica y orden.
- **Redacción de la especificación BDD (entregable central):** por cada slice redacta sus **escenarios
  Given-When-Then** en formato Gherkin y, debajo, una sección mínima de **restricciones no funcionales**
  vinculadas a ese comportamiento (p. ej. rendimiento, latencia).
- **Validación y firma humana:** presenta el plan de slices con sus BDD; el humano valida la lógica de
  negocio y solicita reescrituras instantáneas si la IA malinterpretó; cierra con la firma `/aprobar`,
  tras la cual el harness guarda formalmente los artefactos BDD.

**Modo Ajuste (Inyección de Features / Change Management, reapertura del bucle):**

- Reabre el harness cuando llega una **feature nueva** después de validar una slice ("Agregar la
  feature X a la Stab 2"), la traduce a escenarios **BDD** y calcula su **impacto técnico**.
- **Cirugía precisa sobre `roadmap-manifest.json`**: no borra lo ya hecho; reestructura el futuro —
  **Opción A (Expansión)** inyecta la feature dentro de una slice existente; **Opción B (Nueva
  Rebanada)** crea una slice intermedia y desplaza el calendario.
- Deja el `roadmap-manifest.json` mutado y firmado para que el bucle (Arnés 3→6) se reanude.

## 3. Alcance — qué NO hace (límites)

- **No** define el stack, el andamiaje de carpetas ni las reglas de gobernanza/linter → eso es el
  **Arnés 2 (Architecture)**.
- **No** genera tipos, esquemas, contratos de API ni mocks → eso es el **Arnés 3 (Contract & Mold)**.
- **No** descompone tareas atómicas RED/GREEN/REFACTOR ni asigna feature branch → eso es el **Arnés 4
  (Tactical Planning)**.
- **No** escribe código ni ejecuta TDD → eso es el **Arnés 5 (Execution)**.
- **No** valida en Sandbox, no corre regresión/E2E ni hace merge a `main` → eso es el **Arnés 6
  (Validation)**.
- **No** diseña la **maquinaria agéntica fina** de este propio arnés (instancias A/B/C, workers,
  checkpoints, rúbrica, contratos) → eso es el **diseño del harness**, paso siguiente a este brief.

## 4. Insumos disponibles

| ID | Insumo | Origen |
|----|--------|--------|
| I-1 | Definición de CADEN y de los 6 arneses (fuente de verdad) | `900_inputs/statement_vertical_slices.md` |
| I-2 | Paso a paso del Discovery (Engine BDD) y Protocolo de Inyección de Features | `900_inputs/statement_vertical_slices.md` (§"Paso a Paso Harness Discovery" y §"Protocolo de Inyección de Features") |
| I-3 | Metodología y principios de construcción del harness (P1–P8, E1–E12, patrón A/B/C) | `905_methodology/methodology.md`, `905_methodology/principles.md` |
| I-4 | Memoria de construcción del proyecto (estado, decisiones, lecciones) | `800_persistence/` |

> **Insumo en tiempo de operación (no de construcción):** el archivo **`scope.md`** (en
> `900_documents/` de la raíz del proyecto cliente) con la descripción de alto nivel, y las respuestas
> del cliente al cuestionario de comportamiento. Llegan cuando el motor se *opera*, no ahora.

## 5. Artefactos esperados (salida del componente al operar)

El Arnés 010 entrega el paquete que el Arnés 2 (Architecture) y el bucle necesitan para arrancar:

| Artefacto | Propósito |
|-----------|-----------|
| **`roadmap-manifest.json`** | Lista ordenada de Vertical Slices MECE en bandas: **Tracer Bullet → [Stab 1..n] → MVP → [Evol 1..n] → Final** (3 anclas obligatorias: Tracer/MVP/Final), con dependencias y orden. Archivo **vivo**: el modo Ajuste lo muta. |
| **Escenarios BDD por slice** | Given-When-Then en Gherkin por cada slice (embebidos en el manifest o como Markdown individuales). |
| **Restricciones no funcionales por slice** | Sección mínima ligada al comportamiento de cada slice (p. ej. rendimiento, latencia, límites). |
| **Registro de firma (`/aprobar`)** | Evidencia de la validación y aprobación humana del plan de slices. |

> Los *paths* exactos, el esquema preciso del `roadmap-manifest.json` y la mecánica de cada artefacto se
> fijan en el **diseño del harness** (paso siguiente).

## 6. Criterios de éxito (Done)

1. El humano **aprueba explícitamente** el plan de slices con sus BDD mediante la firma `/aprobar`
   ("Sí, esto es exactamente lo que queremos"). Gate humano obligatorio (P5).
2. **No emergen contradicciones nuevas** en 2 rondas consecutivas de preguntas/validación.
3. Las Vertical Slices son **MECE** (mutuamente excluyentes y colectivamente exhaustivas) y están
   **clasificadas** en la estructura de bandas **Tracer Bullet → [Stab 1..n] → MVP → [Evol 1..n] →
   Final**, con las **3 anclas obligatorias** presentes (Tracer/MVP/Final, mínimo 3 slices) y su
   **orden de dependencia** calculado.
4. **Cada slice** tiene **≥1 escenario BDD** (Given-When-Then) y su sección de **restricciones no
   funcionales**.
5. Toda **Épica** detectada en el prompt quedó **triturada** en slices manejables (ninguna slice
   excede el tamaño de una rebanada).
6. **Modo Ajuste:** una feature inyectada queda reflejada en `roadmap-manifest.json` sin borrar lo
   aprobado (Expansión o Nueva Rebanada), con el calendario reordenado y vuelta a firmar.

## 7. Riesgos / advertencias

- **Confusión de planos (L-001):** el 010 descubre *el negocio del cliente a fabricar*, no la
  maquinaria que lo fabrica. El `roadmap-manifest.json` es estado de operación, no memoria de
  construcción.
- **Insumo genérico, no fijo:** el insumo es un **`scope.md` arbitrario** que cambia en cada proyecto
  cliente. El diseño no debe acoplarse a un dominio de negocio específico ni asumir un contenido fijo.
- **Slicing deficiente:** slices no-MECE o épicas mal trituradas envenenan todo el bucle aguas abajo
  (Arneses 3–6). El gate humano y la regla MECE son la mitigación.
- **Compromiso prematuro (E11):** fijar el plan a la primera interpretación del prompt antes de
  explorar la amplitud ciega al agente ante información más relevante. Explorar amplio antes de
  profundizar.
- **Modo Ajuste mal aplicado:** introducir features "en caliente" en la ejecución (en vez de mutar
  primero el roadmap) genera deuda técnica. Toda feature nueva pasa por este arnés antes de tocar
  código.

## 8. Siguiente paso

Tras **aprobar este brief**: **diseñar el Arnés 010** (instancias A/B/C, workers, política de
herramientas y escalamiento, checkpoints canónicos, política de fallback, trigger de context reset,
rúbrica de evaluación y Sprint Contract), tomando como guía a adaptar el paso a paso del statement y la
metodología `905_methodology/`. El **plan de implementación** viene *después* del diseño (orden del
método: **brief → diseño → plan → construir**). El diseño se materializará en `705_design/`.
