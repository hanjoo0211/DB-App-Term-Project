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
                    cur.execute("SELECT * FROM account WHERE ID = '{}';".format(id))
                    account_info = cur.fetchall()
                    cur.execute("select type, count(code) as traded from trade natural join category group by type order by traded desc")
                    popular_category = cur.fetchall()[0][0]
                    cur.execute("select buyer, sum(trade_price) as sum_buy from trade group by buyer order by sum_buy desc")
                    most_buy_id = cur.fetchall()[0][0]
                    cur.execute("select seller, sum(trade_price) as sum_sell from trade group by seller order by sum_sell desc")
                    most_sell_id = cur.fetchall()[0][0]
                    cur.execute("SELECT * FROM items ORDER BY code, name, price, seller;")
                    items = cur.fetchall()
                    return render_template(
                        "login_success.html", 
                        current_id = id, 
                        account_info = account_info,
                        popular_category = popular_category,
                        most_buy_id = most_buy_id,
                        most_sell_id = most_sell_id,
                        items = items
                        )
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


@app.route('/admin_function', methods=['post'])
def admin_function():
    id = request.form["id"]
    send = request.form["send"]

    if send == 'users info':
        cur.execute("SELECT * FROM users NATURAL JOIN account;")
        users_info = cur.fetchall()
        return render_template("users_info.html", current_id = id, users_info = users_info)
    elif send == 'trades info':
        cur.execute("SELECT * FROM trade;")
        trades_info = cur.fetchall()
        return render_template("trades_info.html", current_id = id, trades_info = trades_info)

    return render_template("main.html")


@app.route('/add_item_page', methods=['post'])
def add_item_page():
    id = request.form["id"]
    cur.execute("SELECT * FROM category;")
    categories = cur.fetchall()
    return render_template("add_item.html", current_id = id, categories = categories)


@app.route('/add_item', methods=['post'])
def add_item():
    id = request.form["id"]
    code = request.form["code"]
    name = request.form["name"]
    price = int(request.form["price"])
    stock = int(request.form["stock"])
    send = request.form["send"]
    
    if send == 'add':
        is_duplicate = False
        cur.execute("SELECT code, name, price, seller, stock FROM items;")
        items = cur.fetchall()
        for item in items:
            if (code, name, price, id) == item[0:4]:
                cur.execute("UPDATE items SET stock = stock + '{}' where code = '{}' and name = '{}' and price = '{}' and seller = '{}';".format(stock, code, name, price, id))
                is_duplicate = True
        if not is_duplicate:
            cur.execute("INSERT INTO items VALUES('{}', '{}', '{}', '{}', '{}');".format(code, name, price, stock, id))
        connect.commit()
    
    cur.execute("SELECT * FROM account WHERE ID = '{}';".format(id))
    account_info = cur.fetchall()
    cur.execute("select type, count(code) as traded from trade natural join category group by type order by traded desc")
    popular_category = cur.fetchall()[0][0]
    cur.execute("select buyer, sum(trade_price) as sum_buy from trade group by buyer order by sum_buy desc")
    most_buy_id = cur.fetchall()[0][0]
    cur.execute("select seller, sum(trade_price) as sum_sell from trade group by seller order by sum_sell desc")
    most_sell_id = cur.fetchall()[0][0]
    cur.execute("SELECT * FROM items ORDER BY code, name, price, seller;")
    items = cur.fetchall()
    return render_template(
        "login_success.html", 
        current_id = id, 
        account_info = account_info,
        popular_category = popular_category,
        most_buy_id = most_buy_id,
        most_sell_id = most_sell_id,
        items = items
        )


@app.route('/buy_item_page', methods=['post'])
def buy_item_page():
    id = request.form["id"]
    code = request.form["code"]
    name = request.form["name"]
    price = request.form["price"]
    stock = request.form["stock"]
    seller = request.form["seller"]  
    cur.execute("SELECT * FROM account WHERE ID = '{}';".format(id))
    account_info = cur.fetchall()
    return render_template(
        "buy_item.html",
        current_id = id,
        code = code,
        name = name,
        price = price,
        stock = stock,
        seller = seller,
        account_info = account_info
        )


