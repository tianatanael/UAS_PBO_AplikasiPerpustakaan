from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask import send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

import pymysql.cursors, os, datetime, random, string