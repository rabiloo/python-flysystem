from datetime import datetime
from pathlib import Path
from typing import IO, Any, Dict, List

from typing_extensions import Self

from ..adapters import FilesystemAdapter
from ..visibility import Visibility


class InMemoryFile(object):
    def __init__(self) -> None:
        self._contents = ""
        self._last_modified = int(datetime.now().timestamp())
        self._visibility = Visibility.PUBLIC

    def read(self) -> str:
        return self._contents

    def read_stream(self) -> None:
        # TODO
        return ""

    #     tempfile = NamedTemporaryFile()
    #     tempfile.write

    def file_size(self) -> int:
        return len(self._contents)

    def last_modified(self) -> int:
        return self._last_modified

    def mime_type(self) -> str:
        # TODO
        return ""

    def visibility(self) -> str:
        return self._visibility

    def with_contents(self, contents: str, timestamp: int = None) -> Self:
        self._contents = contents
        self._last_modified = timestamp or int(datetime.now().timestamp())
        return self

    def with_visibility(self, visibility: str) -> Self:
        self._visibility = visibility
        return self

    def with_last_modified(self, timestamp: int) -> Self:
        self._last_modified = timestamp
        return self


class InMemoryFilesystemAdapter(FilesystemAdapter):
    def __init__(self, default_visibility: str = Visibility.PUBLIC) -> None:
        self.files: dict = {}
        self.default_visibility = default_visibility

    def file_exists(self, path: str) -> bool:
        """
        Determine if a file exists.
        Arguments:
            path: The file path
        Returns:
            True if the file exsited
        """
        file_ = self.files.get(path)
        return file_ is not None and isinstance(file_, InMemoryFile)

    def directory_exists(self, path: str) -> bool:
        """
        Determine if a directory exists.
        Arguments:
            path: The directory path
        Returns:
            True if the directory exsited
        """
        dir_ = self.files.get(path)
        return dir_ is not None and isinstance(dir_, dict)

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

    def create_directory(self, path: str, options: Dict[str, Any] = None):
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

    def list_contents(self, path: str) -> List[str]:
        """
        Get all (recursive) of the directories within a given directory.
        Arguments:
            path: Directory path
        Returns:
            List all directories in the given directory
        """

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
