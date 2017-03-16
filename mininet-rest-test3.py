#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
import timeit, numpy

TOT_NODES = 2
TEST_REPS = 5

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

# BEGIN: specific test server    
    h1.cmdPrint('python rest_srv.py &')
# END: specific test server    

    print "PMDEBUG Starting test: tot_nodes={}, bw={}, delay={}, loss={}. TEST_REPS={}".format(TOT_NODES, banwid, tdelay, tloss, TEST_REPS)
    tvalues =[]
    out_file = '>> outf_{}_{}_{}_{}'.format(TOT_NODES, banwid, tdelay, tloss)
    for num in range(TEST_REPS):
        start_time = timeit.default_timer()
        
        for k in range( 2, TOT_NODES+1 ):
            c_node = net.get( 'h%s' % (k) )

# BEGIN: specific test client    
            c_node.cmd('python rest_cli.py'+out_file)
# END: specific test client    

        elapsed = timeit.default_timer() - start_time
        tvalues.append(elapsed)

    print "PMDEBUG Average elapsed time = ", numpy.mean(tvalues), " sec"
    net.stop()

if __name__ == '__main__':
#    setLogLevel( 'info' )
    for i in [0, 5, 10]: 
        perfTest( banwid=1, tdelay='50ms', tloss=i)
