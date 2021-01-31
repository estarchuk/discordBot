import string
import finder
import requests
import stonkPrice
import json

bad_words = ["fuck", "shit", "ass", 'bitch', 'cuck', 'fag', 'cunt']
gaming = ["gaming", "minecraft", "car soccer", "valorant", 'game']
im = ['im', 'i\'m']


async def commands(message):
    msg = message.content

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    await AutoBotResponseToMessages(message, msg)

    await GetTempForSpecifiedLocation(message)

    if message.content.startswith('$stonk'):
        finder.parseMessage(message)
        await finder.ping()

    if message.content.startswith('$price'):

        split = message.content.split(" ")
        symbol = split[1].upper()
        stonk = stonkPrice.getStonk(symbol)

        if stonk[1]:
            full = stonk[0]
            data = full['data']
            quote = data['quote']
            name = data['name']
            local_currency = quote['CAD']
            price = '{:.2f}'.format(local_currency['price'])
            currency = 'CAD'
        else:
            price = '{:.2f}'.format(stonk[0])
            name = symbol
            currency = 'USD'

        await message.channel.send(
            'The current price of ' + name + ' is ' + price + ' ' + currency
        )


async def GetTempForSpecifiedLocation(message):
    if message.content.startswith('$temp'):

        #First set the city name to a capitalized first letter
        SPLIT = message.content.split(" ", 1)
        CITY = SPLIT[1]
        CITY = string.capwords(CITY)

        #auto correct the city name if it is one of these
        if CITY == 'Victoria':
            CITY = 'Victoria, CA'
        if CITY == 'Grand Forks':
            CITY = 'Grand Forks, CA'

        #create the url for the openweathermap site to get the data from
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        API_KEY = 'a79339a9332f239b64d3d0d20e57fe91'
        URL = BASE_URL + 'q=' + CITY + "&appid=" + API_KEY

        #get the response from the site
        response = requests.get(URL)

        #if it is a valid response do the following
        if response.status_code == 200:
            data = response.json()
            weather = data['weather']
            weather_data = weather[0]
            description = weather_data['description']
            main = data['main']
            value = '{0:.2f}'.format(main['temp'] - 273.15)

        #print the formated message out
        await message.channel.send(
            'The current condition in ' + CITY + ' is ' + description + ' and the temperature is ' + value)


async def AutoBotResponseToMessages(message, msg):
    #respond to swear words
    if any(word in msg.lower() for word in bad_words):
        await message.channel.send("Watch your mouth!")
    #no swears so respond to gaming
    elif any(word in msg.lower() for word in gaming):
        await message.channel.send("gaming")
    #no gaming so respond if says i'm
    elif any(word in msg.lower() for word in im):
        msg = msg.split(" ")
        msg.pop(0)
        msg = " ".join(msg)
        await message.channel.send("Hello " + msg + ", i'm Dad")
