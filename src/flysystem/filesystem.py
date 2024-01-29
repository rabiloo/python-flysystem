"""
Module flysystem
"""

from abc import ABCMeta, abstractmethod
from typing import IO, Any, Dict, List

from .adapters import FilesystemAdapter
from .path import PathNormalizer, WhitespacePathNormalizer


class FilesystemReader(metaclass=ABCMeta):
    """
    This interface contains everything to read from and inspect a filesystem.
    All methods containing are non-destructive.
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
            True if the directory exsited
        """

    @abstractmethod
    def has(self, path: str) -> bool:
        """
        Determine if a directory or file exists.
        Arguments:
            path: The directory or file path
        Returns:
            True if the directory exsited
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
        Read the contents of a file as tream
        Arguments:
            path: The file path
        Returns:
            The contents of file as stream
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
    def visibility(self, path: str) -> str:
        """
        Get visibility of file
        Arguments:
            path: The file path
        Returns:
            The file's visibility
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


class FilesystemWriter(metaclass=ABCMeta):
    """
    This interface contains everything to write to a filesystem.
    All methods containing are non-destructive.
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
        Copy a file
        Arguments:
            source: Path to source file
            destination: Path to destination file
            options: Move options
        Returns:
            None
        """


class FilesystemOperator(FilesystemReader, FilesystemWriter, metaclass=ABCMeta):
    """
    This interface contains everything from FilesystemReader and FilesystemWriter
    """


class Filesystem(FilesystemOperator):
    """
    Filesystem
    """

    def __init__(
        self,
        adapter: FilesystemAdapter,
        config: Dict[str, Any] = None,
        path_normalizer: PathNormalizer = None,
    ):
        self.adapter = adapter
        self.config = config
        self.path_normalizer = path_normalizer or WhitespacePathNormalizer()

    def has(self, path: str) -> bool:
        path = self.path_normalizer.normalize(path)
        return self.adapter.file_exists(path) or self.adapter.directory_exists(path)

    def file_exists(self, path: str) -> bool:
        return self.adapter.file_exists(self.path_normalizer.normalize(path))

    def write(self, path: str, contents: str, options: Dict[str, Any] = None):
        self.adapter.write(
            self.path_normalizer.normalize(path),
            contents,
            (self.config or {}) | (options or {}),
        )

    def write_stream(self, path: str, resource: IO, options: Dict[str, Any] = None):
        self.adapter.write_stream(
            self.path_normalizer.normalize(path),
            resource,
            (self.config or {}) | (options or {}),
        )

    def read(self, path: str) -> str:
        return self.adapter.read(self.path_normalizer.normalize(path))

    def read_stream(self, path: str):
        return self.adapter.read_stream(self.path_normalizer.normalize(path))

    def delete(self, path: str):
        self.adapter.delete(self.path_normalizer.normalize(path))

    def visibility(self, path: str) -> str:
        return self.adapter.visibility(self.path_normalizer.normalize(path))

    def set_visibility(self, path: str, visibility: str):
        self.adapter.set_visibility(self.path_normalizer.normalize(path), visibility)

    def file_size(self, path: str) -> int:
        return self.adapter.file_size(self.path_normalizer.normalize(path))

    def mime_type(self, path: str) -> str:
        return self.adapter.mime_type(self.path_normalizer.normalize(path))

    def last_modified(self, path: str) -> int:
        return self.adapter.last_modified(self.path_normalizer.normalize(path))

    def directory_exists(self, path: str) -> bool:
        return self.adapter.directory_exists(self.path_normalizer.normalize(path))

    def delete_directory(self, path: str):
        self.adapter.delete_directory(self.path_normalizer.normalize(path))

    def create_directory(self, path: str, options: Dict[str, Any] = None):
        self.adapter.create_directory(self.path_normalizer.normalize(path), (self.config or {}) | (options or {}))

    def list_contents(self, path: str) -> List[str]:
        return self.adapter.list_contents(self.path_normalizer.normalize(path))

    def copy(self, source: str, destination: str, options: Dict[str, Any] = None):
        self.adapter.copy(
            self.path_normalizer.normalize(source),
            self.path_normalizer.normalize(destination),
            (self.config or {}) | (options or {}),
        )

    def move(self, source: str, destination: str, options: Dict[str, Any] = None):
        self.adapter.move(
            self.path_normalizer.normalize(source),
            self.path_normalizer.normalize(destination),
            (self.config or {}) | (options or {}),
        )
