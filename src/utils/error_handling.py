"""Utilities for handling errors."""

from __future__ import annotations

from typing import NoReturn

from .logging import setup_logger

# Set up logger from the utilities module
logger = setup_logger()


def raise_error(exception_type: type[Exception], message: str) -> NoReturn:
    """Raise an exception with a given message.

    Parameters
    ----------
    ----------:
    exception_type: type[Exception]
        The type of exception to raise.
    message: str
        The message for the exception.

    """
    logger.error(message)
    raise exception_type(message)
