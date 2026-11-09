from subprocess import CompletedProcess
from unittest.mock import Mock

import main


def test_absent_usd_is_not_killed(monkeypatch) -> None:
    command = Mock(return_value=CompletedProcess([], 0, b"No tasks found"))
    monkeypatch.setattr(main.subprocess, "run", command)
    main.stop_usd()
    command.assert_called_once()
    assert command.call_args.args[0][0] == "tasklist"


def test_running_usd_is_killed_without_shell(monkeypatch) -> None:
    command = Mock(
        return_value=CompletedProcess([], 0, b'"UnifiedServiceDesk.exe","123"')
    )
    monkeypatch.setattr(main.subprocess, "run", command)
    main.stop_usd()
    assert command.call_count == 2
    assert command.call_args.args[0] == [
        "taskkill",
        "/F",
        "/T",
        "/IM",
        "UnifiedServiceDesk.exe",
    ]
    assert command.call_args.kwargs["check"] is True
    assert command.call_args.kwargs["timeout"] == 10
