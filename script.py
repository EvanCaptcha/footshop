import requests
import json
import string
import random
from random import randint
import threading
credit_card = '4147202344402480'
card_url = 'https://api2.checkout.com/v2/tokens/card'
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "AUTHORIZATION": "pk_76be6fbf-2cbb-4b4a-bd3a-4865039ef187",
    "Content-Type": "application/json",
    "Origin": "https://js.checkout.com",
    "Referer": "https://js.checkout.com/frames/?v=1.0.16&publicKey=pk_76be6fbf-2cbb-4b4a-bd3a-4865039ef187&localisation=EN-GB&theme=standard",
    "Sec-Fetch-Mode": "cors",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
}
payload = {
    "number": credit_card,
    "expiryMonth": "03",
    "expiryYear": "23",
    "cvv": "320",
    "requestSource": "JS"
}
headers2 = {
    "content-type": "application/json,application/json",
    "accept": "application/json",
    "accept-encoding": "gzip, deflate",
    "accept-language": "en-US,en;q=0.8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
}
threads=1

def task():
    print('Generating token')
    response = requests.post(card_url, json=payload, headers=headers)
    json_data = json.loads(response.text)
    json_token = json_data["id"]
    print(json_token)
    raffle_api_link = 'https://releases.footshop.com/api/registrations/create/9wfdJW0Bq3iiUGQBc7Fp'
    def random_string_generator_variable_size(min_size, max_size, allowed_chars):
        return ''.join(random.choice(allowed_chars) for x in range(randint(min_size, max_size)))

    chars = string.ascii_letters
    rando = random_string_generator_variable_size(6, 12, chars)
    print('Random String of random length (6-12) = ' + rando)
    randoAddy = random_string_generator_variable_size(3, 3, chars)
    print(randoAddy)

    def random_with_N_digits(n):
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1
        return randint(range_start, range_end)

    phoneNumber = random_with_N_digits(10)

    payload2 ={
            "sizerunId": "2de350ce-d569-11e9-bf68-1666500de9f2",
            "account": "New Customer",
            "email": rando + "@pinguaccounts.com",
            "phone": "8879905653",
            "gender": "Mr",
            "firstName": "Evan",
            "lastName": "Wohl",
            "birthday": "1997-04-04",
            "deliveryAddress": {
                "country": "US",
                "state": "NY",
                "county": "",
                "city": "Chappaqua",
                "street": "Quaker Lane",
                "houseNumber": randoAddy + " 21",
                "additional": "",
                "postalCode": "10514"
            },
            "consents": [
                "privacy-policy-101"
            ],
            "cardToken": json_token,
            "cardLast4": "2480"
        }
    response2 = requests.post(raffle_api_link, json=payload2, headers=headers2)
    print(response2.text)
    json_raffle = json.loads(response2.text)
    json_3ds = json_raffle["secure3DRedirectUrl"]
    print("Your 3D secure link is: " + json_3ds)


# create threads
jobs = []
for i in range(0, threads):
    jobs.append(threading.Thread(target=task))

# start  threads
for j in jobs:
    j.start()

# ensure all threads have been finished
for j in jobs:
    j.join()

