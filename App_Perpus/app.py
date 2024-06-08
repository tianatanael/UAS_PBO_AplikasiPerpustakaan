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

#fungsi koneksi ke basis data
def openDb():
    global conn, cursor
    conn = pymysql.connect(db="db_perpustakaan", user="root", passwd="",host="localhost",port=3306,autocommit=True)
    cursor = conn.cursor()	

#fungsi menutup koneksi
def closeDb():
    global conn, cursor
    cursor.close()
    conn.close()