"""
Module flysystem
"""

from enum import Enum
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
        return cls(f"Corrupted path detected: {path}")


@final
class InvalidVisibilityProvided(FlyFilesystemException):
    """
    InvalidVisibilityProvided exception
    """

    @classmethod
    def with_visibility(cls, visibility: str) -> Self:
        return cls(f"Invalid visibility provided. Expected either 'public' or 'private', received '{visibility}'")


@final
class FilesystemOperationFailed(Enum):
    OPERATION_WRITE = "WRITE"
    OPERATION_UPDATE = "UPDATE"
    OPERATION_EXISTENCE_CHECK = "EXISTENCE_CHECK"
    OPERATION_DIRECTORY_EXISTS = "DIRECTORY_EXISTS"
    OPERATION_FILE_EXISTS = "FILE_EXISTS"
    OPERATION_CREATE_DIRECTORY = "CREATE_DIRECTORY"
    OPERATION_DELETE = "DELETE"
    OPERATION_DELETE_DIRECTORY = "DELETE_DIRECTORY"
    OPERATION_MOVE = "MOVE"
    OPERATION_RETRIEVE_METADATA = "RETRIEVE_METADATA"
    OPERATION_COPY = "COPY"
    OPERATION_READ = "READ"
    OPERATION_SET_VISIBILITY = "SET_VISIBILITY"
    OPERATION_LIST_CONTENTS = "LIST_CONTENTS"


class UnableToOperateToFile(FlyFilesystemException):
    """
    Unable to operate to file exception
    """

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self._operation = ""
        self._location = ""
        self._reason = ""

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
class UnableToCheckExistence(UnableToOperateToFile):
    @classmethod
    def with_location(cls, location: str, reason: str = "") -> Self:
        msg = f"Unable to check existence file from location: {location}. {reason}".rstrip()
        this = cls(msg)
        this._operation = FilesystemOperationFailed.OPERATION_FILE_EXISTS.value
        this._location = location
        this._reason = reason
        return this


@final
class UnableToCopyFile(UnableToOperateToFile):
    @classmethod
    def with_location(cls, source: str, destination: str, reason: str = "") -> Self:
        msg = f"Unable to copy file from location: {source} to {destination}. {reason}".rstrip()
        this = cls(msg)
        this._operation = FilesystemOperationFailed.OPERATION_COPY.value
        this._location = source
        this._reason = reason
        return this


@final
class UnableToCheckDirectoryExistence(UnableToOperateToFile):
    @classmethod
    def with_location(cls, location: str, reason: str = "") -> Self:
        msg = f"Unable to check existence directory from location: {location}. {reason}".rstrip()
        this = cls(msg)
        this._operation = FilesystemOperationFailed.OPERATION_DIRECTORY_EXISTS.value
        this._location = location
        this._reason = reason
        return this


@final
class UnableToCreateDirectory(UnableToOperateToFile):
    @classmethod
    def with_location(cls, location: str, reason: str = "") -> Self:
        msg = f"Unable to create directory from location: {location}. {reason}".rstrip()
        this = cls(msg)
        this._operation = FilesystemOperationFailed.OPERATION_CREATE_DIRECTORY.value
        this._location = location
        this._reason = reason
        return this


@final
class UnableToDeleteDirectory(UnableToOperateToFile):
    @classmethod
    def with_location(cls, location: str, reason: str = "") -> Self:
        msg = f"Unable to delete directory from location: {location}. {reason}".rstrip()
        this = cls(msg)
        this._operation = FilesystemOperationFailed.OPERATION_DELETE_DIRECTORY.value
        this._location = location
        this._reason = reason
        return this


@final
class UnableToDeleteFile(UnableToOperateToFile):
    @classmethod
    def with_location(cls, location: str, reason: str = "") -> Self:
        msg = f"Unable to delete file from location: {location}. {reason}".rstrip()
        this = cls(msg)
        this._operation = FilesystemOperationFailed.OPERATION_DELETE.value
        this._location = location
        this._reason = reason
        return this


@final
class UnableToMoveFile(UnableToOperateToFile):
    @classmethod
    def with_location(cls, source: str, destination: str, reason: str = "") -> Self:
        msg = f"Unable to move file from location: {source} to {destination}. {reason}".rstrip()
        this = cls(msg)
        this._operation = FilesystemOperationFailed.OPERATION_MOVE.value
        this._location = source
        this._reason = reason
        return this


@final
class UnableToReadFile(UnableToOperateToFile):
    @classmethod
    def with_location(cls, location: str, reason: str = "") -> Self:
        msg = f"Unable to read file from location: {location}. {reason}".rstrip()
        this = cls(msg)
        this._operation = FilesystemOperationFailed.OPERATION_READ.value
        this._location = location
        this._reason = reason
        return this


@final
class UnableToRetrieveMetadata(UnableToOperateToFile):
    @classmethod
    def with_location(cls, location: str, reason: str = "") -> Self:
        msg = f"Unable to retrieve metadata from location: {location}. {reason}".rstrip()
        this = cls(msg)
        this._operation = FilesystemOperationFailed.OPERATION_RETRIEVE_METADATA.value
        this._location = location
        this._reason = reason
        return this


@final
class UnableToWriteFile(UnableToOperateToFile):
    @classmethod
    def with_location(cls, location: str, reason: str = "") -> Self:
        msg = f"Unable to write file from location: {location}. {reason}".rstrip()
        this = cls(msg)
        this._operation = FilesystemOperationFailed.OPERATION_WRITE.value
        this._location = location
        this._reason = reason
        return this
