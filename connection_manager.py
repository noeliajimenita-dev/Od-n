from .connection_state import TelegramConnectionState, can_transition


class TelegramConnectionManager:
    def __init__(self):
        self.states: dict[str, TelegramConnectionState] = {}

    def register_bot(self, bot_name: str) -> None:
        if not bot_name.strip():
            raise ValueError("El nombre del bot no puede estar vacío.")

        self.states.setdefault(
            bot_name,
            TelegramConnectionState.DISCONNECTED,
        )

    def get_state(self, bot_name: str) -> TelegramConnectionState:
        if bot_name not in self.states:
            raise KeyError(f"Bot no registrado: {bot_name}")

        return self.states[bot_name]

    def transition(
        self,
        bot_name: str,
        target: TelegramConnectionState,
    ) -> None:
        current = self.get_state(bot_name)

        if not can_transition(current, target):
            raise ValueError(
                f"Transición no permitida: {current.value} -> {target.value}"
            )

        self.states[bot_name] = target

    def get_all_states(self) -> dict[str, TelegramConnectionState]:
        return dict(self.states)
