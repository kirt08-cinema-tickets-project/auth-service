from kirt08_contracts.events.rmq_otp_contract import rmq_otp_contract

from src.core.config import settings

from src.core.rabbitmq import RabbitMQPublisher 
from src.core.rabbitmq.exceptions import ProblemsWithRMQException


class Service_RMQ:
    def __init__(self, publisher: RabbitMQPublisher):
        self._publisher = publisher
   
    async def put_otp_code(self, identifier: str, type_: str, code: str) -> None:
        data = rmq_otp_contract(
            identifier = identifier,
            type_= type_,
            code = code,
        )
        try:
            await self._publisher.publish(
                queue_name = settings.rmq_queue.notification_queue,
                message = data.model_dump_json()
            )
        except:
            raise ProblemsWithRMQException


