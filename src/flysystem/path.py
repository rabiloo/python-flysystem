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
        path = normpath(path.replace("\\", "/")).rstrip("/")

        if path == ".":
            path = ""

        if path.startswith("/"):
            path = "/" + path.lstrip("/")

        return path
