import sqlite3
""" SQLite functions used in ../main.py """
def insert_qa(c, conn, q, a):
    c.execute("INSERT OR REPLACE INTO smartq (question, answer) VALUES (?, ?)", (q, a))
    conn.commit()

def answer_to_q(c, conn, q):
    c.execute("SELECT answer FROM smartq WHERE question=?", (q,))
    return c.fetchall()

def all_q_a(c, conn):
    c.execute("SELECT * FROM smartq")
    return c.fetchall()

def delete_q(c, conn, q):
    c.execute("DELETE FROM smartq WHERE question=?", (q,))
    conn.commit()

"""Syntax for creating table"""
table_syntax = """CREATE TABLE IF NOT EXISTS smartq (
    question VARCHAR(32) NOT NULL PRIMARY KEY,
    answer VARCHAR(1024) NOT NULL)"""  