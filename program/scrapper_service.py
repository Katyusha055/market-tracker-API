import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import program.scrapper.web_scrapper as ws
import program.normalizers.normalizer as nz
import program.normalizers.sql_utils as squ
import program.normalizers.validator as val
import program.db_utils.connect as con
import program.db_utils.schema as sch
import program.db_utils.writer as wrt

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

def scrapper_pipeline(pages):
    raw_data = ws.newegg_scrapper(pages)
    normalized_data = []
    for i in raw_data:
        to_append = nz.normalizer(i.get('description'), i.get("price"), i.get('source'))
        #print(to_append)
        validation_flag = val.validator(to_append)
        #print(validation_flag)
        if validation_flag:
            sql_ready = squ.sql_normalizer(to_append)
            normalized_data.append(sql_ready)
            #print(sql_ready)
        else:
            continue
    
    report = {
        'Products Scrapped': 0,
        'Duplicate Products': 0,
        'New Products': 0,
        'Price Data Inserted': 0
    }
    report['Products Scrapped'] = len(normalized_data)
    with con.connect() as conn:
        sch.init_db(conn)

        for i in normalized_data:
            was_new = wrt.write_data(conn, i) #this variable is to know if a product already exists or was added (will be true if it was new)
            if was_new:
                report['New Products'] += 1
            else:
                report['Duplicate Products'] += 1 
            report['Price Data Inserted'] += 1
        
        logging.info('Data inserted into SQL database succesfully')
    return report

