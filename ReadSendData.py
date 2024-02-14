import time
from dataclasses import dataclass
from typing import List, Any


@dataclass
class Event:
    recipients: List[str]


@dataclass
class Result:
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Handler:
    def readData(self) -> Any:
        pass

    def sendData(self, dest: str, payload: Any) -> str:
        pass

    def performOperation(self):
        events = []

        while True:
            data = self.readData()
            if not data:
                break

            for event in events:
                for recipient in event.recipients:
                    result = self.sendData(recipient, data)
                    if result == Result.REJECTED:
                        time.sleep(self.timeout())
                    else:
                        event.recipients.remove(recipient)

                if not event.recipients:
                    events.remove(event)

    def timeout(self) -> int:
        return 5  # Пример задержки 5 секунд