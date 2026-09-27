# Audit Log

## Objetivo

El Audit Log registra las acciones importantes realizadas dentro de THE ODIN PROJECT para mantener trazabilidad, seguridad y capacidad de revisión.

Cada evento debe permitir responder:

- Quién realizó la acción.
- Qué acción realizó.
- Por qué se realizó.
- Cuándo ocurrió.
- Cuál fue el resultado.
- Qué tarea estaba relacionada.
- Qué versión estaba involucrada.
- Si existió autorización.
- Cuántos tokens se utilizaron.
- Qué archivos fueron modificados.
- Si ocurrió un error.

## Estructura del evento

Cada `AuditEvent` contiene:

- `event_id`
- `actor`
- `action`
- `reason`
- `result`
- `timestamp`
- `task_id`
- `version`
- `authorization_id`
- `tokens_used`
- `files_changed`
- `error`
- `metadata`

## Actores

Los eventos pueden proceder de:

- `supervisor`
- `worker_1`
- `worker_2`
- `worker_3`
- `worker_4`
- `worker_5`
- `system`
- `user`

Los actores representan el origen de la acción y no otorgan permisos por sí mismos.

## Acciones

Ejemplos de acciones que podrán registrarse:

- Creación de tareas.
- Asignación de tareas.
- Cambios de estado.
- Modificaciones de código.
- Ejecución de pruebas.
- Creación de backups.
- Restauraciones.
- Solicitudes de autorización.
- Aprobaciones.
- Rechazos.
- Uso de recursos.
- Errores.
- Acciones externas autorizadas.

## Resultados

Los resultados deben indicar claramente el resultado de la operación.

Ejemplos:

- `SUCCESS`
- `FAILED`
- `DENIED`
- `CANCELLED`
- `PAUSED`

## Validación

Un evento debe contener como mínimo:

- Identificador.
- Actor.
- Acción.
- Motivo.
- Resultado.

Los tokens utilizados no pueden ser negativos.

Los eventos inválidos no deben registrarse.

Los identificadores de eventos deben ser únicos dentro del registro.

## Inmutabilidad

El sistema está diseñado para conservar la trazabilidad.

Los eventos registrados no deben modificarse para ocultar acciones anteriores.

La persistencia y protección contra alteraciones se implementarán posteriormente.

## Información sensible

El Audit Log nunca debe almacenar:

- API keys.
- Tokens de Telegram.
- Contraseñas.
- Claves privadas.
- Credenciales completas.
- Secretos de servicios externos.

Si una acción utiliza una credencial, el registro debe guardar únicamente información segura sobre la acción realizada.

## Privacidad y seguridad

Los registros deben contener solamente la información necesaria para auditoría.

No deben utilizarse para exponer secretos mediante:

- Telegram.
- Logs públicos.
- Mensajes de error.
- Repositorios.
- Capturas de pantalla.

## Estado general

El sistema puede generar estadísticas sobre:

- Número total de eventos.
- Eventos con errores.
- Eventos relacionados con tareas.
- Actores.
- Acciones.
- Resultados.

Estas estadísticas sirven para supervisión y diagnóstico.

## Integraciones futuras

El Audit Log se integrará posteriormente con:

- Task Manager.
- Resource Manager.
- Permissions.
- Authorization Engine.
- Supervisor.
- Telegram.
- GitHub Automation.
- Backup / Restore.
- Oracle Cloud.

## Seguridad administrativa

Las operaciones sensibles sobre los registros deberán estar protegidas mediante el sistema de permisos y autorización.

La capacidad de auditar no debe depender únicamente de la confianza en un worker.

El Supervisor tampoco debe poder eliminar sus propias protecciones para ocultar una acción.

## Estado del módulo

M4 incluye actualmente:

- Modelo `AuditEvent`.
- `AuditLogger`.
- Estado del Audit Log.
- Pruebas automáticas.
- Validación.
- Documentación.

La persistencia permanente y las protecciones avanzadas se implementarán en módulos posteriores.
