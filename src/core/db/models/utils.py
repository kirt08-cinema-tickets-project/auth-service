import enum

class Roles(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    
class Type(str, enum.Enum):
    email = "email"
    phone = "phone"