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
- id_buku (varchar(8)) PRIMARYKEY
- judul (varchar(100))
- penulis (varchar(100))
- penerbit (varchar(50))
- tglterbit (date)
- lokasi (varchar(50))
- jumlah (int(3))
- tersedia (int(3))
- tglmasuk (date)
2. staff
- id (varchar(11)) PRIMARYKEY
- nik (int(11))
- nama (varchar(50))
- tgllahir (date)
- password (varchar(255))
