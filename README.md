       
**Structure of Config file**
  
_`{
	"alert": {
		"cpu": {
			"critical": 90,
			"warning": 80,
			"repeat": 3
		},
		"memory": {
			"virtual":{
				"critical": 40,
				"warning": 50,
				"repeat": 3
			},
			"swap": {
				"critical": 35,
				"warning": 45,
				"repeat": 3
		    }
		},
		"disk": {
			"critical": 10,
			"warning": 30,
			"repeat": 3
		},
		"processes": [{
			"name": "<<app_name>>",
			"start_script": "<<process_start_script>>"
		}, {
			"name": "<<app_name_2>>",
			"start_script": "<<process_start_script_2>>"
		}]
	},
	"emailTo": "<<email_address>>"
}`_

**How to run**
1.  <code>
        pyhton main.py {{time_interval}} {{absolute_config_file_path}}
    </code>
   
    _Param:_
        
        1. 'time_interval' is in int. It is optional. Default value is **3**
        2. 'absolute_config_file_path' is a **JSON** config file required to grab the metrics for system, app, and network.
            It is optional. The default file is under /resource/monitor.cfg.json.
2. <code>
    pyhton main.py
   </code> 

3. The sample service response http://10.249.106.250:2126/stats 
NOTE: The Ip change on every system restart due to VPN.

<code>
{
  "virtual_memory_stat": "62.4",
  "time": "1486362932.03",
  "docker": [
    {
      "admiring_davinci": {
        "memory_stats": {
          "fields": {
            "usage": 164147200,
            "limit": 2096275456
          }
        },
        "cpu_usage": {
          "fields": {
            "values": 0
          }
        },
        "network_stats": {
          "fields": {
            "tx_dropped": 0,
            "rx_packets": 84,
            "rx_bytes": 14618,
            "tx_errors": 0,
            "rx_errors": 0,
            "tx_bytes": 5265,
            "rx_dropped": 0,
            "tx_packets": 46
          }
        }
      }
    },
    {
      "goofy_goldberg": {
        "memory_stats": {
          "fields": {
            "usage": 26066944,
            "limit": 2096275456
          }
        },
        "cpu_usage": {
          "fields": {
            "values": 0
          }
        },
        "network_stats": {
          "fields": {
            "tx_dropped": 0,
            "rx_packets": 77,
            "rx_bytes": 4532,
            "tx_errors": 0,
            "rx_errors": 0,
            "tx_bytes": 1250,
            "rx_dropped": 0,
            "tx_packets": 17
          }
        }
      }
    }
  ],
  "hostname": "MACAIM00057.local",
  "disk_stat": "28.4",
  "swap_memory_stat": "62.4",
  "cpu_stat": "16.0"
}
</code>


**Dependent libraries**
1. psutils
2. zmq
3. docker
4. flask