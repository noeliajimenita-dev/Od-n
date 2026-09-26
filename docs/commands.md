# THE ODIN PROJECT — Control Commands

## 1. STATUS

Command:

STATUS

Purpose:

Show the current state of THE ODIN PROJECT.

The status should include, when available:

- Supervisor state
- Worker states
- Active tasks
- Pending approvals
- Resource usage
- Provider status
- Server status
- Errors
- Current versions

Example:

SYSTEM STATUS

Supervisor: ACTIVE
Workers: 5/5
Active Tasks: 2
Pending Approvals: 1
Errors: 0

Gemini:
Used Today: 0
Remaining: CONFIGURED LIMIT
Status: AVAILABLE

Groq:
Used Today: 0
Remaining: CONFIGURED LIMIT
Status: AVAILABLE

Server:
Status: NOT CONFIGURED

## 2. STOP ALL

Command:

STOP ALL

Purpose:

Immediately place the system into an emergency stopped state.

Expected behavior:

- Pause all workers.
- Stop new tasks.
- Stop new applications.
- Stop restricted external actions.
- Stop new deliveries.
- Preserve backups.
- Preserve task state.
- Record the event.
- Report active tasks.

The command must not delete data.

## 3. PAUSE

Command:

PAUSE

Purpose:

Temporarily pause normal operations.

Expected behavior:

- Stop starting new non-urgent tasks.
- Preserve current state.
- Preserve active task information.
- Wait for a resume command.

## 4. RESUME

Commands:

RESUME

BACK TO NORMAL

Purpose:

Return the system to normal operation after a pause.

Expected behavior:

- Restore permitted operations.
- Preserve previously configured limits.
- Resume pending tasks according to their stored state.

## 5. REDO

Commands:

REDO

REWORK

Purpose:

Request that an eligible task be performed again.

Expected behavior:

- Identify the target task.
- Preserve the previous result.
- Create a new execution attempt.
- Record the reason.
- Respect resource and permission limits.

## 6. APPROVAL

Examples:

APPROVED

GENEHMIGT

Purpose:

Authorize a previously requested restricted action.

Expected behavior:

- Verify that a matching authorization request exists.
- Mark the request as approved.
- Record the authorization.
- Allow the authorized action to continue.

## 7. REJECTION

Examples:

REJECTED

DECLINED

ABGELEHNT

Purpose:

Reject a pending authorization request.

Expected behavior:

- Mark the request as rejected.
- Prevent the restricted action.
- Preserve the request in the audit record.

## 8. Unknown Commands

Unknown or ambiguous commands must not trigger sensitive actions.

The system should:

1. Report that the command was not recognized.
2. Request clarification when appropriate.
3. Keep the current safety state unchanged.

## 9. Command Security

Commands that control sensitive operations must be validated before execution.

The system must not execute a command solely because similar text appears inside an unrelated message.

## 10. Command Logging

Important commands should be recorded with:

- Date and time
- Sender
- Command
- Target
- Previous state
- New state
- Result

## 11. Core Rule

Control commands must change system state only through the authorized control layer.

Workers must not bypass the Supervisor or security mechanisms to execute restricted commands.
