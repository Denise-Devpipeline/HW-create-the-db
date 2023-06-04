import psycopg2

from flask import Flask, request, jsonify

conn = psycopg2.connect("dbname='Users' user='denisejustice' host='localhost'")
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
         active smallint DEFAULT=1
      );
   """)

    cursor.execute("""
     CREATE TABLE IF NOT EXIST Organizations (
        org_id SERIAL PRIMARY KEY,
        name VARCHAR NOT NULL,
        phone VARCHAR,
        city VARCHAR,
        state VARCHAR,
        active smallint
     );
       """)
    print("Creating Tables...")
    conn.commit()


app = Flask(__name__)

# Route to Add User to Database


@app.route('/user/add', methods=['POST'])
def user_add():
    post_data = request.form if request.form else request.get_json
    first_name = post_data.get('first_name')
    last_name = post_data.get('last_name')
    email = post_data.get('email')
    phone = post_data.get('phone')
    city = post_data.get('city')
    state = post_data.get('state')
    org_id = post_data.get('org_id')
    active = post_data.get('active')

    cursor.execute(
        "INSTERT INTO USERS (first_name, last_name, email, phone, city, state, org_id, active) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", [first_name, last_name, email, phone, city, state, org_id, active])
    conn.commit()
    return jsonify("User created"), 201


@app.route('/all-users', method=["GET"])
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


@app.route('/users/get', methods=['GET'])
def all_active_endpoint():
    users = all_active_users()
    return jsonify("This is all the active users John."), 200


create_all()


if __name__ == "__main__":
    create_all()  # run tables
    app.run(port="8086", host="0.0.0.0", debug=True)  # runs flask
