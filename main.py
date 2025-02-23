import requests
import random
import json
import time

print("\033[1;33m==============================================\033[0m")
print("\033[1;33m   𝙁 𝙊 𝙍 𝙀 𝙎 𝙏 𝘼 𝙍 𝙈 𝙔   \033[0m")
print("\033[1;36m 𝙹𝚘𝚒𝚗 𝚞𝚜: 𝚑𝚝𝚝𝚙𝚜://𝚝.𝚖𝚎/𝚏𝚘𝚛𝚎𝚜𝚝𝚊𝚛𝚖𝚢 \033[0m")
print("\033[1;33m==============================================\033[0m")

from eth_account import Account
from mnemonic import Mnemonic

# Enable HD wallet features
Account.enable_unaudited_hdwallet_features()

# Ask user for the number of wallets to generate
num_wallets = int(input("How many Ethereum wallets do you want to create? "))

for i in range(num_wallets):
    mnemo = Mnemonic("english")
    mnemonic_phrase = mnemo.generate(strength=128)  # 12-word seed phrase
    account = Account.from_mnemonic(mnemonic_phrase)

    wallet_address = account.address
    private_key = account.key.hex()

    # Append wallet address and private key to wallet.txt
    with open("wallet.txt", "a") as f:
        f.write(f"{wallet_address}:{private_key}\n")

    # Append full details to eth_account.txt
    with open("eth_account.txt", "a") as f:
        f.write(f"Wallet {i+1}:\n")
        f.write(f"Address: {wallet_address}\n")
        f.write(f"Private Key: {private_key}\n")
        f.write(f"Seed Phrase: {mnemonic_phrase}\n")
        f.write("-" * 40 + "\n")  # Separator for readability

    print(f"Wallet {i+1} created: {wallet_address}")

print(f"{num_wallets} Ethereum wallets created successfully! @itsmesatyavir")


# Function to read wallet addresses from a file
def read_wallets(file_path):
    wallets = []
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split(':')
            if len(parts) == 2:
                wallets.append(parts[0])  # Extract ETH address
    return wallets

# Function to generate a random referral code
def generate_referral_code():
    return f"0x{random.randint(10**7, 10**8-1):x}"

# Function to get points from a referral code
def get_points_from_referral_code(referral_code):
    url = f"https://boustneqsaombfmtfffq.supabase.co/rest/v1/waitlist?referral_code=eq.{referral_code}&select=points"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJvdXN0bmVxc2FvbWJmbXRmZmZxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk3MzA0NTQsImV4cCI6MjA1NTMwNjQ1NH0.FeSHmHVeSQvQ2hVz0PHYBhFTijOY2U_U_zl4LIxFG_w",  # Your token
        "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJvdXN0bmVxc2FvbWJmbXRmZmZxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk3MzA0NTQsImV4cCI6MjA1NTMwNjQ1NH0.FeSHmHVeSQvQ2hVz0PHYBhFTijOY2U_U_zl4LIxFG_w",  # Your API key
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0].get('points', 0)  # Retrieve points from response
    return 100  # Return 100 if not found or an error occurs

# Function to register a new user
def register_user(full_name, email, eth_address, new_referral_code, referrer_code):
    points = get_points_from_referral_code(referrer_code)  # Get points from referrer code
    url = "https://boustneqsaombfmtfffq.supabase.co/rest/v1/waitlist"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJvdXN0bmVxc2FvbWJmbXRmZmZxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk3MzA0NTQsImV4cCI6MjA1NTMwNjQ1NH0.FeSHmHVeSQvQ2hVz0PHYBhFTijOY2U_U_zl4LIxFG_w",  # Your token
        "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJvdXN0bmVxc2FvbWJmbXRmZmZxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk3MzA0NTQsImV4cCI6MjA1NTMwNjQ1NH0.FeSHmHVeSQvQ2hVz0PHYBhFTijOY2U_U_zl4LIxFG_w",  # Your API key
    }
    
    data = {
        "full_name": full_name,
        "email": email,
        "eth_address": eth_address,
        "referral_code": new_referral_code,  # New user's referral code
        "points": points  # Points from the referrer code
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.status_code, response.text

# Function to save account details to a file
def save_account(file_path, email, eth_address, referral_code):
    with open(file_path, 'a') as f:
        f.write(f"{email}:{eth_address}:{referral_code}\n")

# Main function to execute the process
def main():
    wallets = read_wallets("wallet.txt")  # Read wallets from file
    if not wallets:
        print("No wallets found!")
        return
    
    # Input referrer code at runtime
    referrer_code = input("Enter the referrer code: ").strip()
    
    while wallets:
        eth_address = wallets.pop(0)
        full_name = f"User{len(wallets)}"
        email = f"user{len(wallets)}@jobcyvn.site"
        
        # Generate a random referral code for the new account
        new_referral_code = generate_referral_code()
        
        # Register the new user
        status, response = register_user(full_name, email, eth_address, new_referral_code, referrer_code)
        if status == 201:
            print(f"Registered: {email} - {eth_address} with ref: {new_referral_code}")
            save_account("data.txt", email, eth_address, new_referral_code)  # Save account details
        else:
            print(f"Failed: {response}")
        
        time.sleep(2)  # Prevent API spam

# Run the main function
if __name__ == "__main__":
    main()
