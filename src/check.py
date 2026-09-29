"""Скрипт для запуска всех линтеров и проверок одной командой."""

import subprocess
import sys


def run_command(command: list[str]) -> int:
    """Запускает системную команду и возвращает её код возврата."""
    print(f"▶️ Запуск: {' '.join(command)}...")
    result = subprocess.run(command, check=False)
    if result.returncode == 0:
        print("✅ Успешно!\n")
    else:
        print(f"❌ Ошибка! Код возврата: {result.returncode}\n")
    return result.returncode


def main() -> None:
    """Последовательно запускает весь стек проверок кода."""
    commands = [
        ["black", "--check", "src"],
        ["ruff", "check", "src"],
        ["mypy", "src"],
        ["pylint", "src"],
    ]

    has_errors = False
    for cmd in commands:
        if run_command(cmd) != 0:
            has_errors = True

    if has_errors:
        print("🚨 Некоторые проверки провалены!")
        sys.exit(1)
    else:
        print("🎉 Все проверки успешно пройдены! Код идеален. ✨")


if __name__ == "__main__":
    main()
