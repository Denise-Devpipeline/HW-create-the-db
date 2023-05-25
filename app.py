import psycopg2
from flask import Flask, request, jsonify

conn = psycopg2.connect("dbname='users' user='denisejustice' host='localhost'")
cursor = conn.cursor()


def create_all():
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS Users (
         user_id SERIAL PRIMARY KEY,
         first_name VARCHAR NOT NULL,
         last_name VARCHAR,
         email VARCHAR NOT NULL UNIQUE,
         phone VARCHAR,
         city VARCHAR,
         state VARCHAR,
         org_id int,
         active smallint
      );
   """)

    conn.commit()


def all_active_users():
    cursor.execute("SELECT * FROM Users WHERE active =1")
    results = cursor.fetchall()
    if not results:
        return jsonify("No active users to return"), 404
    users_result = []
    for row in rows:
        user = {
            'user_id': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'email': row[3],
            'phone': row[4],
            'city': row[5],
            'state': row[6],
            'orig_id': row[7],
            'active': row[8]
        }


app = Flask(__name__)


@app.route('/users/get', methods=['GET'])
def all_active_endpoint():
    users = all_active_users()
    return jsonify("This is all the active users John."), 200


create_all()


if __name__ == "__main__":
    app.run(port="8086", host="0.0.0.0")
