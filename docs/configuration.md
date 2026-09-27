# Configuración de THE ODIN PROJECT

## Objetivo

Este documento define cómo se configura THE ODIN PROJECT y cómo se deben gestionar sus variables de entorno y credenciales.

## Variables de entorno

La plantilla principal se encuentra en:

`.env.example`

Las variables reales deben almacenarse únicamente en el entorno de ejecución y nunca directamente en el código fuente.

## Proveedores de IA

THE ODIN PROJECT contempla:

- Gemini como proveedor principal.
- Groq como proveedor complementario.

Las claves correspondientes se cargarán mediante variables de entorno.

## Telegram

Cada bot tendrá su propio token.

Se contempla:

- 1 token para el Supervisor.
- 5 tokens para los Worker Bots.

Los tokens nunca deben aparecer en:

- Código fuente.
- Commits.
- Logs.
- Mensajes de Telegram.
- Capturas de pantalla.
- Documentación pública.

## GitHub

El acceso automatizado a GitHub utilizará una credencial almacenada de forma segura.

El repositorio principal y la rama `main` deben mantenerse protegidos.

## Límites de recursos

La configuración permite establecer:

- Límite diario de tokens.
- Límite mensual de tokens.
- Reserva de seguridad.
- Alertas de consumo.

El sistema debe detener o pausar nuevas tareas cuando se alcance un límite configurado.

## Autorización humana

Las acciones sensibles deben requerir autorización humana.

Esto incluye especialmente:

- Gastos.
- Servicios de pago.
- Publicaciones.
- Entregas definitivas.
- Cambios importantes en producción.
- Uso de credenciales sensibles.
- Acciones externas de alto impacto.

## Oracle Cloud

La configuración de Oracle Cloud se añadirá cuando llegue el módulo correspondiente.

No se deben introducir credenciales de Oracle Cloud durante M1.

## Regla principal

Las credenciales son configuración privada, no código.

THE ODIN PROJECT debe poder ejecutarse sin que ninguna clave secreta esté almacenada dentro del repositorio.
