import asyncio
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


class Response(Enum):
    Success = "Success"
    RetryAfter = "RetryAfter"
    Failure = "Failure"


@dataclass
class ApplicationResponse:
    application_id: str
    status: Response
    description: str
    last_request_time: datetime
    retriesCount: int or None


async def get_application_status1(identifier: str) -> Response:
    return Response.Success


async def get_application_status2(identifier: str) -> Response:
    return Response.Failure


async def perform_operation() -> ApplicationResponse:
    application_id = "12345"

    async def fetch_status(service, identifier):
        if service == 1:
            return await get_application_status1(identifier)
        elif service == 2:
            return await get_application_status2(identifier)

    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        tasks = [loop.run_in_executor(executor, fetch_status, service, application_id) for service in range(1, 3)]
        responses = await asyncio.gather(*tasks)
        status = Response.Success if all(response == Response.Success for response in responses) else Response.Failure
        description = "All services processed successfully" if status == Response.Success else "At least one service failed"
        last_request_time = datetime.now()
        retries_count = None
        return ApplicationResponse(application_id, status, description, last_request_time, retries_count)


loop = asyncio.get_event_loop()
result = loop.run_until_complete(perform_operation())
print(result)
