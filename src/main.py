# -*- coding: utf-8 -*-

"""
Mail Automation
"""

import argparse
import email
import imaplib
from email.header import decode_header
from typing import Any

from logger import logger
from tools import get_credentials, get_senders, split_messages


def login(
    mail_provider: str = "imap.gmail.com",
    mailbox: str = "INBOX"
) -> imaplib.IMAP4_SSL:

    imap = imaplib.IMAP4_SSL(mail_provider)
    credentials = get_credentials()

    imap.login(
        credentials['USERNAME'],
        credentials['PASSWORD']
    )
    imap.select(mailbox)

    return imap


def fetch(imap, message: bytes) -> list[tuple[bytes, bytes]]:
    _, msg = imap.fetch(message, "(RFC822)")
    return msg[0][1]


def get_message(
    imap: imaplib.IMAP4_SSL,
    **kwargs: Any
) -> tuple[imaplib.IMAP4_SSL, list[bytes]]:

    _, messages = imap.search(None, "ALL")

    if 'sender' in kwargs.keys():
        _, messages = imap.search(None, f'FROM {kwargs["sender"]}')

    return imap, split_messages(messages)


def delete_mails(imap: imaplib.IMAP4_SSL, sender: str) -> None:
    """
    Source: https://www.thepythoncode.com/article/deleting-emails-in-python
    """

    # Main loop
    for mail in get_message(imap, sender=sender):

        try:
            _, msg = imap.fetch(mail, "(RFC822)")

        except Exception:
            logger.info("Mail not fetched\n")
            continue

        except KeyboardInterrupt:
            logger.info("Interrupted\n")
            continue

        imap.store(mail, "+FLAGS", "\\Deleted")

        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                subject = decode_header(msg["Subject"])[0][0]

                if isinstance(subject, bytes):
                    subject = subject.decode()

        logger.info(f"Deleted: {subject}")


def main():

    logger.info("BEGIN")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--senders",
        type=str,
        nargs='+',
        help="Write the senders here.",
    )
    args = parser.parse_args()

    logger.info("Logging in\n")
    imap = login()

    if args.senders:
        senders = args.senders
    else:
        senders = get_senders()

    for sender in senders:
        try:
            logger.info(f"Deleting mail from {sender}")
            delete_mails(imap, sender)

        except Exception as exception_instance:
            logger.info(f"Email from {sender} not deleted")
            logger.exception(f"{exception_instance}\n")

    logger.info("Expunging")
    imap.expunge()

    logger.info("Closing")
    imap.close()

    logger.info("Logging out")
    imap.logout()

    logger.info("DONE.\n")


if __name__ == "__main__":
    main()


# TODO: add option for getting senders from text or argparse
