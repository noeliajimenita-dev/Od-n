# M6 — Checklist del Sistema de Autorización

## Solicitudes

- [x] Crear `AuthorizationRequest`.
- [x] Generar identificador único.
- [x] Registrar acción solicitada.
- [x] Registrar solicitante.
- [x] Registrar motivo.
- [x] Asociar una tarea opcional.
- [x] Registrar fecha de creación.
- [x] Mantener estado de resolución.

## Gestión

- [x] Crear `AuthorizationManager`.
- [x] Crear solicitudes.
- [x] Consultar solicitudes.
- [x] Obtener todas las solicitudes.
- [x] Obtener solicitudes pendientes.
- [x] Aprobar solicitudes.
- [x] Rechazar solicitudes.
- [x] Contabilizar solicitudes.
- [x] Contabilizar solicitudes pendientes.

## Seguridad

- [x] Una solicitud pendiente puede aprobarse.
- [x] Una solicitud pendiente puede rechazarse.
- [x] Una solicitud resuelta no puede aprobarse nuevamente.
- [x] Una solicitud resuelta no puede rechazarse nuevamente.
- [x] Las solicitudes no almacenan credenciales.
- [x] La autorización no ejecuta automáticamente la acción.

## Estado

- [x] Crear resumen de autorizaciones.
- [x] Contabilizar solicitudes pendientes.
- [x] Contabilizar solicitudes aprobadas.
- [x] Contabilizar solicitudes rechazadas.

## Pruebas

- [x] Probar creación de solicitudes.
- [x] Probar solicitudes pendientes.
- [x] Probar aprobación.
- [x] Probar rechazo.
- [x] Probar solicitudes desconocidas.
- [x] Probar solicitudes ya resueltas.
- [x] Probar resumen de autorizaciones.

## Documentación

- [x] Documentar el sistema de autorización.
- [x] Documentar el flujo de aprobación.
- [x] Documentar acciones sensibles.
- [x] Documentar la autoridad del usuario.
- [x] Documentar las reglas de seguridad.

## Estado del módulo

M6 — Authorization Engine: ESTRUCTURA COMPLETA.

Las integraciones con Telegram y los modelos de IA se
implementarán en módulos posteriores.
