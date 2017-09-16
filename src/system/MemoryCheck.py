#! /usr/bin/python

import psutil
import Config
from utils import Logger

class MemoryCheck():

    def __init__(self):
        self.config = Config.Config()
        self.logger = Logger.Logger(self.__class__.__name__).get()

    VIRTUAL_CRITICAL = None
    VIRTUAL_WARNING = None
    SWAP_CRITICAL = None
    SWAP_WARNING = None
    REPEAT = None


    def checkVirtualMemoryUse(self):
        result_dic = {}
        self.__getVirtualMemConfig__()
        virtual_mem_percent = psutil.virtual_memory().percent
        if virtual_mem_percent > self.VIRTUAL_CRITICAL:
            self.logger.warning('CRITICAL VIRTUAL MEMORY - Percentage of memory used is %d', virtual_mem_percent)
            result_dic["virtual_memory_stat"] = str(virtual_mem_percent)
        elif virtual_mem_percent > self.VIRTUAL_WARNING:
            self.logger.warning('CRITICAL VIRTUAL MEMORY - Percentage of memory used is %d', virtual_mem_percent)
            result_dic["virtual_memory_stat"] = str(virtual_mem_percent)

        #return list(result)
        return result_dic

    def checkSwapMemoryUse(self):
        result_dic = {}
        self.__getSwapMemConfig__()
        swap_mem_percent = psutil.virtual_memory().percent
        if swap_mem_percent > self.VIRTUAL_CRITICAL:
            self.logger.warning('CRITICAL SWAP MEMORY - Percentage of memory used is %d', swap_mem_percent)
            result_dic["swap_memory_stat"] = str(swap_mem_percent)

        elif swap_mem_percent > self.VIRTUAL_WARNING:
            self.logger.warning('CRITICAL SWAP MEMORY - Percentage of memory used is %d', swap_mem_percent)
            result_dic["swap_memory_stat"] = str(swap_mem_percent)
        #return list(result)
        return result_dic

    def __getVirtualMemConfig__(self):
        virtual_mem_config = self.config.getVirtualMemoryData()

        self.VIRTUAL_CRITICAL = virtual_mem_config[0]
        self.VIRTUAL_WARNING = virtual_mem_config[1]
        self.REPEAT = virtual_mem_config[2]

    def __getSwapMemConfig__(self):
        swap_mem_config = self.config.getSwapMemoryData()

        self.SWAP_CRITICAL = swap_mem_config[0]
        self.SWAP_WARNING = swap_mem_config[1]
        self.REPEAT = swap_mem_config[2]


# if __name__ == '__main__':
#     memoryCheck = MemoryCheck()
#     return_val = memoryCheck.checkVirtualMemoryUse()
#     memoryCheck.checkSwapMemoryUse()
