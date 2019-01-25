import argparse
import re
import subprocess


PATTERN = 'TLS Error: TLS key negotiation failed'
OFFSETVALUE = 50

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

    def getUniqueIpList(self):

        return list(set(self.iplist))

    def getIpList(self):

        return self.iplist


class RunCommand(object):

    def __init__(self):
        pass

    def runCommand(self, ipaddr):

        opts = {'iptables':'/sbin/iptables', 'rule':'INPUT', 'ipaddress':ipaddr, 'action':'DROP'}
        ipcmd = '{iptables} -A {rule} -s {ipaddress} -j {action}'.format(**opts)

        print ipcmd
        subprocess.call(ipcmd, shell=True)

    def getIpFromIptables(self, ipaddr):

        opts = {'iptables': '/sbin/iptables', 'rule': '-L', 'nodns': '-n'}
        ipcmd = '{iptables} {rule} {nodns}'.format(**opts)

        print ipcmd

        output = subprocess.check_output(ipcmd)
        
        if ipaddr in output:
            print 'Ip Addr already dropped'
            return True

        return False



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process Python Input')
    parser.add_argument('--source', '-s', metavar='S', nargs='+', dest='sourceIn',
                        help='an integer for the accumulator')

    args = parser.parse_args()

    print args.sourceIn

    p = OpenVPNLogParser(args.sourceIn[0])

    p.parseLog()

    rc = RunCommand()

    for item in p.getUniqueIpList():
        print " {} : {}".format(item, p.getIpList().count(item))
        if p.getIpList().count(item) > OFFSETVALUE:
            if not rc.getIpFromIptables(item):
                rc.runCommand(item)
