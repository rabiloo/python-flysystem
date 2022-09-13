from pathlib import Path
from typing import IO
from ..adapters import FilesystemAdapter
from ..visibility import (
    PortableUnixVisibilityConverter,
    UnixVisibilityConverter,
)


class LocalFilesystemAdapter(FilesystemAdapter):
    """
    Local filesystem adapter class
    """

    def __init__(
        self, location: str, visibility_converter: UnixVisibilityConverter = None
    ) -> None:
        self.rootLocation = location
        self.visibility_converter = (
            visibility_converter or PortableUnixVisibilityConverter()
        )

    def file_exists(self, path: str) -> bool:
        """
        Determine if a file exists.
        Arguments:
            path: The file path
        Returns:
            True if the file exsited
        """
        return Path(path).is_file()

    def directory_exists(self, path: str) -> bool:
        """
        Determine if a directory exists.
        Arguments:
            path: The directory path
        Returns:
            True if the directory exsited
        """
        return Path(path).is_dir()

    def write(self, path: str, contents: str, options: dict[str, any] = None):
        """
        Write the contents of a file.
        Arguments:
            path: The file path
            contents: The contents to write
            options: Write options
        Returns:
            None
        """

    def write_stream(self, path: str, resource: IO, options: dict[str, any] = None):
        """
        Write the contents of a file from stream
        Arguments:
            path: The file path
            contents: The stream
            options: Write options
        Returns:
            None
        """

    def read(self, path: str) -> str:
        """
        Get the contents of a file.
        Arguments:
            path: The file path
        Returns:
            The contents of file as string
        """
        return Path(path).read_text()

    def read_stream(self, path: str) -> IO:
        """
        Read the contents of a file as tream
        Arguments:
            path: The file path
        Returns:
            The contents of file as stream
        """
        return Path(path).open("r")

    def delete(self, path: str):
        """
        Delete a file
        Arguments:
            path: The file path
        Returns:
            None
        """
        Path(path).unlink(missing_ok=True)

    def delete_directory(self, path: str):
        """
        Recursively delete a directory.
        Arguments:
            path: Directory path to delete
        Returns:
            True if the directory is deleted successfully
        """

    def create_directory(self, path: str, options: dict[str, any] = None):
        """
        Create a directory.
        Arguments:
            path: Directory path to create
            options: Options for create
        Returns:
            True if the directory is created successfully
        """

    def set_visibility(self, path: str, visibility: str):
        """
        Set file visibility
        Arguments:
            path: The file path
            visibility: New visibility (Valid value: "public" and "private")
        Returns:
            None
        """

    def visibility(self, path: str) -> str:
        """
        Get visibility of file
        Arguments:
            path: The file path
        Returns:
            The file's visibility
        """

    def file_size(self, path: str) -> int:
        """
        Get size of file
        Arguments:
            path: The file path
        Returns:
            The file size in bytes
        """

    def mime_type(self, path: str) -> str:
        """
        Get mimetype of file
        Arguments:
            path: The file path
        Returns:
            The file's mimetype
        """

    def last_modified(self, path: str) -> int:
        """
        Get last modified time
        Arguments:
            path: The file path
        Returns:
            The file's last modified time as timestamp
        """

    def list_contents(self, path: str) -> list[str]:
        """
        Get all (recursive) of the directories within a given directory.
        Arguments:
            directory: Directory path
        Returns:
            List all directories in the given directory
        """

    def copy(self, source: str, destination: str, options: dict[str, any] = None):
        """
        Copy a file
        Arguments:
            source: Path to source file
            destination: Path to destination file
            options: Copy options
        Returns:
            None
        """

    def move(self, source: str, destination: str, options: dict[str, any] = None):
        """
        Copy a file
        Arguments:
            source: Path to source file
            destination: Path to destination file
            options: Move options
        Returns:
            None
        """
