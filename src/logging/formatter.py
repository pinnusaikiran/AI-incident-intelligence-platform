import logging
from src.logging.context import request_id

class RequestFormatter(logging.Formatter):
    def format(self,record):
        record.request_id=request_id.get()
        return super().format(record)