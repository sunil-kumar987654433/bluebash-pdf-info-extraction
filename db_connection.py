import psycopg2
import os
import logging
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(filename="error_file.log",
                    format='%(asctime)s %(message)s',
                    filemode='a',
                    level=logging.INFO
                    )
cur = None
conn = None

try:
    conn = psycopg2.connect(
        dbname= os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT"),
        password=os.environ.get("DB_PASSWORD")
    )
    
    cur = conn.cursor()
    logging.info("Connection successful!")
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    conn.commit()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS items(
        id SERIAL PRIMARY KEY,
        content TEXT,
        embeding VECTOR(1536)
    )""")

    conn.commit()
except Exception as e:
    logging.exception("exception: ", e)
    if cur:
        cur.close()
    if conn:
        conn.close()

if conn is None:
    logging.error("database not connected.")
else:
    logging.info("Database operations completed successfully.")





