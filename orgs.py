from flask import Flask, request, jsonify
from conn import *


def create_all():
    cursor.execute("""
     CREATE TABLE IF NOT EXISTS Organizations (
        org_id SERIAL PRIMARY KEY,
        name VARCHAR NOT NULL,
        phone VARCHAR,
        city VARCHAR,
        state VARCHAR,
        active smallint
     );
       """)

    cursor.execute("""
      CREATE TABLE IF NOT EXISTS UsersOrganizationsXref (
        user_id INT,
        org_id INT,
        FOREIGN KEY(user_id) REFERENCES(Users(user_id),
        FOREIGN KEY(org_id)REFERENCES Organizations(org_id),
        PRIMARY KEY(user_id, org_id)
        );

      """)

    conn.commit()
    print("Creating Tables...")


app = Flask(__name__)


@app.route('/organization/create', methods=['POST'])
def org_create():
    post_data = request.form if request.form else request.get_json
    name = post_data.get('first_name')
    phone = post_data.get('phone')
    city = post_data.get('city')
    state = post_data.get('state')
    active = post_data.get('active')

    cursor.execute(
        """INSERT INTO ORGANIZATIONS (name, phone, city, state, active) VALUES (%s,%s,%s,%s,%s)""", [name, phone, city, state, active])
    org_id = cursor.fetchone()[0]
    conn.commit()
    return jsonify({"Organization Created": org_id}),  201


@app.route('/all-active-orgs', methods=["GET"])
def all_active_orgs():
    # why wouldn't this work?
    cursor.execute("SELECT * FROM orgs WHERE active =1")
    results = cursor.fetchall()
    if not results:
        return jsonify("No active orgs to return"), 404
    else:
        active_orgs_result = []
        for result in results:
            results_dict = {
                'org_id': result[0],
                'first_name': result[1],
                'last_name': result[2],
                'email': result[3],
                'phone': result[4],
                'city': result[5],
                'state': result[6],
                'orig_id': result[7],
                'active': result[8]
            }
            active_orgs_result.append(results_dict)
        return jsonify(active_orgs_result), 200

# FIX THIS SECTION......


@app.route('/organizations/<org_id>', methods=['GET'])
def get_org_by_id(org_id):
    cursor.execute("SELECT name, phone, city, state, active FROM Organizations WHERE org_id = %s;",
                   [org_id])
    result = cursor.fetchone()
    if not result:
        return jsonify("That organization does not exist."), 404
    else:
        results_dict = {
            'org_id': result[0],
            'name': result[1],
            'phone': result[2],
            'city': result[3],
            'state': result[4],
            'active': result[5]
        }
        return jsonify(results_dict), 200


@app.route('/org/activate/<org_id>', methods=["PATCH"])
def activate_org(org_id):
    cursor.execute(
        "UPDATE Organizations SET active = 1 WHERE org_id = %s", [org_id])
    conn.commit()
    return jsonify("Organization Activated!"), 200


@app.route('/org/deactivated/<org_id>', methods=["PATCH"])
def deactivate_org(org_id):
    cursor.execute(
        "UPDATE Organizations SET active = 0 WHERE org_id = %s", [org_id])
    conn.commit()
    return jsonify("Organization Deactivated!"), 200


@app.route('/org/update/<org_id>', methods=["PUT"])
def org_update_by_id(org_id):
    cursor.execute("SELECT name, phone, city, state, active FROM orgs WHERE org_id = %s;",
                   [org_id])
    result = cursor.fetchone()
    if not result:
        return jsonify("Organization does not exist."), 404
    else:
        result_dict = {
            'org_id': result[0],
            'name': result[1],
            'phone': result[2],
            'city': result[3],
            'state': result[4],
            'active': result[5]
        }
    post_data = request.form if request.form else request.json

    for key, val in post_data.copy().items():
        if not val:
            post_data.pop(key)
    result_dict.update(post_data)

    cursor.execute('''UPDATE Organizations SET 
    name = %s,
    phone = %s,
    city = %s,
    state = %s,
    active = %s

    WHERE org_id = %s;
    ''',
                   [result_dict['name'],
                    result_dict['phone'],
                    result_dict['city'],
                    result_dict['state'],
                    result_dict['active']])
    conn.commit()
    return jsonify("Organization Updated!")


@app.route('/org/delete/<org_id>', methods=["DELETE"])
def delete_org(org_id):
    cursor.execute("DELETE FROM Organizations WHERE org_id = %s", [org_id])
    conn.commit()
    return jsonify("Organization Deleted!"), 200
