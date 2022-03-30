import sqlite3
import time
import random
connection = sqlite3.connect('stock.db')
cursor = connection.cursor()
command_all = "SELECT * FROM stock"
command_own = "SELECT * FROM stock WHERE own>0"
cursor.execute(command_all)
timer = 0
def money():
    cursor.execute("SELECT * FROM money")
    rows = cursor.fetchall()
    print("還剩",rows[0][0],"元")
def ownstock():
    cursor.execute(command_own)
    rows = cursor.fetchall()
    for i in rows:
        print(i)

def record():
    cursor.execute("SELECT * FROM record")
    rows = cursor.fetchall()
    for i in rows:
        print(i)


def buy(index,number):
    global timer
    timer += 1
    cursor.execute("SELECT * FROM stock WHERE num = "+str(index))
    rows = cursor.fetchall()
    buy_or_sell = "buy" 
    price = rows[0][1]
    cost = int(price)*int(number)
    own_number = rows[0][2]
    final_own = int(own_number)+int(number)
    cursor.execute('UPDATE stock SET own = '+str(final_own)+' WHERE num = '+str(index))
    connection.commit()
    cursor.execute("SELECT * FROM record")
    cursor.execute("INSERT INTO record VALUES(?,?,?,?,?)",(index,price,number,cost,buy_or_sell))
    connection.commit()
    cursor.execute("SELECT * FROM money")
    rows = cursor.fetchall()
    money = int(rows[0][0]) - cost
    cursor.execute('UPDATE money SET m = '+str(money))
    connection.commit()

def sell(index,number):
    global timer
    timer += 1
    cursor.execute("SELECT * FROM stock WHERE num = "+str(index))
    rows = cursor.fetchall()
    own_number = rows[0][2]
    buy_or_sell = "sell" 
    price = rows[0][1]
    cost = int(price)*int(number)
    final_own = int(own_number)-int(number)
    cursor.execute('UPDATE stock SET own = '+str(final_own)+' WHERE num = '+str(index))
    connection.commit()
    cursor.execute("SELECT * FROM record")
    cursor.execute("INSERT INTO record VALUES(?,?,?,?,?)",(index,price,number,cost,buy_or_sell))
    connection.commit()
    cursor.execute("SELECT * FROM money")
    rows = cursor.fetchall()
    money = int(rows[0][0]) + cost
    cursor.execute('UPDATE money SET m = '+str(money))
    connection.commit()

def see_all():
    cursor.execute(command_all)
    rows = cursor.fetchall()
    for i in rows:
        print(i)

while True:

    selec =  input()
    if selec == "seeall":
        see_all()
    elif selec == "buy":
        index = input("輸入購買編號：")       
        number = input("輸入購買張數：")
        buy(index,number)
    elif selec == "sell":
        index = input("輸入賣出編號：")       
        number = input("輸入賣出張數：")
        sell(index,number)
    elif selec == "ownstock":
        ownstock()
    elif selec == "record":
        record()
    elif selec == "money":
        money()
    elif(selec == "end"):
        break