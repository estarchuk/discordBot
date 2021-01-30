import discord
import Commands

client = discord.Client()



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



# DO NOT LEAVE THE TOKEN IN. DELETE BEFORE EVERY PUSH
client.run('')
