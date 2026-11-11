[![Русский](https://img.shields.io/badge/%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9-181717?style=for-the-badge)](README.ru.md)

# USD Log Collector

A Windows utility for collecting Microsoft Dynamics 365 Unified Service Desk logs. It closes USD and saves a ZIP archive named after an eight-digit LDAP ID.

## Features

- Collects nested files from the log folder while skipping symbolic links.
- Validates the LDAP ID and folder accessibility before closing USD.
- Protects existing archives from overwriting and removes the new partial file if an error occurs.

## Installation and startup

Requires Windows x64, Python 3.11–3.14, and [uv](https://docs.astral.sh/uv/). The runtime version and exact dependencies are listed in [.python-version](.python-version), [pyproject.toml](pyproject.toml), and [uv.lock](uv.lock).

```powershell
uv sync --locked
uv run --locked python main.py --destination "C:\Support\Logs"
```

The destination folder must already exist. By default, logs are read from `%APPDATA%\Microsoft\Microsoft Dynamics® 365 Unified Service Desk\4.1.1.1319`. Specify the path explicitly to use a different location:

```powershell
uv run --locked python main.py --source "C:\Support\UsdLogs" --destination "C:\Support\Archives"
```

### Building the EXE

On Windows, run:

```powershell
uv run --locked --group build pyinstaller main.spec --noconfirm
```

Output: `dist/usd-log-collector.exe`.

## Usage

Enter an eight-digit LDAP ID and click "Сохранить" (Save). The application forcibly closes `UnifiedServiceDesk.exe` and its child processes, then creates `LDAP.zip` in the selected folder. If that name already exists, select another folder or rename the previous archive.

The archive contains USD diagnostic data. Choose a folder with appropriate access permissions and review the contents before sharing it.

## Checks

```powershell
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy
uv run --locked pytest -W error
```

Tests use temporary files and mock Windows commands. They check archiving, error handling, and the interface without accessing user logs.

## Limitations

The EXE build and the full workflow on Windows with USD installed require separate verification. Archiving is synchronous: with large logs, the window may temporarily stop responding, and another save is blocked until the operation completes.
