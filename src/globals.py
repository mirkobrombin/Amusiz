import os
from pathlib import Path

amazon_uri = "https://music.amazon.it"
cookies_path = f"{Path.home()}/.cache/cookies.txt"

if "SNAP" in os.environ:
    cookies_path = f"{os.environ['SNAP_USER_DATA']}/cookies.txt"
