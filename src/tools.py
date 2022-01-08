import json
from pathlib import Path
from typing import Any, Union


def remove_empty(senders: list[str]) -> list[str]:
    return [sender for sender in senders if len(sender) != 0]


def get_senders() -> list[str]:
    file = Path.joinpath(Path.cwd(), "data", "senders.txt")
    with open(file, "r") as f:
        senders = f.read()
    return remove_empty(senders.split(sep="\n"))


def _go_up(path: Path) -> Path:
    return path.parent


def _load_json(file: Union[str, Path]) -> dict[Any, Any]:
    with open(file, 'r') as f:
        data = json.load(f)
    return data


def get_credentials() -> dict[str, str]:

    def get_file(path: Path) -> Path:
        return Path.joinpath(path, "credentials.json")

    def get_path(path: Path) -> Path:
        return Path.joinpath(path, 'data')

    path = get_path(Path.cwd())

    try:
        credentials = _load_json(get_file(path))

    except FileNotFoundError:
        path = _go_up(path)
        credentials = _load_json(get_file(path))

    return credentials
