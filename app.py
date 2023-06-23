from flask import Flask, request, jsonify
from conn import *
import users
import orgs

app = Flask(__name__)


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
         active smallint DEFAULT 1
      );
   """)

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
        FOREIGN KEY(user_id) REFERENCES Users(user_id),
        FOREIGN KEY(org_id) REFERENCES Organizations(org_id),
        PRIMARY KEY(user_id, org_id)
        );

      """)

    conn.commit()
    print("Creating Tables...")


# @app.route('/user/create', methods=['POST'])
# def user_create():
#     post_data = request.form if request.form else request.json
#     return users.user_create(post_data)


# @app.route('/all-active-users', methods=["GET"])
# def all_active_users():
#     return users.all_active_users()


# @app.route('/users/<id>', methods=['GET'])
# def get_user_by_id(id):
#     return users.get_user_by_id(id)


# @app.route('/user/activate/<id>', methods=["PATCH"])
# def activate_user(id):
#     return users.activate_user(id)


# @app.route('/user/deactivated/<id>', methods=["PATCH"])
# def deactivate_user(id):
#     return users.deactivate_user(id)


# @app.route('/user/update/<id>', methods=["PUT"])
# def user_update_by_id(id):
#     post_data = request.form if request.form else request.json
#     return users.user_update_by_id(id, post_data)


# @app.route('/user/delete/<id>', methods=["DELETE"])
# def delete_user(id):
#     return users.delete_user(id)


# # ORGANIZATIONS


# @app.route('/organization/create', methods=['POST'])
# def org_create():
#     post_data = request.form if request.form else request.json
#    #  return post_data
#     return orgs.org_create(post_data)


# @app.route('/all-active-orgs', methods=["GET"])
# def all_active_orgs():
#     return orgs.all_active_orgs()


# @app.route('/organizations/<org_id>', methods=['GET'])
# def get_org_by_id(org_id):
#     return orgs.get_org_by_id(org_id)


@app.route('/org/activate/<org_id>', methods=["PATCH"])
def activate_org(org_id):
    return orgs.activate_org(org_id)


# @app.route('/org/deactivated/<org_id>', methods=["PATCH"])
# def deactivate_org(org_id):
#     return orgs.deactivate_org(org_id)


# @app.route('/org/update/<org_id>', methods=["PUT"])
# def org_update_by_id(org_id):
#     post_data = request.form if request.form else request.json
#     return orgs.org_update_by_id(org_id, post_data)


# @app.route('/org/delete/<org_id>', methods=["DELETE"])
# def delete_org(org_id):
#     return orgs.delete_org(org_id)


if __name__ == "__main__":
    create_all()  # run tables
    app.run(port="8084", host="0.0.0.0", debug=True)  # runs flask
