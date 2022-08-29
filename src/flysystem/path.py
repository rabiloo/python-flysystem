"""
Module flysystem
"""

from abc import ABCMeta, abstractmethod
from os.path import normpath


class PathNormalizer(metaclass=ABCMeta):
    """
    Path normalizer interface
    """

    @abstractmethod
    def normalize(self, path: str) -> str:
        """
        Normalize path
        Arguments:
            path: The path
        Returns:
            Represents the normalized path as string
        """


class WhitespacePathNormalizer(PathNormalizer):
    """
    Whitespace path normalizer
    """

    def normalize(self, path: str) -> str:
        """
        Normalize path
        Arguments:
            path: The path
        Returns:
            Represents the normalized path as string
        """
        path = self._replace_windows_directory_separator(path)
        return self._normalize_relative_path(path)

    def _replace_windows_directory_separator(self, path: str) -> str:
        """
        Replace Windows directory separator ("\") to Unix directory separator ("/")
        Arguments:
            path: The path
        Returns:
            The path after it replaced
        """
        return path.replace("\\", "/")

    def _normalize_relative_path(self, path: str) -> str:
        """
        Normalize relative path
        Arguments:
            path: The path
        Returns:
            Represents the normalized path as string
        """
        path = normpath(path).strip("/")
        if path == ".":
            path = ""
        return path
