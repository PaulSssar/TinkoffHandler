from dataclasses import dataclass
import time


@dataclass
class Success:
    application_status: str
    application_id: str


@dataclass
class RetryAfter:
    delay: int


@dataclass
class Failure:
    ex: Exception


@dataclass
class ApplicationStatusResponse:
    id: str
    status: str


@dataclass
class Handler:
    def performOperation(self, id: str) -> ApplicationStatusResponse:
        start_time = time.time()
        response1 = self.getApplicationStatus1(id)
        if isinstance(response1, Success):
            return ApplicationStatusResponse(id=response1.application_id, status=response1.application_status)
        elif isinstance(response1, RetryAfter):
            if time.time() - start_time >= 15:
                return ApplicationStatusResponse.Failure(lastRequestTime=None, retriesCount=1)

        response2 = self.getApplicationStatus2(id)
        if isinstance(response2, Success):
            return ApplicationStatusResponse(id=response2.application_id, status=response2.application_status)
        elif isinstance(response2, RetryAfter):
            if time.time() - start_time >= 15:
                return ApplicationStatusResponse.Failure(lastRequestTime=None, retriesCount=2)

        return ApplicationStatusResponse.Failure(lastRequestTime=None, retriesCount=2)


@dataclass
class Client:
    def getApplicationStatus1(self, id: str):
        pass

    def getApplicationStatus2(self, id: str):
        pass


client = Client()
handler = Handler()

response = handler.performOperation("12345")
print(response)
