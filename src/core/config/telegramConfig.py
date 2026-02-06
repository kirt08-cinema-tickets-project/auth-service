from pydantic import BaseModel

class TelegramBotConfig(BaseModel):
    id : str = "1"
    token : str = "1"
    username : str = "1"

class TelegramConfig(BaseModel):
    bot : TelegramBotConfig = ""
    redirect_origin : str = "1"
