#!/usr/bin/env python3
"""Returns the log message with obfuscated fields."""
import logging
import re
from typing import List


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """Instantiates log objects."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def filter_datum(
        self,
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

    def format(self, record: logging.LogRecord) -> str:
        """Formats a log record."""
        log_message = record.getMessage()
        obf_message = self.filter_datum(
            self.fields,
            self.REDACTION,
            log_message,
            self.SEPARATOR)
        record.msg = obf_message
        return super().format(record)
