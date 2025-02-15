from scapy.all import IP, TCP, sniff, Raw

def packet_handler(packet):
    '''
    Callback function to handle the packets captured by the sniffer.
    params:
        packet: The packet captured by the sniffer.
    '''
    # Verify if the packet has a TCP layer and a Raw layer
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        packet = bytes(packet[Raw]) # Obtain the packet as bytes
        print("Packet:", packet, "\n")

'''
Start sniffing the packets on the loopback interface
The loopback interface is used to capture the packets sent to localhost, the name can be found by executing int.py
The function packet_handler will be called for each packet captured
'''
sniff(iface="Software Loopback Interface 1", prn=packet_handler, filter="tcp port 503", count=20) 