@app.route('/buy_item', methods=['post'])
def buy_item():
    id = request.form["id"]
    code = request.form["code"]
    name = request.form["name"]
    price = int(request.form["price"])
    stock = int(request.form["stock"])
    seller = request.form["seller"] 
    how_many = int(request.form["how_many"])

    cur.execute("SELECT * FROM account WHERE ID = '{}';".format(id))
    account_info = cur.fetchall()
    total_price = price * how_many
    cur.execute("select discount from account natural join rating_info where id = '{}'".format(id))
    discount_rate = cur.fetchall()[0][0]
    discount_price = total_price * discount_rate // 100
    final_price = total_price - discount_price
    
    if how_many > stock:
        return render_template("error.html", current_id = id, error_messege = "You picked more than stock!")
    elif final_price > int(account_info[0][1]):
        return render_template("error.html", current_id = id, error_messege = "Your balance is less than final price!")
    else:
        return render_template(
        "trade_item.html",
        current_id = id,
        code = code,
        name = name,
        price = price,
        stock = stock,
        seller = seller,
        account_info = account_info,
        how_many = how_many,
        total_price = total_price,
        discount_price = discount_price,
        final_price = final_price
        )


@app.route('/confirm_trade', methods=['post'])
def confirm_trade():
    id = request.form["id"]
    code = request.form["code"]
    name = request.form["name"]
    price = int(request.form["price"])
    stock = int(request.form["stock"])
    seller = request.form["seller"] 
    how_many = int(request.form["how_many"])
    total_price = int(request.form["total_price"])
    final_price = int(request.form["final_price"])

    cur.execute("UPDATE account SET balance = balance - '{}' where id = '{}';".format(final_price, id))
    cur.execute("UPDATE account SET balance = balance + '{}' where id = '{}';".format(total_price, seller))

    cur.execute("SELECT balance FROM account WHERE ID = '{}';".format(id))
    buyer_balance = cur.fetchall()[0][0]
    cur.execute("SELECT balance FROM account WHERE ID = '{}';".format(seller))
    seller_balance = cur.fetchall()[0][0]

    cur.execute("SELECT rating, condition FROM rating_info WHERE condition < '{}' order by condition desc;".format(buyer_balance))
    buyer_rating = cur.fetchall()[0][0]
    cur.execute("SELECT rating, condition FROM rating_info WHERE condition < '{}' order by condition desc;".format(seller_balance))
    seller_rating = cur.fetchall()[0][0]

    cur.execute("UPDATE account SET rating = '{}' where id = '{}';".format(buyer_rating, id))
    cur.execute("UPDATE account SET rating = '{}' where id = '{}';".format(seller_rating, seller))

    cur.execute("INSERT INTO trade VALUES('{}', '{}', '{}', '{}');".format(id, seller, code, total_price))
    if how_many == stock:
        cur.execute("DELETE FROM items WHERE code = '{}' and name = '{}' and price = '{}' and seller = '{}';".format(code, name, price, seller))
    else:
        cur.execute("UPDATE items SET stock = stock - '{}' where code = '{}' and name = '{}' and price = '{}' and seller = '{}';".format(how_many, code, name, price, seller))

    connect.commit()

    cur.execute("SELECT * FROM account WHERE ID = '{}';".format(id))
    account_info = cur.fetchall()
    cur.execute("select type, count(code) as traded from trade natural join category group by type order by traded desc")
    popular_category = cur.fetchall()[0][0]
    cur.execute("select buyer, sum(trade_price) as sum_buy from trade group by buyer order by sum_buy desc")
    most_buy_id = cur.fetchall()[0][0]
    cur.execute("select seller, sum(trade_price) as sum_sell from trade group by seller order by sum_sell desc")
    most_sell_id = cur.fetchall()[0][0]
    cur.execute("SELECT * FROM items ORDER BY code, name, price, seller;")
    items = cur.fetchall()
    return render_template(
        "login_success.html", 
        current_id = id, 
        account_info = account_info,
        popular_category = popular_category,
        most_buy_id = most_buy_id,
        most_sell_id = most_sell_id,
        items = items
        )

@app.route('/error_return', methods=['post'])
def error_return():
    id = request.form["id"]
    cur.execute("SELECT * FROM account WHERE ID = '{}';".format(id))
    account_info = cur.fetchall()
    cur.execute("select type, count(code) as traded from trade natural join category group by type order by traded desc")
    popular_category = cur.fetchall()[0][0]
    cur.execute("select buyer, sum(trade_price) as sum_buy from trade group by buyer order by sum_buy desc")
    most_buy_id = cur.fetchall()[0][0]
    cur.execute("select seller, sum(trade_price) as sum_sell from trade group by seller order by sum_sell desc")
    most_sell_id = cur.fetchall()[0][0]
    cur.execute("SELECT * FROM items ORDER BY code, name, price, seller;")
    items = cur.fetchall()
    return render_template(
        "login_success.html", 
        current_id = id, 
        account_info = account_info,
        popular_category = popular_category,
        most_buy_id = most_buy_id,
        most_sell_id = most_sell_id,
        items = items
        )

if __name__ == '__main__':
    app.run()
