# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import logging
import sys

__all__ = ["DuplicateMessageFilter"]

"""
USAGE:
logger1 = logging.getLogger("logger1")
logger2 = logging.getLogger("logger2")

formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")

handler1 = logging.StreamHandler()
handler1.setFormatter(formatter)
handler1.addFilter(DuplicateMessageFilter())

handler2 = logging.StreamHandler()
handler2.setFormatter(formatter)
handler2.addFilter(DuplicateMessageFilter())
logger1.addHandler(handler1)
logger2.addHandler(handler2)
"""


class DuplicateMessageFilter(logging.Filter):
    def __init__(self, name=""):
        super().__init__(name)
        self.last_log = None

    def filter(self, record):
        current_log = record.msg
        if current_log != self.last_log:
            self.last_log = current_log
            return True
        return False


uidom_logger = logging.getLogger("UiDOM")

formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")

stdout_info = logging.StreamHandler(stream=sys.stdout)
stdout_info.setLevel(logging.INFO)
stdout_info.setFormatter(formatter)
stdout_info.addFilter(DuplicateMessageFilter("UiDOM"))

uidom_logger.addHandler(stdout_info)
