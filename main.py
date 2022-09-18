#!/usr/bin/python3

import configparser
from os import path
import discord
from discord import app_commands
import traceback

# Config
config = configparser.ConfigParser()
if not path.isfile('config.ini'):
    config['config'] = {'status': 'Being bad at changing nicknames',
            'token': ''}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
config.read('config.ini')

class CommandsClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # Command tree for the app
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

class ChangeNickname(discord.ui.Modal, title="Change Nickname"):
    def __init__(self, *, member: discord.Member, interaction: discord.Interaction):
        super().__init__(custom_id = "changenickname")
        self.member = member
        self.interaction = interaction
        self.add_item(discord.ui.TextInput(label="Nickname", placeholder=self.member.name, default=self.member.nick, required=False, max_length=32))

    async def on_submit(self, interaction: discord.Interaction):
        try:
            await self.member.edit(nick=str(self.children[0].value), reason='Action requested by ' + str(self.interaction.user))
        except discord.errors.Forbidden:
            await interaction.response.send_message('Looks like I don\'t have permission to change that user\'s nickname! Please ensure that my role is above that user\'s highest role in the role list and that I have the "Manage Nicknames" permission.', ephemeral=True)
        else:
            await interaction.response.send_message('Nickname successfully changed!', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('An unknown error ocurred changing that user\'s nickname.', ephemeral=True)
        traceback.print_tb(error.__traceback__)
        print(error)

intents=discord.Intents.default()
client=CommandsClient(intents=intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(config['config']['status']))

@client.tree.command()
async def help(interaction: discord.Interaction):
    """Displays the bot's help, containing a list of commands and how to change a user's nickname."""
    embed = discord.Embed(title='Help', color=discord.Color(0x000000))
    embed.add_field(name="To change ***any*** user's nickname:", value="Right-click on the user, then go to apps > change nickname. (Or on mobile, tap on the user, then go to apps > change nickname). From there, a dialog should pop up that will allow you to enter a new nickname. Leave it blank to remove their nickname. Once you're done, click submit.", inline=False)
    embed.add_field(name="/help", value="Displays this help message.", inline=True)
    embed.add_field(name="/ping", value="Checks if the bot is online and displays its latency.", inline=True)
    await interaction.response.send_message(embed=embed)

@client.tree.command()
async def ping(interaction: discord.Interaction):
    """Checks if the bot is online and displays its latency."""
    await interaction.response.send_message('Pong! Latency: {0}ms'.format(round(client.latency * 1000, 1)))

@client.tree.context_menu(name="Change Nickname")
async def change_nickname(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_modal(ChangeNickname(member=member, interaction=interaction))

client.run(config['config']['token'])
