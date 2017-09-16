import json
import sys
import datetime

import docker




class DockerMetrics:
    def __init__(self):
        #self.container_host_ip = container_host_ip
        #self.container_host_port = container_host_port
        self.json_body_final = {}
        self.DockerClient = docker.Client(base_url='unix://var/run/docker.sock', timeout=2)

    def inspect_all_containers(self):
        '''
            Get the container statistics, choose from available options
            u'blkio_stats', u'precpu_stats', u'read', u'memory_stats', u'pids_stats', u'networks', u'cpu_stats'
        '''
        docker_list = list()
        finalDict ={}
        if len(self.DockerClient.containers()) == 0:
            print (datetime.datetime.now().strftime("[%d-%m-%Y %H:%M:%S.%f]\t") + "No containers running")
            return None
        dictionary = {}
        self.stats = ""
        for container in self.DockerClient.containers():
            try:
                stats = self.DockerClient.stats(container['Id'])
                data = stats.next()
            except Exception, e:
                break

            self.json_container_data = json.loads(data)
            container_name = str(container['Names'][0]).replace('/','')
            mem = {}
            mem['usage'] = self.json_container_data['memory_stats']['usage']
            mem['limit'] = self.json_container_data['memory_stats']['limit']
            mem_body = self.__json_body_constructor__('memory_stats', mem)
            net_body = self.__json_body_constructor__('network_stats', self.json_container_data['networks']['eth0'])
            cpu_usage_param = {}
            cpuDelta = self.json_container_data['cpu_stats']['cpu_usage']['total_usage'] - \
                       self.json_container_data['precpu_stats']['cpu_usage']['total_usage']
            cpustats_usage = self.json_container_data['cpu_stats']['system_cpu_usage']
            precpu_stats = None
            try:
                precpu_stats =self.json_container_data['precpu_stats']['system_cpu_usage']
            except Exception, e:
                precpu_stats = self.json_container_data['precpu_stats']['cpu_usage']['total_usage']
            systemDelta = cpustats_usage - precpu_stats
            test_data = len(self.json_container_data['cpu_stats']['cpu_usage']['percpu_usage'])
            RESULT_CPU_USAGE = float((cpuDelta / systemDelta) * 100 * test_data)
            cpu_usage_param['values'] = RESULT_CPU_USAGE
            cpu_body = self.__json_body_constructor__('system_cpu_usage', cpu_usage_param)
            dictionary = {}
            dictionary["memory_stats"] = mem_body
            dictionary["cpu_usage"] = cpu_body
            dictionary["network_stats"] = net_body

            #print ("***** Final Dict ****", final_dict)
            Dict = {}
            Dict[container_name]=dictionary

            docker_list.append(Dict)
            # if bool(finalDict): # False when empty
            #     finalDict.update(Dict)
            # else:
            #     finalDict= Dict.copy()
        finalDict={"docker":docker_list}
        return finalDict

    def __json_body_constructor__(self, stats_name, data):
        self.stats_name = stats_name
        self.data = data

        json_body_skeleton = {"fields": 'dat4'}

        json_body_skeleton['fields'] = self.data

        return json_body_skeleton