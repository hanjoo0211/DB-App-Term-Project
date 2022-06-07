# DB App Term Project Report

## Schema Diagram

![schema_diagram.png](DB%20App%20Term%20Project%20Report%203c3ece1c8e014660a2d70eed6742d77a/schema_diagram.png)

## HTML / Functions

> `main.html`
> 

![Untitled](DB%20App%20Term%20Project%20Report%203c3ece1c8e014660a2d70eed6742d77a/Untitled.png)

## `register()`

로그인 화면에서 `login`시 id와 password를 대조하여 로그인 성공과 실패 여부를 구분합니다. 성공 시 다음 화면으로 이동하며 실패 시 에러 창이 뜨고 다시 로그인 창으로 돌아옵니다.

또한 다음 메인 화면에서 띄워줄 정보들을 SQL문으로 받아옵니다.

```python
cur.execute("SELECT * FROM account WHERE ID = '{}';".format(id))
account_info = cur.fetchall()
```

계정 정보를 띄워주기 위해 account 테이블에서 정보를 받아옵니다.

```python
cur.execute("select type, count(code) as traded from trade natural join category group by type order by traded desc")
popular_category = cur.fetchall()[0][0]
cur.execute("select buyer, sum(trade_price) as sum_buy from trade group by buyer order by sum_buy desc")
most_buy_id = cur.fetchall()[0][0]
cur.execute("select seller, sum(trade_price) as sum_sell from trade group by seller order by sum_sell desc")
most_sell_id = cur.fetchall()[0][0]
```

popular category, best buyer, best seller를 표시하기 위한 정보를 받아옵니다.

```python
cur.execute("SELECT * FROM items ORDER BY code, name, price, seller;")
items = cur.fetchall()
```

판매중인 상품들을 표시하기 위한 정보를 받아옵니다.

로그인 화면에서 `register`를 누를 시 입력한 id와 password대로 가입합니다. 만약 같은 id가 있을 시 가입에 실패합니다.

```python
cur.execute("INSERT INTO users VALUES('{}', '{}');".format(id, password))
cur.execute("INSERT INTO account VALUES('{}', 10000, 'beginner');".format(id))
connect.commit()
```

중복된 id가 없을 시 users 테이블과 account 테이블에 새로운 계정 정보를 삽입합니다.

> `login_success.html`
> 

admin으로 접속 시

![Untitled](DB%20App%20Term%20Project%20Report%203c3ece1c8e014660a2d70eed6742d77a/Untitled%201.png)

일반 user로 접속 시

![Untitled](DB%20App%20Term%20Project%20Report%203c3ece1c8e014660a2d70eed6742d77a/Untitled%202.png)

## `admin_function()`

admin 계정으로 접속 시 볼 수 있는 부분입니다.

> `users_info.html`
> 

![Untitled](DB%20App%20Term%20Project%20Report%203c3ece1c8e014660a2d70eed6742d77a/Untitled%203.png)

```python
if send == 'users info':
cur.execute("SELECT * FROM users NATURAL JOIN account;")
users_info = cur.fetchall()
return render_template("users_info.html", current_id = id, users_info = users_info)
```

`users info`를 누르면 모든 계정 정보를 볼 수 있습니다.

> `trades_info.html`
> 

![Untitled](DB%20App%20Term%20Project%20Report%203c3ece1c8e014660a2d70eed6742d77a/Untitled%204.png)

```python
elif send == 'trades info':
cur.execute("SELECT * FROM trade;")
trades_info = cur.fetchall()
return render_template("trades_info.html", current_id = id, trades_info = trades_info)
```

`trades info`를 누르면 모든 거래 내역을 볼 수 있습니다.

## `user_function()` # 추가기능!!

admin 계정이 아닌 일반 계정으로 접속 시 볼 수 있는 부분입니다.

> `trades_info.html`
> 

![Untitled](DB%20App%20Term%20Project%20Report%203c3ece1c8e014660a2d70eed6742d77a/Untitled%205.png)

```python
if send == 'my trades info':
cur.execute("SELECT * FROM trade WHERE buyer = '{}' or seller = '{}';".format(id, id))
trades_info = cur.fetchall()
return render_template("trades_info.html", current_id = id, trades_info = trades_info)
```

`my trades info`를 누르면 내가 buyer이거나 seller인 거래내역만 출력됩니다.

> `edit_password.html`
> 

![Untitled](DB%20App%20Term%20Project%20Report%203c3ece1c8e014660a2d70eed6742d77a/Untitled%206.png)

```python
elif send == 'edit password':
cur.execute("SELECT * FROM users NATURAL JOIN account where id = '{}';".format(id))
user_info = cur.fetchall()
return render_template("edit_password.html", current_id = id, user_info = user_info)
```

`edit_password()`

```python
cur.execute("SELECT password FROM users where id = '{}';".format(id))
password = cur.fetchall()[0][0]
if old_pwd == password:
cur.execute("UPDATE users SET password = '{}' where id = '{}';".format(new_pwd, id))
connect.commit()
```

`edit password`를 누르면 비밀번호를 수정할 수 있습니다. 기존 비밀번호를 정확히 입력할 경우 비밀번호가 변경되고, 그렇지 않을 경우 경고 메시지 창으로 넘어갑니다.

> `delete_account.html`
> 

![Untitled](DB%20App%20Term%20Project%20Report%203c3ece1c8e014660a2d70eed6742d77a/Untitled%207.png)

