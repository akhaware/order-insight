from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_FILE_NAME = "order_insight.log"
LOG_DIRECTORY_NAME = "logs"
MAX_BYTES = 1_048_576
BACKUP_COUNT = 3


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def get_log_directory() -> Path:
    return get_project_root() / LOG_DIRECTORY_NAME


def get_log_file_path() -> Path:
    return get_log_directory() / LOG_FILE_NAME


def configure_logging(level: int = logging.INFO) -> Path:
    log_directory = get_log_directory()
    log_directory.mkdir(parents=True, exist_ok=True)
    log_file = get_log_file_path()

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s [%(funcName)s] - %(message)s"
    )

    if root_logger.handlers:
        root_logger.handlers.clear()

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=MAX_BYTES,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    return log_file
