# Decisions — Motor FODA

> Decisiones de diseño y arquitectura tomadas durante la construcción del motor FODA.
> Registro tipo ADR (Architecture Decision Record) resumido.

---

## Índice
- [D-001 — Dos planos: Motor (FODA) e Instancia (fda)](#d-001--dos-planos-motor-foda-e-instancia-fda)
- [D-002 — Memoria de construcción en 800_persistence/](#d-002--memoria-de-construcción-en-800_persistence)
- [D-003 — Comandos de sesión ejecutan con Sonnet](#d-003--comandos-de-sesión-ejecutan-con-sonnet)

---

## Decisiones

### D-001 — Dos planos: Motor (FODA) e Instancia (fda)
- **Estado:** Aceptada
- **Fecha:** 2026-06-27
- **Contexto:** El producto debe escalar a muchas empresas sin mezclar el código del harness con el de cada cliente.
- **Decisión:** Separar en dos planos que nunca se mezclan: el **MOTOR** (`foda-*`, definiciones canónicas reutilizables) y la **INSTANCIA** (`fda-*`, una carpeta externa por cliente). El runtime de la instancia nunca vuelve al motor. El puente es un instalador de terminal.
- **Origen:** `990_documents/expected_solution.md`.

### D-002 — Memoria de construcción en 800_persistence/
- **Estado:** Aceptada
- **Fecha:** 2026-06-27
- **Contexto:** Los archivos de memoria crecerán y no se quiere leerlos completos cada vez.
- **Decisión:** Mantener 4 archivos (`progress.md`, `tasks.md`, `lessons.md`, `decisions.md`), cada uno con un **índice** al inicio para búsqueda rápida.

### D-003 — Comandos de sesión ejecutan con Sonnet
- **Estado:** Aceptada
- **Fecha:** 2026-06-27
- **Contexto:** La sesión de trabajo corre con Opus, pero los comandos `foda-progress` y `foda-next` son tareas mecánicas (leer estado, actualizar persistencia, commit/push) que no requieren el modelo más potente.
- **Decisión:** Fijar `model: sonnet` en el frontmatter de ambos comandos. Cada slash-command puede declarar su propio modelo sin alterar el modelo de la sesión.
- **Consecuencias:** Ejecución más rápida y económica de los protocolos de inicio/cierre. Si se requiere más capacidad de razonamiento en un comando futuro, se ajusta su frontmatter individualmente.

---

<!--
Plantilla para nuevas decisiones:
### D-XXX — <título>
- **Estado:** Propuesta | Aceptada | Reemplazada por D-YYY
- **Fecha:** YYYY-MM-DD
- **Contexto:** por qué surge la decisión.
- **Decisión:** qué se decidió.
- **Alternativas consideradas:** opciones descartadas y por qué.
- **Consecuencias:** implicaciones.
-->
