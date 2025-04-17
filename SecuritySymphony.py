#    __                         __                                      
#  _/  |_  _________    _______/  |________   ____   ____  ____   ____  
#  \   __\/  _ \__  \  /  ___/\   __\_  __ \_/ __ \_/ ___\/  _ \ /    \ 
#   |  | (  <_> ) __ \_\___ \  |  |  |  | \/\  ___/\  \__(  <_> )   |  \
#   |__|  \____(____  /____  > |__|  |__|    \___  >\___  >____/|___|  /
#                   \/     \/                    \/     \/           \/ 
#  SecuritySymphony v1.0                                                                     
                                                                     

import scapy.all as scapy
import time
import logging
import threading
from playsound import playsound
import matplotlib.pyplot as plt
from collections import defaultdict
import random

# Setup logging
def setup_logging():
    logging.basicConfig(
        filename="cyber_orchestra.log",
        filemode="w",
        format="%(asctime)s - %(message)s",
        level=logging.INFO
    )

# Play sound based on protocol or severity
def play_protocol_sound(protocol, severity):
    sound_library = {
        "TCP_low": "tcp_low.wav",
        "TCP_medium": "tcp_medium.wav",
        "TCP_high": "tcp_high.wav",
        "UDP_low": "udp_low.wav",
        "UDP_medium": "udp_medium.wav",
        "UDP_high": "udp_high.wav",
    }
    key = f"{protocol}_{severity}"
    if key in sound_library:
        playsound(sound_library[key])

# Visualize sound intensity feedback
def visualize_intensity(intensity_data):
    while True:
        plt.clf()
        labels = list(intensity_data.keys())
        values = list(intensity_data.values())
        plt.bar(labels, values, color="orange")
        plt.xlabel("Protocol Severity")
        plt.ylabel("Intensity")
        plt.title("Sound Intensity Feedback")
        plt.pause(0.5)

# Detect anomalies with melodies and visuals
def detect_anomalies(packet, intensity_data):
    try:
        if packet.haslayer(scapy.IP):
            ip_layer = packet[scapy.IP]
            src = ip_layer.src
            dst = ip_layer.dst
            ttl = ip_layer.ttl
            size = len(packet)
            protocol = packet.payload.name
            severity = "low"
            
            # Determine anomaly severity
            if ttl < 20 or size > 1500:
                severity = "medium" if ttl < 10 or size > 2000 else "high"
                intensity_data[f"{protocol}_{severity}"] += random.randint(10, 20)  # Simulate intensity increment
                
                # Log and alert
                logging.warning(f"Anomaly: Protocol={protocol}, Src={src}, Dst={dst}, TTL={ttl}, Size={size}, Severity={severity}")
                print(f"[ALERT] Protocol: {protocol}, Severity: {severity}")
                
                # Trigger sound
                threading.Thread(target=play_protocol_sound, args=(protocol, severity), daemon=True).start()
    except Exception as e:
        logging.error(f"Error processing packet: {e}")

def main():
    setup_logging()
    print("=== Interactive Cybersecurity Orchestra ===")
    
    # Initialize sound intensity data
    intensity_data = defaultdict(int)
    
    # Start visualizer in a separate thread
    threading.Thread(target=visualize_intensity, args=(intensity_data,), daemon=True).start()
    
    print("Monitoring network traffic for anomalies...")
    try:
        scapy.sniff(filter="ip", prn=lambda packet: detect_anomalies(packet, intensity_data), store=False)
    except PermissionError:
        print("You need administrative privileges to run this script!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    plt.ion()  # Enable interactive mode for visualizer
    main()