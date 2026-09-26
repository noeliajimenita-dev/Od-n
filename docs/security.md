# THE ODIN PROJECT — Security Rules

## 1. General Security

THE ODIN PROJECT must operate with security protections enabled by default.

The system must prioritize:

1. Safety
2. Credential protection
3. Permission control
4. Resource protection
5. Backup and recovery
6. Auditability

## 2. Credentials

The following must never be stored directly in source code:

- API keys
- Telegram tokens
- GitHub tokens
- Passwords
- Private keys
- Cloud credentials
- Other authentication secrets

Credentials must be provided through secure environment variables, GitHub Secrets or an appropriate secret-management system.

Credentials must never be intentionally displayed in:

- Source code
- Commits
- Logs
- Telegram messages
- Error reports
- Screenshots

## 3. Minimum Permissions

Each component should receive only the permissions required for its task.

Workers must not receive unnecessary administrative permissions.

The Supervisor must not be able to remove its own security protections.

## 4. Protected Actions

The following actions require human authorization when configured as restricted:

- Spending money
- Activating paid services
- Buying services
- Changing credentials
- Changing sensitive permissions
- Publishing applications
- Delivering client work
- Important external actions
- Protected production changes
- Merging protected production code

## 5. Backups

The system must maintain recoverable previous versions.

The Supervisor must not:

- Delete all backups.
- Remove the only recovery mechanism.
- Hide important changes.
- Delete audit records to conceal actions.

## 6. GitHub Protection

The stable `main` branch should remain protected.

Development should normally occur on separate branches.

The system must not automatically:

- Delete the repository.
- Disable branch protection.
- Delete version history.
- Rewrite history to hide changes.

## 7. Audit

Important actions should be recorded with information such as:

- Date and time
- Component or bot
- Action
- Reason
- Result
- Resource usage
- Files modified
- Previous version
- New version
- Authorization status
- Errors

Audit records should remain recoverable.

## 8. Resource Protection

AI providers and external services must operate under configured limits.

When a safety reserve or configured limit is reached:

1. Stop new consumption.
2. Pause the affected operation.
3. Save the current state.
4. Notify the Supervisor.
5. Notify the user when required.
6. Wait for reset or authorization.

## 9. Emergency Stop

The system must support a global emergency stop command.

`STOP ALL` should:

- Pause all bots.
- Stop new tasks.
- Stop new applications.
- Stop pending restricted external actions.
- Stop new deliveries.
- Preserve backups.
- Save current state.
- Report active tasks.

It must not delete data.

## 10. Recovery

Security protections must remain available after:

- Application restart
- Server restart
- Deployment
- Worker failure
- Temporary provider failure

The system should preserve enough state to resume safely.

## 11. Security Principle

THE ODIN PROJECT follows the principle:

"Autonomy for work, human authorization for sensitive actions."

Security protections must remain active even when the system is operating autonomously.
