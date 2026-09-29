from .connection_supervisor import TelegramConnectionSupervisor


def build_connection_supervisor_report(
    supervisor: TelegramConnectionSupervisor,
) -> str:
    connected = supervisor.connected_bots()
    disconnected = supervisor.disconnected_bots()

    total = len(connected) + len(disconnected)
    global_status = "ALL_CONNECTED" if supervisor.all_connected() else "CONNECTION_ISSUES"

    lines = [
        "TELEGRAM CONNECTION SUPERVISOR",
        f"Total bots: {total}",
        f"Connected: {len(connected)}",
        f"Disconnected: {len(disconnected)}",
        f"Global status: {global_status}",
    ]

    if connected:
        lines.append(f"Connected bots: {', '.join(connected)}")

    if disconnected:
        lines.append(f"Disconnected bots: {', '.join(disconnected)}")

    return "\n".join(lines)
