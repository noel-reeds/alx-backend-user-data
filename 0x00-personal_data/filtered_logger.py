#!/usr/bin/env python3
"""Returns the log message with obfuscated fields."""
import logging
import mysql.connector
import os
import re
from typing import List

PII_FIELDS = ('password', 'email', 'ssn', 'phone', 'name')


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
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


def get_logger() -> logging.Logger:
    """creates a custom logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=list(PII_FIELDS))
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.propagate = False


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to a database"""
    config = {
        'user': os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        'password': os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        'host': os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        'database': os.getenv('PERSONAL_DATA_DB_NAME')
    }
    if not config['database']:
        raise ValueError
    try:
        connector = mysql.connector.connect(**config)
        return connector
    except mysql.connector.Error as err:
        print(f'Error:' {err})
        return None
