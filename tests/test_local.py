import io
import time

from typing import IO

import pytest

from flysystem.adapters.local import LocalFilesystemAdapter
from flysystem.error import (
    UnableToCopyFile,
    UnableToCreateDirectory,
    UnableToDeleteDirectory,
    UnableToDeleteFile,
    UnableToMoveFile,
    UnableToReadFile,
    UnableToRetrieveMetadata,
    UnableToWriteFile,
)

filesystem = LocalFilesystemAdapter(".")


@pytest.mark.parametrize(
    "path,expected,error",
    (
        ("resources/tmp", True, None),
        ("resources/tmp2", True, None),
        ("/usr/tmp", False, UnableToCreateDirectory),
    ),
)
def test_create_directory(path: str, expected: bool, error: Exception):
    if error is not None:
        with pytest.raises(error):
            filesystem.create_directory(path)
    else:
        assert filesystem.create_directory(path) == expected


@pytest.mark.parametrize(
    "path,expected,error",
    (
        ("resources/tmp/tmp.txt", "hello world", None),
        ("resources/tmp3/tmp.txt", "hello world", UnableToWriteFile),
        ("resources/tmp/", "hello world", UnableToWriteFile),
        ("/usr/tmp.txt", "hello world", UnableToWriteFile),
    ),
)
def test_write(path: str, expected: str, error: Exception):
    if error is not None:
        with pytest.raises(error):
            filesystem.write(path, expected)
    else:
        filesystem.write(path, expected)
        assert filesystem.read(path) == expected


@pytest.mark.parametrize(
    "path,expected,error",
    (
        ("resources/tmp/tmp.txt", io.StringIO("hello world"), None),
        ("resources/tmp3/tmp.txt", io.StringIO("hello world"), UnableToWriteFile),
        ("resources/tmp/", io.StringIO("hello world"), UnableToWriteFile),
        ("/usr/tmp.txt", io.StringIO("hello world"), UnableToWriteFile),
    ),
)
def test_write_stream(path: str, expected: IO, error: Exception):
    value = expected.getvalue()
    if error is not None:
        with pytest.raises(error):
            filesystem.write_stream(path, expected)
    else:
        filesystem.write_stream(path, expected)
        assert filesystem.read(path) == value


@pytest.mark.parametrize(
    "path,expected",
    (
        ("resources/tmp", False),
        ("resources/tmp/tmp.txt", True),
        ("resources/tmp/tmp2.txt", False),
        ("/usr/tmp", False),
    ),
)
def test_file_exists(path: str, expected: bool):
    assert filesystem.file_exists(path) == expected


@pytest.mark.parametrize(
    "path,expected",
    (
        ("resources/tmp/tmp.txt", False),
        ("resources/tmp", True),
        ("resources/tmp2", True),
        ("resources", True),
        ("/usr/tmp/", False),
    ),
)
def test_directory_exists(path: str, expected: str):
    assert filesystem.directory_exists(path) == expected


@pytest.mark.parametrize(
    "path,expected,error",
    (
        ("resources/tmp/tmp.txt", "hello world", None),
        ("resources/tmp/", "", UnableToReadFile),
        ("/usr/tmp.txt", "", UnableToReadFile),
        ("/run/sudo", "", UnableToReadFile),
    ),
)
def test_read(path: str, expected: str, error: Exception):
    if error is not None:
        with pytest.raises(error):
            filesystem.read(path)
    else:
        assert filesystem.read(path) == expected


@pytest.mark.parametrize(
    "path,expected,error",
    (
        ("resources/tmp/tmp.txt", "hello world", None),
        ("resources/tmp/", "", UnableToReadFile),
        ("/usr/tmp.txt", "", UnableToReadFile),
        ("/run/sudo", "", UnableToReadFile),
    ),
)
def test_read_stream(path: str, expected: str, error: Exception):
    if error is not None:
        with pytest.raises(error):
            filesystem.read_stream(path)
    else:
        with filesystem.read_stream(path) as rfile:
            assert rfile.read().strip() == expected


