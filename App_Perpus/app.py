from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask import send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

import pymysql.cursors, os, datetime, random, string
import locale
from datetime import datetime

application = Flask(__name__)
conn = cursor = None
application.secret_key = 'your secret key'

#My SQL Configuration
application.config['MYSQL_HOST'] = 'localhost'
application.config['MYSQL_USER'] = 'root'
application.config['MYSQL_PASSWORD'] = ''
application.config['MYSQL_DB'] = 'db_perpus'

application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_perpus'

db = SQLAlchemy(application)    
mysql = MySQL(application)

#fungsi koneksi ke basis data
def openDb():
    global conn, cursor
    conn = pymysql.connect(db="db_perpus", user="root", passwd="",host="localhost",port=3306,autocommit=True)
    cursor = conn.cursor()	

#fungsi menutup koneksi
def closeDb():
    global conn, cursor
    cursor.close()
    conn.close()

# Halaman-halaman dalam aplikasi
# Home
@application.route('/')
@application.route('/collection/')
def home():
    if 'staff_forgot' in session:
        return redirect(url_for('staff_forgot_entry'))
    if 'id' in session:
        id = True
    else:
        id = False

    openDb()
    container = []
    sql = "SELECT * FROM buku ORDER BY tglmasuk DESC;"
    cursor.execute(sql)
    results = cursor.fetchall()
    for data in results:
        container.append(data)
    closeDb()
    return render_template ('home.html', container=container, id=id)

# Halaman data buku
@application.route('/collection/<id_buku>/')
def book(id_buku):
    if 'staff_forgot' in session:
        return redirect(url_for('staff_forgot_entry'))
    if 'id' in session:
        id = True
    else:
        id = False

    openDb()
    sql = f"SELECT * FROM buku WHERE id_buku='{id_buku}';"
    cursor.execute(sql)
    data = cursor.fetchone()
    locale.setlocale(locale.LC_TIME, 'id_ID')# Set the locale to Indonesian
    date_string = data[8].strftime('%A, %d-%m-%Y')# Assume data[8] is a datetime object
    closeDb()
    return render_template('book.html', data=data, id=id, date_string=date_string)

# Halaman about
@application.route("/about/")
def about():
    if 'id' in session:
        id = True
    else:
        id = False

    return render_template('about.html', id=id)

# Halaman contact
@application.route("/contact/")
def contact():
    if 'id' in session:
        id = True
    else:
        id = False

    return render_template('contact.html', id=id)

# Login
@application.route('/staff/login/', methods=['GET','POST'])
def staff_login():
    if 'id' in session:
        return redirect(url_for('home'))
    if 'staff_forgot' in session:
        return redirect(url_for('staff_forgot_entry'))

    if request.method == "POST":
        id = request.form["id"]
        password = request.form["password"]
        
        cur = mysql.connection.cursor()
    
        cur.execute(f"SELECT id, password FROM staff WHERE id = '{id}'")
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[1], password):
            session["id"] = user[0]
            return redirect(url_for("home"))
        else:
            return render_template("staff_login.html", error="Invalid ID or password!")
    return render_template("staff_login.html")

SECRET_CODE = "0019"

# Register
@application.route('/staff/register/', methods=['GET','POST'])
def staff_register():
    if 'id' in session:
        return redirect(url_for('home'))
    if 'staff_forgot' in session:
        return redirect(url_for('staff_forgot_entry'))

    generated_id = generate_id()

    if request.method == "POST":
        id = request.form["id"]
        nik = request.form["nik"]
        nama = request.form["nama"]
        tgllahir = request.form["tgllahir"]

        password = request.form['password']

        confirm_pwd = request.form['confirm_password']

        if password != confirm_pwd:
            return render_template('staff_register.html', id=generated_id, error='Passwords do not match!')

        hashed_password = generate_password_hash(password) #Hash the password

        code = request.form["code"]
        if code != SECRET_CODE:
            return render_template('staff_register.html', id=generated_id, error="Wrong Code.")

        openDb()
        # SQL SYNTAX untuk memasukan username dan password di tabel karyawan
        cursor.execute(f"INSERT INTO staff(id, nik, nama, tgllahir, password) values('{id}', '{nik}', '{nama}', '{tgllahir}', '{hashed_password}')")
        conn.commit()
        closeDb()
        return redirect(url_for("staff_login"))
    
    return render_template('staff_register.html', id=generated_id)

@application.route('/clear_session1/')
def clear_session1():
    session.pop('staff_forgot', None)
    return redirect(url_for('staff_forgot'))

