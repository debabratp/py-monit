#! /usr/bin/python

import json
import sys
from utils import Logger


class Config():

    def __init__(self):
        self.logger = Logger.Logger(self.__class__.__name__).get()
        global data
        #home = expanduser("~")
        #logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename=home+'/py-monit.log',
         #                   level=logging.DEBUG)

        self.file_name = "resources/monitor.cfg.json"
        # Check the length of args
        total_args = len(sys.argv)
        if ( total_args == 2 ) and ( str.__contains__(sys.argv[1],"/") ) :
            self.file_name = sys.argv[1]
        elif total_args == 3:
            if not str.isdigit(sys.argv[1]):
                self.file_name = sys.argv[1]
            else:
                self.file_name = sys.argv[2]


       # try:
        if self.file_name is not None:
            with open(self.file_name) as self.file:
                #print("Data", json.load(self.file))
                data = json.load(self.file)
                self.logger.info("Data %s",data)
        #except Exception:
         #   logging.error("File not found")
         #   raise IOError("File not found")


    def getCPUData(self):
        cpuData = []

        if data is not None:
            critical = data["alert"]["cpu"]["critical"]
            cpuData.append(critical)

            warning = data["alert"]["cpu"]["warning"]
            cpuData.append(warning)

            repeat = data["alert"]["cpu"]["repeat"]
            cpuData.append(repeat)
        #print(cpuData)
        return cpuData

    def getVirtualMemoryData(self):
        memData = []

        if data is not None:
            critical = data["alert"]["memory"]["virtual"]["critical"]
            memData.append(critical)

            warning = data["alert"]["memory"]["virtual"]["warning"]
            memData.append(warning)

            repeat = data["alert"]["memory"]["virtual"]["repeat"]
            memData.append(repeat)
        return memData

    def getSwapMemoryData(self):
        memData = []

        if data is not None:
            critical = data["alert"]["memory"]["swap"]["critical"]
            memData.append(critical)

            warning = data["alert"]["memory"]["swap"]["warning"]
            memData.append(warning)

            repeat = data["alert"]["memory"]["swap"]["repeat"]
            memData.append(repeat)
        return memData

    def getDiskData(self):
        diskData = []

        if data is not None:

            critical = data["alert"]["disk"]["critical"]
            diskData.append(critical)

            warning = data["alert"]["disk"]["warning"]
            diskData.append(warning)

            repeat = data["alert"]["disk"]["repeat"]
            diskData.append(repeat)

        return diskData

    # Return array of process name and scripts. It contains array of arrays.
    def getProcesses(self):
        processes = []
        values = []

        if data is not None:
            processes = data["alert"]["processes"]
        for process in processes:
            values.append(process.values())
        return values
    #TODO
    def getNetworks(self):
        networks = []
        values = []

        if data is not None:
            networks = data["alert"]["networks"]
        for network in networks:
            values.append(network.values())
        return values

    def getEmail(self):
        return data["emailTo"]

#
if __name__ == '__main__':
    config = Config()
    result = config.getCPUData()
    print( "RESULT", result )