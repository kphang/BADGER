from tenacity import retry, stop_after_attempt, before_log
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

logger = logging.getLogger(__name__)
logging.debug("hi")
@retry(stop=stop_after_attempt(3), before=before_log(logger, logging.DEBUG))
def raise_my_exception():
    raise ValueError("Fail")

raise_my_exception()