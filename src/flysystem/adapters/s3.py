import os

from typing import IO, Any, Dict, List

import boto3

from botocore.client import ClientError, Config

from ..adapters import FilesystemAdapter
from ..error import (
    UnableToCheckDirectoryExistence,
    UnableToCheckExistence,
    UnableToCopyFile,
    UnableToCreateDirectory,
    UnableToDeleteDirectory,
    UnableToDeleteFile,
    UnableToMoveFile,
    UnableToReadFile,
    UnableToRetrieveMetadata,
    UnableToWriteFile,
)


class S3FilesystemAdapter(FilesystemAdapter):
    """
    Local filesystem adapter class
    """

    def __init__(
        self, endpoint_url: str, access_key_id: str, secret_access_key: str, bucket_name: str, region_name: str
    ) -> None:
        session = boto3.Session(aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
        self._s3 = session.resource(
            "s3", endpoint_url=endpoint_url, region_name=region_name, config=Config(signature_version="s3v4")
        )
        self._client = session.client(
            "s3", endpoint_url=endpoint_url, region_name=region_name, config=Config(signature_version="s3v4")
        )
        self._bucket_name = bucket_name
        self._bucket = self._s3.Bucket(bucket_name)

    def file_exists(self, path: str) -> bool:
        """
        Determine if a file exists.
        Arguments:
            path: The file path
        Returns:
            True if the file existed
        """
        try:
            self._bucket.Object(path).load()
        except ClientError as ex:
            if ex.response["Error"]["Code"] == "404":
                return False
            raise UnableToCheckExistence.with_location(path, str(ex))
        return True

    def directory_exists(self, path: str) -> bool:
        """
        Determine if a directory exists.
        Arguments:
            path: The directory path
        Returns:
            True if the directory existed
        """
        try:
            paginator = self._client.get_paginator("list_objects_v2")
            page_iterator = paginator.paginate(Bucket=self._bucket_name, Prefix=path)
            for page in page_iterator:
                if "Contents" in page:
                    return True
            return False
        except ClientError as ex:
            raise UnableToCheckDirectoryExistence.with_location(path, str(ex))

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
            self._bucket.Object(path).put(Body=contents)
        except ClientError as ex:
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
            self._client.upload_fileobj(resource, self._bucket_name, path)
        except ClientError as ex:
            raise UnableToWriteFile.with_location(path, str(ex))
        except TypeError as ex:
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
            file_obj = self._bucket.Object(path)
            file_content = file_obj.get()["Body"].read().decode("utf-8")
        except ClientError as ex:
            raise UnableToReadFile.with_location(path, str(ex))
        return file_content

    def read_bytes(self, path: str) -> bytes:
        """
        Get the contents of a file.
        Arguments:
            path: The file path
        Returns:
            The contents of file as string
        """
        try:
            file_obj = self._bucket.Object(path)
            file_content = file_obj.get()["Body"].read()
        except ClientError as ex:
            raise UnableToReadFile.with_location(path, str(ex))
        return bytes(file_content)

    def read_stream(self, path: str) -> IO:
        """
        Read the contents of a file as stream
        Arguments:
            path: The file path
        Returns:
            The contents of file as stream
        """
        try:
            file_obj = self._bucket.Object(path)
            stream = file_obj.get()["Body"]
        except ClientError as ex:
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
        if path.endswith("/"):
            raise UnableToDeleteFile.with_location(path, "Could not delete directory")
        try:
            self._bucket.Object(path).delete()
        except ClientError as ex:
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
            # List all objects with the directory prefix
            objects_to_delete = []
            paginator = self._client.get_paginator("list_objects_v2")
            page_iterator = paginator.paginate(Bucket=self._bucket_name, Prefix=path)
            for page in page_iterator:
                objects_to_delete.extend(page.get("Contents", []))

            # Delete the objects in batches of 1000 (S3 limit)
            while objects_to_delete:
                objects_batch = objects_to_delete[:1000]
                self._client.delete_objects(
                    Bucket=self._bucket_name, Delete={"Objects": [{"Key": obj_key["Key"]} for obj_key in objects_batch]}
                )
                objects_to_delete = objects_to_delete[1000:]
        except ClientError as ex:
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
            self._bucket.Object(path).put(Body=b"")
        except ClientError as ex:
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
        # try:
        #     self._bucket.Object(path).Acl().put(ACL=self.visibility_converter.for_file(visibility))
        # except ClientError:
        #     pass
        raise NotImplementedError

    def visibility(self, path: str) -> str:
        """
        Get visibility of file
        Arguments:
            path: The file path
        Returns:
            The file's visibility
        """
        # object_acl = self._client.get_object_acl(Bucket=self._bucket_name, Key=path)
        # grant = object_acl.get("Grants")[0]
        # visibility = grant.get("Permission")
        #
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
            obj = self._bucket.Object(path)
            file_size = obj.content_length
        except ClientError as ex:
            raise UnableToRetrieveMetadata.with_location(path, str(ex))
        return file_size

    def mime_type(self, path: str) -> str:
        """
        Get mimetype of file
        Arguments:
            path: The file path
        Returns:
            The file's mimetype
        """
        try:
            obj = self._bucket.Object(path)
            mime_type = obj.content_type
        except ClientError as ex:
            raise UnableToRetrieveMetadata.with_location(path, str(ex))
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
            obj = self._bucket.Object(path)
            last_modified_timestamp = obj.last_modified
        except ClientError as ex:
            raise UnableToRetrieveMetadata.with_location(path, str(ex))
        return int(last_modified_timestamp.timestamp() * 1000)

    def list_contents(self, path: str) -> List[str]:
        """
        Get all (recursive) of the directories within a given directory.
        Arguments:
            path: Directory path
        Returns:
            List all directories in the given directory
        """
        file_keys = []
        try:
            paginator = self._client.get_paginator("list_objects_v2")
            page_iterator = paginator.paginate(Bucket=self._bucket_name, Prefix=path)

            # Collect all file keys (names) within the directory
            for page in page_iterator:
                if "Contents" in page:
                    for obj in page["Contents"]:
                        file_keys.append(obj["Key"])
        except ClientError:
            return []
        return file_keys

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
        if source.endswith("/"):
            raise UnableToCopyFile.with_location(source, destination, "Could not copy directory to file")
        if destination.endswith("/"):
            destination = os.path.join(destination, os.path.basename(source))
        try:
            self._bucket.Object(destination).copy_from(CopySource={"Bucket": self._bucket_name, "Key": source})
        except ClientError as ex:
            raise UnableToCopyFile.with_location(source, destination, str(ex))

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
        if source.endswith("/"):
            raise UnableToMoveFile.with_location(source, destination, "Could not move directory to file")
        if destination.endswith("/"):
            destination = os.path.join(destination, os.path.basename(source))
        try:
            self._bucket.Object(destination).copy_from(CopySource={"Bucket": self._bucket_name, "Key": source})
            self._bucket.Object(source).delete()
        except ClientError as ex:
            raise UnableToMoveFile.with_location(source, destination, str(ex))
