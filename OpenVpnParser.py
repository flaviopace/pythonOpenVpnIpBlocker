import argparse

PATTERN = 'TLS Error: TLS key negotiation failed'

class OpenVPNLogParser(object):

    def __init__(self,filein):
        self.filein = filein
        pass

    def parseLog(self):
        with open(self.filein) as vpnlog:
            for line in vpnlog:
                if PATTERN in line:
                    print line

        pass

    def getIp(self):
        pass



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process Python Input')
    parser.add_argument('--source', '-s', metavar='S', nargs='+', dest='sourceIn',
                        help='an integer for the accumulator')

    args = parser.parse_args()

    print args.sourceIn

    p = OpenVPNLogParser(args.sourceIn[0])

    p.parseLog()