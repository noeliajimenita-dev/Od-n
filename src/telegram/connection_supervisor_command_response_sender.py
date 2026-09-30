from typing import Callable


class ConnectionSupervisorCommandResponseSender:
    def __init__(
        self,
        sender: Callable[[str], None],
    ):
        self.sender = sender

    def send(self, response: str) -> None:
        if not response:
            return

        self.sender(response)
