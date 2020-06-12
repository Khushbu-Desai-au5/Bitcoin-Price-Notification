# Bitcoin-Price-Notification

As we all know, Crypto Currency price is a fickle thing.You never really know where it’s going to be at the end of the day. 
So,instead of constantly checking various sites for the latest updates,this python program push crypto currency price notifications at certain time interval and also notify when price reach to a certain value as theresold value provided by user.


## Getting Started

Setting up a virtual environment.(To create an isolated environment for Project)

```
pip install virtualenv #install virtual environment

cd your_project 

virtualenv env 

.\env\Scripts\activate  #Activate the virtual environment
```

External Module Installation

```
pip install argparse (To make it easy to write user-friendly command-line interfaces)
pip install requests (To send HTTP requests and get responce from it)

```

### Set up command line interface

```
optional arguments:

  -h, --help            show this help message and exit
  -t THRESHOLD, --Threshold THRESHOLD
                        Enter Threshold Price for Emergency Notification
  -i INTERVAL, --Interval INTERVAL
                        Enter Notification Time Interval in Seconds
  -c COINTYPE, --CoinType COINTYPE
                        Enter Type of Crypto-Currency
  -n NOTIFICATION, --notification NOTIFICATION
                        Enter where you want notification: Email or Telegram
  -e EXCHANGE, --exchange EXCHANGE
                        Enter exchange currency in which you want
                        notification(write only 3 digit e.g. INR)
                        
```

If user didn't give above optional argument then python will consider below default parameter
```
threshold = 10000
interval = 60
coinType = 'Bitcoin'
notification = 'Telegram'
exchange = "USD"
```
## Work Flow

<img src="https://github.com/Khushbu-Desai-au5/Bitcoin-Price-Notification/blob/master/Diagram.PNG"/>


As shown in diagram,this utility will make an API call to coinmarket API to get latest price of crypto currency.

If user give coin type of crypto currency ,then it will fetch the price for that coin type. coin type such as Bitcoin, Ethereum, Ripple etc..

If user didn't give coin type then by default it will fetch bitcoin crypto currency price.

This utility will call fetch price API after every time Interval given by user or if its not given then it will take default interval.

After getting latest price,if user has choose exchange option,python program will call exchangerateapi to get latest exchange rate of currency and convert crypto price into currency chosen by user.

If user didn't give any exchange currency then by default it will give price in USD.

Now, to send notifications at certain time interval and also to send notification when price reach to a certain value as theresold value provided by user,this utility use the automation website IFTTT. 

IFTTT (“if this, then that”) is a web service that bridges the gap between different apps and devices.

For that we need to create four IFTTT applets:

1) Emergency notification when crypto price falls under a certain threshold (To send notification to Telegram)
2) Regular Telegram updates on the crypto currency price.(To send notification to Telegram)
3) Emergency notification when crypto price falls under a certain threshold (To send notification to Email)
4) Regular Telegram updates on the crypto currency price.(To send notification to Email)

Applet will be triggered by our Python app which will consume the data from the Coinmarketcap API.

An IFTTT applet is composed of two parts: a trigger and an action.

Our Python app will make an HTTP request to the webhook URL which will trigger an action.

There are two option for notification :

1)Telegram
2)Email

User can choose any option.if user didn't give any notification type then by default notification send to telegram.
Same for thersold value(price falls under some value),user can choose when they want emergency notification.

## Below are screenshot of notifications:

#### Telegram Emergency notification


<img src="https://github.com/Khushbu-Desai-au5/Bitcoin-Price-Notification/blob/master/Emergency%20telegram%20notification.png" width=700/>

#### Telegram Regular notification


<img src="https://github.com/Khushbu-Desai-au5/Bitcoin-Price-Notification/blob/master/Regular%20telegram%20notification.PNG" width=700/>

#### Email Emergency notification


<img src="https://github.com/Khushbu-Desai-au5/Bitcoin-Price-Notification/blob/master/Emergency%20Email%20notification.png" width=700/>



#### Email Regular notification


<img src="https://github.com/Khushbu-Desai-au5/Bitcoin-Price-Notification/blob/master/Regular%20Email%20notification.PNG" width=700/>





