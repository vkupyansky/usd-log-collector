# USD Log Collector

Windows-утилита для сбора логов Microsoft Dynamics 365 Unified Service Desk. Закрывает USD и сохраняет ZIP-архив с именем из восьмизначного LDAP. Исходный проект 2021 года на PyQt5.

## Запуск

Нужны Windows x64, Python 3.11–3.14 и [uv](https://docs.astral.sh/uv/).

```powershell
uv sync --locked
uv run --locked python main.py --destination "C:\Support\Logs"
```

Папка назначения должна существовать. Укажите LDAP и нажмите «Сохранить». Перед архивированием программа принудительно закрывает `UnifiedServiceDesk.exe` вместе с дочерними процессами. Существующий архив не перезаписывается.

По умолчанию исходные логи берутся из `%APPDATA%\Microsoft\Microsoft Dynamics® 365 Unified Service Desk\4.1.1.1319`. Для другой версии или расположения задайте путь явно:

```powershell
uv run --locked python main.py --source "C:\Support\UsdLogs" --destination "C:\Support\Archives"
```

Сетевые адреса и учётные данные в исходниках не хранятся. Архивы содержат диагностические данные USD, поэтому выбирайте папку с подходящими правами доступа и проверяйте содержимое перед передачей.

## Проверка и сборка

```powershell
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy
uv run --locked pytest -W error
uv run --locked --group build pyinstaller main.spec --noconfirm
```

EXE собирается на Windows в `dist/usd-log-collector.exe`. Старые готовые сборки и установщик в репозиторий не входят. Текущий статус и ограничения описаны в [STATE.md](STATE.md).
