# Integración de Telegram — THE ODIN PROJECT

## 1. Objetivo

El módulo M7 prepara la comunicación entre THE ODIN PROJECT
y Telegram.

El sistema tendrá seis bots:

- Supervisor
- Worker 1
- Worker 2
- Worker 3
- Worker 4
- Worker 5

Cada bot tendrá su propio chat de Telegram.

---

## 2. Arquitectura

```text
                    TELEGRAM
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   Supervisor       Worker 1        Worker 2
        │
        ├────────── Worker 3
        ├────────── Worker 4
        └────────── Worker 5
