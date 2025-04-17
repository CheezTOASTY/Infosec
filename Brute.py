#    __                         __                                      
#  _/  |_  _________    _______/  |________   ____   ____  ____   ____  
#  \   __\/  _ \__  \  /  ___/\   __\_  __ \_/ __ \_/ ___\/  _ \ /    \ 
#   |  | (  <_> ) __ \_\___ \  |  |  |  | \/\  ___/\  \__(  <_> )   |  \
#   |__|  \____(____  /____  > |__|  |__|    \___  >\___  >____/|___|  /
#                   \/     \/                    \/     \/           \/ 
#  Brute v1.4                                                                     
                                                                     

import requests
from threading import Thread, Lock
import logging
import os

# Setup logging
def setup_logging():
    logging.basicConfig(
        filename="bruteforce_results.log",
        filemode="w",
        format="%(asctime)s - %(message)s",
        level=logging.INFO
    )

# Log results
def log_result(url, status):
    logging.info(f"{status}: {url}")

# Directory brute-force function
def brute_force(base_url, wordlist, status_codes, headers, proxies, lock, recurse):
    try:
        with open(wordlist, "r") as file:
            directories = file.readlines()
    except FileNotFoundError:
        print("Wordlist file not found. Please check the file path.")
        return

    for directory in directories:
        directory = directory.strip()
        url = f"{base_url.rstrip('/')}/{directory}"
        
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=5)
            if response.status_code in status_codes:
                with lock:
                    print(f"[{response.status_code}] Found: {url}")
                    log_result(url, f"Status {response.status_code}")
                # Recursive directory search
                if recurse and response.status_code == 200:
                    brute_force(url, wordlist, status_codes, headers, proxies, lock, recurse)
        except requests.exceptions.RequestException as e:
            with lock:
                print(f"[Error] {url} - {e}")
                log_result(url, "Error")
                
def process_wordlist(base_url, wordlist, status_codes, headers, proxies, recurse):
    lock = Lock()
    threads = []
    try:
        with open(wordlist, "r") as file:
            directories = file.readlines()
    except FileNotFoundError:
        print("Wordlist file not found. Please check the file path.")
        return
    
    for directory in directories:
        directory = directory.strip()
        thread = Thread(
            target=brute_force,
            args=(base_url, wordlist, status_codes, headers, proxies, lock, recurse)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Main program
def main():
    setup_logging()
    print("=== Enhanced Directory Brute-Forcer ===")

    # Get user inputs
    base_url = input("Enter the target base URL (e.g., http://example.com): ").strip()
    wordlist = input("Enter the path to the wordlist file: ").strip()
    filter_status_codes = input("Enter HTTP status codes to filter (e.g., 200,403), or leave blank for all: ").strip()
    proxy = input("Enter a proxy (e.g., http://127.0.0.1:8080), or leave blank for none: ").strip()
    recurse = input("Enable recursive scanning? (yes/no): ").strip().lower()

    # Prepare headers, proxies, and filters
    headers = {"User-Agent": "Mozilla/5.0 (DirectoryBruteForcer)"}
    proxies = {"http": proxy, "https": proxy} if proxy else None
    status_codes = list(map(int, filter_status_codes.split(","))) if filter_status_codes else [200, 403, 404]
    recurse = recurse == "yes"
    
    # Start brute-forcing
    process_wordlist(base_url, wordlist, status_codes, headers, proxies, recurse)

    print("Brute-force completed! Results are logged in 'bruteforce_results.log'.")

if __name__ == "__main__":
    main()