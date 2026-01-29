import random
import hashlib

def service_generate_code() -> tuple[str, str]:
    code : str = str(random.randint(100000, 999999))
    hashed_code : str = hashlib.sha256(code.encode()).hexdigest()
    return (code, hashed_code)
