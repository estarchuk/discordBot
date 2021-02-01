import discord
import botCommands

client = discord.Client()

#get the file token to run the bot off c drive
file = open("C:\\Discord bot code\\bot code.txt", "r")
SecurityTokenForBotCode = file.read()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #This await is needed to call to the commands file
    #The commands file will contain all of the possible keyword commands
    #and will not return anything
    await botCommands.commands(message, client)





client.run(SecurityTokenForBotCode)
