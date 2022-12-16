# Create Environment
# pip install flask
# pip install pymysql
# pip install flask-mysql

from flask import Flask, jsonify, request, session
import pymysql
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY="secret_sauce",
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",
)

# connect database
mysql = MySQL()
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "Develope@123"
app.config["MYSQL_DATABASE_DB"] = "auction"
app.config["MYSQL_DATABASE_HOST"] = "127.0.0.1"
mysql.init_app(app)


# login
@app.route("/api2/login", methods=["POST"])
def login():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        query = "SELECT * FROM user WHERE email = %s AND password = %s"
        bind = (request.json["email"], request.json["password"])
        cursor.execute(query, bind)
        user = cursor.fetchone()
        if user["email"]:
            session["user"] = user
            return jsonify({"login": True})
    except Exception as e:
        return jsonify({"login": False})
    finally:
        cursor.close()
        conn.close()


# check if logged in
@app.route("/api2/login", methods=["GET"])
def check_session():
    if session.get("user"):
        return jsonify({"login": True})

    return jsonify({"login": False})


# logout
@app.route("/api2/login", methods=["DELETE"])
def logout():
    session["user"] = {}
    return jsonify({"logout": True})


# get current user
@app.route("/api2/user", methods=["GET"])
def user_data():
    if session.get("user"):
        return jsonify({session["user"]})

    return jsonify({"login": False})


# this route should only work if logged in
@app.route("/api2/protected-data", methods=["GET"])
def protected_data():
    if session["user"]:
        return jsonify({"get-this-data": "Only if logged in"})

    return jsonify({"login": False})


# this route should work even if you are not logged in
@app.route("/api2/unprotected-data", methods=["GET"])
def unprotected_data():
    return jsonify({"get-this-data": "Even if you are logged out"})


@app.route("/api2/user", methods=["POST"])
def insert_user():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        query = "INSERT INTO user SET firstname = %s, lastname = %s, email = %s, password = %s"
        bind = (
            request.json["firstname"],
            request.json["lastname"],
            request.json["email"],
            request.json["password"],
        )
        cursor.execute(query, bind)
        conn.commit()

        return jsonify({"data": cursor.lastrowid})
    except Exception as e:
        print(e)
        return jsonify({"error couldnot type user"})
    finally:
        cursor.close()
        conn.close()


@app.route("/api2/users", methods=(["GET"]))
def get_user():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM user")
        rows = cursor.fetchall()
        # print(rows)
        response = jsonify(rows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route("/api2/listdesc", methods=(["GET"]))
def get_desc():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute(
            "SELECT id,name,SUBSTRING(Description,1,20) FROM  autction_object"
        )

        rows = cursor.fetchall()
        # print(rows)
        response = jsonify(rows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route("/api2/detailpage", methods=(["GET"]))
def get_detailpage():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM  autction_object")

        rows = cursor.fetchall()
        # print(rows)
        response = jsonify(rows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route("/api2/insertitem", methods=["POST"])
def insert_item():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        query = "INSERT INTO autction_object SET name = %s, Description = %s, start_time = %s, end_time = %s, user = %s"
        bind = (
            request.json["name"],
            request.json["Description"],
            request.json["start_time"],
            request.json["end_time"],
            request.json["user"],
        )
        cursor.execute(query, bind)
        conn.commit()

        return jsonify({"data": cursor.lastrowid})
    except Exception as e:
        print(e)
        return jsonify({"error couldnot type user"})
    finally:
        cursor.close()
        conn.close()


@app.route("/api2/currentbid", methods=(["GET"]))
def get_currentbid():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute(
            "SELECT name,description,start_time, end_time,bid.price, autction_object.id from autction_object LEFT JOIN bid ON bid.autction_object=bid.id"
        )

        rows = cursor.fetchall()
        # print(rows)
        response = jsonify(rows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route("/api2/5recentbid", methods=(["GET"]))
def get_recentbid():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute(
            "SELECT * from bid join autction_object on bid.autction_object = autction_object.id where autction_object.id = 5 order by price desc limit 5"
        )

        rows = cursor.fetchall()
        # print(rows)
        response = jsonify(rows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route("/api2/updatebid", methods=["POST"])
def updatebid():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        query = "SELECT price, user_id FROM bid WHERE autction_object = %s ORDER BY price LIMIT 5"
        bind = request.json["autction_object"]
        cursor.execute(query, bind)
        biditem = cursor.fetchone()
        if not (biditem["user_id"] == request.json["user_id"]):
            if biditem["price"] < request.json["price"]:
                query = "UPDATE bid SET price = %s WHERE autction_object = %s"
                bind = (request.json["price"], request.json["autction_object"])
                cursor.execute(query, bind)
                conn.commit()
                return jsonify({"updated": "your bid have been registred! "})
            else:
                return jsonify({"updated": "you need to put a heigher bid! "})
        else:
            return jsonify({"updated": "you can't bid on your own items"})
    except Exception as e:
        return jsonify({"update": str(e)})
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(debug=True, load_dotenv=True)
