# Facturas de restaurante

Flama era mi bar de vinos. Al revisar los borradores de IVA encontrábamos errores una y otra vez; en una ocasión, la diferencia fue de cientos de euros. Para poder contrastar el borrador había que procesar todas las facturas de los proveedores y hacer las cuentas por nuestra cuenta.

De ahí salió esta herramienta: pasar facturas en PDF o imagen a datos que se puedan ordenar, revisar y comparar. El script original usa un modelo con visión; los ensayos posteriores exploraron OCR y comparación con registros de compras.

**Estado: exploración histórica.** Los datos extraídos requieren revisión contra el documento original.

## Qué hay acá

- `process_invoices.py`: la primera implementación, con configuración externa y conexiones a Azure y Google Sheets.
- `ejemplos/facturas-ficticias.csv`: datos inventados para ilustrar las columnas, sin documentos ni cifras de un negocio real.
- `.gitignore`: exclusión de configuración, credenciales y documentos de trabajo.

La configuración y las credenciales no se distribuyen. El script original necesita adaptar el entorno y sus servicios antes de usarse.

## Qué sigue abierto

Cómo señalar extracciones dudosas, volver a la factura y conservar correcciones al comparar información.

[La exploración completa](https://tomasrene.com/experimentos/restaurantes) · [Catálogo de exploraciones](https://github.com/tomasrene/exploraciones)

Nombre anterior: `flama-facturas`. Se conserva la historia. El resumen de ventas que estaba en la rama principal se retiró de esa versión; los commits anteriores aún lo contienen.
