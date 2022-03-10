```python
r1.cmd("/usr/sbin/zebra -f /tmp/quagga/zebra-{n}.conf -d -A 127.0.0.1 -i /tmp/zebra-{n}.pid > logs/zebra-{n}.log 2>&1".format(n=r1.name))
time.sleep(2)
r1.cmd("/usr/sbin/ripd -f /tmp/quagga/ripd-{n}.conf -d -A 127.0.0.1 -i /tmp/ripd-{n}.pid > logs/ripd-{n}.log 2>&1".format(n=r1.name))
r2.cmd("/usr/sbin/zebra -f /tmp/quagga/zebra-{n}.conf -d -A 127.0.0.1 -i /tmp/zebra-{n}.pid > logs/zebra-{n}.log 2>&1".format(n=r2.name))
time.sleep(2)
r2.cmd("/usr/sbin/ripd -f /tmp/quagga/ripd-{n}.conf -d -A 127.0.0.1 -i /tmp/ripd-{n}.pid > logs/ripd-{n}.log 2>&1".format(n=r2.name))
```