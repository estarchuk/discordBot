from discord.ext import commands

bot = commands.Bot(command_prefix='$')

#get the file token to run the bot off c drive
file = open("C:\\Discord bot code\\bot code.txt", "r")
SecurityTokenForBotCode = file.read()

bot.load_extension("stockCog")
bot.load_extension("botCommands")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):

    #This await is needed to call to the commands file
    #The commands file will contain all of the possible keyword commands
    #and will not return anything
    await bot.process_commands(message)


bot.run(SecurityTokenForBotCode)
