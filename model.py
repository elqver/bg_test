import sqlite3
from threading import Thread
import requests
import hashlib
from emailserve import send_results
import os.path

#Check existing of db, create one
if not(os.path.exists('md5.db')):
    connection = sqlite3.connect('md5.db')
    conn = connection.cursor()
    with connection:
        conn.execute('''CREATE TABLE tasks (
                     ID text PRIMARY KEY,
                     URL text,
                     email text,
                     progress text,
                     hash text)''')
        connection.commit()

#calculate md5 hash by url with chunks (4KB)
def md5(url):
    hash_md5 = hashlib.md5()

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=4096):
                hash_md5.update(chunk)
    return hash_md5.hexdigest()

#take task id and return dictionary with enough information (status for sure, md5 and url if exists)
def check(id):
    connection = sqlite3.connect('md5.db')
    conn = connection.cursor()

    with connection:
        conn.execute("""SELECT hash, progress, URL FROM tasks
                    WHERE id = :id""", {'id': id})
        raw_data = conn.fetchone()
        if raw_data:
            return {'md5': raw_data[0],
                'status': raw_data[1],
                'url': raw_data[2]}
        else:
            return {'status': "does not exist"}

class Task(Thread):
    """
    Creating background task which calculating md5 by url
    Example:
        robot = Task('any_unique_name_as_id', 'http://google.com/robots.txt', 'target@anymail.com')
        robot.run()
    """
    def __init__(self, id, url, email):
        Thread.__init__(self)
        self.id = id
        self.url = url
        self.email = email

    def run(self):

        #Create connection and cursor for every single Thread
        connection = sqlite3.connect('md5.db')
        conn = connection.cursor()

        #sure close connection
        with connection:
            #add Task to db with progress: 'running', hash: 'None'
            conn.execute("INSERT INTO tasks VALUES (:id, :url, :email, :progress, :hash)",
                  {'id': self.id, 'url': self.url, 'email': self.email, 'progress': 'running', 'hash':'None'})
            connection.commit()
            try:
                #Try to calculate hash
                #Edit db if ok with hash and progress
                hash = md5(self.url)
                conn.execute("""UPDATE tasks SET progress = 'done', hash = :hash
                                WHERE id = :id""", {'hash': hash, 'id': self.id})
                connection.commit()
                send_results(self.email, self.url, hash)
            except:
                #Except edit db with progress: 'error'
                conn.execute("""UPDATE tasks SET progress = 'error'
                                WHERE id = :id""", {'id': self.id})
                connection.commit()
