from datetime import datetime
from ..redis_client import set_with_ttl, get_and_delete


def generate_qr_token(course_id: int) -> str:
    token = f"QR:{course_id}:{int(datetime.utcnow().timestamp())}"
    set_with_ttl(f"qr:{token}", "1", 300)
    return token


def consume_qr_token(qr_token: str) -> bool:
    return get_and_delete(f"qr:{qr_token}") is not None
