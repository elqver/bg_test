import sqlite3
from threading import Thread
import requests
import hashlib
from emailserve import send_results

connection = sqlite3.connect('md5.db')
conn = connection.cursor()

try:
    conn.execute('''CREATE TABLE tasks (
                 ID text PRIMARY KEY,
                 URL text,
                 email text,
                 progress text,
                 hash text)''')
    connection.commit()
except:
    pass

def md5(url):
    hash_md5 = hashlib.md5()

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=4096):
                hash_md5.update(chunk)
    return hash_md5.hexdigest()

def check(id):
    connection = sqlite3.connect('md5.db')
    conn = connection.cursor()
    conn.execute("""SELECT hash, progress, URL FROM tasks
                    WHERE id = :id""", {'id': id})
    raw_data = conn.fetchone()
    return {'md5': raw_data[0],
            'status': raw_data[1],
            'url': raw_data[2]}
    connection.close()

class Task(Thread):

    def __init__(self, id, url, email):
        Thread.__init__(self)
        self.id = id
        self.url = url
        self.email = email

    def run(self):
        connection = sqlite3.connect('md5.db')
        conn = connection.cursor()
        with conn:
            print('here')
            conn.execute("INSERT INTO tasks VALUES (:id, :url, :email, :progress, :hash)",
                  {'id': self.id, 'url': self.url, 'email': self.email, 'progress': 'running', 'hash':'None'})
            connection.commit()
            try:
                hash = md5(self.url)
                conn.execute("""UPDATE tasks SET progress = 'done', hash = :hash
                                WHERE id = :id""", {'hash': hash, 'id': self.id})
                connection.commit()
                print(hash)
                send_results(self.email, self.url, hash)
            except:
                conn.execute("""UPDATE tasks SET progress = 'error'
                                WHERE id = :id""", {'id': self.id})
                connection.commit()
