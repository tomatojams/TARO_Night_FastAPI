from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
import time
from util.csrf_manager import validate_csrf_token


# 다른 패키지 설치하면 안될수있음
# 로그 미들웨어 클래스
class ShowRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        body_bytes = await request.body()
        try:
            body = await request.json()
        except Exception:
            body = body_bytes.decode("utf-8")

        response = await call_next(request)
        process_time = time.time() - start_time
        time_formatted = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

        log_message = (
            f"LOG - Request: {request.method} Url: {request.url.path} "
            f"- Body: {body} Completed in {process_time:.2f} seconds "
            f"- Time: {time_formatted}"
        )
        print(log_message)
        return response


# CSFR 검증
class CSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        print("Request URL", request.url.path)
        if request.method == "POST" and request.url.path == "/user/login":

            csrf_token = request.headers.get("X-CSRF-Token")
            if not csrf_token or not validate_csrf_token(csrf_token):
                error_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                log_message = (
                    f"CSRF validation failed - Time: {error_time}, "
                    f"Method: {request.method}, URL: {request.url.path}, "
                    f"Error: CSRF token missing or invalid"
                )
                print(log_message)
                raise HTTPException(
                    status_code=403, detail="CSRF token missing or invalid"
                )
            else:
                success_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                log_message = (
                    f"CSRF validation successful - Time: {success_time}, "
                    f"Method: {request.method}, URL: {request.url.path}"
                )
                print(log_message)

        response = await call_next(request)
        return response
