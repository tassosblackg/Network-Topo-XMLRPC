import sys
import random
import subprocess
from time import time, sleep
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client as cl
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info

# mininet topology
class MyTopology(Topo):
  def build(self, n=2):
    switch = self.addSwitch("sw1")
    embedder = self.addHost("embedder")
    self.addLink(embedder, switch)
    # Python's range(N) generates 0..N-1
    for h in range(n):
        host = self.addHost("server%s" % (h + 1))
        self.addLink(host, switch)
            
  # Main Function
def simpleTest():
  "Create and test a simple network"

  print("Clearing old topologies....\n")
  output = subprocess.run(["sudo", "mn", "-c"])
  print(output)

  topo = MyTopology(n=4)
  net = Mininet(topo)
  net.start()
  print("Dumping host connections")
  dumpNodeConnections(net.hosts)
  print("Testing network connectivity")
  net.pingAll()


  # simple connection test between client/server
  # server or client is a specific host

  emb = net.get("embedder") # working as client
  server1 = net.get("server1") # host working as server

  print(emb.IP(), server1.IP())
  # 10.0.0.1       10.0.0.2
  p1 = server1.popen("python3 tserver.py")
  sleep(1)
  # passing as arguments IP, current_cpu_load new_cpu_request values
  res2 = emb.cmdPrint("python3 tclient.py 10.0.0.2 0.8 0.1")

  # Get the response break down to 'Accepted =True' , new_cpu_load_available
  outp = res2.split(",")
  # print(outp[0], outp[1])

  cpu_load_val = outp[1].strip() # remove escape characters from the end
  # print(i, float(i))
  print(" Request Accepted from Server ? %s %.2f" % (outp[0],float(cpu_load_val)))

  p1.terminate() # stop server running in the background of server1-host

  net.stop() # stop network
  
  
  
  
if __name__ == "__main__":
  # Tell mininet to print useful information
  setLogLevel("info")
  simpleTest()
