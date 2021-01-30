import requests

bad_words = ["fuck", "shit", "ass"]
gaming = ["gaming", "minecraft", "car soccer", "valorant"]

async def commands(message):

    msg = message.content

    if any(word in msg for word in bad_words):
        await message.channel.send("Watch your mouth!")

    if any(word in msg for word in gaming):
        await message.channel.send("gaming")

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$temp'):
        CITY = message.content[1]
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        API_KEY = 'a79339a9332f239b64d3d0d20e57fe91'
        URL = BASE_URL + 'q=' + CITY + "&appid=" + API_KEY

        response = requests.get(URL)
        if response.status_code == 200:
            data = response.json()
            main = data['main']
            value = '{0:.2f}'.format(main['temp'] - 273.15)

        await message.channel.send('the temperature today in victoria is: ' + value)
