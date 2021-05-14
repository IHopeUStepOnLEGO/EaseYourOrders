from scripts.qrgenerator import createQRCode
from flask.globals import request
from server import STATIC_PATH
from flask import render_template, url_for, redirect
import sqlite3

import scripts.qrgenerator as QRGenModule

DB_NAME = "eyo.db"
IMG_PATH = "./static/images/"

def db_clear_all_orders():
    conn = sqlite3.connect(STATIC_PATH + "" + "./database/" + "" + DB_NAME)
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

    if request.method == 'POST':

        print(request.form.get('delete_button'))

        # delete_id = request.form.get('delete_button')
        # status_id = request.form.get('status_button')

        # if delete_id is not None:
        #     conn = sqlite3.connect(STATIC_PATH + "" + "./database/" + "" + DB_NAME)
        #     c = conn.cursor()

        #     c.execute("DELETE FROM orders WHERE ID = ?", (delete_id))
        #     conn.commit()
        #     conn.close()

        # if status_id is not None:
        #     conn = sqlite3.connect(STATIC_PATH + "" + "./database/" + "" + DB_NAME)
        #     c = conn.cursor()

        #     c.execute("UPDATE orders SET status = 1 WHERE ID = ?", (status_id))
        #     conn.commit()
        #     conn.close()
            
            
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
        #db_create_orders_table()

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