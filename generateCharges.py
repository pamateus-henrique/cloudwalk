# This script generates a given number of POST requests per minute to a local server endpoint (http://localhost:5000/createCharge) with random data for each request. 
# The user is prompted to choose whether to generate valid or invalid credit card numbers for the requests.
# The script generates random CPFs (Brazilian tax identification number), credit card numbers, expiration dates, CVCs (Card Verification Code), and amounts for each request. 
# It uses the Faker library to generate the credit card numbers and adds a '1' to the beginning of the number to create an invalid credit card number.
# The script also includes functions to generate a random CPF and to calculate the verification digits for a Brazilian CPF. 
# Finally, it includes a loop that waits for 1 minute between batches of requests and toggles between generating valid and invalid requests.


import requests
import time
import random
import datetime
from faker import Faker
from faker.providers import credit_card


# Set the number of requests per minute
requests_per_minute = int(input("Enter the number of requests per minute: "))

# Generate a random CPF
def generate_cpf():
    # Generate random CPF digits
    digits = [random.randint(0, 9) for _ in range(9)]

    # Calculate the first verification digit
    sum = 0
    for i in range(9):
        sum += digits[i] * (10 - i)
    digit1 = 11 - (sum % 11)
    digit1 = digit1 if digit1 <= 9 else 0

    # Calculate the second verification digit
    sum = 0
    for i in range(9):
        sum += digits[i] * (11 - i)
    sum += digit1 * 2
    digit2 = 11 - (sum % 11)
    digit2 = digit2 if digit2 <= 9 else 0

    # Format the CPF as a string with a mask
    cpf = '{}{}{}{}{}{}{}{}{}{}{}'.format(*digits, digit1, digit2)
    cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    return cpf

# Generate a random credit card number
def generate_credit_card_number():
    fake = Faker()
    fake.add_provider(credit_card)
    return fake.credit_card_number()

# Generate an invalid credit card number
def generate_invalid_credit_card_number():
    fake = Faker()
    fake.add_provider(credit_card)
    cc_number = fake.credit_card_number()
    return '1' + cc_number

# Generate a random expiration date in the format "MM/YY"
def generate_expiration_date():
    year = random.randint(2026, 2030)
    month = random.randint(1, 12)
    return f"{month:02}/{str(year)[-2:]}"

# Generate a random CVC
def generate_cvc():
    return str(random.randint(100, 999))

# Prompt the user to choose whether to generate valid or invalid requests
is_valid = True
choice = input("Generate valid requests? (y/n) ")
if choice.lower() == 'n':
    is_valid = False

# Create post requests to localhost:5000/createCharge
while True:
    for i in range(requests_per_minute):
        # Generate random data for the post request
        cpf = generate_cpf()
        issuer = random.choice(['Bank of America', 'Chase', 'Wells Fargo', 'Citibank', 'American Express', 'Capital One', 'Discover', 'US Bank', 'PNC Bank', 'TD Bank', 'HSBC', 'BB&T', 'SunTrust', 'Fifth Third Bank', 'KeyBank', 'Regions Bank', 'M&T Bank', 'Ally Bank', 'Huntington Bank', 'First Citizens Bank', 'Santander Bank', 'BBVA', 'Charles Schwab Bank', 'Axos Bank', 'EverBank', 'Bank of the West', 'Flagstar Bank', 'BMO Harris Bank', 'New York Community Bank', 'TCF Bank', 'Zions Bank', 'Webster Bank', 'MB Financial Bank', 'BancorpSouth Bank', 'First Horizon Bank', 'Old National Bank', 'First Commonwealth Bank', 'Cadence Bank', 'United Community Bank', 'Renasant Bank', 'First Financial Bank', 'Simmons Bank', 'Community Bank', 'First Midwest Bank', 'Independent Bank', 'Camden National Bank', 'First Merchants Bank', 'Investors Bank', 'First Financial Bank', 'North Shore Bank', 'Centennial Bank', 'Rockland Trust', 'Chemical Bank', 'Thrivent Federal Credit Union', 'Seacoast Bank', 'Wintrust Bank', 'National Cooperative Bank', 'South State Bank', 'Busey Bank', 'Bank of Marin', 'Columbia State Bank', 'Banner Bank', 'Bank of Hawaii', 'Pacific Premier Bank', 'Community Trust Bank', 'Bangor Savings Bank', 'Ameris Bank', 'Heartland Bank', 'Community Bank of the Chesapeake', 'Luther Burbank Savings', 'First Volunteer Bank', 'CenterState Bank', 'Bank of Sun Prairie', 'Lake City Bank', 'The Bryn Mawr Trust Company', 'Mechanics Bank', 'First Northern Bank', 'LNB Community Bank', 'Farmers & Merchants Bank', 'Westamerica Bank', 'First Business Bank', 'EagleBank', 'German American Bank', 'Pathfinder Bank', 'First Commonwealth Bank of Pennsylvania', 'Alpine Bank', 'IncredibleBank', 'New York Business Development Corporation', 'People’s United Bank', 'First Security Bank', 'First Bank and Trust', 'Mercer Savings Bank', 'Bridgewater Savings Bank', 'Academy Bank', 'Cornerstone Bank', 'First Federal Bank of Wisconsin', 'Pioneer Bank', 'Exchange Bank', 'Barrington Bank & Trust Company', 'Mound City Bank', 'The Conway National Bank', 'First Internet Bank', 'Cornerstone Community Bank', 'Sound Bank', 'Community Bank of Louisiana', 'New Era Bank', 'Civista Bank'])
        if is_valid:
            credit_card_number = generate_credit_card_number()
        else:
            credit_card_number = generate_invalid_credit_card_number()
        expiration_date = generate_expiration_date()
        cvc = generate_cvc()
        amount = random.randint(10, 1000)

        # Send the post request
        print(cpf, credit_card_number, expiration_date, cvc, amount)
        response = requests.post('http://localhost:5000/createCharge', json={
            'cpf': cpf,
            'cardNumber': credit_card_number,
            'ExpirationDate': expiration_date,
            'cvc': cvc,
            'amount': amount,
            'issuer': issuer
        })

        # Print the response status code and content
        print(f"Response: {response.status_code} {response.content}")
    
    # Wait for 1 minute before sending more requests
    time.sleep(60)
    # Toggle between generating valid and invalid requests
    is_valid = not is_valid
