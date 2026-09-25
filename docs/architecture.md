# THE ODIN PROJECT — Architecture

## 1. Overview

THE ODIN PROJECT is a modular AI-agent system composed of one Supervisor and five specialized Worker Bots.

The system is designed to operate with centralized control, resource limits, permissions, backups, testing and human authorization for sensitive actions.

## 2. Main Components

### Supervisor

The Supervisor coordinates the entire system.

Responsibilities:

- Receive and interpret tasks.
- Create and assign tasks.
- Coordinate Worker Bots.
- Review results.
- Control permissions.
- Control resource consumption.
- Manage backups.
- Coordinate GitHub operations.
- Detect errors.
- Request human authorization when required.
- Report system status through Telegram.

### Worker Bots

There are five Worker Bots.

Each Worker Bot performs specialized tasks assigned by the Supervisor.

Workers must:

- Follow assigned permissions.
- Respect resource limits.
- Preserve task state.
- Report errors.
- Run required tests.
- Never perform restricted actions without authorization.

## 3. Telegram

The system uses six Telegram chats:

- Bot 1
- Bot 2
- Bot 3
- Bot 4
- Bot 5
- Supervisor

Telegram is used as the control and communication interface.

The system must support commands such as:

- STATUS
- STOP ALL
- PAUSE
- RESUME
- REDO
- APPROVE
- REJECT

## 4. GitHub

GitHub is the central repository for:

- Source code.
- Documentation.
- Tests.
- Version history.
- Branches.
- Backups and version references.
- Authorized deployment workflows.

The main branch must remain protected.

Development should normally occur on separate branches.

## 5. Oracle Cloud

Oracle Cloud Free Tier is the planned environment for 24/7 execution.

Oracle Cloud is intended to run the actual ODIN application.

GitHub stores and versions the code; Oracle Cloud executes the authorized version.

The system must not automatically activate paid infrastructure or services.

## 6. AI Providers

Gemini is the primary AI provider.

Groq is a complementary provider.

API credentials must never be stored directly in source code.

Credentials will be provided through secure environment variables or secret-management mechanisms.

## 7. Resource Management

The Resource Manager controls AI resource consumption.

It must support:

- Daily limits.
- Monthly limits.
- Per-bot limits.
- Per-task limits.
- Per-model limits.
- Safety reserves.
- Usage tracking.
- Resource warnings.
- Automatic task pausing when configured limits are reached.

## 8. Task Management

Tasks have controlled states.

Example lifecycle:

IDLE
→ WORKING
→ TESTING
→ COMPLETED

Error lifecycle:

WORKING
→ ERROR
→ PAUSED

Task state must remain recoverable after an application restart.

## 9. Permissions

The system uses permission levels to restrict sensitive operations.

Sensitive actions include:

- Spending money.
- Using paid services.
- Changing credentials.
- Changing sensitive permissions.
- Publishing applications.
- Delivering client work.
- Important external actions.
- Protected production changes.

These actions require human authorization when configured as restricted.

## 10. Backup and Recovery

Before important modifications:

1. Identify the current version.
2. Verify the existing version.
3. Create or verify a backup.
4. Create a version/tag when appropriate.
5. Make changes on a controlled branch.
6. Run tests.
7. Compare versions.
8. Keep the previous version available.

The system must remain recoverable after errors.

## 11. Security Principles

- Never expose API keys.
- Never hardcode credentials.
- Never disable security protections automatically.
- Never delete all backups.
- Never delete audit records automatically.
- Never bypass authorization requirements.
- Use minimum required permissions.
- Preserve version history.

## 12. Deployment Flow

The planned deployment flow is:

GitHub
→ authorized version
→ automated checks
→ secure deployment
→ Oracle Cloud
→ restart ODIN
→ health check
→ Telegram status report

Only authorized versions should reach the production environment.

## 13. Human Authority

The user remains the final authority over sensitive actions.

The system may prepare, analyze and request authorization, but restricted actions must not be executed without the required approval.

## 14. Design Principle

Autonomy for work, human authorization for sensitive actions.
