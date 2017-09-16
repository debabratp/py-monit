#! /usr/bin/python


import psutil
import Config
from utils import Logger

class DiskCheck():

    def __init__(self):
        self.config = Config.Config()
        self.logger = Logger.Logger(self.__class__.__name__).get()

    CRITICAL = None
    WARNING = None
    REPEAT = None

    def __getDiskConfig__(self):
        disk_data = self.config.getDiskData()
        self.CRITICAL = disk_data[0]
        self.WARNING = disk_data[1]
        self.REPEAT = disk_data[2]

    def checkDisk(self):
        disk_percent_use =  psutil.disk_usage("/").percent
        self.__getDiskConfig__()

        result_dic = {}
        if disk_percent_use > self.CRITICAL:
            self.logger.warning('CRITICAL DISK SPACE - Percentage of disk used is %f', disk_percent_use)
            result_dic["disk_stat"] = str(disk_percent_use)
        elif disk_percent_use > self.WARNING:
            self.logger.warning('WARNING DISK SPACE - Percentage of disk used is %f', disk_percent_use)
            result_dic["disk_stat"] = str(disk_percent_use)
        #return list(result)
        return result_dic
# if __name__ == '__main__':
#     diskcheck = DiskCheck()
#     diskcheck.checkDisk()