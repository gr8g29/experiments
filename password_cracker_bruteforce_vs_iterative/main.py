# password cracker made in python

######### IMPORTS #########

import random
import time
from itertools import product, islice


######### USEFUL FUNCTIONS #########

# function to generate a random password
def generate_password(length, chars):
    password = ""
    for i in range(length):
        password += random.choice(chars)
    return password

# function to calculate how many attemps are made per second on average for bruteforce method
def measure_attempts_per_second_brute(length, chars, sample_size= 100000):
    start = time.time()
    for _ in range(sample_size):
        generate_password(length, chars)
    end = time.time()
    elapsed = end - start
    return sample_size / elapsed

# function to calculate how many attemps are made per second on average for iteration method
def measure_attempts_per_second_iteration(length, chars, sample_size = 100000):
    start = time.time()
    _ = list(islice(product(chars, repeat = length), sample_size))  
    end = time.time()
    elapsed = end - start
    return sample_size / elapsed


# function to format time in a readable way in the terminal
def format_time(seconds):
    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    if days >= 1:
        return f"{int(days)}d {int(hours)}h {int(minutes)}m"
    elif hours >= 1:
        return f"{int(hours)}h {int(minutes)}m {int(sec)}s"
    elif minutes >= 1:
        return f"{int(minutes)}m {int(sec)}s"
    else:
        return f"{int(sec)} seconds"


######### SETUP #########

characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;':\",.<>?/"
#test_password = generate_password(random.randint(x,y), characters) # this is the password that will be cracked
test_password = input("Enter the password you want to crack: ")
print(f"\nPassword to crack: {test_password}")
chars = ""
pw_length = int(input("\nEnter the length of the password you want to crack: "))
numbers = input("Does your password contain numbers? (y/n): ")
letters = input("Does your password contain letters? (y/n): ")
if letters.lower() == "y":
    letters_caps = input("Does your password contain only capital letters? (y/n): ")
    if letters_caps.lower() == "n":
        letters_miniscule = input("Does your password contain only lowercase letters? (y/n): ")
special = input("Does your password contain special characters? (y/n): ")

if numbers.lower() == "y":
    chars += "0123456789"
if letters.lower() == "y":
    if letters_caps.lower() == "y":
        chars += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    else:
        if letters_miniscule.lower() == "y":
            chars += "abcdefghijklmnopqrstuvwxyz"
        else:
            chars += "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" 
if special.lower() == "y":
    chars += "!@#$%^&*()_+-=[]{}|;':\",.<>?/"

if numbers.lower() == "n" and letters.lower() == "n" and special.lower() == "n":
    print("\nYou must select at least one character type.")
    exit()

print(f'\nCharacters used: {chars}')


######### CRACKING PASSWORD #########

# brute force password cracker
def crack_password_bruteforce(length, chars):
    attempts = 0
    while True:
        password = generate_password(length, chars)
        attempts += 1
        if password == test_password:
            print(f"\nPassword cracked with the bruteforce method: {password}")
            print(f"\nAttempts: {attempts}")
            print("")
            break

# iteration password cracker
def crack_password_iterative(length, chars):
    attempts = 0
    for attempt in product(chars, repeat = length):
        guess = ''.join(attempt)
        attempts += 1
        if guess == test_password:
            print(f"\nPassword cracked with the iteration method: {guess}")
            print(f"\nAttempts: {attempts}")
            break




######### MAIN #########

print("\nSelect a method to crack the password.")
method = input("Enter 1 for brute force or 2 for iteration: ")
# bruteforce method
if method == "1":
    # estimate total time to crack
    attempts_per_sec = measure_attempts_per_second_brute(pw_length, chars)
    total_combinations = len(chars) ** pw_length
    # brute force = random guessing = might take very long or get lucky
    # iteration = guarantees to eventually find it, in worst case all combinations
    avg_attempts_needed = total_combinations # worst case
    estimated_time = avg_attempts_needed / attempts_per_sec
    print("\nMeasuring cracking speed...")
    print(f"Estimated brute-force speed: {int(attempts_per_sec):,} attempts/second")
# iteration method
elif method == "2":
    # estimate total time to crack
    attempts_per_sec = measure_attempts_per_second_iteration(pw_length, chars)
    total_combinations = len(chars) ** pw_length # average
    # brute force = random guessing = might take very long or get lucky
    # iteration = guarantees to eventually find it, in worst case all combinations
    avg_attempts_needed = total_combinations / 2
    estimated_time = avg_attempts_needed / attempts_per_sec
    print("\nMeasuring cracking speed...")
    print(f"Estimated iteration speed: {int(attempts_per_sec):,} attempts/second")
else:
    print("No method selected. Exiting...")
    exit()


print(f'Estimated amount of attempts needed: {int(avg_attempts_needed):,}')
if format_time(estimated_time) == "0 seconds":
    print("Estimated time to crack: less than 1 second")
else:
    print(f"Estimated average time to crack: {format_time(estimated_time)}")

# ask user if they want to continue
continuing = input("\nDo you want to continue? (y/n): ")
if continuing.lower() == "y":
    if method == "1":
        print("\nStarting brute-force password cracker...")
        crack_password_bruteforce(pw_length, chars)
    elif method == "2":
        print("\nStarting iterative password cracker...")
        crack_password_iterative(pw_length, chars)
    else:
        print("\nNo method selected. Exiting...")
        exit()
else:
    print("\nExiting...")
    exit()


