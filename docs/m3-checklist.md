# M3 — Task Manager Checklist

## Objetivo

Verificar que el Task Manager pueda administrar de forma segura el ciclo de vida de las tareas antes de integrarlo con los módulos posteriores.

## Estructura

- [x] `src/task_manager/__init__.py`
- [x] `src/task_manager/states.py`
- [x] `src/task_manager/task.py`
- [x] `src/task_manager/manager.py`
- [x] `src/task_manager/status.py`

## Estados

- [x] `PENDING`
- [x] `ANALYZING`
- [x] `PROPOSING`
- [x] `WAITING_APPROVAL`
- [x] `WORKING`
- [x] `TESTING`
- [x] `WAITING_USER`
- [x] `COMPLETED`
- [x] `PAUSED`
- [x] `RESOURCE_LIMIT`
- [x] `ERROR`
- [x] `STOPPED`

## Funciones

- [x] Crear tareas.
- [x] Generar identificadores únicos.
- [x] Definir prioridad.
- [x] Consultar tareas.
- [x] Obtener todas las tareas.
- [x] Asignar tareas a workers.
- [x] Controlar transiciones.
- [x] Guardar resultados.
- [x] Registrar errores.
- [x] Eliminar tareas.
- [x] Contabilizar tareas.
- [x] Generar estado general.

## Seguridad

- [x] Rechazar identificadores vacíos.
- [x] Rechazar descripciones vacías.
- [x] Rechazar prioridades inválidas.
- [x] Rechazar tareas duplicadas.
- [x] Rechazar responsables vacíos.
- [x] Rechazar transiciones no permitidas.
- [x] Generar error cuando una tarea no existe.
- [x] No almacenar credenciales.
- [x] No ejecutar acciones externas directamente.

## Pruebas

- [x] Pruebas del modelo `Task`.
- [x] Pruebas del `TaskManager`.
- [x] Pruebas del estado general.
- [x] Pruebas de estados.
- [x] Pruebas de transiciones.
- [x] Pruebas de errores.
- [x] Pruebas de tareas finalizadas.

## Documentación

- [x] Documentación del Task Manager.
- [x] Estados documentados.
- [x] Transiciones documentadas.
- [x] Integraciones futuras documentadas.

## Integración pendiente

El módulo todavía debe conectarse posteriormente con:

- [ ] Resource Manager.
- [ ] Audit Log.
- [ ] Permissions.
- [ ] Authorization Engine.
- [ ] Telegram.
- [ ] Supervisor.
- [ ] Workers.
- [ ] Scheduler.

Estas integraciones pertenecen a módulos posteriores.

## API y credenciales

- [x] No requiere API keys.
- [x] No requiere tokens de Telegram.
- [x] No requiere credenciales de GitHub.
- [x] No requiere credenciales de Oracle Cloud.

## Criterio de cierre

M3 puede considerarse estructuralmente completo cuando:

1. El código esté guardado en GitHub.
2. Las pruebas automáticas pasen correctamente.
3. Las transiciones sean respetadas.
4. Los errores sean controlados.
5. La documentación esté actualizada.
6. No existan credenciales dentro del código.
7. Las integraciones futuras permanezcan separadas de este módulo.

## Próximo módulo

M4 — Audit Log
