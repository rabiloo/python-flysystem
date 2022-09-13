"""
Module flysystem
"""

from typing import Final
from typing_extensions import Self


class FlyFilesystemException(Exception):
    """
    Base exception class for FlyFilesystem package
    """


@Final
class CorruptedPathDetected(FlyFilesystemException):
    """
    CorruptedPathDetected exception
    """

    @classmethod
    def for_path(cls, path: str) -> Self:
        return cls("Corrupted path detected: " + path)


@Final
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

    @Final
    def operation(self) -> str:
        return self._operation

    @Final
    def location(self) -> str:
        return self._location

    @Final
    def reason(self) -> str:
        return self._reason


@Final
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


@Final
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
