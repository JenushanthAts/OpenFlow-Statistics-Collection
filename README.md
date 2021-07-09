# OpenFlow-Statistics-Collection
Getting statistics collection of openflow networks for custom topology using Mininet-Wifi and Ryu 

## Prerequisites :
1. Mininet wifi(last version)
2. Ryu Controller - version 4.30
3. Python - version 3.8 / suitable one
4. Ubuntu - version 20.04 is better / 18.04 

### Step 1: 
Create custom topology which you wish .And the topology is completely written in python. Look at my code , here I have choosen 2 wireless-access points and 5 stations which can able to move(mobility) , then run the code in your terminal eventually you can get like this.

![alt text](https://github.com/JenushanthAts/OpenFlow-Statistics-Collection/blob/master/Figure_1.png?raw=true)


### Step 2:
connect Ryu-controller which can work as remote controller and run it along with traffic-monitoring file .

```
ryu-manager Traffic_monitor.py
```

Then you can check the trace files which contains openflow statistics collection in your directory where you have implemented your program.


#### Hope this will help you .Best wishes.







