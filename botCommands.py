import string
from asyncio import sleep

import discord

import finder
import requests
import stonkPrice
from discord.ext import commands

'''
This is the bot commands file where the following happens
-respond hello and you are welcome as requested by the user
-auto respond to key words defined in the global lists
-get the temperature and weather conditions for the city specified by user
-respond to the stonk keyword with the stock that the users should look at
-respond to the price keyword with the price of the stock that the user specifies
-ping all the users in the bot pings channel 
'''

bad_words = ["fuck", "shit", "ass", 'bitch', 'cuck', 'fag', 'cunt']
gaming = ["gaming", "minecraft", "car soccer", "valorant", 'game']
im = ['im', 'i\'m']



class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='weather')
    async def GetTempForSpecifiedLocation(self, ctx, *, city):
        # First set the city name to a capitalized first letter
        CITY = city
        CITY = string.capwords(CITY)

        # auto correct the city name if it is one of these
        if CITY == 'Victoria':
            CITY = 'Victoria, CA'
        if CITY == 'Grand Forks':
            CITY = 'Grand Forks, CA'

        # create the url for the openweathermap site to get the data from
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        API_KEY = 'a79339a9332f239b64d3d0d20e57fe91'
        URL = BASE_URL + 'q=' + CITY + "&appid=" + API_KEY

        # get the response from the site
        response = requests.get(URL)

        # if it is a valid response do the following
        if response.status_code == 200:
            data = response.json()
            weather = data['weather']
            weather_data = weather[0]
            description = weather_data['description']
            main = data['main']
            value = '{0:.2f}'.format(main['temp'] - 273.15)

        # print the formatted message out
        await ctx.send(
            'The current condition in ' + CITY + ' is ' + description + ' and the temperature is ' + value
        )

    @commands.command()
    async def stonk(self, ctx):
        finder.parseMessage(ctx)
        await finder.ping()

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        em = discord.Embed(title='Help', description='Use $help <command> for help with a command')
        #em.add_field(name='1', value='This bot will also auto respond to key words in messages if it detects them.', inline=False)
        #em.add_field(name='2', value='here are the key commands you will need to know', inline=False)
        #em.add_field(name='3', value='$stonk **stonk you want info on**')
        #em.add_field(name='4', value='$price **stock you are looking for**')
        #em.add_field(name='5', value='$weather **city you are interested in**')
        await ctx.send(embed=em)

    @help.command()
    async def weather(self, ctx):
        em = discord.Embed(title='$weather', description='Usage: $weather <city> to get the weather in a city')
        await ctx.send(embed=em)




async def commands(message):
    msg = message.content

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('thanks stonks'):
        await message.channel.send('You are very welcome')

    await AutoBotResponseToMessages(message, msg)


async def AutoBotResponseToMessages(message, msg):
    # respond to swear words
    if any(word in msg.lower() for word in bad_words):
        await message.channel.send("Watch your mouth!")
    # no swears so respond to gaming
    elif any(word in msg.lower() for word in gaming):
        await message.channel.send("gaming")
    # no gaming so respond if says i'm
    elif any(word in msg.lower() for word in im):
        msg = msg.split(" ")
        msg.pop(0)
        msg = " ".join(msg)
        await message.channel.send("Hello " + msg + ", i'm Dad")


async def pingUsers(bot):
    channel = bot.get_channel(805601797422579742)
    await channel.send("yo @everyone, check out this stock, **insert stock here** , making these money moves")


def setup(bot):
    bot.add_cog(BotCommands(bot))
