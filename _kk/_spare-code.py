    outfiles, errfiles = {}, {}
    outfiles[ h1 ] = '%s.out' % h1.name
    errfiles[ h1 ] = '%s.err' % h1.name
    h1.cmd( 'echo >', outfiles[ h1 ] )
    h1.cmd( 'echo >', errfiles[ h1 ] )




    outfiles, errfiles = {}, {}

    outfiles[ h1 ] = '%s.out' % h.name
    errfiles[ h1 ] = '%s.err' % h.name
    outfiles[ h2 ] = '%s.out' % h.name
    errfiles[ h2 ] = '%s.err' % h.name
    
    h1.cmd( 'echo >', outfiles[ h1 ] )
    h1.cmd( 'echo >', errfiles[ h1 ] )
    h2.cmd( 'echo >', outfiles[ h2 ] )
    h2.cmd( 'echo >', errfiles[ h2 ] )

    # Start pings
    h.cmdPrint('ping', server.IP(),
               '>', outfiles[ h ],
               '2>', errfiles[ h ],
               '&' )

    print "Monitoring output for", seconds, "seconds"
    for h, line in monitorFiles( outfiles, seconds, timeoutms=500 ):
        if h:
            print '%s: %s' % ( h.name, line )


