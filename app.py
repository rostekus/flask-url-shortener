import sqlite3
from hashids import Hashids
from flask import Flask, render_template, request, flash, redirect, url_for
import re
DATABASE_PATH = 'db/database.db'

# connecting to database
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    curr = conn.cursor()
    conn.row_factory = sqlite3.Row
    return conn, curr

def cast_query(query):
    query = list(query)
    return query[0]

def is_url_in_db(url):
    
    conn, curr = get_db_connection()
    with conn:
        rowid = curr.execute('SELECT id FROM urls WHERE original_url =  (?) ',(url,)).fetchone()
        if rowid:
            return cast_query(rowid)
        else:
            return 0


