# The script is a Python Flask web application that implements an API endpoint for creating a charge. 
# The API endpoint receives a JSON payload with the customer's CPF, CVC, expiration date, and credit card number. 
# The script then validates the input data using four validation functions: is_valid_cpf, is_valid_cvc, is_valid_expiration_date, and is_valid_credit_card_number.
# If the input data is invalid, the API returns a 'denied' status with a 400 HTTP response code. 
# Otherwise, the API creates a new transaction record in a MySQL database, sets the transaction status to 'approved', and returns the status with a 200 HTTP response code.



from flask import Flask, request
import re
from datetime import datetime
import mysql.connector

app = Flask(__name__)

def is_valid_cpf(cpf: str) -> bool:

    # Verifica a formatação do CPF
    if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
        return False

    # Obtém apenas os números do CPF, ignorando pontuações
    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    # Verifica se o CPF possui 11 números ou se todos são iguais:
    if len(numbers) != 11 or len(set(numbers)) == 1:
        return False

    # Validação do primeiro dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        return False

    # Validação do segundo dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        return False

    return True

def is_valid_cvc(cvc):
    return bool(re.match('^[0-9]{3}$', cvc))

def is_valid_expiration_date(expiration_date):
    try:
        expiration_date = datetime.strptime(expiration_date, '%m/%y')
        return expiration_date > datetime.now()
    except ValueError:
        return False

def is_valid_credit_card_number(cardNo):
     
    nDigits = len(cardNo)
    nSum = 0
    isSecond = False
     
    for i in range(nDigits - 1, -1, -1):
        d = ord(cardNo[i]) - ord('0')
     
        if (isSecond == True):
            d = d * 2
  
        # We add two digits to handle
        # cases that make two digits after
        # doubling
        nSum += d // 10
        nSum += d % 10
  
        isSecond = not isSecond
     
    if (nSum % 10 == 0):
        return True
    else:
        return False

def is_valid_amount(amount):
    return amount < 2000

BLOCKED_ISSUERS = ['Citibank', 'North Shore Bank', 'Centennial Bank', 'Thrivent Federal Credit Union']  # List of blocked issuers

@app.route('/createCharge', methods=['POST'])
def handle_post_request():
    data = request.get_json()
    cpf = data.get('cpf')
    cvc = data.get('cvc')
    expiration_date = data.get('ExpirationDate')
    card_number = data.get('cardNumber')
    issuer = data.get('issuer')
    amount = data.get('amount')

    status = 'approved'
    time = datetime.now().strftime('%Y-%m-%d %H:%M:00')
    try:
        cnx = mysql.connector.connect(user='mateus', password='mateus99790087',
                                       host='localhost', database='cwtask1')
        cursor = cnx.cursor()

        add_transaction = ("INSERT INTO requests "
                           "(time, status, cpf, cvc, expiration_date, credit_card_number, issuer) "
                           "VALUES (%s, %s, %s, %s, %s, %s, %s)")

        if not is_valid_cpf(cpf):
            cpf = None
            status = 'failed'
        if not is_valid_cvc(cvc):
            cvc = None
            status = 'failed'
        if not is_valid_expiration_date(expiration_date):
            expiration_date = None
            status = 'failed'
        if not is_valid_credit_card_number(card_number):
            card_number = None
            status = 'failed'
        if not is_valid_amount(amount):
            status = 'reversed'
        if issuer in BLOCKED_ISSUERS:  # Check if issuer is in the list of blocked issuers
            status = 'denied'

        transaction_data = (time, status, cpf, cvc, expiration_date, card_number, issuer)

        cursor.execute(add_transaction, transaction_data)
        cnx.commit()

        cursor.close()
        cnx.close()

        if status == 'denied':
            return 'Issuer is blocked', 400
        if status == 'failed': 
            return 'Invalid data', 400

    except mysql.connector.Error as err:
        print(err)
        status = 'denied'

    if status == 'denied':
        return 'Invalid data', 400
    else:
        print(data)
        return status

if __name__ == '__main__':
    app.run(debug=True)