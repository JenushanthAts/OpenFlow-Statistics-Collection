#!/usr/bin/python
import csv
import datetime
import time
from ryu.app import simple_switch_13
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib import hub
from operator import attrgetter
#from oslo_config import cfg

class CollectTrainingStatsApp(simple_switch_13.SimpleSwitch13):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    
    def __init__(self, *args, **kwargs):
        super(CollectTrainingStatsApp, self).__init__(*args, **kwargs)
        self.interval=5
        
        # to calculate deltas for bandwith usage calculation
        self.flow_byte_counts = {}
        
        # to calculate deltas for bandwith usage calculation
        self.port_byte_counts = {}
        
        list1=['Time','Datapath','in port','eth_dst','out port','packet count','byte count','flow speed(Kbps)']
        list2=['Time','Datapath','port','rx_packets','rx_bytes','rx_errors','tx_packets','tx_bytes','tx_errors'
                  ,'rx_bitrate(kbps)','tx_bitrate(kbps)','bandwidth(kbps)']
        
        with open('Flow_Stats_Trace.csv', 'w') as f:
            write = csv.writer(f)
            write.writerow(list1)
        
        with open('Port_Stats_Trace.csv', 'w') as f:
            write = csv.writer(f)
            write.writerow(list2)
        
        #self.CONF=cfg.CONF
        #self.CONF.register._opts([cfg.IntOpt('INTERVAL',default=10,help=('Monitoring Interval'))])
        #self.logger.info("Interval Value %d",self.CONF.INTERVAL)
        
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self.monitor)
        
    #Asynchronous message
    @set_ev_cls(ofp_event.EventOFPStateChange,[MAIN_DISPATCHER, DEAD_DISPATCHER])
    def state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath

        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]


    def monitor(self):
        while True:
            #self.logger.debug('Monitoring interval')
            for dp in self.datapaths.values():
                self.request_stats(dp)
            #hub.sleep(CollectTrainingStatsApp.interval )
            hub.sleep(self.interval )


    def request_stats(self, datapath):
        self.logger.debug('send stats request: %016x', datapath.id)
        ofproto = datapath.ofproto        
        parser = datapath.ofproto_parser

        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)
   
   
    # Convert from data to bitrate(Kbps)
    @staticmethod
    def bitrate(self,data):
        return round(float(data * 8.0 / (self.interval*1000)),2)  
        
    #convert datapath to decimal   
    @staticmethod
    def data_convert(dpid):
        return ("{:.8f}".format(float(dpid)))

        
    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        #create a trace text file
        
        file1 = open("Flow_Stats_Trace.csv","a+")        
        body = ev.msg.body
        #current time with date-->datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #current time--> datetime.datetime.now().time()
        for stat in sorted([flow for flow in body if flow.priority == 1],
                           key=lambda flow: (flow.match['in_port'],
                                             flow.match['eth_dst'])):
                                             
            in_port = stat.match['in_port']
            out_port = stat.instructions[0].actions[0].port
            eth_dst = stat.match['eth_dst']

            # Check if we have a previous byte count reading for this flow
            # and calculate bandwith usage over the last polling interval
            key = (ev.msg.datapath.id, in_port, eth_dst, out_port)
            rate = 0
            if key in self.flow_byte_counts:
                cnt = self.flow_byte_counts[key]
                rate = self.bitrate(self,stat.byte_count - cnt)
            self.flow_byte_counts[key] = stat.byte_count
             
            file1.write("{},{},{},{},{},{},{},{}\n"
                .format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),self.data_convert(ev.msg.datapath.id),stat.match['in_port'],
                        stat.match['eth_dst'],stat.instructions[0].actions[0].port,
                        stat.packet_count, stat.byte_count,rate))
        file1.close()
       
    
    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):

        file0 = open("Port_Stats_Trace.csv","a+")
        body = ev.msg.body
        for stat in sorted(body, key=attrgetter('port_no')):
             if stat.port_no != ofproto_v1_3.OFPP_LOCAL:
                key = (ev.msg.datapath.id, stat.port_no)
                rx_bitrate, tx_bitrate = 0, 0
                total_Kbps=0
                if key in self.port_byte_counts:
                    cnt1, cnt2 = self.port_byte_counts[key]
                    rx_bitrate = self.bitrate(self,stat.rx_bytes - cnt1)
                    tx_bitrate = self.bitrate(self,stat.tx_bytes - cnt2)
                    total_Kbps= rx_bitrate + tx_bitrate
                self.port_byte_counts[key] = (stat.rx_bytes, stat.tx_bytes)
                
                file0.write("{},{},{},{},{},{},{},{},{},{},{},{}\n"
                       .format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),self.data_convert(ev.msg.datapath.id),
                              stat.port_no,stat.rx_packets,stat.rx_bytes,stat.rx_errors,stat.tx_packets,stat.tx_bytes,stat.tx_errors,
                              rx_bitrate,tx_bitrate,total_Kbps))
        file0.close()
    
