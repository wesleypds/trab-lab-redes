#!/usr/bin/python
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
import time
import os

def run_router(router):
    name = router.name
    services = ["zebra", "ospfd"]
    for srv in services:
        cmd = f"/usr/sbin/{srv} "
        cmd += f"-f /tmp/quagga/{srv}-{name}.conf -d -A 127.0.0.1 "
        cmd += f"-z /tmp/zebra-{name}.api -i /tmp/{srv}-{name}.pid "
        cmd += f"> /tmp/{srv}-{name}-router.log 2>&1"
        router.cmd(cmd)
        time.sleep(1)
    

def topology(remote_controller):
    "Create a network."
    net = Mininet_wifi()

    info("*** Adding stations/hosts\n")

    h1 = net.addHost("h1", ip="192.0.2.1/24")
    h2 = net.addHost("h2", ip="192.0.2.2/24")
    h3 = net.addHost("h3", ip="203.0.113.1/24")
    h4 = net.addHost("h4", ip="203.0.113.2/24")
    h5 = net.addHost("h5", ip="198.51.100.1/24")
    h6 = net.addHost("h6", ip="198.51.100.2/24")

    r1 = net.addHost("r1", ip="192.0.2.254/24")
    r2 = net.addHost("r2", ip="10.10.100.2/24")
    r3 = net.addHost("r3", ip="10.10.102.2/24")
    r4 = net.addHost("r4", ip="10.10.105.1/24")
    r5 = net.addHost("r5", ip="10.10.105.2/24")
    r6 = net.addHost("r6", ip="10.10.203.1/24")
    r7 = net.addHost("r7", ip="203.0.113.254/24")
    r8 = net.addHost("r8", ip="10.10.204.1/24")
    r9 = net.addHost("r9", ip="10.10.207.1/24")
    r10 = net.addHost("r10", ip="10.10.208.1/24")
    r11 = net.addHost("r11", ip="198.51.100.254/24")

    info("*** Adding Switches (core)\n")

    switch1 = net.addSwitch("switch1")
    switch2 = net.addSwitch("switch2")
    switch3 = net.addSwitch("switch3")

    info("*** Creating links\n")

    net.addLink(h1, switch1, bw=1000)
    net.addLink(h2, switch1, bw=1000)
    net.addLink(r1, switch1, bw=1000)

    net.addLink(h3, switch2, bw=1000)
    net.addLink(h4, switch2, bw=1000)
    net.addLink(r7, switch2, bw=1000)

    net.addLink(h5, switch3, bw=1000)
    net.addLink(h6, switch3, bw=1000)
    net.addLink(r11, switch3, bw=1000)

    net.addLink(r1, r2, bw=1000)
    net.addLink(r1, r3, bw=1000)

    net.addLink(r2, r4, bw=1000)

    net.addLink(r3, r4, bw=1000)

    net.addLink(r4, r5, bw=1000)

    net.addLink(r5, r6, bw=1000)
    net.addLink(r5, r10, bw=1000)

    net.addLink(r6, r7, bw=1000)
    net.addLink(r6, r9, bw=1000)

    net.addLink(r7, r8, bw=1000)

    net.addLink(r8, r9, bw=1000)
    net.addLink(r8, r10, bw=1000)

    net.addLink(r9, r10, bw=1000)

    net.addLink(r10, r11, bw=1000)

    info("*** Starting network\n")
    net.start()
    net.staticArp()

    info("*** Applying switches configurations\n")

    switch1.cmd("ovs-ofctl add-flow {} \"actions=output:NORMAL\"".format(switch1.name))
    switch2.cmd("ovs-ofctl add-flow {} \"actions=output:NORMAL\"".format(switch2.name))
    switch3.cmd("ovs-ofctl add-flow {} \"actions=output:NORMAL\"".format(switch3.name))
    
    h1.cmd("ip route add default via 192.0.2.254")
    h2.cmd("ip route add default via 192.0.2.254")
    h3.cmd("ip route add default via 203.0.113.254")
    h4.cmd("ip route add default via 203.0.113.254")
    h5.cmd("ip route add default via 198.51.100.254")
    h6.cmd("ip route add default via 198.51.100.254")

    r1.cmd("ifconfig r1-eth1 10.10.100.1/24 up")
    r1.cmd("ifconfig r1-eth2 10.10.102.1/24 up")
    
    r2.cmd("ifconfig r2-eth1 10.10.101.1/24 up")

    r3.cmd("ifconfig r3-eth1 10.10.103.1/24 up")

    r4.cmd("ifconfig r4-eth1 10.10.101.2/24 up")
    r4.cmd("ifconfig r4-eth2 10.10.103.2/24 up")

    r5.cmd("ifconfig r5-eth1 10.10.200.1/24 up")
    r5.cmd("ifconfig r5-eth2 10.10.201.1/24 up")

    r6.cmd("ifconfig r6-eth1 10.10.201.2/24 up")
    r6.cmd("ifconfig r6-eth2 10.10.202.1/24 up")

    r7.cmd("ifconfig r7-eth1 10.10.202.2/24 up")
    r7.cmd("ifconfig r7-eth2 10.10.205.1/24 up")

    r8.cmd("ifconfig r8-eth1 10.10.205.2/24 up")
    r8.cmd("ifconfig r8-eth2 10.10.206.1/24 up")

    r9.cmd("ifconfig r9-eth1 10.10.204.2/24 up")
    r9.cmd("ifconfig r9-eth2 10.10.203.2/24 up")

    r10.cmd("ifconfig r10-eth1 10.10.200.2/24 up")
    r10.cmd("ifconfig r10-eth2 10.10.207.2/24 up")
    r10.cmd("ifconfig r10-eth3 10.10.206.2/24 up")

    r11.cmd("ifconfig r11-eth1 10.10.208.2/24 up")

    # r1.cmd("/usr/sbin/zebra -f /tmp/quagga/zebra-{n}.conf -d -A 127.0.0.1 -i /tmp/zebra-{n}.pid > logs/zebra-{n}.log 2>&1".format(n=r1.name))
    # time.sleep(2)
    # r1.cmd("/usr/sbin/ripd -f /tmp/quagga/ripd-{n}.conf -d -A 127.0.0.1 -i /tmp/ripd-{n}.pid > logs/ripd-{n}.log 2>&1".format(n=r1.name))
    # r2.cmd("/usr/sbin/zebra -f /tmp/quagga/zebra-{n}.conf -d -A 127.0.0.1 -i /tmp/zebra-{n}.pid > logs/zebra-{n}.log 2>&1".format(n=r2.name))
    # time.sleep(2)
    # r2.cmd("/usr/sbin/ripd -f /tmp/quagga/ripd-{n}.conf -d -A 127.0.0.1 -i /tmp/ripd-{n}.pid > logs/ripd-{n}.log 2>&1".format(n=r2.name))

    run_router(r1)
    run_router(r2)
    run_router(r3)
    run_router(r4)
    run_router(r5)
    run_router(r6)
    run_router(r7)
    run_router(r8)
    run_router(r9)
    run_router(r10)
    run_router(r11)


    info("*** Running CLI\n")

    CLI(net)

    info("*** Stopping network\n")
    net.stop()
    os.system("killall -9 zebra ripd bgpd ospfd > /dev/null 2>&1")


if __name__ == "__main__":
    os.system("rm -f /tmp/zebra-*.pid /tmp/ripd-*.pid /tmp/ospfd-*.pid")
    os.system("rm -f /tmp/bgpd-*.pid /tmp/*-router.log")
    os.system("rm -fr /tmp/zebra-*.api")
    os.system("mn -c >/dev/null 2>&1")
    os.system("killall -9 zebra ripd bgpd ospfd > /dev/null 2>&1")
    os.system("rm -fr /tmp/quagga")
    os.system("cp -rvf conf/ /tmp/quagga")
    os.system("chmod 777 /tmp/quagga -R")
    os.system("echo 'hostname zebra' > /etc/quagga/zebra.conf")
    os.system("chmod 777 /etc/quagga/zebra.conf")
    # os.system("systemctl start zebra.service")

    setLogLevel("info")
    remote_controller = False
    topology(remote_controller)
