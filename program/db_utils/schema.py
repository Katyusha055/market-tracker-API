import logging

logger = logging.getLogger(__name__)

#basically initializing the database by creating the tables we'll be using in case they are not created yet
def init_db(connect):
    with connect.cursor() as cur:
        cur.execute('''CREATE TABLE IF NOT EXISTS products (
                    id SERIAL PRIMARY KEY,
                    brand VARCHAR(100) NOT NULL,
                    ram_type VARCHAR(10) NOT NULL,
                    speed INTEGER NOT NULL,
                    total_gb INTEGER NOT NULL,
                    modules INTEGER NOT NULL,
                    gb_per_module INTEGER NOT NULL,
                    source VARCHAR(100) NOT NULL,
                    raw_listing TEXT NOT NULL,

                    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

                    UNIQUE (brand, ram_type, speed, total_gb, modules, gb_per_module, source)
                );''')
        cur.execute('''CREATE TABLE IF NOT EXISTS price_history (
                    id SERIAL PRIMARY KEY,

                    product_id INTEGER NOT NULL,
                    price NUMERIC(10,2) NOT NULL,

                    scraped_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

                    FOREIGN KEY (product_id)
                        REFERENCES products(id)
                        ON DELETE CASCADE
                    );''')
        logger.info('Initialized database succesfully')        
            
