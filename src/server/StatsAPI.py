#! /usr/bin/python

import json

from lib.Flask import Flask

from utils import Logger
import socket

from messaging import Subscriber
import flask

logger = Logger.Logger("StatsAPI").get()
app = Flask(__name__)
try:
    hostname = socket.gethostbyname(socket.gethostname())
except socket.gaierror:
    hostname = "localhost"

sub = None
if sub is None:
    sub = Subscriber.Subscriber()

@app.route('/stats')
def getSystemStats():
    stats = sub.getData()

    #response.set_header("content-type", "application/json")
    json_str = json._default_encoder.encode(stats)
    if isinstance(json_str, str) :
        print "True"
        json_str.replace("\\\"","\"")
    logger.info("The Response message is %s",json_str)
    resp = flask.Response(json_str)
    resp.headers['Content-Type']='application/json'
    #resp.headers("content-type", "application/json")
    return resp
'''
@get('/memory')
def get_memory():
    memory_check = MemoryCheck.MemoryCheck()
    mem_data = memory_check.checkVirtualMemoryUse() + memory_check.checkSwapMemoryUse()
    response.set_header("content-type", "application/json")
    json_str = json._default_encoder.encode(mem_data)
    return json_str

@get('/disk')
def get_disk():
    disk_check = DiskCheck.DiskCheck()
    disk_data = disk_check.checkDisk()
    response.set_header("content-type", "application/json")
    json_str = json._default_encoder.encode(disk_data)
    return json_str
'''
#server='eventlet'
app.run(host=hostname, port=5105, debug=True, )
