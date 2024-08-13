#!/usr/bin/env python3
"""returns the log message with obfuscated fields"""
import logging
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def filter_datum(fields, redaction, message, separator):
    """obfuscates log message fields"""
    for field in fields:
        pattern_str = field +'=[^;]*'
        repl_str = field +'='+redaction
        print(re.sub(pattern_str, repl_str, message))
