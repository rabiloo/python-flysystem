"""
Module flysystem
"""

from abc import ABCMeta, abstractmethod
from typing import Final, final

from .error import InvalidVisibilityProvided


@final
class Visibility:
    """
    Visibility class
    """

    PUBLIC: Final[str] = "public"
    PRIVATE: Final[str] = "private"

    @staticmethod
    def validate(visibility: str):
        if visibility != Visibility.PUBLIC and visibility != Visibility.PRIVATE:
            raise InvalidVisibilityProvided.with_visibility(visibility)


class UnixVisibilityConverter(metaclass=ABCMeta):
    """
    UnixVisibilityConverter interface
    """

    @abstractmethod
    def default_for_directory(self) -> int:
        """
        Get default Unix visibility for directory
        Arguments:
            None
        Returns:
            Unix visibility format (int)
        """

    @abstractmethod
    def for_file(self, visibility: str) -> int:
        """
        Convert visibility to Unix visibility for file
        Arguments:
            visibility: The file visibility (string format)
        Returns:
            Unix visibility format (int)
        """

    @abstractmethod
    def for_directory(self, visibility: str) -> int:
        """
        Convert visibility to Unix visibility for directory
        Arguments:
            visibility: The directory visibility (string format)
        Returns:
            Unix visibility format (int)
        """

    @abstractmethod
    def inverse_for_file(self, visibility: int) -> str:
        """
        Convert Unix visibility to visibility for file
        Arguments:
            visibility: The file visibility (int format)
        Returns:
            The visibility format (string)
        """

    @abstractmethod
    def inverse_for_directory(self, visibility: int) -> str:
        """
        Convert Unix visibility to visibility for directory
        Arguments:
            visibility: The directory visibility (int format)
        Returns:
            The visibility format (string)
        """


class PortableUnixVisibilityConverter(UnixVisibilityConverter):
    """
    Portable Unix Visibility Converter class
    """

    def __init__(
        self,
        file_public: int = 0o644,
        file_private: int = 0o600,
        directory_public: int = 0o755,
        directory_private: int = 0o700,
        default_directory: str = Visibility.PRIVATE,
    ) -> None:
        self.file_public = file_public
        self.file_private = file_private
        self.directory_public = directory_public
        self.directory_private = directory_private
        self.default_directory = default_directory

    def default_for_directory(self) -> int:
        """
        Get default Unix visibility for directory
        Arguments:
            None
        Returns:
            Unix visibility format (int)
        """
        return (
            self.directory_public
            if self.default_directory == Visibility.PUBLIC
            else self.directory_private
        )

    def for_file(self, visibility: str) -> int:
        """
        Convert visibility to Unix visibility for file
        Arguments:
            visibility: The file visibility (string format)
        Returns:
            Unix visibility format (int)
        """
        Visibility.validate(visibility)
        return (
            self.file_public if visibility == Visibility.PUBLIC else self.file_private
        )

    def for_directory(self, visibility: str) -> int:
        """
        Convert visibility to Unix visibility for directory
        Arguments:
            visibility: The directory visibility (string format)
        Returns:
            Unix visibility format (int)
        """
        Visibility.validate(visibility)
        return (
            self.directory_public
            if visibility == Visibility.PUBLIC
            else self.directory_private
        )

    def inverse_for_file(self, visibility: int) -> str:
        """
        Convert Unix visibility to visibility for file
        Arguments:
            visibility: The file visibility (int format)
        Returns:
            The visibility format (string)
        """
        if visibility == self.file_public:
            return Visibility.PUBLIC
        elif visibility == self.file_private:
            return Visibility.PRIVATE
        # Default
        return Visibility.PUBLIC

    def inverse_for_directory(self, visibility: int) -> str:
        """
        Convert Unix visibility to visibility for directory
        Arguments:
            visibility: The directory visibility (int format)
        Returns:
            The visibility format (string)
        """
        if visibility == self.directory_public:
            return Visibility.PUBLIC
        elif visibility == self.directory_private:
            return Visibility.PRIVATE
        # Default
        return Visibility.PUBLIC
