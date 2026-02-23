from dataclasses import asdict

#function to write the data into the database
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
        #query to insert data into products table
        cur.execute('''
        INSERT INTO products (brand, ram_type, speed, total_gb, modules, gb_per_module, source, raw_listing)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (brand, ram_type, speed, total_gb, modules, gb_per_module, source)
        DO NOTHING
        RETURNING id;
        ''', product_values)
        
        result = cur.fetchone()
        was_new = None
        product_id = None
        if result is None:
            unique_values = [
            data['brand'],
            data['ram_type'],
            data['speed'],
            data['total_gb'],
            data['modules'],
            data['gb_per_module'],
            data['source']
            ]
            was_new = False #product already exists if the prior sql query did not return an id
            cur.execute(''' 
            SELECT id
            FROM products
            WHERE brand=%s
            AND ram_type=%s
            AND speed=%s
            AND total_gb=%s
            AND modules=%s
            AND gb_per_module=%s
            AND source=%s
            ''', unique_values) #query to get the id from the product just inserted
            product_id = cur.fetchone()[0]
        else:
            #in case the product is new 
            was_new = True
            product_id = result[0]

        price_history_values = [data['price'], product_id]
        cur.execute(
        '''INSERT INTO price_history (price, product_id)
        VALUES (%s, %s)''', price_history_values  
        ) #query to insert into price_history table

        return was_new

