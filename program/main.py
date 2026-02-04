import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import web_scrapper as ws
import normalizer as nz

#setting up the logging system
def setup_logging():
    log_dir = Path("logs")

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(logging.INFO)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(file_handler)
    root.addHandler(console)

raw_data = ws.newegg_scrapper()
normalized_strings = []

for i in raw_data:
    to_append = nz.normalizer(i.get('description'), i.get("price"))
    normalized_strings.append(to_append)

print(normalized_strings)