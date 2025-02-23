import psycopg2


conn = psycopg2.connect(
    dbname="vectordb_db",
    user="postgres",
    host="localhost",
    port="5432",
    password='postgres'
)
cur = conn.cursor()