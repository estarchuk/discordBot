import string

import requests

bad_words = ["fuck", "shit", "ass", "bitch", "cuck", "fag", "cunt"]
gaming = ["game", "gaming", "minecraft", "car soccer", "valorant"]
im = ["im", "Im", "I\'m", "i\'m"]

async def commands(message):

    msg = message.content

    await AutoBotResponses(message, msg)

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$temp'):
        await tempResponse(message)


async def tempResponse(message):
    #corrects the city name if needed
    SPLIT = message.content.split(" ", 1)
    CITY = SPLIT[1]
    CITY = string.capwords(CITY)
    if CITY == 'Victoria':
        CITY = 'Victoria, CA'
    if CITY == 'Grand Forks':
        CITY = 'Grand Forks, CA'

    #base information needed to get the information
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    API_KEY = 'a79339a9332f239b64d3d0d20e57fe91'
    URL = BASE_URL + 'q=' + CITY + "&appid=" + API_KEY
    #try and get the data from the site
    response = requests.get(URL)
    #if successful
    if response.status_code == 200:
        #find the weather conditions and the temperature
        data = response.json()
        weather = data['weather']
        weather_data = weather[0]
        description = weather_data['description']
        main = data['main']
        value = '{0:.2f}'.format(main['temp'] - 273.15)
    #print out the temp and conditions in a readable format
    await message.channel.send('The current condition in ' + CITY + ' is ' + description + ' and the temperature is ' + value)

async def AutoBotResponses(message, msg):
    #check the post for bad words
    if any(word in msg for word in bad_words):
        await message.channel.send("Watch your mouth!")
    #if no bad words check to see if there should be gaming
    elif any(word in msg for word in gaming):
        await message.channel.send("gaming")
    #if no bad words and not gaming then
    #check to see if a response about being dad is fitting
    elif any(word in msg for word in im):
        msg = msg.split(" ")
        msg.pop(0)
        msg = " ".join(msg)
        await message.channel.send("Hello " + msg + ", i'm Dad")
