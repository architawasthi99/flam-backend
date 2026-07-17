import time

from app.core.config import BACKOFF_BASE

def retry_delay(attempts: int):

    delay = BACKOFF_BASE ** attempts

    time.sleep(delay)
