#! /usr/bin/python
import json
import socket
import time
import sys
sys.path.append('lib/site-packages')

import zmq
from utils import Logger


class Producer:

    def __init__(self):
        self.sock_obj = None
        self.logger = Logger.Logger(self.__class__.__name__).get()
        try:
            self.hostname = socket.gethostbyname(socket.gethostname())
        except socket.gaierror:
            self.hostname = "localhost"

        if self.sock_obj is None:
            self.sock_obj = self.__init__pub()

    def __init__pub(self):
        context = zmq.Context()
        sock = context.socket(zmq.PUB)
        sock.bind("tcp://"+self.hostname+":5690")
        return sock

    def publishDataToZeroMQ(self,data):

        #published_data = list()
        published_data = data.copy()

        extra_data = {}
        extra_data["hostname"]=socket.gethostname()
        extra_data["time"]= str(time.time())

        published_data.update(extra_data)

        #published_data.append(list(extra_list))
        #published_data.append(data)

        data_in_json = json.dumps(published_data)

        self.logger.info("Published data is %s", data_in_json)
        self.sock_obj.send_json(data_in_json)
