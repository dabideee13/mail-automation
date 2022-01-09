# TODO: get unique senders' email

from logger import logger
from main import fetch, get_message, login
from tools import extract_sender


def export_senders(data: list[tuple[str, str]]) -> None:
    with open("senders.txt", "w") as f:
        for elem in data:
            f.write(elem + "\n")


def main():

    logger.info("BEGIN")

    logger.info("Logging in")
    imap = login()

    logger.info("Extracting messages")
    imap, messages = get_message(imap)

    logger.info("Extracting senders")

    senders = []
    for message in messages:
        name, email = extract_sender(fetch(imap, message))
        logger.info(f"Collecting {name}")
        senders.append(email)

    logger.info("Exporting senders")
    export_senders(senders)


if __name__ == "__main__":
    main()
