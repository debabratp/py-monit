#! /usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import threading
import time
import logging

from os import kill, killpg, setsid, getpid

import signal

import subprocess

from messaging import Producer
from system import DockerMetrics
from system.CPUCheck import CPUCheck
from system.DiskCheck import DiskCheck
from system.MemoryCheck import MemoryCheck
from utils import Alerts
from utils import Logger


class Main(threading.Thread):

    original_sigint = None

    def __init__(self, thread_id, name, arg):
        self.logger = Logger.Logger(self.__class__.__name__).get()

        global producer
        producer = Producer.Producer()
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.arg = arg

    def run(self):
        threadLock.acquire()
        self.logger.info("Starting Main thread ..........")
        if ( self.arg is not None ) and ( str.isdigit(self.arg) ):
            self.runCheck(int(self.arg))
        else:
            self.runCheck(3)# Default

    def runCheck(self,delay):

        while True:
            try:
                time.sleep(delay)
                diskCheck = DiskCheck()
                disk_result = diskCheck.checkDisk()

                self.raiseAlert(disk_result)

                memoryCheck = MemoryCheck()
                virtual_mem_result = memoryCheck.checkVirtualMemoryUse()
                swap_mem_result = memoryCheck.checkSwapMemoryUse()
                mem_result = virtual_mem_result.copy()
                mem_result.update(swap_mem_result)

                self.raiseAlert(mem_result)

                cpuCheck = CPUCheck()
                cpu_result = cpuCheck.totalCpuCheck()
                docker_stats = None
                try:
                    s = subprocess.check_output('docker ps', shell=True)# Check for Docker present in a system
                    if s is not None:
                        dockerMetrics = DockerMetrics.DockerMetrics()
                        docker_stats = dockerMetrics.inspect_all_containers()
                except Exception, e:
                    self.logger.info("No Docker found", e.message)

                # Publish the stats to ZeroMQ
                self.publishSysStatToZeroMQ(cpu_result,mem_result,disk_result,docker_stats)

                # Raise Alert TODO
                #self.raiseAlert(cpu_result)

            except RuntimeError:
                self.logger.info("Error in running Main class")

    #TODO
    '''
    This method has to be extend to send email and raise tickets

    '''
    def raiseAlert(self,result):
        alerts = Alerts.Alerts()
        if len(result) != 0:
            alerts.sendEmail(result)

    def publishSysStatToZeroMQ(self,cpu,mem,disk,docker_stats):
        data_cpu = cpu.copy()
        data_cpu.update(mem)

        data_disk = data_cpu.copy()
        data_disk.update(disk)

        data_docker = data_disk.copy()
        if docker_stats is not None:
            data_docker = data_disk.copy()
            data_docker.update(docker_stats)

        producer.publishDataToZeroMQ(data_docker)

    def exit_gracefully(self,signum, frame):
        # restore the original signal handler as otherwise evil things will happen
        # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
        global original_sigint
        signal.signal(signal.SIGINT, original_sigint)

        try:
            if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
                sys.exit(1)

        except KeyboardInterrupt:
            print("Ok ok, quitting")
            sys.exit(1)

        # restore the exit gracefully handler here
        signal.signal(signal.SIGINT, self.exit_gracefully)

    def set_signals(self):
        global original_sigint
        original_sigint = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGALRM, self.exit_gracefully)
        signal.signal(signal.SIGHUP, signal.SIG_IGN)

if __name__ == '__main__':

    threadLock = threading.Lock()
    threads = []
    # Create new threads
    thread1 = None
    try:
        my_argv = sys.argv[1]
        thread1 = Main(1, "Main-1", my_argv)
    except IndexError:
        logging.warn("Main thread will start with 'DEFAULT' argumants.")
        thread1 = Main(1, "Main-1", None)
    thread1.set_signals()
    thread1.start()