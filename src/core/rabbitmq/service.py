from kirt08_contracts.events.rmq_otp_contract import rmq_otp_contract
from kirt08_contracts.events.rmq_change_email_contract import rmq_change_email_contract
from kirt08_contracts.events.rmq_change_phone_contract import rmq_change_phone_contract

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
        # try:
        await self._publisher.publish(
            queue_name = settings.rmq_queue.notification_otp_queue,
            message = data.model_dump_json()
        )
        # except:
        #     raise ProblemsWithRMQException
        
    async def put_email_change_code(self, email: str, code: str) -> None:
        data = rmq_change_email_contract(
            email = email,
            code = code
        )
        try:
            await self._publisher.publish(
                queue_name = settings.rmq_queue.notification_change_email_queue,
                message = data.model_dump_json()
            )
        except:
            raise ProblemsWithRMQException


