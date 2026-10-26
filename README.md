# Facturas de restaurante

Pruebas para pasar de facturas en PDF o imagen a datos que se puedan revisar y comparar. El caso de origen es **Flama**.

El script convierte una página del PDF a imagen, solicita una extracción estructurada a un modelo con visión y prepara datos para una planilla. Los ensayos posteriores exploraron OCR y comparación con registros de compras.

**Estado: exploración histórica.** La extracción requiere revisión contra el documento original. Este repositorio no constituye un sistema contable integrado.

## Qué hay acá

- `process_invoices.py`: la primera implementación, con configuración externa y conexiones a Azure y Google Sheets.
- `ejemplos/facturas-ficticias.csv`: datos inventados para ilustrar las columnas, sin documentos ni cifras de un negocio real.
- `.gitignore`: exclusión de configuración, credenciales y documentos de trabajo.

La configuración y las credenciales no se distribuyen. El script original necesita adaptar el entorno y sus servicios antes de usarse.

## Qué sigue abierto

Cómo señalar extracciones dudosas, volver a la factura y conservar correcciones al comparar información.

[La exploración completa](https://tomasrene.com/experimentos/restaurantes) · [Catálogo de exploraciones](https://github.com/tomasrene/exploraciones)

Nombre anterior: `flama-facturas`. Se conserva la historia. El resumen de ventas que estaba en la rama principal se retiró de esa versión; los commits anteriores aún lo contienen.
