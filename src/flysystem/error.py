"""
Module flysystem
"""


class CorruptedPathDetected(RuntimeError):
    """
    CorruptedPathDetected error
    """

    def __init__(self, path: str, *args: object):
        super().__init__("Corrupted path detected", path, *args)
