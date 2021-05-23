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

# flask config
app = Flask(__name__)
app.config['SECRET_KEY'] = 'BzkEv2cCs0'

# Hashids config
hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])

# home page
@app.route('/', methods=('GET', 'POST'))

def index():
    conn, curr = get_db_connection()
    # check method 
    if request.method == 'POST':
        #getting user input
        url = request.form['url']

        if not url:
            flash('The URL is required!')
            return redirect(url_for('index'))
        # inserting url into database
        url_id = is_url_in_db(url)
        if url_id ==0:

            with conn:
                url_data = curr.execute('INSERT INTO urls (original_url) VALUES (?)',
                                        (url,))
                conn.commit()
    
            url_id = cast_query(url_data)
        # creating unique 4 character string
        
        hashid = hashids.encode(url_id)
        short_url = request.host_url + hashid
        # return shorten link 
        return render_template('index.html', short_url=short_url)

    return render_template('index.html')

