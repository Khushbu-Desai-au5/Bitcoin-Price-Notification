import argparse
import requests
import time
from datetime import datetime

REGULAR_NOTIFICATION_TELEGRAM = "regular_notification_telegram"
EMERGENCY_NOTIFICATION_TELEGRAM = "emergency_notification_telegram"

REGULAR_NOTIFICATION_EMAIL = "regular_notification_email"
EMERGENCY_NOTIFICATION_EMAIL = "emergency_notification_email"

crypto_api_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency'\
    '/listings/latest?CMC_PRO_API_KEY=ff7ff90a-f2b8-4f96-8e00-a8a27b86213c'
ifttt_url = 'https://maker.ifttt.com/trigger/{notification_type}/with/key/'\
    'fFA5mGSE4cW_nekvFEAreEwlU3_neAgv7LscMuQxzX_'

currency_converter_api = 'https://api.exchangeratesapi.io/latest?base=USD'


# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-t", "--Threshold",
                    help="Enter Threshold Price for Emergency Notification")
parser.add_argument("-i", "--Interval",
                    help=" Enter Notification Time Interval in Seconds")
parser.add_argument("-c", "--CoinType",
                    help="Enter Type of Crypto-Currency")
parser.add_argument("-n", "--notification",
                    help='Enter where you want notification: Email or Telegram'
                    )
parser.add_argument("-e", "--exchange",
                    help='''Enter exchange currency in which you want
                    notification(write only 3 digit e.g. INR)'''
                    )


# Read arguments from command line
args = parser.parse_args()

# if user didn't give optional argument then below will consider by python

threshold = 10000
interval = 60
coinType = 'Bitcoin'
notification = 'Telegram'
exchange = "USD"


if args.Threshold:
    threshold = args.Threshold
if args.Interval:
    interval = args.Interval
if args.CoinType:
    coinType = args.CoinType
if args.notification:
    notification = args.notification
if args.exchange:
    exchange = args.exchange
    exchange = exchange.upper()


def get_cryptoCurrency_latest_price(coinType, currency):
    response = requests.get(crypto_api_url)
    jsonRes = response.json()
    data = jsonRes['data']
    obj = ''
    for x in data:
        if(x['name'].lower() == coinType.lower()):
            obj = x
            break
    if(obj != ''):
        price = float(obj['quote']['USD']['price'])
        if (currency != "USD"):
            currency_responce = requests.get(currency_converter_api)
            currency_responce_json = currency_responce.json()
            exchange_rate = currency_responce_json['rates']
            for key in exchange_rate.keys():
                if (key == currency):
                    rate = exchange_rate[currency]
                    final_rate = (price*rate)
                    return {'price': final_rate, 'exchange': currency}
        exchange = "USD"
        return {'price': price, 'exchange': exchange}
    else:
        print('Invalid crypto currency')
        return None


def format_objectToSend(objectToSend):
    formatted_date = objectToSend['date'].strftime('%d.%m.%Y %H:%M')
    coinType = objectToSend['coinType'].capitalize()
    price = round(objectToSend['price'], 2)

    output = {'value1': coinType, 'value2': price, 'value3': exchange,
              'occurredAt': formatted_date
              }
    return output


def push_ifttt_notification(notification, data):
    if(notification == "telegram"):
        ifttt_notification_url = ifttt_url.format(
            notification_type=REGULAR_NOTIFICATION_TELEGRAM)
    elif(notification == "telegram_emergency"):
        ifttt_notification_url = ifttt_url.format(
            notification_type=EMERGENCY_NOTIFICATION_TELEGRAM)
    elif(notification == "email"):
        ifttt_notification_url = ifttt_url.format(
            notification_type=REGULAR_NOTIFICATION_EMAIL)
    elif(notification == "email_emergency"):
        ifttt_notification_url = ifttt_url.format(
            notification_type=EMERGENCY_NOTIFICATION_EMAIL)
    else:
        print("invalid notification type")
        return

    requests.post(ifttt_notification_url, json=data)


while True:
    # Make a API call to coinmarket API to get latest price of crypto currency
    output = get_cryptoCurrency_latest_price(coinType, exchange)
    date = datetime.now()
    price = float(output['price'])
    currency = output['exchange']
    objectToSend = {'price': price, 'date': date,
                    'coinType': coinType, 'exchange': currency}

    if(price):
        if(price <= float(threshold)):
            push_ifttt_notification(notification.lower()+"_emergency",
                                    format_objectToSend(objectToSend,
                                                        )
                                    )

        push_ifttt_notification(notification.lower(), format_objectToSend(
            objectToSend))
    else:
        break

    time.sleep(int(interval))
