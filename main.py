import os
import discord
from discord import app_commands

client = discord.Client(intents=discord.Intents.all())
cmds = app_commands.CommandTree(client)

#Event: When bot joins server
@client.event
async def on_ready():
  await cmds.sync()
  print("I'm in")
  print(client.user)

#Event: When a message is sent
#@client.event
#async def on_message(message):
#    if message.author != client.user:
#        await #message.channel.send(message.content[::-1])

#Command: Basic /test Command
#@cmds.command(name='test', description='Test Command')
#async def test_command(interaction):
#  await interaction.response.send_message('Testing Successful.')

#Command: Post Website Link
@cmds.command(name='website', description='Displays the studio website link.')
async def get_website(ctx):
  await ctx.response.send_message('https://catdadstudios.us')

#Command: Open Support Ticket
@cmds.command(name='ticket', description='Opens a support ticket.')
async def support_ticket(ctx, *, topic: str):
  guild = ctx.guild
  member = ctx.user
  channel_name = str('ticket-' + ctx.user.name.lower() + '-' + ctx.user.discriminator)
  guild = ctx.guild
  existing_channel = discord.utils.get(guild.channels, name=channel_name)
  support_category = discord.utils.get(guild.categories, name='Product-Support')
  
  if existing_channel is not None:
    await ctx.response.send_message('Support ticket already open. Close the old one first.')
  else:
    admin_role = discord.utils.get(guild.roles, name='Admin')
    bot_role = discord.utils.get(guild.roles, name='CatDad')
    overwrite_settings = {
      guild.default_role: discord.PermissionOverwrite(read_messages=False),
      member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
      admin_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
      bot_role: discord.PermissionOverwrite(read_messages=True, send_messages=True,manage_channels=True)
    }
    
    await guild.create_text_channel(channel_name, category=support_category, overwrites=overwrite_settings)
    channel = discord.utils.get(ctx.guild.channels, name=channel_name)
    await channel.send('Ticket Subject: ' + topic)
    await ctx.response.send_message('Support ticket opened. A channel has been created for you.')
      

#Command: Close Support Ticket
@cmds.command(name='close-ticket', description='Closes a ticket.')
async def close_ticket(ctx):
  channel_name = str('ticket-' + ctx.user.name.lower() + '-' + ctx.user.discriminator)
  #print(channel_name)
  
  text_channel_list = []
  for guild in client.guilds:
    for channel in guild.text_channels:
        text_channel_list.append(channel)
  for channel in text_channel_list:
    #print(channel.name)
    if channel.name == channel_name:
      await channel.delete()
      await ctx.response.send_message('Support ticket closed.')
      break

client.run(os.environ['DISCORD_BOT_SECRET'])
