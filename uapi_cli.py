#!/usr/bin/env python3
import argparse
import os
import sys
import webbrowser
import json
from pathlib import Path
from uapi import uAPI, APIError

RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
GREY = "\033[90m"

CONFIG_DIR = Path.home() / ".uapi"
CONFIG_FILE = CONFIG_DIR / "config.json"


def save_api_key(api_key: str):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"api_key": api_key}, f)
    print(f"{GREEN}✓ API key saved to {CONFIG_FILE}{RESET}")


def load_api_key() -> str | None:
    # 1. Prefer environment variable
    env_key = os.getenv("UAPI_API_KEY")
    if env_key:
        return env_key

    # 2. Try to load from config file
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text())
            return data.get("api_key")
        except Exception:
            pass

    return None


def get_api_key():
    api_key = load_api_key()
    if api_key:
        return api_key

    print(f"{YELLOW}No API key found.{RESET}")
    print("You can create or retrieve your key here:")
    print(f"{CYAN}https://uapi.nl/api{RESET}\n")

    try:
        webbrowser.open("https://uapi.nl/api", new=2)
        print("(Opened https://uapi.nl/api in your browser.)\n")
    except Exception:
        print("(Please visit https://uapi.nl/api manually.)\n")

    api_key = input(f"{BOLD}Enter your UAPI API key:{RESET} ").strip()
    if not api_key:
        print(f"{YELLOW}No key entered. Exiting.{RESET}")
        sys.exit(1)

    save_api_key(api_key)
    return api_key


def pretty_dict(d, indent=0):
    pad = " " * indent
    for key, value in d.items():
        if isinstance(value, dict):
            print(f"{pad}{BOLD}{CYAN}{key}:{RESET}")
            pretty_dict(value, indent + 2)
        elif isinstance(value, list):
            print(f"{pad}{BOLD}{CYAN}{key}:{RESET}")
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    print(f"{pad}  {GREY}[{i+1}]{RESET}")
                    pretty_dict(item, indent + 4)
                else:
                    print(f"{pad}  {GREEN}{item}{RESET}")
        else:
            print(f"{pad}{CYAN}{key:<25}{RESET}: {GREEN}{value}{RESET}")


def extract(url: str):
    api_key = get_api_key()
    try:
        client = uAPI(api_key=api_key)
        resp = client.extract(url=url)
        data = resp.get("data", {})
        print(f"{BOLD}{MAGENTA}=== Extracted Data ==={RESET}\n")
        if not data:
            print(f"{YELLOW}No data returned.{RESET}")
        else:
            pretty_dict(data)
    except APIError as e:
        print(f"[ERROR] {e.__class__.__name__}: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[UNEXPECTED ERROR] {e}", file=sys.stderr)
        sys.exit(1)


def search(query: str):
    api_key = get_api_key()
    try:
        client = uAPI(api_key=api_key)
        resp = client.search(query=query)
        data = resp.get("data", {})
        print(f"{BOLD}{MAGENTA}=== Answer ==={RESET}\n")
        answer = data.get("answer_text")
        if answer:
            print(f"{GREEN}{answer}{RESET}\n")
        else:
            print(f"{YELLOW}No answer found.{RESET}\n")
        sources = data.get("sources", [])
        if sources:
            print(f"{BOLD}{MAGENTA}=== Sources ==={RESET}")
            for s in sources:
                title = s.get("title", "Untitled source")
                url = s.get("url", "N/A")
                print(f"• {BOLD}{title}{RESET} — {CYAN}{url}{RESET}")
    except APIError as e:
        print(f"[ERROR] {e.__class__.__name__}: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[UNEXPECTED ERROR] {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(prog="uapi", description="uAPI SDK Console Utility")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_extract = subparsers.add_parser("extract", help="Extract structured data from a URL")
    p_extract.add_argument("url")

    p_search = subparsers.add_parser("search", help="Perform a web search or ask a question")
    p_search.add_argument("query", nargs="+")

    args = parser.parse_args()

    if args.command == "extract":
        extract(args.url)
    elif args.command == "search":
        search(" ".join(args.query))


if __name__ == "__main__":
    main()
