#importing the Flask class from flask Lib
from flask import Flask, render_template
import os
from flask import request
from rq import Queue
from rq.job import Job
from worker import conn
import requests
import redis
import time
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import random

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "Queue.db"))

# creating the instance and __name__ is the name of the current module we are working with i.e app.py
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)
r = redis.Redis()
q = Queue(connection=r)

class jobsdb(db.Model):
    jobid = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False, primary_key=False)
    jobresult = db.Column(db.String, nullable=False, primary_key=False)
    isActive = db.Column(db.Boolean, nullable=False, primary_key=False)
    def __repr__(self):
        return "<JobId: {}>".format(self.jobid)
#utility funtion to calculate the number of words in the given url
def count_words_at_url(url):
    start = time.time()
    resp = requests.get(url)
    end = time.time()
    time_elapsed = end - start
    print(f"Time elapsed: {time_elapsed} ms")
    result = len(resp.text.split())
    n = int(random.randint(0, 100000000000))
    newjob = jobsdb(jobid=n, url =url, jobresult = str(result), isActive = True)
    print('database - ',newjob)
    print(Job)
    db.session.add(newjob)
    db.session.commit()
    return result
#creating a route for adding to the queue and showing to the list
@app.route('/', methods=['GET', 'POST'])
def index():
    jobs = q.jobs  # Get a list of jobs in the queue
    message = None
    if request.method == "POST":
        # get url that is entered in the form
        url = request.form['url']    
        job = q.enqueue(count_words_at_url, url)
        print('Job id', job)
        print('Job Enqued date',job.enqueued_at )
        #get the data from the db
        jobs = jobsdb.query.all()
    return render_template('index.html',jobs=jobs)




