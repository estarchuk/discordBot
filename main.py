from discord.ext import tasks

import discord
import botCommands

'''
This is the main file where the following happens
-verify the token stored on the useres c drive
-log on as the bot
-wait for the client messages and pass into the commands file as needed
'''

client = discord.Client()

#get the file token to run the bot off c drive
file = open("C:\\Discord bot code\\bot code.txt", "r")
SecurityTokenForBotCode = file.read()


@client.event
async def on_ready():
    change_status.start()
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #This await is needed to call to the commands file
    #The commands file will contain all of the possible keyword commands
    #and will not return anything
    await botCommands.commands(message, client)

@tasks.loop(hours=1)
async def change_status():
    ranking = finder.get()
    await botCommands.pingUsers(client)





client.run(SecurityTokenForBotCode)
