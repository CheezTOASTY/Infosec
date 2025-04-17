#    __                         __                                      
#  _/  |_  _________    _______/  |________   ____   ____  ____   ____  
#  \   __\/  _ \__  \  /  ___/\   __\_  __ \_/ __ \_/ ___\/  _ \ /    \ 
#   |  | (  <_> ) __ \_\___ \  |  |  |  | \/\  ___/\  \__(  <_> )   |  \
#   |__|  \____(____  /____  > |__|  |__|    \___  >\___  >____/|___|  /
#                   \/     \/                    \/     \/           \/ 
#  v1.1                                                                     
                                                                     

import socket
from threading import Thread
import logging

def setup_logging():
    logging.basicConfig(
        filename="port_scan_results.log",
        filemode="w",
        format="%(asctime)s - %(message)s",
        level=logging.INFO
    )

def log_result(port, status):
    logging.info(f"Port {port}: {status}")

def scan_port(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((host, port)) == 0:
                print(f"[+] Port {port} is open")
                log_result(port, "Open")
            else:
                log_result(port, "Closed")
    except Exception as e:
        log_result(port, f"Error - {e}")

def main():
    setup_logging()
    host = input("Enter the target IP or hostname: ")
    start_port = int(input("Enter the starting port: "))
    end_port = int(input("Enter the ending port: "))
    
    print(f"Scanning {host} from port {start_port} to {end_port}...")
    
    threads = []
    for port in range(start_port, end_port + 1):
        thread = Thread(target=scan_port, args=(host, port))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print("Scanning completed!")
    print("Results have been saved to 'port_scan_results.log'.")

if __name__ == "__main__":
    main()