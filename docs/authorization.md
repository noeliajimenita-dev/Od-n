# Sistema de Autorización — THE ODIN PROJECT

## 1. Objetivo

El sistema de autorización gestiona las acciones que requieren
aprobación del usuario antes de poder ejecutarse.

Su función es separar:

- La solicitud de una acción.
- La decisión del usuario.
- La ejecución posterior de la acción.

Una autorización aprobada no ejecuta por sí misma la acción.

---

## 2. Solicitud de autorización

Cada solicitud contiene información como:

- `request_id`
- `action`
- `requester`
- `reason`
- `task_id`
- `created_at`
- `approved`
- `resolved`

El `request_id` identifica de forma única cada solicitud.

---

## 3. Estados

Una solicitud puede encontrarse en tres situaciones principales:

### Pendiente

La solicitud fue creada pero todavía no recibió una decisión.

```text
PENDING
