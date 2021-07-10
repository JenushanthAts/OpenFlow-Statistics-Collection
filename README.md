# OpenFlow-Statistics-Collection
Getting statistics collection of openflow networks for custom topology using Mininet-Wifi and Ryu 

## Prerequisites :
1. Mininet wifi(last version)
2. Ryu Controller - version 4.30
3. Python - version 3.8 / suitable one
4. Ubuntu - version 20.04 is better / 18.04 

### Step 1:
connect Ryu-controller which can work as remote controller and run it along with traffic-monitoring file in one tab.

```
ryu-manager Traffic_monitor.py
```


### Step 2: 
![alt text](https://github.com/JenushanthAts/OpenFlow-Statistics-Collection/blob/master/mytopology.png?raw=true)
This is my custom-topology .

The topology is completely written in python. Look at my code , here I have choosen one OVS-SWitch , 2 wireless-access points and 5 stations which can able to move(mobility) , then run the code in another tab.

```
sudo python3 Custom_topology_mobility.py
```

Eventually you will get like this
![alt text](https://github.com/JenushanthAts/OpenFlow-Statistics-Collection/blob/master/Figure_1.png?raw=true)



Then you can check the trace files which contains openflow statistics collection(Port statistics and Flow statistics) in your directory where you have implemented your program.


#### Hope this will help you .Best wishes.







