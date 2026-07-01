# Cuestionario de negocio — respondido (golden client C1)

> **Insumo de prueba** del flujo `010_discovery` en su peldaño **L0** (sin intake en vivo: se parte de
> este cuestionario **ya respondido**). Plano CONSTRUCCIÓN (`D-001`); simula las respuestas de una empresa
> ficticia. Coherente con la fuente cruda generada (`generator/generate_c1.py`): periodicidad mensual,
> grain producto×geo superficial, estacionalidad de diciembre.
>
> **Empresa simulada:** *Bebidas Andinas S.A.S.* — distribuidor de gaseosas y aguas, un centro de
> distribución. **≥3 stakeholders de áreas distintas** (planeación, comercial, logística).

---

## Datos de la empresa
- **Razón social:** Bebidas Andinas S.A.S.
- **Sector:** Distribución de bebidas no alcohólicas (gaseosas, agua con gas).
- **Cobertura geográfica:** 1 centro de distribución — *CD Bogotá Norte* (Bogotá, Colombia, región Andina).
- **Portafolio:** una familia (*Bebidas*), categoría *Bebidas no alcohólicas*, subcategoría *Gaseosas*,
  ~7 SKUs activos (colas, naranja, limón, uva, agua con gas; presentaciones 350ml / 500ml / 1.5L).

---

## Stakeholder 1 — Jefa de Planeación de Demanda (área: Planeación)

1. **¿Qué problema de planeación quieren resolver?**
   "Hoy planeamos la compra y el inventario 'a ojo', con promedios simples de los últimos meses. Nos
   quedamos cortos en temporada alta y sobra producto en temporada baja. Queremos un **pronóstico de
   demanda por SKU y por mes** confiable para los próximos meses."

2. **¿Con qué anticipación necesitan el pronóstico?**
   "Mensual, con un horizonte de al menos **6 meses** hacia adelante."

3. **¿Cómo se comporta la demanda a lo largo del año?**
   "Sube fuerte en **diciembre** (fiestas) y cae en **enero y febrero**. El resto del año es más plano,
   con un leve repunte a mitad de año."

4. **¿Qué impacto tiene equivocarse?**
   "Agotados en diciembre = ventas perdidas. Exceso en enero = costo de inventario y producto cerca de
   vencer."

## Stakeholder 2 — Gerente Comercial (área: Comercial / Ventas)

1. **¿Qué mueve las ventas además de la temporada?**
   "Las **promociones** de fin de año y los eventos. Bajar el precio mueve volumen, sobre todo en las
   presentaciones grandes (1.5L)."

2. **¿Los productos se comportan igual entre sí?**
   "No. La **cola 350ml** es la de mayor rotación; la **uva** es de nicho, mucho menor volumen. El **agua
   con gas** viene creciendo."

3. **¿Hipótesis de negocio que les gustaría validar?**
   "Que el pico de diciembre justifica **acumular inventario** desde octubre-noviembre, y que una baja de
   precio del 5% en temporada aumenta la demanda de forma material."

## Stakeholder 3 — Coordinador de Logística / Inventarios (área: Logística)

1. **¿Qué necesitan del pronóstico para operar?**
   "Saber cuánto pedir por SKU cada mes para no quedarnos cortos ni llenar la bodega. Manejamos un
   **lead time** de reposición de proveedores de varias semanas."

2. **¿Costos relevantes?**
   "El **costo de mantener inventario** (bodega, capital, merma) y el **costo de oportunidad** cuando nos
   agotamos. Cada SKU tiene su **precio de venta** y su **costo unitario**."

3. **¿Qué tan estacional es la operación de bodega?**
   "Muy marcada por diciembre; en enero-febrero sobra espacio."

---

## Síntesis para Discovery (lo que el flujo debe capturar)
- **Problema:** pronóstico de demanda mensual por SKU, horizonte ≥6 meses, para planear compra e inventario.
- **Hipótesis de comportamiento (testeable en `040_exploration`):**
  - H1: la demanda **sube en diciembre** y **baja en enero-febrero** (estacionalidad anual).
  - H2: existe **heterogeneidad entre SKUs** (cola 350ml alta rotación; uva de nicho).
  - H3: una **baja de precio** en temporada incrementa la demanda (base para un escenario what-if en `065`).
- **Cobertura de áreas:** Planeación, Comercial, Logística (3 áreas distintas — cumple el mínimo de `010`).
