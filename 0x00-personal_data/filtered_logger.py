#!/usr/bin/env python3
"""Returns the log message with obfuscated fields."""
import logging
import re
from typing import List

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """Obfuscates log message fields."""
    for field in fields:
        pattern_str = field + f'=[^{separator}]*'
        repl_str = field + '=' + redaction
        message = re.sub(pattern_str, repl_str, message)
    return message
