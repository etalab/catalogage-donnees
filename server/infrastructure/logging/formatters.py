import http
import logging
from typing import Any

from pythonjsonlogger import jsonlogger


class JsonFormatter(jsonlogger.JsonFormatter):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["reserved_attrs"] = [
            # Drop Uvicorn's extras
            # See: https://github.com/madzak/python-json-logger/issues/97
            "color_message",
            *jsonlogger.RESERVED_ATTRS,
        ]
        super().__init__(*args, **kwargs)


class AccessJsonFormatter(JsonFormatter):
    def add_fields(
        self, log_record: dict, record: logging.LogRecord, message_dict: dict
    ) -> None:
        super().add_fields(log_record, record, message_dict)

        # Comes from Uvicorn's access_logger.info(<message>, *args)
        assert record.args

        client_addr, method, full_path, http_version, status_code = record.args
        assert isinstance(status_code, int)

        try:
            status_phrase = http.HTTPStatus(status_code).phrase
        except ValueError:
            status_phrase = ""

        log_record["client_addr"] = client_addr
        log_record["status"] = "%s %s" % (status_code, status_phrase)
        log_record["request_line"] = "%s %s HTTP/%s" % (method, full_path, http_version)
