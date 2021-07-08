import os
from pathlib import Path

amazon_uris = {
    "US": "https://music.amazon.com",
    "IT": "https://music.amazon.it",
    "FR": "https://music.amazon.fr",
    "DE": "https://music.amazon.de",
    "ES": "https://music.amazon.es"
}

cookies_path = f"{Path.home()}/.cache/cookies.sqlite"

if "IS_FLATPAK" in os.environ:
    cookies_path = f"{Path.home()}/.var/app/{os.environ['FLATPAK_ID']}/data/cookies.sqlite"

if "SNAP" in os.environ:
    cookies_path = f"{os.environ['SNAP_USER_DATA']}/cookies.sqlite"
