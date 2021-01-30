import discord
import Commands

client = discord.Client()
file = open("C:\\Discord bot code\\bot code.txt", "r")
securityToken = file.read()


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
    await Commands.commands(message)

#the securiy token is in a file on your C drive or else you can't run the bot
client.run(securityToken)