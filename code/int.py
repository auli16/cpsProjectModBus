import psutil

# Obtain the interfaces of the machine and print them
interfaces = psutil.net_if_addrs()
for iface in interfaces:
    print(iface)
