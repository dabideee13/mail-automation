import json
import re
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


def split_messages(messages: list[bytes]) -> list[bytes]:
    return messages[0].split(b' ')


def _mail_only(matches: list[str]) -> str:
    return [
        string for string in matches
        if ".com" and "@" in string
    ][0]


def _extract_name(text: str) -> str:
    pattern = r"(?<=\")(.*?)(?=\")"
    return re.findall(pattern, text)[0]


def _extract_mail(text: str) -> str:
    pattern = r"(?<=<)(.*?)(?=>)"
    return re.findall(pattern, text)[0]


def extract_sender(mail: bytes) -> tuple[str, str]:
    if not isinstance(mail, bytes):
        raise TypeError("Mail must be of type bytes")

    pattern = r"(?=From)(.*?)(?=\r\n)"

    try:
        matches = re.findall(pattern, mail.decode("UTF-8"))

        if len(matches) > 1:
            matches = _mail_only(matches)

        return _extract_name(matches[0]), _extract_mail(matches[0])

    except:
        return "", ""
