import logging
from src.logging.context import request_id

class RequestFormatter(logging.Formatter):
    def format(self,record: logging.LogRecord) -> str:
        record.request_id=request_id.get()
        return super().format(record)