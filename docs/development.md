# THE ODIN PROJECT — Development Guide

## 1. Development Environment

THE ODIN PROJECT is developed and versioned through GitHub.

The project is designed to run locally during development and later on Oracle Cloud Free Tier for 24/7 execution.

## 2. Repository Rules

The repository must preserve:

- Source code.
- Documentation.
- Tests.
- Version history.
- Backups.
- Configuration templates.

Secrets and credentials must never be committed.

## 3. Branches

Development work should use dedicated branches.

The `main` branch represents the protected stable version.

Changes should be tested before being merged into `main`.

## 4. Changes

Before an important change:

1. Identify the current version.
2. Verify the current state.
3. Create or verify a backup.
4. Create a development branch.
5. Make the changes.
6. Run tests.
7. Review the changes.
8. Compare with the previous version.
9. Request authorization when required.
10. Merge only when authorized.

## 5. Testing

Every important component should have automated tests.

Tests should verify:

- Expected behavior.
- Error handling.
- Permission restrictions.
- Resource limits.
- State recovery.
- Security protections.

A failed critical test must block deployment.

## 6. Configuration

Configuration should be separated from source code.

Sensitive values such as:

- API keys.
- Tokens.
- Passwords.
- Private keys.
- Service credentials.

must be stored using secure environment variables or secret management.

## 7. Resource Safety

AI providers and external services must operate under configured limits.

The system must stop or pause new consumption when a configured safety threshold is reached.

## 8. Deployment

The planned production flow is:

Development
→ Tests
→ Review
→ Authorization
→ Main
→ Deployment
→ Oracle Cloud
→ Health Check

Production deployment must use an authorized version.

## 9. Recovery

If a deployment or update fails:

1. Stop affected operations.
2. Preserve the current state.
3. Record the error.
4. Use the previous valid version when necessary.
5. Restore and test.
6. Report the result.

## 10. Cost Protection

The system must not automatically:

- Activate paid services.
- Upgrade infrastructure.
- Increase billing limits.
- Purchase services.
- Enable paid APIs.

Any action that could create a cost must require the appropriate authorization.

## 11. Development Principle

Build gradually, test each module, preserve previous versions and keep the system recoverable.
