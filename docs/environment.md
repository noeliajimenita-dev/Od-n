# Entornos de THE ODIN PROJECT

## Objetivo

THE ODIN PROJECT utilizará diferentes entornos para separar el desarrollo, las pruebas y la ejecución real del sistema.

## Entornos

### Development

Entorno utilizado durante la construcción del proyecto.

Características:

- Permite desarrollar nuevos módulos.
- Permite realizar pruebas locales.
- No debe utilizarse para acciones reales sensibles.
- No requiere credenciales reales durante las primeras etapas.

Variable:

`APP_ENV=development`

### Testing

Entorno destinado a pruebas automáticas y validaciones.

Características:

- Ejecuta pruebas del sistema.
- Utiliza configuraciones controladas.
- No debe realizar acciones externas reales.
- No debe utilizar credenciales de producción.

Variable:

`APP_ENV=testing`

### Production

Entorno destinado al sistema operativo real.

Características:

- Se utilizará cuando el sistema esté suficientemente probado.
- Las credenciales deberán almacenarse de forma segura.
- Las acciones sensibles permanecerán protegidas.
- El sistema deberá mantener auditoría, backups y límites de recursos.

Variable:

`APP_ENV=production`

## Regla de seguridad

Nunca se deben utilizar credenciales de producción durante pruebas innecesarias.

## Transición entre entornos

El flujo previsto es:

Development
→ Testing
→ Validación
→ Production

Una nueva versión no debe pasar directamente a producción sin las comprobaciones correspondientes.

## Oracle Cloud

Oracle Cloud será considerado posteriormente como entorno de ejecución 24/7.

Su configuración pertenece a módulos posteriores y no debe añadirse durante M1.

## Principio

Cada entorno debe estar claramente identificado para evitar ejecutar accidentalmente acciones reales desde un entorno de desarrollo o pruebas.
