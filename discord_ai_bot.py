import discord
import random
from discord.ext import commands, tasks
from itertools import cycle

#Current Bot Status
client = commands.Bot(command_prefix = '.' )
status = cycle(['(°◡°♡).:｡', '╮ (. ❛ ᴗ ❛.) ╭'])

#Status Updates
@tasks.loop(seconds=15)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

#Bot Status via Python Terminal
@client.event
async def on_ready():
    change_status.start()
    print('Bot is ready')

#Errors
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command use')

#Load, Unload, Reload F(x)s
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')    

#Ping
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)} ms')

#Clear Comments
@client.command()
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify an amount of messages to delete.')

#Magic 8Ball
@client.command(aliases=['8ball', 'test'])
async def _8ball(ctx, *, question):
    responses = ['It is certain.',
                 'It is decidedly so.',
                 'Without a doubt',
                 'Yes - definitely.',
                 'You may rely on it.',
                 'As I see it, yes.',
                 'Most likely.',
                 'Outlook good.',
                 'Yes.',
                 'Signs point to yes.',
                 'Reply hazy, try again.',
                 'Ask again later.',
                 'Better not tell you now.',
                 'Cannot predict now.',
                 'Concentrate and ask again.',
                 "Don't count on it.",
                 'My reply is no.',
                 'My sources say no.',
                 'Outlook not so good.',
                 'Very doubtful.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

#Kick Member Command
@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)

#Ban Member Command
@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned{member.mention}')

#Unban Member Command
@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

#This states whether a member has join the server
@client.event
async def on_member_join(member):
        print(f'{member} has joined a server.')

@client.event
async def on_member_remove(member):
        print(f'{member} has left a server.')

#Where Discord Token is put into account
client.run('NTg0OTY2ODA0MzgwNzEyOTY0.XPjApA.yBB2R-UoOQyGuuCF0EUbhoh8jgo')
