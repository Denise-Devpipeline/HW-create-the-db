import psycopg2

conn = psycopg2.connect(
    "dbname='DBHomework' user='denisejustice' host='localhost'")
cursor = conn.cursor()
