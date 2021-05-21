from scripts.qrgenerator import createQRCode
from flask.globals import request
from server import STATIC_PATH
from flask import render_template, url_for, redirect
import sqlite3
import os

import json


import scripts.qrgenerator as QRGenModule
DB_NAME = "eyo.db"
IMG_PATH = "./static/images/"

def db_clear_all_orders():
    conn = sqlite3.connect(STATIC_PATH + "" + "./database/" + "" + DB_NAME)
    print("\n\n" + STATIC_PATH + "" + "./database/" + "" + DB_NAME + "\n\n")
    c = conn.cursor()

    c.execute("DELETE FROM orders")
    c.execute("DELETE FROM sqlite_sequence WHERE name = 'orders'")

    conn.commit()
    conn.close()

def db_create_orders_table():
    conn = sqlite3.connect(STATIC_PATH + "" + "./database/" + "" + DB_NAME)
    c = conn.cursor()

    c.execute("""CREATE Table orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description text,
        trackinglink text,
        qrcode blob,
        status integer
        )
        """)

    conn.commit()
    conn.close()


def convert_to_binary(__filename__):
    # convert digital data to binary
    with open(__filename__, 'rb') as file:
        blobData = file.read()
    return blobData


def return_template(__template__):


    if request.method == 'DELETE':


         # get id of database entry  
        delete_id = request.get_data().decode()

        print(delete_id)

        # connect to db
        conn = sqlite3.connect(STATIC_PATH + "" + "./database/" + "" + DB_NAME)
        c = conn.cursor()

        # get entry to delete
        c.execute("SELECT * FROM orders WHERE id = ?", (delete_id))
        db_entry = c.fetchone()

        # delete local qr code image
        os.remove(db_entry[3])

        c.execute("DELETE FROM orders WHERE id = ?", (delete_id))

        conn.commit()
        conn.close()

        return json.dumps({"status":True})

    elif request.method == 'PUT':

        # get id of database entry  
        status_id = request.get_data().decode()

        print(status_id)


        # connect to db
        conn = sqlite3.connect(STATIC_PATH + "" + "./database/" + "" + DB_NAME)
        c = conn.cursor()

        # get currently stored status from db
        c.execute("SELECT status FROM orders WHERE id = ?;", (status_id))
        db_status = c.fetchone()

        # toggle status
        if db_status[0]:
            c.execute("UPDATE orders SET status = 0 WHERE id = ?;", (status_id))
        else:
            c.execute("UPDATE orders SET status = 1 WHERE id = ?;", (status_id))

        conn.commit()
        conn.close()

        return json.dumps({"status":True})

    elif request.method == 'POST':
            
        # catch data of form
        description = request.form['new_entry_description']
        trackingLink = request.form['new_entry_trackingLink']

        # connect to db
        conn = sqlite3.connect(STATIC_PATH + "" + "./database/" + "" + DB_NAME)
        c = conn.cursor()

        # insert data into database
        # note: qrcode is of type BLOB, which is a binary format
        c.execute("INSERT INTO orders (description, trackinglink, qrcode, status) VALUES (?, ?, ?, ?);", (description, trackingLink, QRGenModule.createQRCode(trackingLink, description, IMG_PATH), 0))
        conn.commit()
        conn.close()

        return redirect(url_for('orderlist'))


    else:

        # DATABASE DEBUG
        # db_clear_all_orders()
        # db_create_orders_table()

        conn = sqlite3.connect(STATIC_PATH + "" + "./database/" + "" + DB_NAME)
        c = conn.cursor()

        # c.execute("INSERT INTO orders (description, trackinglink, qrcode, status) VALUES ('order1', 'trackingLink1', 'qrcode1', 0)")
        # c.execute("INSERT INTO orders (description, trackinglink, qrcode, status) VALUES ('order2', 'trackingLink2', 'qrcode2', 0)")
        # c.execute("INSERT INTO orders (description, trackinglink, qrcode, status) VALUES ('order3', 'trackingLink3', 'qrcode3', 1)")
        
        c.execute("SELECT * FROM orders")
        data = c.fetchall()

        print(data)

        conn.commit()
        conn.close()

        return str(render_template(__template__, data=data))