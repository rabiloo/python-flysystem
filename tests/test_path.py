import pytest

from flysystem.path import WhitespacePathNormalizer

paths = (
    (".", ""),
    ("/path/to/dir/.", "/path/to/dir"),
    ("/dirname/", "/dirname"),
    ("dirname/..", ""),
    ("dirname/../", ""),
    ("dirname./", "dirname."),
    ("dirname/./", "dirname"),
    ("dirname/.", "dirname"),
    ("./dir/../././", ""),
    ("/something/deep/../../dirname", "/dirname"),
    ("00004869/files/other/10-75..stl", "00004869/files/other/10-75..stl"),
    ("/dirname//subdir///subsubdir", "/dirname/subdir/subsubdir"),
    ("\\dirname\\\\subdir\\\\\\subsubdir", "/dirname/subdir/subsubdir"),
    ("\\\\some\\shared\\\\drive", "/some/shared/drive"),
    ("C:\\dirname\\\\subdir\\\\\\subsubdir", "C:/dirname/subdir/subsubdir"),
    ("C:\\\\dirname\\subdir\\\\subsubdir", "C:/dirname/subdir/subsubdir"),
    ("example/path/..txt", "example/path/..txt"),
    ("\\example\\path.txt", "/example/path.txt"),
    ("\\example\\..\\path.txt", "/path.txt"),
)
normalizer = WhitespacePathNormalizer()


@pytest.mark.parametrize("path,expected", paths)
def test_normalize(path: str, expected: str):
    """
    Test normalize method
    Arguments:
        path: The path to normalize
        expected: The expected normalized path
    Returns:
        None
    """
    assert normalizer.normalize(path) == expected
