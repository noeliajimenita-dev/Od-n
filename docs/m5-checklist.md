# M5 — Checklist del Sistema de Permisos

## Acciones y niveles

- [x] Definir `PermissionLevel`.
- [x] Definir `PermissionAction`.
- [x] Definir permisos predeterminados.
- [x] Identificar acciones que requieren aprobación.
- [x] Identificar acciones denegadas.

## Roles

- [x] Definir Supervisor.
- [x] Definir Worker 1.
- [x] Definir Worker 2.
- [x] Definir Worker 3.
- [x] Definir Worker 4.
- [x] Definir Worker 5.
- [x] Definir System.
- [x] Definir User.
- [x] Gestionar roles desconocidos.

## Verificación

- [x] Implementar `PermissionDecision`.
- [x] Implementar `check_permission()`.
- [x] Detectar acciones permitidas.
- [x] Detectar acciones que requieren aprobación.
- [x] Detectar acciones denegadas.

## Estado

- [x] Crear resumen del sistema de permisos.
- [x] Contabilizar acciones permitidas.
- [x] Contabilizar acciones que requieren aprobación.
- [x] Contabilizar acciones denegadas.

## Pruebas

- [x] Probar acciones permitidas.
- [x] Probar acciones sensibles.
- [x] Probar acciones denegadas.
- [x] Probar roles desconocidos.
- [x] Probar resumen de permisos.

## Documentación

- [x] Documentar niveles de permiso.
- [x] Documentar acciones.
- [x] Documentar roles.
- [x] Documentar `Permission Checker`.
- [x] Documentar la regla de aprobación.

## Seguridad

- [x] Las acciones sensibles no se ejecutan automáticamente.
- [x] Las credenciales no se almacenan en el sistema de permisos.
- [x] Las acciones importantes quedan preparadas para autorización posterior.

## Estado del módulo

M5 — Sistema de Permisos: ESTRUCTURA COMPLETA.

Las autorizaciones reales y el flujo de aprobación del usuario
se implementarán en M6.
