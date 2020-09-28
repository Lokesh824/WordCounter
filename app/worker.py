import redis
from rq import Worker, Queue, Connection
from .config import DevelopmentConfig
from flask import Flask, render_template


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

listen = app.config['QUEUE_NAME']
conn = redis.from_url(app.config['REDISTOGO_URL'])
R_SERVER = redis.Redis("localhost")
if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()



