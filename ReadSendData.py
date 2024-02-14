import asyncio

from enum import Enum
from typing import List
from dataclasses import dataclass


@dataclass
class Result(Enum):
    Accepted = "Accepted"
    Rejected = "Rejected"


async def read_data() -> Event:
    recipients = List[Address()]
    payload = Payload()
    return Event(recipients=recipients, payload=payload)


async def send_data(dest: Address, payload: Payload) -> Result:
    return Result.Accepted


async def perform_operation() -> None:
    while True:
        event = await read_data()
        for recipient in event.recipients:
            result = await send_data(recipient, event.payload)
            if result == Result.Rejected:
                await asyncio.sleep(timeout_seconds)


loop = asyncio.get_event_loop()
loop.run_until_complete(perform_operation())
