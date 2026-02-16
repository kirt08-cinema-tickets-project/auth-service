from pydantic import BaseModel


class RmqQueueConfig(BaseModel):
    notification_queue: str = ""