```python
elif send == 'delete account':
cur.execute("SELECT * FROM users NATURAL JOIN account where id = '{}';".format(id))
user_info = cur.fetchall()
return render_template("delete_account.html", current_id = id, user_info = user_info)
```

`delete_account()`

```python
cur.execute("SELECT password FROM users where id = '{}';".format(id))
password = cur.fetchall()[0][0]
if old_pwd == password:
cur.execute("DELETE FROM account where id = '{}';".format(id))
cur.execute("DELETE FROM users where id = '{}';".format(id))
connect.commit()
```

`delete account`를 누를 경우 계정 삭제 화면으로 넘어갑니다. 비밀번호를 정확하게 입력하고 삭제 버튼을 누르면 계정이 삭제되고 로그인 화면으로 돌아갑니다.

## `message()` # 추가기능!!!

다른 user에게 메시지를 보낼 수 있는 기능입니다.

> `message.html()`
> 

![Untitled](DB%20App%20Term%20Project%20Report%203c3ece1c8e014660a2d70eed6742d77a/Untitled%208.png)

```python
cur.execute("SELECT * FROM message WHERE receiver = '{}';".format(id))
messages = cur.fetchall()
cur.execute("SELECT id FROM users WHERE id != '{}';".format(id))
users = cur.fetchall()
```

메시지 창에 접속하면 자신에게 도착한 메시지들이 출력됩니다.

`send_msg()`

```python
id = request.form["id"]
receiver = request.form["receiver"]
msg = request.form["msg"]
time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
cur.execute("INSERT INTO message VALUES('{}', '{}', '{}', '{}');".format(id, receiver, msg, time))
connect.commit()
```

다른 user를 선택해 메시지를 작성하여 보냅니다.

`delete_message()`

```python
cur.execute("DELETE FROM message where receiver = '{}' and sender = '{}' and msg = '{}' and time = '{}';".format(id, sender, msg, time))
connect.commit()
```

선택한 행의 메시지를 삭제합니다.

## `add_item_page()`

> `add_item.html`
> 

![Untitled](DB%20App%20Term%20Project%20Report%203c3ece1c8e014660a2d70eed6742d77a/Untitled%209.png)

```python
cur.execute("SELECT * FROM category;")
categories = cur.fetchall()
```

`add`버튼을 누를 경우 상품 추가 화면으로 이동합니다. 상단에는 존재하는 카테고리 목록이 출력되고, code는 선택, name은 문자열 입력, price와 stock은 숫자를 입력할 수 있습니다. 

`add_item()`

```python
cur.execute("SELECT code, name, price, seller, stock FROM items;")
items = cur.fetchall()
for item in items:
    if (code, name, price, id) == item[0:4]:
        cur.execute("UPDATE items SET stock = stock + '{}' where code = '{}' and name = '{}' and price = '{}' and seller = '{}';".format(stock, code, name, price, id))
        is_duplicate = True
if not is_duplicate:
    cur.execute("INSERT INTO items VALUES('{}', '{}', '{}', '{}', '{}');".format(code, name, price, stock, id))
connect.commit()
```

전부 작성한 뒤 `add`버튼을 누르면 상품 목록에 등록됩니다. 같은 상품이 있을 시 stock에 개수가 추가됩니다.

## `buy_item_page()`

> `buy_item.html`
> 

![Untitled](DB%20App%20Term%20Project%20Report%203c3ece1c8e014660a2d70eed6742d77a/Untitled%2010.png)

`buy_item()`

```python
cur.execute("SELECT * FROM account WHERE ID = '{}';".format(id))
account_info = cur.fetchall()
total_price = price * how_many
cur.execute("select discount from account natural join rating_info where id = '{}'".format(id))
discount_rate = cur.fetchall()[0][0]
discount_price = total_price * discount_rate // 100
final_price = total_price - discount_price
```

item 표 중에서 `buy`버튼을 누를 경우 해당 상품 구입 화면으로 이동합니다. 상단에는 상품 정보가 출력되고, 몇 개를 살 지 숫자를 입력할 수 있습니다. `buy`버튼을 누르면 구매 확정 페이지로 이동합니다.

```python
if how_many > stock:
		return render_template("error.html", current_id = id, error_messege = "You picked more than stock!")
elif final_price > int(account_info[0][1]):
		return render_template("error.html", current_id = id, error_messege = "Your balance is less than final price!")
```

구매량이 잔량보다 많거나 balance가 구매금액보다 적으면 구매할 수 없습니다.

## `confirm_trade()`

> `trade_item.html`
> 

![Untitled](DB%20App%20Term%20Project%20Report%203c3ece1c8e014660a2d70eed6742d77a/Untitled%2011.png)

전체 구매 금액과 rating에 맞는 할인 금액을 출력합니다.

```python
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
```

`confirm` 버튼을 누르면 거래가 확정되고 데이터베이스에 거래 내역이 기록됩니다. 거래 내역에 맞게 각 user의 balance가 조정되고 rating 역시 조정됩니다.

## `error_return()`

item 화면으로 돌아가야할 때 사용하는 함수입니다. `register()`에 쓰였던 함수를 다시 쓰고 있습니다.

> `error.html`
> 

![Untitled](DB%20App%20Term%20Project%20Report%203c3ece1c8e014660a2d70eed6742d77a/Untitled%2012.png)

```python
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
```

다른 함수에서 `error_message`를 작성해서 같이 넘기면 `error.html`에 출력됩니다.

```python
if how_many > stock:
        return render_template("error.html", current_id = id, error_messege = "You picked more than stock!")
```
