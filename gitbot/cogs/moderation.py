
# Create imports

import discord
from discord.ext import commands
import time
import asyncio
from datetime import datetime

# Create the moderation cog class

class moderation(commands.Cog):

    def __init__(self, vbot):
        self.vbot = vbot

    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.trigger_typing()
        
        await ctx.send('Pong!')

    # Mute command. Turned out to be more janky than I expected. Oh well.

    @commands.command(name='mute')
    async def mute(self, ctx, member: discord.Member, mute_time, *, reason='No Reason Specified'):
        mutedrole = ctx.guild.get_role(role) #put the role id here
        await member.add_roles(mutedrole, atomic=True)
        await ctx.trigger_typing()
        time.sleep(1)
        await ctx.send(f'{member.mention} was muted by {ctx.message.author.mention} for {mute_time}m. Reason: {reason}')

        # We don't just want to announce it in chat, we also want to ceate a 
        # Moderation Action Review Form or M.A.R.F and drop it in a log channel.
        # I really should move this embed to a file with a collection of them
        # but I will have to do that later.

        logchannel = ctx.guild.get_channel(channel) #put the channel here



        logembed = discord.Embed(
            title = 'Action Taken:',
            description = 'User was muted.',
            colour = discord.Colour.red()
        )

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        logembed.set_footer(text=f'{dt_string}')
        logembed.set_thumbnail(url='urltoimage')
        logembed.set_author(name='Moderation Action Review Form',
        icon_url='urltoimage')
        logembed.add_field(name='Moderator:', value=f'{ctx.message.author.mention}', inline=False)
        logembed.add_field(name='Muted User:', value=f'{member.mention}', inline=True)
        logembed.add_field(name='Mute Length:', value=f'{mute_time}m', inline=True)
        logembed.add_field(name='Reason Specified:', value=f'{reason}', inline=False)
        await logchannel.send(embed=logembed)

        # Now we want to start an asyncio.sleep (yeah I don't know either) for the specified time.
        # After the time runs out, unmute the user. Note that if you manually unmute the user, it will
        # still ping the user and welcome them back. Maybe check if the user is still muted?
        # Or maybe I should just use better code...

        await asyncio.sleep(int(int(mute_time) * 60))
        await member.remove_roles(mutedrole)
        await ctx.send(f'Your time is up, {member.mention}. Welcome back!')

    # Just an unmute command should the mute be manual. Always says it unmutes even if
    # the user isn't muted.
    
    @commands.command(name='unmute')
    async def unmute(self, ctx, member: discord.Member):
        mutedrole = ctx.guild.get_role(roleid) #inupt role id
        await member.remove_roles(mutedrole, atomic=True)
        await ctx.trigger_typing()
        time.sleep(1)
        await ctx.send(f'{member.mention} was unmuted!')

# Setup the cog 

def setup(vbot):
    vbot.add_cog(moderation(vbot))