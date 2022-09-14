"""
Module flysystem
"""

from typing import final
from typing_extensions import Self


class FlyFilesystemException(Exception):
    """
    Base exception class for FlyFilesystem package
    """


@final
class CorruptedPathDetected(FlyFilesystemException):
    """
    CorruptedPathDetected exception
    """

    @classmethod
    def for_path(cls, path: str) -> Self:
        return cls("Corrupted path detected: " + path)


@final
class InvalidVisibilityProvided(FlyFilesystemException):
    """
    InvalidVisibilityProvided exception
    """

    @classmethod
    def with_visibility(cls, visibility: str) -> Self:
        return cls(
            "Invalid visibility provided. Expected either 'public' or 'private', received '{0}'".format(
                visibility
            )
        )


class UnableToOperateToFile(FlyFilesystemException):
    """
    Unable to operatte to file exception
    """

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    @final
    def operation(self) -> str:
        return self._operation

    @final
    def location(self) -> str:
        return self._location

    @final
    def reason(self) -> str:
        return self._reason


@final
class UnableToReadFile(UnableToOperateToFile):
    @classmethod
    def with_location(cls, location: str, reason: str = "") -> Self:
        msg = "Unable to read file from location: {location}. {reason}".format(
            location=location, reason=reason
        ).rstrip()
        this = cls(msg)
        this._operation = "read"
        this._location = location
        this._reason = reason
        return this


@final
class UnableToWriteFile(UnableToOperateToFile):
    @classmethod
    def with_location(cls, location: str, reason: str = "") -> Self:
        msg = "Unable to write file from location: {location}. {reason}".format(
            location=location, reason=reason
        ).rstrip()
        this = cls(msg)
        this._operation = "write"
        this._location = location
        this._reason = reason
        return this
