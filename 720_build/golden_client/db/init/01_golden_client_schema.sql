-- 01_golden_client_schema.sql — schema del tenant de prueba C1 (golden client).
-- Corre una sola vez, en la primera init del contenedor (data dir vacío).
--
-- Plano CONSTRUCCIÓN (D-001). Aislamiento schema-per-tenant (D-027): el golden client es un
-- tenant de prueba más dentro de la base `foda`. Aquí solo se crea el CONTENEDOR (schema vacío);
-- las tablas bronze_*/silver_*/gold_* NO se crean aquí: nacen con el DDL de cada celda del
-- Tracer Bullet (020 crea bronze, 030 silver, 035 gold...), porque cada capa es artefacto de su
-- flujo (000_general_process.md). Ver 720_build/golden_client/C1_design.md §2 y §10.

CREATE SCHEMA IF NOT EXISTS golden_client;

COMMENT ON SCHEMA golden_client IS
  'Tenant de prueba C1 del Tracer Bullet (D-012/D-014). Contenedor de bronze_/silver_/gold_, que nacen en las celdas.';
