#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
import timeit, numpy

TOT_NODES = 10
TEST_REPS = 10

# the last one is the one that will be executed
SERVER_CODE = 'python rest_srv.py &'
SERVER_CODE = 'sudo mosquitto &'

# the last one is the one that will be executed
CLIENT_CODE = 'python rest_cli.py'
CLIENT_CODE = 'python mqtt-test.py'

class SingleSwitchTopo( Topo ):
    "Single switch connected to n hosts."
    def build( self, n, ibw, idelay, iloss ):
    
        lopts = {'bw':ibw, 'delay': idelay, 'loss': iloss, 'max_queue_size': 1000, 'use_htb': True }

        switch = self.addSwitch( 's1' )
        for h in range(n):
            # Each host gets 100% of system CPU
            host = self.addHost( 'h%s' % (h + 1), cpu=1 )
            self.addLink( host, switch, **lopts )

def perfTest( banwid=10, tdelay='50ms', tloss=0):
    "Create network with default values: 10 Mbps, 50ms delay, 0% loss"
    topo = SingleSwitchTopo( n=TOT_NODES, ibw=banwid, idelay=tdelay, iloss=tloss )

    net = Mininet( topo=topo, host=CPULimitedHost, link=TCLink )
    net.start()
    dumpNodeConnections( net.hosts )

    # Run the server on node h1
    h1 = net.get( 'h1' )

# Executing the specific test SERVER on node 'h1'    
    h1.cmd(SERVER_CODE)

    print "PMDEBUG Starting test: bw={}, delay={}, loss={}".format(banwid, tdelay, tloss)
    tvalues =[]
    out_file = ' >> outf_{}_{}_{}_{}'.format(TOT_NODES, banwid, tdelay, tloss)
    for num in range(TEST_REPS):
        start_time = timeit.default_timer()
        
        for k in range( 2, TOT_NODES+1 ):
            c_node = net.get( 'h%s' % (k) )

# Executing the specific test CLIENT on node c_node    
            c_node.cmd(CLIENT_CODE+out_file)

        elapsed = timeit.default_timer() - start_time
        tvalues.append(elapsed)

    print "PMDEBUG Average elapsed time = ", numpy.mean(tvalues), " sec"
    net.stop()

if __name__ == '__main__':
#    setLogLevel( 'info' )
    print "PMDEBUG exp setup: ccode='{}', scode='{}', TOT_NODES={}, TEST_REPS={}".format(CLIENT_CODE, SERVER_CODE, TOT_NODES, TEST_REPS)
    for i in [0]: 
        perfTest( banwid=1, tdelay='50ms', tloss=i)
