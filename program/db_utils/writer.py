from dataclasses import asdict

def write_data(conn, ram_obj):
    data = asdict(ram_obj)
    
    with conn.cursor() as cur:
        product_values = [
            data['brand'],
            data['ram_type'],
            data['speed'],
            data['total_gb'],
            data['modules'],
            data['gb_per_module'],
            data['source'],
            data['raw_listing']
        ]
        cur.execute('''
        INSERT INTO products (brand, ram_type, speed, total_gb, modules, gb_per_module, source, raw_listing)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (brand, ram_type, speed, total_gb, modules, gb_per_module, source)
        DO UPDATE SET brand = EXCLUDED.brand
        RETURNING id;
        ''', product_values)
        result = cur.fetchone()
        price_history_values = [data['price'], result[0]]
        cur.execute(
        '''INSERT INTO price_history (price, product_id)
        VALUES (%s, %s)''', price_history_values
        )

