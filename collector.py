import os
import re
import zipfile
from collections.abc import Callable
from pathlib import Path


def collect_logs(
    source: Path,
    destination: Path,
    ldap: str,
    stop_process: Callable[[], None],
) -> Path:
    if re.fullmatch(r"[0-9]{8}", ldap) is None:
        raise ValueError("LDAP должен содержать ровно 8 цифр")
    if not source.is_dir():
        raise FileNotFoundError("Папка логов USD не найдена. Проверьте --source")
    if not destination.is_dir():
        raise FileNotFoundError("Папка для архива недоступна. Проверьте --destination")
    source = source.resolve()
    destination = destination.resolve()
    if destination == source or source in destination.parents:
        raise ValueError("Папка архива должна находиться за пределами папки логов")

    files: list[Path] = []

    def walk_error(error: OSError) -> None:
        raise error

    for root, directories, filenames in os.walk(source, onerror=walk_error):
        directory = Path(root)
        directories[:] = [
            name for name in directories if not (directory / name).is_symlink()
        ]
        files.extend(
            directory / name
            for name in filenames
            if not (directory / name).is_symlink()
        )
    if not files:
        raise FileNotFoundError("В папке USD нет логов для сохранения")

    archive_path = destination / f"{ldap}.zip"
    try:
        archive = archive_path.open("xb")
    except FileExistsError:
        raise FileExistsError(
            "Архив с таким LDAP уже существует. Выберите другую папку или переименуйте архив"
        ) from None
    try:
        with archive:
            stop_process()
            with zipfile.ZipFile(
                archive, "w", compression=zipfile.ZIP_DEFLATED
            ) as output:
                for file in sorted(files):
                    output.write(file, file.relative_to(source.parent))
    except BaseException:
        archive_path.unlink()
        raise
    return archive_path
