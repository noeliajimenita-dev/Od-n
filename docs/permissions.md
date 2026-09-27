# Sistema de Permisos — THE ODIN PROJECT

## 1. Objetivo

El sistema de permisos controla qué acciones pueden realizar
el Supervisor, los Worker Bots y otros componentes del sistema.

Su objetivo es evitar que una acción sensible se ejecute sin
la autorización correspondiente.

---

## 2. Niveles de permiso

El sistema utiliza tres niveles:

### ALLOWED

La acción puede ejecutarse directamente si el componente
también tiene acceso a los recursos necesarios.

### REQUIRES_APPROVAL

La acción está disponible, pero necesita autorización antes
de ejecutarse.

Ejemplos:

- Fusionar cambios en `main`.
- Publicar.
- Entregar un trabajo a un cliente.
- Gastar dinero.
- Añadir o modificar credenciales.
- Desplegar en producción.
- Ejecutar acciones externas sensibles.

### DENIED

La acción no está permitida para ese rol.

---

## 3. Acciones

Las acciones controladas incluyen:

- `READ_CODE`
- `READ_DOCUMENTATION`
- `ANALYZE_TASK`
- `CREATE_TASK`
- `ASSIGN_TASK`
- `CREATE_BRANCH`
- `MODIFY_CODE`
- `RUN_TESTS`
- `CREATE_BACKUP`
- `USE_AI_PROVIDER`
- `USE_RESOURCE`
- `MERGE_MAIN`
- `DELETE_CODE`
- `DELETE_BACKUP`
- `PUBLISH`
- `DELIVER_TO_CLIENT`
- `SPEND_MONEY`
- `ADD_CREDENTIAL`
- `CHANGE_CREDENTIAL`
- `DEPLOY_PRODUCTION`
- `EXECUTE_EXTERNAL_ACTION`

---

## 4. Regla principal

Una acción marcada como `REQUIRES_APPROVAL` no se considera
autorizada automáticamente.

El sistema debe detenerse y solicitar la autorización
correspondiente antes de ejecutarla.

Esto es especialmente importante para:

- Dinero.
- Credenciales.
- Publicaciones.
- Entregas.
- Producción.
- Cambios importantes en `main`.
- Acciones externas sensibles.

---

## 5. Permission Checker

El archivo:

`src/permissions/checker.py`

proporciona la función:

`check_permission(role, action)`

Esta función devuelve un `PermissionDecision` con:

- `role`
- `action`
- `level`
- `allowed`
- `requires_approval`

Ejemplo conceptual:

```text
worker_1 + READ_CODE
        ↓
     ALLOWED
        ↓
   puede continuar
