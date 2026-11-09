# USD Log Collector

Windows-утилита для сбора логов Microsoft Dynamics 365 Unified Service Desk. Закрывает USD и сохраняет ZIP-архив с именем из восьмизначного LDAP.

## Возможности

- Сбор вложенных файлов из папки логов с пропуском символьных ссылок.
- Проверка LDAP и доступности папок до закрытия USD.
- Защита существующего архива от перезаписи и удаление нового частичного файла при ошибке.

## Установка и запуск

Нужны Windows x64, Python 3.11–3.14 и [uv](https://docs.astral.sh/uv/). Версия среды и точные зависимости указаны в [.python-version](.python-version), [pyproject.toml](pyproject.toml) и [uv.lock](uv.lock).

```powershell
uv sync --locked
uv run --locked python main.py --destination "C:\Support\Logs"
```

Папка назначения должна существовать. По умолчанию логи берутся из `%APPDATA%\Microsoft\Microsoft Dynamics® 365 Unified Service Desk\4.1.1.1319`. Для другого расположения задайте путь явно:

```powershell
uv run --locked python main.py --source "C:\Support\UsdLogs" --destination "C:\Support\Archives"
```

### Сборка EXE

На Windows выполните:

```powershell
uv run --locked --group build pyinstaller main.spec --noconfirm
```

Результат: `dist/usd-log-collector.exe`.

## Использование

Введите LDAP из восьми цифр и нажмите "Сохранить". Программа принудительно закроет `UnifiedServiceDesk.exe` вместе с дочерними процессами и создаст `LDAP.zip` в выбранной папке. При совпадении имени выберите другую папку или переименуйте прежний архив.

Архив содержит диагностические данные USD. Выбирайте папку с подходящими правами доступа и проверяйте содержимое перед передачей.

## Проверки

```powershell
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy
uv run --locked pytest -W error
```

Тесты используют временные файлы и подменяют Windows-команды. Они проверяют архивирование, ошибки и интерфейс без доступа к пользовательским логам.

## Ограничения

Сборка EXE и полный сценарий на Windows с установленным USD требуют отдельной проверки. Архивирование синхронное: при большом объёме логов окно может временно не отвечать, а повторное сохранение блокируется до завершения.
