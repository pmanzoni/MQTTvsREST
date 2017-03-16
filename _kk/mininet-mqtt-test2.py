#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
import paho.mqtt.client as mqtt
import sys
import time
import random
import numpy
import json


# MQTT client code START
broker_add = '10.0.0.1'
sensor_name = 'sensor1'

def on_connect(mqttc, obj, flags, rc):
    print "Connected to %s:%s" % (mqttc._host, mqttc._port)

def on_message(mqttc, obj, msg):
    print "message received"
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    mqttc.disconnect()

def on_publish(mqttc, obj, mid):
    print "message published: "+str(mid)

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)
# MQTT client code END

class SingleSwitchTopo( Topo ):
    "Single switch connected to n hosts."
    def build( self, n=2, ibw=10, idelay='5ms', iloss=0 ):
    
        # default 10 Mbps, 5ms delay, 2% loss, 1000 packet queue
        lopts = {'bw':ibw, 'delay': idelay, 'loss': iloss, 'max_queue_size': 1000, 'use_htb': True }
        print lopts

        switch = self.addSwitch( 's1' )
        for h in range(n):
            # Each host gets 50%/n of system CPU
            host = self.addHost( 'h%s' % (h + 1), cpu=1 )
            self.addLink( host, switch, **lopts )

def perfTest( banwid=10, tdelay='50ms', tloss=0):
    "Create network and run simple performance test"
    topo = SingleSwitchTopo( n=2, ibw=banwid, idelay=tdelay, iloss=tloss )
    net = Mininet( topo=topo, host=CPULimitedHost, link=TCLink )
    net.start()
    dumpNodeConnections( net.hosts )

#    print "Pre-Starting test..."
#    net.pingAll()

    h1, h2 = net.get( 'h1', 'h2' )

#    net.iperf( (h1, h2) )
    
    print h1.cmd('sudo mosquitto &')

    print "Starting test..."
    tvalues =[]
    for num in range(5):
        start_time = time.clock()

        h2.cmd("""
            mqttc = mqtt.Client()
            mqttc.loop_start()
            print "000"
            mqttc.on_message = on_message
            mqttc.on_connect = on_connect
            mqttc.on_publish = on_publish
            mqttc.on_subscribe = on_subscribe
            print "A"
            mqttc.connect(broker_add, 1883, keepalive=60)
            print "B"
            mqttc.subscribe(sensor_name, 0)
            print "C"
            new_s_value = random.randint(1, 1000)
            print "D"
            new_sensor_t = {'value': str(new_s_value)}
            print "E"
            the_msg_str = json.dumps(new_sensor_t)
            print "F"
            mqttc.publish(sensor_name,the_msg_str)
            print "G"
            """)
        
        elapsed = time.clock() - start_time
        tvalues.append(elapsed)
        print elapsed*1000, "msec"

    print "Average elapsed time = ", numpy.mean(tvalues)*1000, " msec"
    net.stop()

if __name__ == '__main__':

#    setLogLevel( 'info' )
    for i in [0.001, 100]: 
        perfTest( banwid=i, tdelay='50ms', tloss=0)
