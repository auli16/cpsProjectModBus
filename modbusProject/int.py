import psutil

# Ottieni tutte le interfacce di rete
interfaces = psutil.net_if_addrs()

# Stampa i nomi leggibili delle interfacce
for iface in interfaces:
    print(iface)
