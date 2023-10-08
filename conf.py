import sqlite3



def Connect():
    conn = sqlite3.connect('memeory.db')
    return conn


