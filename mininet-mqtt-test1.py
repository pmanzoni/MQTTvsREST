#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
import time, numpy

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
    
    h1.cmd('sudo mosquitto &')

    print "Starting test..."
    tvalues =[]
    for num in range(5):
        start_time = time.clock()
        
        result = h1.cmd('python mqtt_test.py')

        elapsed = time.clock() - start_time
        tvalues.append(elapsed)
        print elapsed*1000, "msec"

    print "Average elapsed time = ", numpy.mean(tvalues)*1000, " msec"
    net.stop()

if __name__ == '__main__':
#    setLogLevel( 'info' )
    for i in [0.001, 100]: 
        perfTest( banwid=i, tdelay='50ms', tloss=0)
