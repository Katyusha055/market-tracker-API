import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import program.scrapper.web_scrapper as ws
import program.normalizers.normalizer as nz
import program.normalizers.sql_utils as squ
import program.normalizers.validator as val

#setting up the logging system
def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

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
    if not root.handlers:
        root.setLevel(logging.DEBUG)
        root.addHandler(file_handler)
        root.addHandler(console)

setup_logging()

raw_data = ws.newegg_scrapper()
normalized_data = []
for i in raw_data:
    to_append = nz.normalizer(i.get('description'), i.get("price"), i.get('source'))
    print(to_append)
    validation_flag = val.validator(to_append)
    print(validation_flag)
    if validation_flag:
        sql_ready = squ.sql_normalizer(to_append)
        normalized_data.append(sql_ready)
        print(sql_ready)
    else:
        continue

