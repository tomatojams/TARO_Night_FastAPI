from uuid import uuid4
import time


# 간단코드
# csrf_tokens = {}
#
#
# def generate_csrf_token():
#     token = str(uuid4())
#     csrf_tokens[token] = True
#     return token
#
#
# def validate_csrf_token(token):
#     return token in csrf_tokens
#
csrf_tokens = {}
csrf_token_expiry = {}


# 시간이 경과하면 사용못하게 기능추가
def validate_csrf_token(token: str) -> bool:
    current_time = time.time()
    if token in csrf_tokens and csrf_token_expiry[token] > current_time:
        return True
    return False


def generate_csrf_token() -> str:
    token = str(uuid4())
    csrf_tokens[token] = True
    csrf_token_expiry[token] = time.time() + 3600  # Token valid for 1 hour
    return token
