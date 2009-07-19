# This is the blocking Get Poetry Now! client.

import datetime, optparse, socket


def parse_args():
    usage = """usage: %prog [options] [hostname]:port ...

This is the Get Poetry Now! client, blocking edition.
Run it like this:

  python get-poetry.py port1 port2 port3 ...

If you are in the base directory of the twisted-intro package,
you could run it like this:

  python blocking-client/get-poetry.py 1001 1002 1003

to grab poetry from servers on ports 1001, 1002, and 1003.

Of course, there need to be servers listening on those ports
for that to work.
"""

    parser = optparse.OptionParser(usage)

    _, addresses = parser.parse_args()

    if not addresses:
        print parser.format_help()
        parser.exit()

    def parse_address(addr):
        if ':' not in addr:
            host = ''
            port = addr
        else:
            host, port = addr.split(':', 1)

        if not port.isdigit():
            parser.error('Ports must be integers.')

        return host, int(port)

    return map(parse_address, addresses)


def get_poetry(address):
    """Download a piece of poetry from the given address."""

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)

    poem = ''

    while True:

        # This is the 'blocking' call in this synchronous program.
        # The recv() method will block for an indeterminate period
        # of time waiting for bytes to be received from the server.

        bytes = sock.recv(1024)

        if not bytes:
            break

        poem += bytes

    return poem


def main():
    addresses = parse_args()

    elapsed = datetime.timedelta()

    for address in addresses:
        print 'Getting poetry from: %s' % (address,)
        start = datetime.datetime.now()

        # Each execution of 'get_poetry' corresponds to the
        # execution of one synchronous task in Figure 1 here:
        # http://dpeticol.webfactional.com/blog/?p=1209

        poem = get_poetry(address)

        time = datetime.datetime.now() - start
        print 'Got a poem from %s in %s' % (address, time)
        elapsed += time

    print 'Got %d poems in %s' % (len(addresses), elapsed)


if __name__ == '__main__':
    main()