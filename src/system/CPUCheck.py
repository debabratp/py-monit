#! /usr/bin/python

import psutil
import Config
from utils import Logger

class CPUCheck():

    def __init__(self):
        self.config = Config.Config()
        self.logger = Logger.Logger(self.__class__.__name__).get()

    CRITICAL = None
    WARNING = None
    REPEAT = None

    def totalCpu(self):
        total_cpu_use = psutil.cpu_percent(interval=1, percpu=False)
        return total_cpu_use

    def percoreCpu(self):
        percore_cpu_use = []
        cpu_id = 0

        for cpu in psutil.cpu_percent(interval=1, percpu=True):
            array_line = str(cpu_id), cpu
            percore_cpu_use.append(array_line)
            cpu_id += 1
        return percore_cpu_use

    #check total CPU
    def totalCpuCheck(self):
        # type: () -> cpuCheck
      result_dic = {}
      self.__getCPUCheckConfigVal__()
      total_cpu_use =  self.totalCpu()
      percore_cpu_use = self.percoreCpu()

      for repeat in range(self.REPEAT):
          if total_cpu_use > self.CRITICAL:
            self.logger.warning('CRITICAL - Total CPU use is %i', total_cpu_use)
            #result.add('{"critical_cpu":' + str(total_cpu_use) + "}")
            result_dic["cpu_stat"] =  str(total_cpu_use)
          elif total_cpu_use > self.WARNING:
            self.logger.warning('WARNING - Total CPU use is %i', total_cpu_use)
            result_dic["cpu_stat"] =  str(total_cpu_use)

          else:
            for core in percore_cpu_use:
              if core[1] > self.WARNING:
                self.logger.warning('WARNING - CPU Core %s is at %d', core[0], core[1])
                result_dic["cpu_stat"] = str(core[1])

              else:
                continue
      #values = list(result)
      #return list(result)
      return result_dic

    def __getCPUCheckConfigVal__(self):
        cpuData = self.config.getCPUData()
        self.CRITICAL = cpuData[0]
        self.WARNING = cpuData[1]
        self.REPEAT = cpuData[2]
#
if __name__ == '__main__':
    checkCpu = CPUCheck()
    result = checkCpu.totalCpuCheck()
    print( "RESULT", result )
