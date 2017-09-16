#! /usr/bin/python

import logging
import os


class Logger(object):
    def __init__(self, name):
        name = name.replace('.log', '')
        logger = logging.getLogger('log_namespace.%s :: ' % name)
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            if not os.path.exists(os.path.expanduser("~")+"/monitoring/logs"):
                os.makedirs(os.path.expanduser("~")+"/monitoring/logs")
            file_name = os.path.join(os.path.expanduser("~")+"/monitoring/logs", '%s.log' % name)
            handler = logging.FileHandler(file_name)
            formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s %(message)s')
            handler.setFormatter(formatter)
            handler.setLevel(logging.DEBUG)
            logger.addHandler(handler)
        self._logger = logger

    def get(self):
        return self._logger