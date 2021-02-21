#!/usr/bin/python3

import configparser
from os import path
import re
from discord.ext import commands
import discord
from string import Template

# Read config
config = configparser.ConfigParser()
if not path.isfile('config.ini'):
    config['config'] = {'status': 'Being bad at changing nicknames',
            'token': ''}
    config['prefixes'] = {}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
config.read('config.ini')

async def get_prefix(bot, message):
    '''Check the prefix for the guild the command is in. The commands module will run this function every time a message is recieved and it checks if it's a command.'''
    guild = str(message.guild.id)
    if guild in config['prefixes']:
        return config['prefixes'][guild]
    else:
        return '%'

client = commands.Bot(command_prefix=get_prefix, help_command=None)

@client.event
async def on_ready():
    '''Set status and log that we logged in'''
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(config['config']['status']))

@client.command(pass_context=True)
async def help(ctx):
    '''Help command'''
    #TODO: Actually write the help command

@client.command(pass_context=True)
async def ping(ctx):
    '''Send "Pong! (bot latency)" in the channel the command was run in'''
    await ctx.send('Pong! Latency: {0}ms'.format(round(client.latency * 1000, 1)))

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def prefix(ctx, prefix):
    '''Change the bot's prefix in the current guild'''
    config['prefixes'][str(ctx.guild.id)] = prefix.replace('%', '%%') # Replace % with %% because % is a special character in the config library
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    # We have to use the Template method here because f-strings and such may allow for abitrary variable retrieval by users (see https://realpython.com/python-string-formatting/#4-template-strings-standard-library)
    response = Template('Prefix changed to $prefix')
    await ctx.send(response.substitute(prefix=prefix))

@client.command(pass_context = True)
async def changenick(ctx, user: discord.Member, nickname):
    await client.change_nickname(user, nickname)

client.run(config['config']['token'])
