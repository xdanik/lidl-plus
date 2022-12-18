#!/usr/bin/env python3
import argparse
import json
import sys
from getpass import getpass
from pathlib import Path

if __name__ == '__main__':
    sys.path.append(str(Path(__file__).parent))
    from api import LidlPlusApi, WebBrowserException
else:
    from lidlplus import LidlPlusApi
    from lidlplus.api import WebBrowserException


def get_arguments():
    """Get parsed arguments."""
    parser = argparse.ArgumentParser(description="Lidl Plus api")
    parser.add_argument("-c", "--country", help="country (DE, EN, FR, IT, ...)")
    parser.add_argument("-l", "--language", help="language (de, be, nl, at, ...)")
    parser.add_argument("-u", "--user", help="Lidl Plus login user")
    parser.add_argument("-p", "--password", help="Lidl Plus login password")
    parser.add_argument("-r", "--refresh-token", help="refresh token to authenticate")
    subparser = parser.add_subparsers(title="commands", metavar="command", required=True)
    auth = subparser.add_parser("auth", help="authenticate and get refresh_token")
    auth.add_argument("auth", help="authenticate and get refresh_token", action="store_true")
    receipt = subparser.add_parser("receipt", help="last receipt as json")
    receipt.add_argument("receipt", help="last receipt as json", action="store_true")
    receipt.add_argument("-a", "--all", help="fetch all receipts", action="store_true")
    return vars(parser.parse_args())


def check_auth():
    try:
        import oic
        import seleniumwire
        import getpass
    except ImportError:
        print("To login and receive a refresh token you need to install all auth requirements:")
        print("  pip install \"lidl-plus[auth]\"")
        print("You also need google chrome to be installed.")
        exit(1)


def lidl_plus_login(args):
    language = args.get("language") or input("Enter your language (DE, EN, ...): ")
    country = args.get("country") or input("Enter your country (de, at, ...): ")
    if args.get("refresh_token"):
        return LidlPlusApi(language, country, args.get("refresh_token"))
    username = args.get("username") or input("Enter your lidl plus username (phone number): ")
    password = args.get("password") or getpass("Enter your lidl plus password: ")
    check_auth()
    lidl_plus = LidlPlusApi(language, country)
    try:
        lidl_plus.login(username, password, lambda: input("Enter your verify code: "))
    except WebBrowserException:
        print("Can't connect to web browser. Please install Chrome, Chromium or Firefox")
        exit(101)
    return lidl_plus


def print_refresh_token(args):
    lidl_plus = lidl_plus_login(args)
    length = len(token := lidl_plus.refresh_token) - len("refresh token")
    print(f"{'-' * (length // 2)} refresh token {'-' * (length // 2 - 1)}\n{token}\n{'-' * len(token)}")


def print_tickets(args):
    lidl_plus = lidl_plus_login(args)
    if args.get("all"):
        tickets = [lidl_plus.ticket(ticket["id"]) for ticket in lidl_plus.tickets()]
    else:
        tickets = lidl_plus.ticket(lidl_plus.tickets()[0]["id"])
    print(json.dumps(tickets, indent=4))


def main():
    args = get_arguments()
    if args.get("auth"):
        print_refresh_token(args)
    elif args.get("receipt"):
        print_tickets(args)


if __name__ == '__main__':
    main()
