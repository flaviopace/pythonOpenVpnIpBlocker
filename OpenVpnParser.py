import argparse
import re


PATTERN = 'TLS Error: TLS key negotiation failed'

class OpenVPNLogParser(object):

    def __init__(self,filein):
        self.filein = filein
        self.iplist = []
        pass

    def parseLog(self):
        with open(self.filein) as vpnlog:
            for line in vpnlog:
                if PATTERN in line:
                    #print line
                    self.iplist.append(self.getIp(line))

        pass

    def getIp(self, stringIn):

        return re.findall( r'[0-9]+(?:\.[0-9]+){3}', stringIn)[0]
        pass

    def getIpList(self):

        return list(set(self.iplist))



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process Python Input')
    parser.add_argument('--source', '-s', metavar='S', nargs='+', dest='sourceIn',
                        help='an integer for the accumulator')

    args = parser.parse_args()

    print args.sourceIn

    p = OpenVPNLogParser(args.sourceIn[0])

    p.parseLog()

    print p.getIpList()

