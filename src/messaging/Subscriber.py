import zmq
import socket
from utils import Logger

class Subscriber:

    def __init__(self):
        self.logger = Logger.Logger(self.__class__.__name__).get()

        context = zmq.Context()
        global sock
        sock = context.socket(zmq.SUB)
        sock.setsockopt(zmq.SUBSCRIBE, "")
        sock.connect("tcp://" + socket.gethostbyname(socket.gethostname()) + ":5690")

    def getData(self):
        while True:
            message= sock.recv()
            self.logger.info("Subscriber message %s",message)
            return message