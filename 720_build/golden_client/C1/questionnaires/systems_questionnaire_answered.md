# Cuestionario técnico (área de sistemas) — respondido (golden client C1)

> **Insumo de prueba** del flujo `010_discovery` (peldaño **L0**). Plano CONSTRUCCIÓN (`D-001`). Simula la
> entrevista al área de sistemas de *Bebidas Andinas S.A.S.*. Coherente con la fuente cruda generada:
> entrega en **CSV**, periodicidad **mensual**, ~36 meses de historia, grain producto×geo declarado.

---

## Entrevistado: Analista de Sistemas / TI

1. **¿Desde cuándo tienen datos históricos de demanda?**
   "Tenemos registros mensuales de los **últimos 36 meses** (3 años) confiables. Antes de eso los datos
   son irregulares y preferimos no usarlos."

2. **¿Qué tan confiable/completa está la información?**
   "Buena en general, pero hay **algunos meses con huecos** (registros faltantes) y de vez en cuando
   **filas duplicadas** por reprocesos del ERP. Nada masivo, pero existe."

3. **¿Cuál es el medio de acceso a los datos?**
   "Exportamos a **archivos CSV** desde el ERP. No damos acceso directo a la base de datos ni tenemos API.
   Podemos entregar un CSV mensual."

4. **¿Qué estructura tienen esos archivos? (columnas)**
   "Cada fila es la **demanda de un producto en un mes** en el centro de distribución. Columnas (con
   nuestros nombres):
   - `periodo` (primer día del mes)
   - `familia`, `categoria`, `subcategoria`, `sku`, `nombre_producto`
   - `region`, `pais`, `ciudad`, `sede`
   - `cantidad_demandada`
   - `precio_unitario_venta`, `costo_unitario_venta`, `costo_inventario`"

5. **¿Un solo archivo o varios?**
   "Un **único archivo** de demanda histórica mensual. (Aparte podemos entregar más adelante los actuals
   recientes para monitoreo.)"

6. **¿Grain / nivel de detalle?**
   - **Producto:** familia → categoría → subcategoría → **SKU** (hoy: 1 familia, 1 categoría, 1
     subcategoría, ~7 SKUs).
   - **Geografía:** región → país → ciudad → **sede** (hoy: 1 sede, CD Bogotá Norte).
   - **Periodicidad:** **mensual**.

7. **¿Volumen?**
   "Pequeño: ~7 SKUs × 1 sede × 36 meses ≈ 250 filas. Crecerá cuando abramos más sedes o SKUs."

---

## Síntesis para Discovery (contrato de datos declarado)
- **Archivos esperados:** 1 CSV de demanda histórica mensual (+ entregas posteriores de actuals para `075`).
- **Medio de acceso:** CSV (no BD directa, no API).
- **Periodicidad de la demanda:** mensual (rige la agregación en `035_derivation`).
- **Grain producto × geografía (`D-014`):** producto (familia→categoría→subcategoría→SKU) × geo
  (región→país→ciudad→sede); hoy en su forma mínima (1×1×1×7 SKU, 1 sede) → **~7 series**.
- **Calidad conocida:** huecos ocasionales y duplicados por reprocesos (a resolver en `030_cleaning`).
- **Parámetros financieros:** vienen **en el mismo archivo** (precio/costo unitario, costo de inventario) →
  los leerá `070_reporting` desde bronze (`D-019`).
