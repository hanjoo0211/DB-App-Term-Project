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
                    return "ID " + id + " has logged in"
                else:
                    return "Incorrect Password"
        if is_user is False:
            return "Incorrect ID"

    elif send == 'sign up':
        cur.execute("INSERT INTO users VALUES('{}', '{}');".format(id, password))
        connect.commit()
        return "ID " + id + " has signed up"

    # return id + " " + password + " " + send


if __name__ == '__main__':
    app.run()
