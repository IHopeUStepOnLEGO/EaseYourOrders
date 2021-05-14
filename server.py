from flask import Flask, render_template
import sqlite3

STATIC_PATH = "./static"
app = Flask(__name__, template_folder= STATIC_PATH + "/templates")

# import external scripts here
from scripts.utils import remove_files, init_filesystem
import scripts.orderlist as OrderlistModule
import scripts.qrgenerator as QRGenModule

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/orderlist', methods=['GET', 'POST'])
def orderlist():
    return OrderlistModule.return_template('orderlist.html')

@app.route('/qrgen', methods=['GET', 'POST'])
def qrgenerator():
    return QRGenModule.return_template('qrgenerator.html')


if __name__ == '__main__':
    # delete all qr code images on server restart
    #remove_files(QRGenModule.IMAGE_FILE_PATH)

    # create folders on the static path, if they do not already exist
    init_filesystem(STATIC_PATH)
  
    app.run(host="0.0.0.0", debug=True)

