# Boring imports

import discord
from discord.ext import commands, tasks
import os
import time
import random
import statuses


# Define bot and set our desired prefix

vbot = commands.Bot(command_prefix='$')

# Log in server chat lines, these should be moved to a seperate file
# and imported to save on space. Meh.

spookyterrarialines = ['A horrible chill goes down your spine...', 'Screams echo around you...']

# On Ready event call, say the line! Also start our status changer loop

@vbot.event
async def on_ready():
    print('Bot is ready')
    channel = vbot.get_channel(channel) #put channel here
    await channel.send(random.choice(spookyterrarialines))
    change_status.start()
    
# Create our status changer loop

@tasks.loop(seconds=int(random.randrange(300, 900, 60)))
async def change_status():
    await vbot.change_presence(status=discord.Status.idle, activity=discord.Game(random.choice(statuses.statusentry)))

# This was a say command I added at the beginning of this bots creation. Just here
# to be here.

@vbot.command(name='say')
async def _say(ctx, *, arg):
    await ctx.trigger_typing()
    time.sleep(0.5)
    await ctx.send(arg)

# Lets setup some commands to load/unload/reload our modules   

@vbot.command()
async def load(ctx, extension):
    vbot.load_extension(f'cogs.{extension}')

@vbot.command()
async def unload(ctx, extension):
    vbot.unload_extension(f'cogs.{extension}')

@vbot.command()
async def reload(ctx, extension):
    vbot.unload_extension(f'cogs.{extension}')
    await ctx.trigger_typing()
    time.sleep(5)
    vbot.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} module was reloaded!')

# Of course, we want to autoload the modules when we start the bot.

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        vbot.load_extension(f'cogs.{filename[:-3]}')
        print(f'{filename} cog was loaded!')



    



# Now lets run the bot and supply a token!

vbot.run('token')