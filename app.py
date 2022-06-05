import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)
connect = psycopg2.connect("dbname=term user=postgres password=0000")
cur = connect.cursor()  # create cursor


@app.route('/')
def main():
    return render_template("main.html")


@app.route('/return', methods=['post'])
def re_turn():
    return render_template("main.html")


@app.route('/print_table', methods=['post'])
def print_table():
    cur.execute("SELECT * FROM users;")
    result = cur.fetchall()

    return render_template("print_table.html", users=result)


@app.route('/register', methods=['post'])
def register():
    id = request.form["id"]
    password = request.form["password"]
    send = request.form["send"]

    if send == 'login':
        is_user = False
        cur.execute("SELECT * FROM users;")
        user_data = cur.fetchall()
        for user in user_data:
            if id == user[0]:
                is_user = True
                if password == user[1]:
                    return render_template("login_success.html")
                else:
                    return render_template("login_fail.html")
        if is_user is False:
            return render_template("login_fail.html")

    elif send == 'sign up':
        is_id_duplicate = False
        cur.execute("SELECT id FROM users;")
        user_data = cur.fetchall()
        for user_id in user_data:
            if id == user_id[0]:
                is_id_duplicate = True
                return render_template("ID_collision.html")
        if not is_id_duplicate:
            cur.execute("INSERT INTO users VALUES('{}', '{}');".format(id, password))
            cur.execute("INSERT INTO account VALUES('{}', 10000, 'beginner');".format(id))
            connect.commit()
            return render_template("register_success.html")

    # return id + " " + password + " " + send


if __name__ == '__main__':
    app.run()
