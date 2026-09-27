# M2 — Resource Manager

## Objetivo

El Resource Manager controla el consumo de recursos de THE ODIN PROJECT para evitar que una tarea utilice más recursos de los permitidos.

## Recursos principales

El sistema podrá controlar:

- Tokens de modelos de IA.
- Límites diarios.
- Límites mensuales.
- Consumo por tarea.
- Consumo por bot.
- Consumo por proveedor.
- Reserva de seguridad.

## Proveedores

Los proveedores previstos son:

- Gemini como proveedor principal.
- Groq como proveedor complementario.

La conexión real con estos proveedores se realizará posteriormente.

## Límites

Cada recurso puede tener:

- Límite diario.
- Límite mensual.
- Reserva de seguridad.

El sistema no debe utilizar la reserva de seguridad para tareas normales.

## Alertas

El Resource Manager contempla alertas en:

- 50%.
- 75%.
- 90%.
- 100%.

Estas alertas permitirán informar al Supervisor sobre el consumo.

## Protección

Cuando un límite sea alcanzado:

1. No se deben iniciar nuevas tareas que requieran ese recurso.
2. Las tareas activas deben manejarse de forma segura.
3. El Supervisor debe recibir el estado correspondiente.
4. El sistema debe conservar el registro del consumo.
5. No se debe cambiar el límite automáticamente para continuar trabajando.

## Reserva de seguridad

La reserva existe para evitar que el sistema consuma todos los recursos disponibles.

Ejemplo:

Si el límite es de 1000 tokens y la reserva es del 10%:

- Límite: 1000.
- Reserva: 100.
- Presupuesto utilizable: 900.

## Consumo

Antes de ejecutar una tarea se debe comprobar si existe presupuesto suficiente.

Después de utilizar recursos, el consumo debe registrarse.

## Errores

El Resource Manager debe rechazar valores inválidos como:

- Consumo negativo.
- Límites negativos.
- Reservas superiores al 100%.

## Seguridad

El Resource Manager no debe:

- Crear gastos automáticamente.
- Cambiar límites para evitar una restricción.
- Ocultar consumo.
- Ignorar la reserva de seguridad.
- Revelar credenciales.

## Próxima integración

En módulos posteriores se añadirá:

- Consumo real de Gemini.
- Consumo real de Groq.
- Seguimiento por bot.
- Seguimiento por tarea.
- Persistencia del consumo.
- Alertas mediante Telegram.
- Pausa automática al alcanzar límites.
