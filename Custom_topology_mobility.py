#!/usr/bin/python
#"Example to create a Mininet-WiFi topology and connect it to the internet via NAT"
import sys
from mininet.node import Controller,RemoteController,OVSSwitch
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
#from mininet.link import TCLink
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import OVSKernelAP


def topology(args):

    "Create a network."

    net = Mininet_wifi(controller=Controller,switch=OVSSwitch,accessPoint=OVSKernelAP)
    
    info("*** Creating stations\n")
    sta1 = net.addStation( 'sta1' , mac= '00:00:00:00:00:01' , ip = '10.0.0.1/8' )
    sta2 = net.addStation( 'sta2' , mac= '00:00:00:00:00:02' , ip = '10.0.0.2/8' )
    sta3 = net.addStation( 'sta3' , mac= '00:00:00:00:00:03' , ip = '10.0.0.3/8' )
    sta4 = net.addStation( 'sta4' , mac= '00:00:00:00:00:04' , ip = '10.0.0.4/8' )
    sta5 = net.addStation( 'sta5' , mac= '00:00:00:00:00:05' , ip = '10.0.0.5/8' )
    
    info("*** Creating accesspoints\n")
    ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='g', channel='5', position='50,60,0')
    ap2 = net.addAccessPoint('ap2', ssid='new-ssid', mode='g', channel='4', position='80,60,0')
    
    #info("*** Creating switch\n")
    #s1= net.addSwitch('s1')
    #s1=net.addSwitch('s1',cls = OVSKernelSwitch, protocols='OpenFlow13')
    
    info("*** Creating controller\n")
    c1 = net.addController('c1', controller=RemoteController)
    
    info("*** Configuring propagation model\n")
    net.setPropagationModel(model="logDistance", exp=4)
    
    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()
    
    if '-p' not in args:
        net.plotGraph(max_x=100, max_y=100)

    net.setMobilityModel(time=0, model='GaussMarkov', max_x=100, max_y=100,min_v=0.5, max_v=0.5, seed=20)
    
    info("*** Starting network\n")
    net.build()
    #net.addNAT(name='nat0', linkTo='ap1', ip='192.168.100.254').configDefault()
    #net.addLink(ap1,s1)
    #net.addLink(ap2,s1)
    #1.15292150460685E+018

    
    c1.start()
    ap1.start([c1])
    ap2.start([c1])
    
    #net.addLink(ap1,s1)
    #net.addLink(ap2,s1)
    #s1.start( [c1] )
    
    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()
    
if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
