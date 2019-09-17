import requests
import json
from time import sleep
import random
from random import randint
import string
import threading
from discord_webhook import DiscordWebhook, DiscordEmbed
from license import read_license, verify_license, write_license
from computer import Computer
import sys
import names

# read license key from disk
license_key = read_license()

# license not found, ask for it
if not license_key:
    computer = Computer()

    print("Your unique key is " + computer.get_hwid())
    license_key = input("Enter your license key: ")

# verify license
if verify_license(license_key):
    write_license(license_key)
else:
    print("Invalid license!")
    sys.exit()

site_key = '6LdnDpgUAAAAAFp50woveqE_jH9n3gsXJasjwufq'
url = 'http://extrabutterny.com'
threads = input('How many tasks? ')
API_KEY = input("Whats the API key for 2cap? ")
webhookURL = input("Whats your webhook? ")
cc = input("Whats your credit card number? ")
cvv = input("Whats the cvv? ")
exp_month = input("Whats the expiration month? (ex. 01) ")
exp_year = input("Whats the expiration year? (ex. 23)")
catchall = input("Whats the catchall? (ex. @evxn.io) ")
address = input("Address line 1? ")
address2 = input("Address line 2? (If N/A, put a random Apt #. Ex. Apt #21) ")
city = input('Whats your city? ')
state = input('Whats your state? (ex. NY) ')
zip = input('Whats your zip code? ')
varient = input("Whats the varient? ")

def task():
    s = requests.session()
    # here we post site key to 2captcha to get captcha ID (and we parse it here too)
    captcha_id = s.post("http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(API_KEY, site_key, url)).text.split('|')[1]
    # then we parse gresponse from 2captcha response
    recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
    print("solving ref captcha...")
    while 'CAPCHA_NOT_READY' in recaptcha_answer:
        print('Captcha not ready...')
        sleep(5)
        recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
    recaptcha_answer = recaptcha_answer.split('|')[1]
    def random_string_generator_variable_size(min_size, max_size, allowed_chars):
        return ''.join(random.choice(allowed_chars) for x in range(randint(min_size, max_size)))
    def random_with_N_digits(n):
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1
        return randint(range_start, range_end)

    phoneNumber = random_with_N_digits(10)

    chars = string.ascii_letters
    rando = random_string_generator_variable_size(6, 12, chars)
    randoAddy = random_string_generator_variable_size(3, 3, chars)
    headers = {
        "content-type": "application/json",
        "accept": "application/json",
        "accept-encoding": "gzip, deflate",
        "accept-language": "en-US,en;q=0.8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    }
    email = rando + catchall
    payload = {
        "email": email,
        "product_id": "3906146598960",
        "challenge_response": recaptcha_answer,
 }
    validateEmail = 'https://eb-draw.herokuapp.com/customers/validateEmail'
    s.post(validateEmail, headers=headers, json=payload)
    newUserLink = 'https://eb-draw.herokuapp.com/customers/new'
    newPayload = {
        "first_name": names.get_first_name(gender='male'),
        "last_name": names.get_last_name(),
        "email": email
    }
    response = s.post(newUserLink, headers=headers, json=newPayload)
    json_raffle = json.loads(response.text)
    customerID = json_raffle["id"]

    entryPaylod = {
        "shipping_first_name": names.get_first_name(gender='male'),
        "shipping_last_name": names.get_last_name(),
        "customer_id": customerID,
        "variant_id": varient,
        "street_address": randoAddy + " " + address + " " + address2,
        "city": city,
        "zip": zip,
        "state": state,
        "phone": phoneNumber,
        "country": "United States",
        "delivery_method": "online"

    }
    entryLink = 'https://eb-draw.herokuapp.com/draws/entries/new'
    raffle_id = s.post(entryLink, headers=headers, json=entryPaylod)
    json_raffleid = json.loads(raffle_id.text)
    raffleid = json_raffleid["id"]

    tokenAPI = "https://api.stripe.com/v1/tokens?card[number]=" + cc + "&card[cvc]=" + cvv + "&card[exp_month]=" + exp_month + "&card[exp_year]=" + exp_year + "&guid=45c139ce-e8db-40b6-949d-a49b8d950216&muid=9fec740c-b7c8-46e1-9367-4a0c09cf6ce1&sid=087a8e05-bf23-4bb3-bf25-0bbb916ef0df&payment_user_agent=stripe.js%2Ff13a0323%3B+stripe-js-v3%2Ff13a0323&referrer=https%3A%2F%2Fshop.extrabutterny.com%2Fproducts%2Fadidas-yeezy-350-v2-citrin-fw3042%3Fvariant%3D29633029046320&key=pk_live_u42h9k3kHDcKpj3DjgyIXjc7"
    tokenHeaders = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://js.stripe.com",
        "Referer": "https://js.stripe.com/v3/controller-c62905a44c003da4daa7d77169f71ef7.html",
        "Sec-Fetch-Mode": "cors",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    }
    tokenReq = requests.post(tokenAPI, headers=tokenHeaders)
    json_tokenReq = json.loads(tokenReq.text)
    token = json_tokenReq["id"]
    checkoutlink = 'https://eb-draw.herokuapp.com/draws/entries/checkout'
    checkoutPayload = {
        "checkout_token": token,
        "entry_id": raffleid
    }
    s.post(checkoutlink, headers=headers, json=checkoutPayload)
    webhook = DiscordWebhook(url=webhookURL)
    embed = DiscordEmbed(title='Raffle Bot - Succes!', description='Succesful entry on extra butter - email ' + email, color=int('009000'))
    webhook.add_embed(embed)
    webhook.execute()


# create threads
jobs = []
for i in range(0, int(threads)):
    jobs.append(threading.Thread(target=task))

# start  threads
for j in jobs:
    j.start()

# ensure all threads have been finished
for j in jobs:
    j.join()

