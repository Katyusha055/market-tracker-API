import program.db_utils.connect as con
import program.db_utils.schema as sch
import program.db_utils.writer as wrt
from program.normalizers.sql_utils import sql_normalizer 
import pytest
import psycopg
from dotenv import load_dotenv
import os
from pathlib import Path

#fixtures for the test session
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(env_path)
@pytest.fixture(scope='session')
def setup_test_database():
    #admin conn to create test database
    admin_conn = psycopg.connect(
        dbname = os.getenv('DB_NAME'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        host = os.getenv('DB_HOST'),
        port = os.getenv('DB_PORT')
    )

    admin_conn.autocommit = True

    with admin_conn.cursor() as cur:
        cur.execute('''
            SELECT 1 FROM pg_database 
            WHERE datname = 'market_tracker_tests';                  
''')
        exists = cur.fetchone()
        if not exists:
            cur.execute('''
            CREATE DATABASE market_tracker_tests;
''')
    admin_conn.close()
    yield 
    #basically if the database for testing does not exists yet it will create one, if it already does it won't do anything

#fixture to connect to the test database on each test
@pytest.fixture(scope='function')
def db_connection(setup_test_database):
    conn = psycopg.connect(
        dbname = 'market_tracker_tests',
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        host = os.getenv('DB_HOST'),
        port = os.getenv('DB_PORT')
    )

    with conn.cursor() as cur:
        cur.execute('''
        BEGIN;
''')
    yield conn

    with conn.cursor() as cur:
        cur.execute('''
        ROLLBACK;
''')
    conn.close()
        
#testing the entire pipeline, the reason of why I'm doing just a few 
#tests is (or will be) explained in dev_notes.md
def test_1 (db_connection):
    test = [{'Ram Quantity': ['16'], 'Ram Type': ['DDR4'], 'Ram Speed': ['3200'], 'Ram Brand': ['G.Skill'], 'Original String': 'G.SKILL Ripjaws V Series 16GB 288-Pin PC RAM DDR4 3200 (PC4 25600) Desktop Memory Model F4-3200C16S-16GVK', 'Price': '$129.99–', 'Source': 'Newegg'},
            {'Ram Quantity': ['32', '16'], 'Ram Type': ['DDR5'], 'Ram Speed': ['6000'], 'Ram Brand': ['Corsair'], 'Original String': 'CORSAIR Vengeance RGB 32GB (2 x 16GB) 288-Pin PC RAM DDR5 6000 (PC5 48000) Desktop Memory Model CMH32GX5M2E6000C36W', 'Price': '$439.99–', 'Source': 'Newegg'},
            {'Ram Quantity': ['32', '16'], 'Ram Type': ['DDR5'], 'Ram Speed': ['6000'], 'Ram Brand': ['Crucial'], 'Original String': 'Crucial Pro Overclocking 32GB (2 x 16GB) DDR5 6000 (PC5 48000) Desktop Memory Model CP2K16G60C36U5B', 'Price': '$399.99–', 'Source': 'Newegg'}]
    data = [sql_normalizer(i) for i in test]
    conn = db_connection
    for i in data:
        sch.init_db(conn)
        was_new = wrt.write_data(conn, i)
        assert was_new == True #testing if the products were recognized as new
    assert wrt.write_data(conn, data[0]) == False #product was already inserted and is recognized as that
    
    with conn.cursor() as cur:
        cur.execute('''
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'products';
''')
        columns = {
            row[0] for row in cur.fetchall()
        }
        expected = {
            'id', 'brand', 'ram_type', 'speed', 'total_gb', 'modules', 'gb_per_module', 'source', 'raw_listing', 'created_at'
        }
        assert columns == expected #testing if the table products was created correctly

    with conn.cursor() as cur:
        cur.execute('''
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'price_history';
''')
        columns = {
            row[0] for row in cur.fetchall()
        }
        expected = {
            'id', 'product_id', 'price', 'scraped_at'
        }
        assert columns == expected #testing if the table price history was created correctly
    
    with conn.cursor() as cur:
        cur.execute('''
                    SELECT COUNT(*) FROM products;
''')
        count = cur.fetchone()[0]
        assert count == 3 #there must be 3 products inserted into the table products per the test data

    with conn.cursor() as cur:
        cur.execute('''
                    SELECT COUNT(*) FROM price_history;
''')
        count = cur.fetchone()[0]
        assert count == 4 #there must be 4 products inserted into the table price_history per the test data

    with conn.cursor() as cur:
        cur.execute('''
                    SELECT ph.id
                    FROM price_history ph
                    LEFT JOIN products p ON ph.product_id = p.id
                    WHERE p.id IS NULL
''')
        result = cur.fetchone()
        assert not result #this query tests the FK in the database so every product_id actually comes from the products table