@application.route('/staff/forgot/', methods=['GET','POST'])
def staff_forgot():
    if 'id' in session:
        return redirect(url_for('home'))
    if 'staff_forgot' in session:
        return redirect(url_for('staff_forgot_entry'))

    if request.method == "POST":
        id = request.form['id']
        nik = request.form['nik']
        cur = mysql.connection.cursor()

        cur.execute(f"SELECT id, nik FROM staff WHERE id=%s AND nik=%s", (id,nik))
        user = cur.fetchone()
        cur.close()
        
        if user:
            session['staff_forgot'] = user[0]
            return redirect(url_for('staff_forgot_entry'))
        else:
            return render_template('staff_forgot.html', error='Invalid ID or NIK!!!')

    return render_template('staff_forgot.html')

@application.route('/staff/forgot/entry/',  methods=['GET','POST'])
def staff_forgot_entry():
    if 'id' in session:
        return redirect(url_for('home'))
    if 'staff_forgot' not in session:
        return redirect(url_for('staff_forgot'))

    if request.method == "POST":
        password = request.form['password']
        confirm_pwd = request.form['confirm_password']

        if password != confirm_pwd:
            return render_template('staff_forgot_entry.html', error='Passwords do not match!')

        hashed_password = generate_password_hash(password) #Hash the password

        cur = mysql.connection.cursor()
        cur.execute(f"UPDATE staff SET password=%s WHERE id=%s", (hashed_password, session['staff_forgot']))
        mysql.connection.commit()
        cur.close()

        session.pop('staff_forgot', None)
        return redirect(url_for('staff_login'))

    return render_template('staff_forgot_entry.html')

@application.route('/staff/logout/')
def staff_logout():
    if 'id' not in session:
        return redirect(url_for('home'))
    if 'staff_forgot' in session:
        return redirect(url_for('staff_forgot_entry'))
    session.pop('id', None)
    return redirect(url_for('home'))

@application.route('/staff/collection/tambah/', methods=['GET','POST'])
def staff_tambah_buku():
    if 'id' not in session:
        return redirect(url_for('home'))
    if 'staff_forgot' in session:
        return redirect(url_for('staff_forgot_entry'))
    
    generated_id_buku = generate_id_buku()#Memanggil fungsi untuk mendapatkan id_buku otomatis
    
    if request.method == 'POST':
        id_buku = request.form['id_buku']
        judul = request.form['judul']
        penulis = request.form['penulis']
        penerbit = request.form['penerbit']
        tglterbit = request.form['tglterbit']
        lokasi = request.form['lokasi']
        jumlah = request.form['jumlah']
        tglmasuk = request.form['tglmasuk']

        openDb()
        sql = "INSERT INTO buku (id_buku,judul,penulis,penerbit,tglterbit,lokasi,jumlah, tersedia,tglmasuk) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (id_buku,judul,penulis,penerbit,tglterbit,lokasi,jumlah, jumlah, tglmasuk)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()
        return redirect(url_for('home'))        
    else:
        return render_template('staff_tambah_buku.html', id_buku=generated_id_buku)

@application.route('/staff/collection/edit/<id_buku>', methods=['GET','POST'])
def staff_edit_buku(id_buku):
    if 'id' not in session:
        return redirect(url_for('home'))
    if 'staff_forgot' in session:
        return redirect(url_for('staff_forgot_entry'))
    
    openDb()
    cursor.execute('SELECT * FROM buku WHERE id_buku=%s', (id_buku))
    data = cursor.fetchone()
    
    if request.method == "POST":
        judul = request.form['judul']
        penulis = request.form['penulis']
        penerbit = request.form['penerbit']
        tglterbit = request.form['tglterbit']
        lokasi = request.form['lokasi']
        jumlah = request.form['jumlah']
        tersedia = request.form['tersedia']
        tglmasuk = request.form['tglmasuk']

        sql = "UPDATE buku SET judul=%s, penulis=%s, penerbit=%s, tglterbit=%s, lokasi=%s, jumlah=%s, tersedia=%s, tglmasuk=%s WHERE id_buku=%s"
        val = (judul, penulis, penerbit ,tglterbit, lokasi, jumlah, tersedia, tglmasuk, id_buku)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()
        return redirect(url_for('home'))
    else:
        closeDb()
        return render_template('staff_edit_buku.html', data=data)

