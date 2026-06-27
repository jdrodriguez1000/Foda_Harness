# Decisions — Motor FODA

> Decisiones de diseño y arquitectura tomadas durante la construcción del motor FODA.
> Registro tipo ADR (Architecture Decision Record) resumido.

---

## Índice
- [D-001 — Dos planos: Motor (FODA) e Instancia (fda)](#d-001--dos-planos-motor-foda-e-instancia-fda)
- [D-002 — Memoria de construcción en 800_persistence/](#d-002--memoria-de-construcción-en-800_persistence)

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
