import sqlite3
from threading import Thread
import requests
import hashlib
from emailserve import send_results

print('imported')

conn = sqlite3.connect('md5.db')

try:
    conn.execute('''CREATE TABLE tasks (
                 ID text PRIMARY KEY,
                 URL text,
                 email text,
                 progress text,
                 hash text)''')
except:
    pass

def md5(url):
    hash_md5 = hashlib.md5()

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=4096):
                hash_md5.update(chunk)
    return hash_md5.hexdigest()


class Task(Thread):

    def __init__(self, id, url, email):
        Thread.__init__(self)
        self.id = id
        self.url = url
        self.email = email
        print('we are here', email)

    def run(self):
        conn = sqlite3.connect('md5.db')
        with conn:
            print('here')
            conn.execute("INSERT INTO tasks VALUES (:id, :url, :email, :progress, :hash)",
                  {'id': self.id, 'url': self.url, 'email': self.email, 'progress': 'running', 'hash':'None'})
            conn.commit()
            try:
                hash = md5(self.url)
                conn.execute("""UPDATE tasks SET progress = 'done', hash = :hash
                                WHERE id = :id""", {'hash': hash, 'id': self.id})
                conn.commit()
                print(hash)
                send_results(self.email, self.url, hash)
            except:
                conn.execute("""UPDATE tasks SET progress = 'error during operation'
                                WHERE id = :id""", {'id': self.id})
                conn.commit()
