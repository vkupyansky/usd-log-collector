import subprocess
import zipfile
from pathlib import Path
from unittest.mock import Mock

import pytest

from collector import collect_logs


@pytest.fixture
def folders(tmp_path: Path) -> tuple[Path, Path]:
    source = tmp_path / "logs"
    destination = tmp_path / "archives"
    source.mkdir()
    destination.mkdir()
    return source, destination


def test_zip_contains_nested_logs(folders: tuple[Path, Path]) -> None:
    source, destination = folders
    (source / "trace").mkdir()
    (source / "trace" / "session.log").write_text("diagnostics", encoding="utf-8")
    stop = Mock()

    archive = collect_logs(source, destination, "12345678", stop)

    stop.assert_called_once_with()
    assert archive.name == "12345678.zip"
    with zipfile.ZipFile(archive) as output:
        assert output.namelist() == ["logs/trace/session.log"]
        assert output.read("logs/trace/session.log") == b"diagnostics"


@pytest.mark.parametrize(
    "ldap", ["../12345", "1234567/", "１２３４５６７８", "1234567", "abcdefgh"]
)
def test_invalid_ldap_has_no_side_effects(
    folders: tuple[Path, Path], ldap: str
) -> None:
    source, destination = folders
    stop = Mock()
    with pytest.raises(ValueError, match="8 цифр"):
        collect_logs(source, destination, ldap, stop)
    stop.assert_not_called()
    assert list(destination.iterdir()) == []


def test_empty_logs_do_not_stop_usd(folders: tuple[Path, Path]) -> None:
    source, destination = folders
    stop = Mock()
    with pytest.raises(FileNotFoundError, match="нет логов"):
        collect_logs(source, destination, "12345678", stop)
    stop.assert_not_called()
    assert list(destination.iterdir()) == []


def test_existing_archive_is_preserved(folders: tuple[Path, Path]) -> None:
    source, destination = folders
    (source / "usd.log").write_text("diagnostics", encoding="utf-8")
    archive = destination / "12345678.zip"
    archive.write_bytes(b"existing archive")
    stop = Mock()
    with pytest.raises(FileExistsError, match="уже существует"):
        collect_logs(source, destination, "12345678", stop)
    stop.assert_not_called()
    assert archive.read_bytes() == b"existing archive"


def test_stop_failure_removes_partial_archive(folders: tuple[Path, Path]) -> None:
    source, destination = folders
    (source / "usd.log").write_text("diagnostics", encoding="utf-8")
    stop = Mock(side_effect=subprocess.TimeoutExpired("taskkill", 10))
    with pytest.raises(subprocess.TimeoutExpired):
        collect_logs(source, destination, "12345678", stop)
    assert list(destination.iterdir()) == []


def test_destination_cannot_be_inside_logs(folders: tuple[Path, Path]) -> None:
    source, _ = folders
    nested = source / "output"
    nested.mkdir()
    stop = Mock()
    with pytest.raises(ValueError, match="за пределами"):
        collect_logs(source, nested, "12345678", stop)
    stop.assert_not_called()


def test_symlink_is_not_archived(folders: tuple[Path, Path], tmp_path: Path) -> None:
    source, destination = folders
    outside = tmp_path / "outside.txt"
    outside.write_text("private", encoding="utf-8")
    (source / "external.log").symlink_to(outside)
    stop = Mock()
    with pytest.raises(FileNotFoundError, match="нет логов"):
        collect_logs(source, destination, "12345678", stop)
    stop.assert_not_called()
