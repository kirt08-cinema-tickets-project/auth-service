from pydantic import BaseModel


class RmqQueueConfig(BaseModel):
    notification_otp_queue: str = ""
    notification_change_email_queue: str = ""