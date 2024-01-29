import mimetypes
import shutil

from pathlib import Path
from typing import IO, Any, Dict, List

from ..adapters import FilesystemAdapter
from ..error import (
    UnableToCopyFile,
    UnableToCreateDirectory,
    UnableToDeleteDirectory,
    UnableToDeleteFile,
    UnableToMoveFile,
    UnableToReadFile,
    UnableToRetrieveMetadata,
    UnableToWriteFile,
)
from ..visibility import PortableUnixVisibilityConverter, UnixVisibilityConverter


class LocalFilesystemAdapter(FilesystemAdapter):
    """
    Local filesystem adapter class
    """

    def __init__(self, location: str, visibility_converter: UnixVisibilityConverter = None) -> None:
        self.root_location = location
        self.visibility_converter = visibility_converter or PortableUnixVisibilityConverter()

    def file_exists(self, path: str) -> bool:
        """
        Determine if a file exists.
        Arguments:
            path: The file path
        Returns:
            True if the file existed
        """
        return Path(path).is_file()

    def directory_exists(self, path: str) -> bool:
        """
        Determine if a directory exists.
        Arguments:
            path: The directory path
        Returns:
            True if the directory existed
        """
        return Path(path).is_dir()

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
        try:
            encoding = options.get("encoding") if options else None
            mode = options.get("mode", "w") if options else "w"
            errors = options.get("errors") if options else None
            with Path(path).open(mode, encoding=encoding, errors=errors) as wfile:
                wfile.write(contents)
        except IsADirectoryError as ex:
            raise UnableToWriteFile.with_location(path, str(ex))
        except FileNotFoundError as ex:
            raise UnableToWriteFile.with_location(path, str(ex))
        except PermissionError as ex:
            raise UnableToWriteFile.with_location(path, str(ex))

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
        try:
            encoding = options.get("encoding") if options else None
            mode = options.get("mode", "w") if options else "w"
            errors = options.get("errors") if options else None
            chunk_size = options.get("chunk_size") if options else None
            with Path(path).open(mode, encoding=encoding, errors=errors) as wfile:
                if chunk_size:
                    while True:
                        chunk = resource.read(chunk_size)
                        if not chunk:
                            break
                        wfile.write(chunk)
                else:
                    wfile.write(resource.read())
        except IsADirectoryError as ex:
            raise UnableToWriteFile.with_location(path, str(ex))
        except FileNotFoundError as ex:
            raise UnableToWriteFile.with_location(path, str(ex))
        except PermissionError as ex:
            raise UnableToWriteFile.with_location(path, str(ex))

    def read(self, path: str) -> str:
        """
        Get the contents of a file.
        Arguments:
            path: The file path
        Returns:
            The contents of file as string
        """
        try:
            contents = Path(path).read_text()
        except IsADirectoryError as ex:
            raise UnableToReadFile.with_location(path, str(ex))
        except FileNotFoundError as ex:
            raise UnableToReadFile.with_location(path, str(ex))
        except PermissionError as ex:
            raise UnableToReadFile.with_location(path, str(ex))
        return contents

    def read_stream(self, path: str) -> IO:
        """
        Read the contents of a file as stream
        Arguments:
            path: The file path
        Returns:
            The contents of file as stream
        """
        try:
            stream = Path(path).open("r")
        except IsADirectoryError as ex:
            raise UnableToReadFile.with_location(path, str(ex))
        except FileNotFoundError as ex:
            raise UnableToReadFile.with_location(path, str(ex))
        except PermissionError as ex:
            raise UnableToReadFile.with_location(path, str(ex))
        return stream

    def delete(self, path: str):
        """
        Delete a file
        Arguments:
            path: The file path
        Returns:
            None
        """
        try:
            Path(path).unlink()
        except IsADirectoryError as ex:
            raise UnableToDeleteFile.with_location(path, str(ex))
        except FileNotFoundError as ex:
            raise UnableToDeleteFile.with_location(path, str(ex))
        except PermissionError as ex:
            raise UnableToDeleteFile.with_location(path, str(ex))

    def delete_directory(self, path: str):
        """
        Recursively delete a directory.
        Arguments:
            path: Directory path to delete
        Returns:
            True if the directory is deleted successfully
        """
        try:
            shutil.rmtree(path)
        except NotADirectoryError as ex:
            raise UnableToDeleteDirectory.with_location(path, str(ex))
        except FileNotFoundError as ex:
            raise UnableToDeleteDirectory.with_location(path, str(ex))
        except PermissionError as ex:
            raise UnableToDeleteDirectory.with_location(path, str(ex))
        return True

    def create_directory(self, path: str, options: Dict[str, Any] = None):
        """
        Create a directory.
        Arguments:
            path: Directory path to create
            options: Options for create
        Returns:
            True if the directory is created successfully
        """
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
        except OSError as ex:
            raise UnableToCreateDirectory.with_location(path, str(ex))
        return True

    def set_visibility(self, path: str, visibility: str):
        """
        Set file visibility
        Arguments:
            path: The file path
            visibility: New visibility (Valid value: "public" and "private")
        Returns:
            None
        """
        # Path(path).chmod(self.visibility_converter.for_file(visibility))
        raise NotImplementedError

    def visibility(self, path: str) -> str:
        """
        Get visibility of file
        Arguments:
            path: The file path
        Returns:
            The file's visibility
        """
        # visibility = S_IMODE(Path(path).stat().st_mode)
        # return self.visibility_converter.inverse_for_file(visibility)
        raise NotImplementedError

    def file_size(self, path: str) -> int:
        """
        Get size of file
        Arguments:
            path: The file path
        Returns:
            The file size in bytes
        """
        try:
            size = Path(path).stat().st_size
        except IsADirectoryError as ex:
            raise UnableToRetrieveMetadata.with_location(path, str(ex))
        except FileNotFoundError as ex:
            raise UnableToRetrieveMetadata.with_location(path, str(ex))
        return size

    def mime_type(self, path: str) -> str:
        """
        Get mimetype of file
        Arguments:
            path: The file path
        Returns:
            The file's mimetype
        """
        mime_type, _ = mimetypes.guess_type(path)
        return mime_type

    def last_modified(self, path: str) -> int:
        """
        Get last modified time
        Arguments:
            path: The file path
        Returns:
            The file's last modified time as timestamp
        """
        try:
            time_modified = int(Path(path).stat().st_mtime * 1000)
        except IsADirectoryError as ex:
            raise UnableToRetrieveMetadata.with_location(path, str(ex))
        except FileNotFoundError as ex:
            raise UnableToRetrieveMetadata.with_location(path, str(ex))
        return time_modified

    def list_contents(self, path: str) -> List[str]:
        """
        Get all (recursive) of the directories within a given directory.
        Arguments:
            path: Directory path
        Returns:
            List all directories in the given directory
        """
        return [str(path_) for path_ in Path(path).rglob("*.*")]

    def copy(self, source: str, destination: str, options: Dict[str, Any] = None):
        """
        Copy a file
        Arguments:
            source: Path to source file
            destination: Path to destination file or folder
            options: Copy options
        Returns:
            None
        """
        try:
            shutil.copy2(source, destination)
        except IsADirectoryError as ex:
            raise UnableToCopyFile.with_location(source, destination, str(ex))
        except PermissionError as ex:
            raise UnableToCopyFile.with_location(source, destination, str(ex))

    def move(self, source: str, destination: str, options: Dict[str, Any] = None):
        """
        Move a file
        Arguments:
            source: Path to source file
            destination: Path to destination file ỏ folder
            options: Move options
        Returns:
            None
        """
        try:
            shutil.move(source, destination)
        except IsADirectoryError as ex:
            raise UnableToMoveFile.with_location(source, destination, str(ex))
        except FileNotFoundError as ex:
            raise UnableToMoveFile.with_location(source, destination, str(ex))
        except OSError as ex:
            raise UnableToMoveFile.with_location(source, destination, str(ex))