@pytest.mark.parametrize(
    "path,expected,error",
    (
        ("resources/tmp/tmp.txt", 11, None),
        ("resources/tmp", 4096, None),
        ("/usr/tmp.txt", -1, UnableToRetrieveMetadata),
    ),
)
def test_file_size(path: str, expected: int, error: Exception):
    if error is not None:
        with pytest.raises(error):
            filesystem.file_size(path)
    else:
        assert filesystem.file_size(path) == expected


@pytest.mark.parametrize(
    "path,expected",
    (
        ("resources/tmp/tmp.txt", "text/plain"),
        ("resources/tmp", None),
        ("/run/sudo", None),
    ),
)
def test_mime_type(path: str, expected: str):
    assert filesystem.mime_type(path) == expected


@pytest.mark.parametrize(
    "path,expected",
    (
        ("resources/tmp/tmp.txt", int(time.time() * 1000)),
        ("resources/tmp", int(time.time() * 1000)),
    ),
)
def test_last_modified(path: str, expected: int):
    assert -5 < (expected - filesystem.last_modified(path)) / 1000 / 3600 < 2


@pytest.mark.parametrize(
    "path,expected",
    (
        ("resources/tmp/tmp.txt", []),
        ("resources/tmp", ["resources/tmp/tmp.txt"]),
    ),
)
def test_list_contents(path: str, expected: str):
    assert filesystem.list_contents(path) == expected


@pytest.mark.parametrize(
    "source,destination,error",
    (
        ("resources/tmp/tmp.txt", "resources/tmp2/tmp.txt", None),
        ("resources/tmp/tmp.txt", "resources/tmp2/", None),
        ("resources/tmp/", "resources/tmp2/", UnableToCopyFile),
        ("resources/tmp/tmp.txt", "/usr/", UnableToCopyFile),
        ("/run/sudo", "resources/", UnableToCopyFile),
    ),
)
def test_copy(source: str, destination: str, error: Exception):
    if error is not None:
        with pytest.raises(error):
            filesystem.copy(source, destination)
    else:
        filesystem.copy(source, destination)


@pytest.mark.parametrize(
    "source,destination,error",
    (
        ("resources/tmp/tmp.txt", "resources/tmp2/tmp.txt", None),
        ("resources/tmp/tmp.txt", "resources/tmp2/", UnableToMoveFile),
        ("resources/tmp2/tmp.txt", "/usr/", UnableToMoveFile),
        ("/run/sudo", "resources/", UnableToMoveFile),
    ),
)
def test_move(source: str, destination: str, error: Exception):
    if error is not None:
        with pytest.raises(error):
            filesystem.move(source, destination)
    else:
        filesystem.move(source, destination)


@pytest.mark.parametrize(
    "path,error",
    (
        ("resources/tmp", UnableToDeleteFile),
        ("resources/tmp.txt", UnableToDeleteFile),
        ("/run/sudo", UnableToDeleteFile),
        ("resources/tmp2/tmp.txt", None),
    ),
)
def test_delete(path: str, error: Exception):
    if error is not None:
        with pytest.raises(error):
            filesystem.delete(path)
    else:
        assert filesystem.file_exists(path)
        filesystem.delete(path)
        assert not filesystem.file_exists(path)


@pytest.mark.parametrize(
    "path,expected,error",
    (
        ("resources/tmp.txt", False, UnableToDeleteDirectory),
        ("/run/sudo", False, UnableToDeleteDirectory),
        ("/run/", False, UnableToDeleteDirectory),
        ("resources/tmp/tmp.txt", False, UnableToDeleteDirectory),
        ("resources/tmp", True, None),
        ("resources/tmp2", True, None),
        ("resources/", True, None),
    ),
)
def test_delete_directory(path: str, expected: bool, error: Exception):
    if error is not None:
        with pytest.raises(error):
            filesystem.delete_directory(path)
    else:
        assert filesystem.delete_directory(path) == expected
