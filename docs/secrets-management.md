# Gestión de secretos

## Objetivo

THE ODIN PROJECT debe mantener todas las credenciales fuera del código fuente y del historial público del repositorio.

## Secretos incluidos

Entre los secretos que podrán utilizarse se encuentran:

- Claves de proveedores de IA.
- Tokens de Telegram.
- Credenciales de GitHub.
- Credenciales de servicios externos.
- Credenciales futuras de infraestructura.

## Reglas obligatorias

Los secretos nunca deben:

- Escribirse directamente en archivos `.py`.
- Subirse al repositorio.
- Incluirse en commits.
- Aparecer en logs.
- Enviarse por Telegram.
- Incluirse en capturas de pantalla.
- Mostrarse en mensajes de error.

## Variables de entorno

La aplicación debe obtener los secretos mediante variables de entorno.

El archivo `.env.example` contiene únicamente nombres y ejemplos de configuración.

El archivo `.env` real está protegido mediante `.gitignore`.

## GitHub

Cuando se necesite una credencial para automatización, deberá almacenarse mediante un mecanismo seguro como Secrets, evitando incluirla directamente en el código.

## Rotación

Si una credencial se expone accidentalmente:

1. Detener el uso de la credencial.
2. Revocar o reemplazar la credencial.
3. Revisar dónde fue expuesta.
4. Eliminar la exposición cuando sea posible.
5. Registrar el incidente.
6. Volver a configurar el secreto de forma segura.
7. Verificar que el sistema funcione correctamente.

## Principio de mínimo privilegio

Cada credencial debe tener únicamente los permisos necesarios para realizar su función.

No se deben utilizar credenciales con permisos innecesarios.

## Regla principal

Una credencial debe considerarse información privada.

El sistema debe funcionar sin revelar nunca el valor de un secreto.
