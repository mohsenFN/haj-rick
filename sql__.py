import sqlite3

class DbManager:
    def __init__(self, db_name):
        self.con = sqlite3.connect(db_name, check_same_thread=False)
        self.c = self.con.cursor()

    def create_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS smartq (
                            question VARCHAR(32) NOT NULL PRIMARY KEY,
                            answer VARCHAR(1024) NOT NULL)""" )
        self.con.commit()

    def insert_qa(self, q, a):
        self.c.execute("INSERT OR REPLACE INTO smartq (question, answer) VALUES (?, ?)", (q, a))
        self.con.commit()

    def answer_to_q(self, q):
        self.c.execute("SELECT answer FROM smartq WHERE question=?", (q,))
        return self.c.fetchall()

    def all_q_a(self):
        self.c.execute("SELECT * FROM smartq")
        return self.c.fetchall()

    def delete_q(self, q):
        self.c.execute("DELETE FROM smartq WHERE question=?", (q,))
        self.con.commit()