#fungsi cetak ke PDF
@application.route('/print/<id_buku>', methods=['GET'])
def get_book_data(id_buku):
    # Koneksi ke database
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',  # Password Anda (jika ada)
                                 db='db_perpus',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Query untuk mengambil data pegawai berdasarkan NIK
            sql = "SELECT * FROM buku WHERE id_buku = %s"
            cursor.execute(sql, (id_buku,))
            buku_data = cursor.fetchone()  # Mengambil satu baris data pegawai

            # Log untuk melihat apakah permintaan diterima dengan benar
            print("Menerima permintaan untuk ID buku:", id_buku)

            # Log untuk melihat data yang dikirim ke klien
            print("Data yang dikirim:", buku_data)

            return jsonify(buku_data)  # Mengembalikan data sebagai JSON

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Terjadi kesalahan saat mengambil data'}), 500

    finally:
        connection.close()  # Menutup koneksi database setelah selesai

#fungsi menghapus data
@application.route('/staff/collection/hapus/<id>', methods=['GET','POST'])
def hapus(id):
    if 'id' not in session:
        return redirect(url_for('home'))
    if 'staff_forgot' in session:
        return redirect(url_for('staff_forgot_entry'))
    
    openDb()
    cursor.execute('DELETE FROM buku WHERE id_buku=%s', (id))
    conn.commit()
    closeDb()
    return redirect(url_for('home'))

#Create Model
class Users(db.Model):
    nik = db.Column(db.Integer, primary_key = True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable atribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash)

#fungsi membuat ID staff otomatis
def generate_id():
    # mendefinisikan fungsi openDb(), cursor, dan closeDb() 
    openDb()

    tiga_digit_pertama = 678
    tiga_digit_kedua = 123
    
    # Mengambil empat digit terakhir dari tahun
    year_str = str(tiga_digit_pertama).zfill(2)
    
    # Mengambil dua digit dari bulan
    tiga_digit_str_kedua = str(tiga_digit_kedua).zfill(2)

    # Membuat format nia tanpa nomor urut terlebih dahulu
    base_id_without_number = f"I-{year_str}{tiga_digit_str_kedua}"

    # Mencari nia terakhir dari database untuk mendapatkan nomor urut
    cursor.execute("SELECT id FROM staff WHERE id LIKE %s ORDER BY id DESC LIMIT 1", (f"{base_id_without_number}%",))
    last_nia = cursor.fetchone()

    if last_nia:
        last_number = int(last_nia[0].split("-")[-1])  # Mengambil nomor urut terakhir
        next_number = last_number + 1
        # Membuat nia lengkap dengan nomor urut
        next_id = f"I-{str(next_number).zfill(3)}"
    else:
        next_number = 1  # Jika belum ada data, mulai dari 1
        # Membuat nia lengkap dengan nomor urut
        next_id = f"{base_id_without_number}{str(next_number).zfill(3)}"
    
    closeDb()  # untuk menutup koneksi database 
    
    return next_id

#fungsi membuat ID buku otomatis
def generate_id_buku():
    # mendefinisikan fungsi openDb(), cursor, dan closeDb() 
    openDb()

    tiga_digit_pertama = 336
    # digit_keempat = 1
    
    # Mengambil empat digit terakhir dari tahun
    first_format = str(tiga_digit_pertama).zfill(2)
    
    # Mengambil dua digit dari bulan
    # tiga_digit_str_kedua = str(digit_keempat).zfill(2)

    # Membuat format nia tanpa nomor urut terlebih dahulu
    base_id_without_number = f"B-{first_format}"
    # base_id_without_number = f"B-{first_format}{tiga_digit_str_kedua}"

    # Mencari nia terakhir dari database untuk mendapatkan nomor urut
    cursor.execute("SELECT id_buku FROM buku WHERE id_buku LIKE %s ORDER BY id_buku DESC LIMIT 1", (f"{base_id_without_number}%",))
    last_id_buku = cursor.fetchone()

    if last_id_buku:
        last_number = int(last_id_buku[0].split("-")[-1])  # Mengambil nomor urut terakhir
        next_number = last_number + 1
        # Membuat nia lengkap dengan nomor urut
        next_id = f"B-{str(next_number).zfill(3)}"
    else:
        next_number = 1  # Jika belum ada data, mulai dari 1
        # Membuat nia lengkap dengan nomor urut
        next_id = f"{base_id_without_number}{str(next_number).zfill(3)}"
    
    closeDb()  # untuk menutup koneksi database 
    
    return next_id

#Program utama     
def main():
    application.run(debug=True)

main()