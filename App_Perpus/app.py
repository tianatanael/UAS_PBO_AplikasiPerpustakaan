from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask import send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

import pymysql.cursors, os, datetime, random, string

application = Flask(__name__)
conn = cursor = None
application.secret_key = 'your secret key'

#My SQL Configuration
application.config['MYSQL_HOST'] = 'localhost'
application.config['MYSQL_USER'] = 'root'
application.config['MYSQL_PASSWORD'] = ''
application.config['MYSQL_DB'] = 'db_pegawai'

application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_pegawai'

db = SQLAlchemy(application)    
mysql = MySQL(application)

# fungsi koneksi ke basis data
def openDb():
    global conn, cursor
    conn = pymysql.connect(db="db_perpus", user="root", passwd="", host="localhost", port=3306, autocommit=True)
    cursor = conn.cursor()	

# fungsi menutup koneksi
def closeDb():
    global conn, cursor
    cursor.close()
    conn.close()

# generate 8 random unique varchars
def generate_id(table: str) -> str:
    # Masukkan argumen "staff" untuk id dan "buku" untuk id_buku
    openDb()
    LENGTH = 8

    while True:
        characters = string.ascii_letters + string.digits
        generated_string = ''.join(random.choices(characters, k=LENGTH))
        if table == "staff":
            cursor.execute(f"SELECT id FROM staff WHERE id = '{generated_string}'")
        elif table == "buku":
            cursor.execute(f"SELECT id_buku FROM buku WHERE id_buku = '{generated_string}'")
        temp = cursor.fetchone()
        if not temp:
            break
    closeDb()
    return generated_string


# Halaman-halaman dalam aplikasi


# Jalankan flask app  
def main():
    application.run(debug=True)

main()