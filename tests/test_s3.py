import io
import os
import time

from typing import IO

import pytest

from flysystem.adapters.s3 import S3FilesystemAdapter
from flysystem.error import (
    UnableToCheckExistence,
    UnableToCopyFile,
    UnableToCreateDirectory,
    UnableToDeleteFile,
    UnableToMoveFile,
    UnableToReadFile,
    UnableToRetrieveMetadata,
    UnableToWriteFile,
)

filesystem = S3FilesystemAdapter(
    endpoint_url=os.getenv("AWS_S3_ENDPOINT"),
    access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    bucket_name=os.getenv("AWS_S3_BUCKET"),
    region_name=os.getenv("AWS_DEFAULT_REGION"),
)


@pytest.mark.parametrize(
    "path,expected,error",
    (
        ("tests/tmp/", True, None),
        ("/", False, UnableToCreateDirectory),
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
        ("tests/tmp.txt", "hello world", None),
        ("tests/tmp2.txt", b"hello world", None),
        ("/", b"hello world", UnableToWriteFile),
    ),
)
def test_write(path: str, expected: str, error: Exception):
    if error is not None:
        with pytest.raises(error):
            filesystem.write(path, expected)
    else:
        filesystem.write(path, expected)
        if isinstance(expected, bytes):
            expected = expected.decode("utf-8")
        assert filesystem.read(path) == expected


@pytest.mark.parametrize(
    "path,expected,error",
    (
        ("tests/tmp2.txt", io.BytesIO(b"hello world"), None),
        ("tests/tmp.txt", io.StringIO("hello world"), UnableToWriteFile),
        ("/", io.BytesIO(b"hello world"), UnableToWriteFile),
    ),
)
def test_write_stream(path: str, expected: IO, error: Exception):
    value = expected.getvalue()
    if error is not None:
        with pytest.raises(error):
            filesystem.write_stream(path, expected)
    else:
        filesystem.write_stream(path, expected)
        if isinstance(value, bytes):
            value = value.decode("utf-8")
        assert filesystem.read(path) == value


@pytest.mark.parametrize(
    "path,expected,error",
    (
        ("tests/tmp.txt", True, None),
        ("tests/tmp2/", False, None),
        ("tests/tmp3.txt", False, None),
        ("/", False, UnableToCheckExistence),
    ),
)
def test_file_exists(path: str, expected: bool, error: Exception):
    if error is not None:
        with pytest.raises(error):
            filesystem.file_exists(path)
    else:
        assert filesystem.file_exists(path) == expected


@pytest.mark.parametrize(
    "path,expected",
    (
        ("tests", True),
        ("tests/tmp.txt", True),
        ("tests2", False),
        ("/", True),
    ),
)
def test_directory_exists(path: str, expected: str):
    assert filesystem.directory_exists(path) == expected


@pytest.mark.parametrize(
    "path,expected,error",
    (
        ("tests/tmp.txt", "hello world", None),
        ("tests/tmp3.txt", "", UnableToReadFile),
        ("tests/", "", UnableToReadFile),
        ("/", "", UnableToReadFile),
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
        ("tests/tmp.txt", "hello world", None),
        ("tests/tmp3.txt", "", UnableToReadFile),
        ("tests/", "", UnableToReadFile),
        ("/", "", UnableToReadFile),
    ),
)
def test_read_stream(path: str, expected: str, error: Exception):
    if error is not None:
        with pytest.raises(error):
            filesystem.read_stream(path)
    else:
        steam = filesystem.read_stream(path)
        assert steam.read().strip().decode("utf-8") == expected


@pytest.mark.parametrize(
    "path,expected,error",
    (
        ("tests/tmp.txt", 11, None),
        ("tests/tmp", -1, UnableToRetrieveMetadata),
        ("/", -1, UnableToRetrieveMetadata),
    ),
)
def test_file_size(path: str, expected: int, error: Exception):
    if error is not None:
        with pytest.raises(error):
            filesystem.file_size(path)
    else:
        assert filesystem.file_size(path) == expected


@pytest.mark.parametrize(
    "path,expected,error",
    (
        ("tests/tmp.txt", "binary/octet-stream", None),
        ("tests/tmp", -1, UnableToRetrieveMetadata),
        ("/", -1, UnableToRetrieveMetadata),
    ),
)
def test_mime_type(path: str, expected: str, error: Exception):
    if error is not None:
        with pytest.raises(error):
            filesystem.mime_type(path)
    else:
        assert filesystem.mime_type(path) == expected


@pytest.mark.parametrize(
    "path,expected,error",
    (
        ("tests/tmp.txt", int(time.time() * 1000), None),
        ("tests/", -1, UnableToRetrieveMetadata),
        ("/", -1, UnableToRetrieveMetadata),
    ),
)
def test_last_modified(path: str, expected: int, error: Exception):
    if error is not None:
        with pytest.raises(error):
            filesystem.last_modified(path)
    else:
        assert -5 < (expected - filesystem.last_modified(path)) / 1000 / 3600 < 2


@pytest.mark.parametrize(
    "path,expected",
    (
        ("tests/tmp.txt", ["tests/tmp.txt"]),
        ("tests", ["tests/tmp.txt", "tests/tmp/", "tests/tmp2.txt"]),
    ),
)
def test_list_contents(path: str, expected: str):
    assert filesystem.list_contents(path) == expected


@pytest.mark.parametrize(
    "source,destination,error",
    (
        ("tests/tmp.txt", "tests/tmp/tmp.txt", None),
        ("tests/tmp2.txt", "tests/tmp/", None),
        ("tests/tmp2.txt", "/", None),
        ("tests/", "tests/copy2/", UnableToCopyFile),
        ("/", "tests/", UnableToCopyFile),
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
        ("tests/tmp.txt", "tests/tmp/tmp.txt", None),
        ("tests/tmp2.txt", "tests/tmp/", None),
        ("tests/", "tests/copy2/", UnableToMoveFile),
        ("/", "tests/", UnableToMoveFile),
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
        ("tests/tmp/", UnableToDeleteFile),
        ("/", UnableToDeleteFile),
        ("tmp2.txt", None),
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
    "path,expected",
    (
        ("tests2/", True),
        ("tests/tmp/tmp.txt", True),
        ("tests/tmp/", True),
    ),
)
def test_delete_directory(path: str, expected: bool):
    assert filesystem.delete_directory(path) == expected
