# Task Manager

## Objetivo

El Task Manager administra el ciclo de vida de todas las tareas de THE ODIN PROJECT.

Cada tarea posee:

- Identificador único.
- Descripción.
- Prioridad.
- Estado.
- Responsable.
- Fecha de creación.
- Fecha de actualización.
- Resultado.
- Error.
- Metadatos.

## Estados

Los estados disponibles son:

- `PENDING`
- `ANALYZING`
- `PROPOSING`
- `WAITING_APPROVAL`
- `WORKING`
- `TESTING`
- `WAITING_USER`
- `COMPLETED`
- `PAUSED`
- `RESOURCE_LIMIT`
- `ERROR`
- `STOPPED`

## Transiciones

Una tarea solamente puede cambiar a estados permitidos por el sistema.

Esto evita saltos arbitrarios, por ejemplo:

`PENDING → COMPLETED`

no está permitido.

El flujo normal puede ser:

`PENDING → ANALYZING → PROPOSING → WAITING_APPROVAL → WORKING → TESTING → COMPLETED`

Dependiendo del tipo de tarea, algunas etapas pueden omitirse cuando la lógica del sistema lo permita.

## Asignación

Una tarea puede asignarse a:

- Supervisor.
- Worker 1.
- Worker 2.
- Worker 3.
- Worker 4.
- Worker 5.

La asignación queda registrada dentro de la tarea.

## Prioridad

Cada tarea posee una prioridad numérica.

El valor predeterminado es:

`5`

Los valores menores representan mayor prioridad dentro del sistema.

## Resultados

Una tarea puede almacenar un resultado después de su ejecución.

Cuando se registra un resultado correctamente, cualquier error anterior asociado a la tarea se elimina.

## Errores

Los errores se almacenan sin ocultarlos.

Una tarea puede pasar a:

`ERROR`

cuando una operación no puede continuar correctamente.

El Supervisor podrá utilizar esta información para decidir si:

- Reintentar.
- Pausar.
- Solicitar intervención humana.
- Detener la tarea.

## Tareas finalizadas

Una tarea se considera terminada definitivamente cuando está en:

- `COMPLETED`
- `STOPPED`

Las tareas en otros estados pueden seguir requiriendo procesamiento.

## Estado general

El Task Manager puede generar un resumen con:

- Total de tareas.
- Tareas activas.
- Identificadores de tareas activas.
- Tareas completadas.
- Tareas pausadas.
- Tareas detenidas.
- Tareas con errores.
- Tareas bloqueadas por recursos.
- Distribución de tareas por estado.

## Seguridad

El Task Manager no ejecuta directamente acciones externas.

Su responsabilidad es administrar el ciclo de vida de las tareas.

Las acciones sensibles serán controladas posteriormente mediante:

- Permissions.
- Authorization Engine.
- Resource Manager.
- Supervisor.
- Audit Log.

## Integración futura

El Task Manager se integrará posteriormente con:

- Resource Manager.
- Audit Log.
- Permissions.
- Authorization Engine.
- Telegram.
- Supervisor.
- Workers.
- Scheduler.
- GitHub Automation.

## Estado del módulo

M3 está compuesto por:

- Modelo de tareas.
- Estados.
- Transiciones.
- Gestor de tareas.
- Estado general.
- Pruebas automáticas.
- Documentación.

El módulo todavía requiere su checklist final antes de considerarse cerrado.
