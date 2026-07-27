from starlette.middleware.base import BaseHTTPMiddleware
from uuid import uuid4
import logging
import time

from src.logging.context import request_id


logger = logging.getLogger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):

    async def dispatch(self,request,call_next):
        current_request_id = str(uuid4())

        token=request_id.set(current_request_id)

        logger.info(f"{request.method} {request.url.path}")
        try:
            start_time=time.perf_counter()
            response = await call_next(request)
            duration=time.perf_counter()-start_time
            logger.info("%s %s Status=%s Duration=%.3fs",
                request.method,
                request.url.path,
                response.status_code,
                duration
            )
            return response
        except Exception:

            logger.exception(f"{request.method} {request.url.path}")

            raise 
        
        finally:
            request_id.reset(token)
            