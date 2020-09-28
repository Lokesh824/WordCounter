#importing the Flask class from flask Lib
from flask import Flask, render_template
import os
from flask import request
from rq import Queue
from rq.job import Job
from .worker import conn
import requests
import redis
import time
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import random
from .worker import R_SERVER  
import _pickle as cPickle
import hashlib
from .config import DevelopmentConfig


# creating the instance and __name__ is the name of the current module we are working with i.e app.py
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)
r = redis.Redis()
q = Queue(connection=r)
registry = q.failed_job_registry
    
class jobsdb(db.Model):
    jobid = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False, primary_key=False)
    status = db.Column(db.String, nullable=False, primary_key=False)
    jobresult = db.Column(db.String, nullable=False, primary_key=False)
    isActive = db.Column(db.Boolean, nullable=False, primary_key=False)
    timeTaken = db.Column(db.String, nullable=False, primary_key=False)
    def __repr__(self):
        return "<JobId: {}>".format(self.jobid)
#utility funtion to calculate the number of words in the given url
def count_words_at_url(jobid,url):
    errors = []
    try: 
        start = time.time()
        resp = requests.get(url)
        end = time.time()
        time_elapsed = end - start
        print(f"Time elapsed: {time_elapsed} ms")
    except:
        errors.append(
            "Unable to get URL. Please make sure it's valid and try again."
        )
        return {"error": errors}
    result = len(resp.text.split())
    update_job_status(str(jobid),str(result),time_elapsed)
    db.session.commit()
    return result

def get_job_status(jobid):
    job = Job.fetch(jobid, connection=conn)
    status = job.get_status()
    print('Status: %s' %status )
    return status

def update_job_status(jobid,result, timeTaken):
    status = get_job_status(jobid);
    jobinfo = jobsdb.query.filter_by(jobid=jobid).first()
    jobinfo.status = str(status)
    jobinfo.jobresult = result
    jobinfo.timeTaken = str(timeTaken)
    db.session.commit()

def get_random_number():
    jid = int(random.randint(0, 10000000000000000))
    isValidJId = jobsdb.query.filter_by(jobid=jid).first()
    if isValidJId != None:
        get_random_number()
    return jid
#creating a route for adding to the queue and showing to the list
@app.route('/index', methods=['GET', 'POST'])
def index():
    jobs = q.jobs  # Get a list of jobs in the queue
    if request.method == "POST":
        # get url that is entered in the form
        url = request.form['url']
        JobId = str(get_random_number())
        job = q.enqueue(count_words_at_url, args=(JobId,url), job_id=JobId, result_ttl=5000,  ttl=50)
        newjob = jobsdb(jobid=JobId, url =url, status='queued',jobresult = '', isActive = True, timeTaken = '')
        db.session.add(newjob)
        db.session.commit()
    jobs = db.session.query(jobsdb).filter(jobsdb.jobresult != '')
    return render_template('index.html',jobs=jobs)

@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
    job = Job.fetch(job_key, connection=conn)
    print('the status',job)
    if job.is_finished:
        return str(job.result), 200
    else:   
        return "The Job is still not compleated", 202

@app.route("/qjobs")
def qjobs():
    pjobs = db.session.query(jobsdb).filter(jobsdb.status == 'queued')
    print(pjobs)
    return render_template('pendingjobs.html',pjobs=pjobs)

