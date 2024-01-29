import pytest

from flysystem.error import InvalidVisibilityProvided
from flysystem.visibility import PortableUnixVisibilityConverter, Visibility


class TestVisibility:
    def test_determining_an_incorrect_visibility(self) -> None:
        with pytest.raises(InvalidVisibilityProvided):
            Visibility.validate("invalid-visibility")


class TestPortableUnixVisibilityConverter:
    def test_determining_visibility_for_a_file(self) -> None:
        converter = PortableUnixVisibilityConverter()
        assert 0o644 == converter.for_file(Visibility.PUBLIC)
        assert 0o600 == converter.for_file(Visibility.PRIVATE)

    def test_determining_visibility_for_a_directory(self) -> None:
        converter = PortableUnixVisibilityConverter()
        assert 0o755 == converter.for_directory(Visibility.PUBLIC)
        assert 0o700 == converter.for_directory(Visibility.PRIVATE)

    def test_inversing_for_a_file(self) -> None:
        converter = PortableUnixVisibilityConverter()
        assert Visibility.PUBLIC == converter.inverse_for_file(0o644)
        assert Visibility.PRIVATE == converter.inverse_for_file(0o600)
        assert Visibility.PUBLIC == converter.inverse_for_file(0o404)

    def test_inversing_for_a_directory(self) -> None:
        converter = PortableUnixVisibilityConverter()
        assert Visibility.PUBLIC == converter.inverse_for_directory(0o755)
        assert Visibility.PRIVATE == converter.inverse_for_directory(0o700)
        assert Visibility.PUBLIC == converter.inverse_for_directory(0o505)

    def test_determining_default_for_directories(self) -> None:
        converter = PortableUnixVisibilityConverter()
        assert 0o700 == converter.default_for_directory()

    def test_creating_with_customized_parameters(self) -> None:
        converter = PortableUnixVisibilityConverter(
            file_public=0o640,
            file_private=0o604,
            directory_public=0o740,
            directory_private=0o701,
            default_directory=Visibility.PUBLIC,
        )
        assert 0o740 == converter.default_for_directory()
        assert 0o640 == converter.for_file(Visibility.PUBLIC)
        assert 0o604 == converter.for_file(Visibility.PRIVATE)
        assert 0o740 == converter.for_directory(Visibility.PUBLIC)
        assert 0o701 == converter.for_directory(Visibility.PRIVATE)
