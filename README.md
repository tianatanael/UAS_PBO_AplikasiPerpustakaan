Proyek ini dibuat dalam rangka memenuhi Ujian Akhir Semester mata kuliah Pemrograman Berbasis Objek. 

Library yang dibutuhkan untuk menjalankan aplikasi ini di python adalah:
- flask
- flask-sqlalchemy
- flask-mysqldb
- pymysql

Database yang diperlukan: 
1. db_perpus
   
Table di dalam database: 
1. buku
   a. id_buku (varchar(8)) PRIMARYKEY
   b. judul (varchar(100))
   c. penulis (varchar(100))
   d. penerbit (varchar(50))
   e. tglterbit (date)
   f. lokasi (varchar(50))
   g. jumlah (int(3))
   h. tersedia (int(3))
   i. tglmasuk (date)
2. staff
   a. id (varchar(11)) PRIMARYKEY
   b. nik (varchar(16))
   c. nama (varchar(50))
   d. tgllahir (date)
   e. password (varchar(255))
