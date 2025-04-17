#    __                         __                                      
#  _/  |_  _________    _______/  |________   ____   ____  ____   ____  
#  \   __\/  _ \__  \  /  ___/\   __\_  __ \_/ __ \_/ ___\/  _ \ /    \ 
#   |  | (  <_> ) __ \_\___ \  |  |  |  | \/\  ___/\  \__(  <_> )   |  \
#   |__|  \____(____  /____  > |__|  |__|    \___  >\___  >____/|___|  /
#                   \/     \/                    \/     \/           \/ 
#  Password-Checker v1.1                                                                     
                                                                     

import re
import logging

def setup_logging():
    logging.basicConfig(
        filename="password_strength.log",
        filemode="w",
        format="%(asctime)s - %(message)s",
        level=logging.INFO
    )

def log_result(password, result):
    logging.info(f"Password: {password} - Strength: {result}")

def check_password_strength(password):
    # Initialize strength criteria
    length = len(password) >= 8
    uppercase = re.search(r"[A-Z]", password) is not None
    lowercase = re.search(r"[a-z]", password) is not None
    digit = re.search(r"\d", password) is not None
    special_char = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is not None

    # Calculate password strength
    strength_score = sum([length, uppercase, lowercase, digit, special_char])
    
    # Provide feedback
    if strength_score == 5:
        return "Strong"
    elif strength_score >= 3:
        return "Moderate"
    else:
        return "Weak"

def process_passwords(passwords):
    for password in passwords:
        strength = check_password_strength(password)
        print(f"Password: {password} - Strength: {strength}")
        log_result(password, strength)

def main():
    setup_logging()
    print("=== Password Strength Checker ===")
    
    # Batch input processing
    option = input("Check a single password or process a batch (single/batch)? ").strip().lower()
    if option == "single":
        password = input("Enter a password to check: ")
        strength = check_password_strength(password)
        print(f"Password: {password} - Strength: {strength}")
        log_result(password, strength)
    elif option == "batch":
        print("Enter multiple passwords separated by commas:")
        passwords = input().split(",")
        passwords = [pwd.strip() for pwd in passwords]  # Remove extra whitespace
        process_passwords(passwords)
    else:
        print("Invalid option selected. Please run the script again.")

    print("Results have been logged in 'password_strength.log'.")

if __name__ == "__main__":
    main()