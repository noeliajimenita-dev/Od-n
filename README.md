# THE ODIN PROJECT

Sistema modular de agentes de IA con un Supervisor central, 5 bots especializados, Telegram, GitHub y ejecución 24/7.

## Objetivo

Construir un sistema de agentes de IA modular, seguro y controlado, capaz de coordinar tareas, desarrollar software, analizar trabajos, administrar recursos y ejecutar tareas autorizadas.

## Arquitectura

- 1 Supervisor
- 5 Worker Bots
- 6 chats de Telegram
- Gemini como modelo principal
- Groq como proveedor complementario
- GitHub para código, versiones y backups
- Oracle Cloud Free Tier como entorno previsto para ejecución 24/7

## Principios

- Autonomía para trabajar, autorización humana para acciones sensibles.
- No gastar dinero sin autorización.
- No exponer credenciales.
- No modificar main directamente.
- Mantener backups.
- Registrar acciones importantes.
- Controlar el consumo de recursos.
- Detener tareas cuando alcancen límites configurados.
- Mantener el sistema recuperable ante errores.

## Módulos

- M0 — Repositorio y documentación
- M1 — Configuración y secretos
- M2 — Resource Manager
- M3 — Task Manager y estados
- M4 — Audit Log
- M5 — Permissions
- M6 — Authorization Engine
- M7 — Telegram
- M8 — Supervisor
- M9 — Worker 1
- M10 — GitHub Automation
- M11 — Backup / Restore
- M12 — Testing / Quality
- M13 — APK Builder
- M14 — Update Workflow
- M15 — Oracle Cloud 24/7
- M16 — Deployment
- M17 — Recovery
- M18 — Workers 2–5
- M19 — Scheduler
- M20 — Platform Adapters
- M21 — Applications
- M22 — Contracted Jobs
- M23 — Security Audit
- M24 — Cost Audit
- M25 — Full Integration Test
- M26 — Operational System

## Criterios generales

Cada módulo debe tener:

1. Objetivo definido.
2. Código versionable en GitHub.
3. Pruebas verificables.
4. Manejo de errores.
5. Persistencia cuando sea necesaria.
6. Integración con los módulos anteriores.
7. Protección de credenciales.
8. Ninguna acción sensible sin autorización.

## Estado actual

M0 — EN CONSTRUCCIÓN

## Próximo módulo

M1 — Configuración y secretos
