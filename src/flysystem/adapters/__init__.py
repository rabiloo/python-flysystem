"""
Module flysystem.adapters
"""

from abc import ABCMeta, abstractmethod
from typing import IO, Any, Dict, List


class FilesystemAdapter(metaclass=ABCMeta):
    """
    FilesystemAdapter interface
    """

    @abstractmethod
    def file_exists(self, path: str) -> bool:
        """
        Determine if a file exists.
        Arguments:
            path: The file path
        Returns:
            True if the file exsited
        """

    @abstractmethod
    def directory_exists(self, path: str) -> bool:
        """
        Determine if a directory exists.
        Arguments:
            path: The directory path
        Returns:
            True if the directory existed
        """

    @abstractmethod
    def write(self, path: str, contents: str, options: Dict[str, Any] = None):
        """
        Write the contents of a file.
        Arguments:
            path: The file path
            contents: The contents to write
            options: Write options
        Returns:
            None
        """

    @abstractmethod
    def write_stream(self, path: str, resource: IO, options: Dict[str, Any] = None):
        """
        Write the contents of a file from stream
        Arguments:
            path: The file path
            resource: The stream
            options: Write options
        Returns:
            None
        """

    @abstractmethod
    def read(self, path: str) -> str:
        """
        Get the contents of a file.
        Arguments:
            path: The file path
        Returns:
            The contents of file as string
        """

    @abstractmethod
    def read_stream(self, path: str) -> IO:
        """
        Read the contents of a file as stream
        Arguments:
            path: The file path
        Returns:
            The contents of file as stream
        """

    @abstractmethod
    def delete(self, path: str):
        """
        Delete a file
        Arguments:
            path: The file path
        Returns:
            None
        """

    @abstractmethod
    def delete_directory(self, path: str):
        """
        Recursively delete a directory.
        Arguments:
            path: Directory path to delete
        Returns:
            True if the directory is deleted successfully
        """

    @abstractmethod
    def create_directory(self, path: str, options: Dict[str, Any] = None):
        """
        Create a directory.
        Arguments:
            path: Directory path to create
            options: Options for create
        Returns:
            True if the directory is created successfully
        """

    @abstractmethod
    def set_visibility(self, path: str, visibility: str):
        """
        Set file visibility
        Arguments:
            path: The file path
            visibility: New visibility (Valid value: "public" and "private")
        Returns:
            None
        """

    @abstractmethod
    def visibility(self, path: str) -> str:
        """
        Get visibility of file
        Arguments:
            path: The file path
        Returns:
            The file's visibility
        """

    @abstractmethod
    def file_size(self, path: str) -> int:
        """
        Get size of file
        Arguments:
            path: The file path
        Returns:
            The file size in bytes
        """

    @abstractmethod
    def mime_type(self, path: str) -> str:
        """
        Get mimetype of file
        Arguments:
            path: The file path
        Returns:
            The file's mimetype
        """

    @abstractmethod
    def last_modified(self, path: str) -> int:
        """
        Get last modified time
        Arguments:
            path: The file path
        Returns:
            The file's last modified time as timestamp
        """

    @abstractmethod
    def list_contents(self, path: str) -> List[str]:
        """
        Get all (recursive) of the directories within a given directory.
        Arguments:
            path: Directory path
        Returns:
            List all directories in the given directory
        """

    @abstractmethod
    def copy(self, source: str, destination: str, options: Dict[str, Any] = None):
        """
        Copy a file
        Arguments:
            source: Path to source file
            destination: Path to destination file
            options: Copy options
        Returns:
            None
        """

    @abstractmethod
    def move(self, source: str, destination: str, options: Dict[str, Any] = None):
        """
        Move a file
        Arguments:
            source: Path to source file
            destination: Path to destination file
            options: Move options
        Returns:
            None
        """
