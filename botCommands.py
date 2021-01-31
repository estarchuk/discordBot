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

    if any(word in msg.lower() for word in bad_words):
        await message.channel.send("Watch your mouth!")
    elif any(word in msg.lower() for word in gaming):
        await message.channel.send("gaming")
    elif any(word in msg.lower() for word in im):
        msg = msg.split(" ")
        msg.pop(0)
        msg = " ".join(msg)
        await message.channel.send("Hello " + msg + ", i'm Dad")

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$temp'):
        SPLIT = message.content.split(" ", 1)
        CITY = SPLIT[1]
        CITY = string.capwords(CITY)

        if CITY == 'Victoria':
            CITY = 'Victoria, CA'
        if CITY == 'Grand Forks':
            CITY = 'Grand Forks, CA'

        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        API_KEY = 'a79339a9332f239b64d3d0d20e57fe91'
        URL = BASE_URL + 'q=' + CITY + "&appid=" + API_KEY

        response = requests.get(URL)

        if response.status_code == 200:
            data = response.json()
            weather = data['weather']
            weather_data = weather[0]
            description = weather_data['description']
            main = data['main']
            value = '{0:.2f}'.format(main['temp'] - 273.15)

        await message.channel.send(
            'The current condition in ' + CITY + ' is ' + description + ' and the temperature is ' + value)

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
