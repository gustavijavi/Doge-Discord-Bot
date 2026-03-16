import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio
import json

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='d!', intents=intents)

# set up your own user id in the env file in case you want the bot to @ you specifically at certain points
my_user_id = int(os.getenv('USER_ID'))


@bot.event
async def on_ready():
    if not os.path.exists('data.json'):
        data = {
            "registered_message_channels": {},
            "registered_clip_channels": {},
            "registered_users": {},
            "settings": {}
        }
        
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)

    bot.status.name = "testing twin"
    
    print(f"{bot.user.name}, is ready to chud it out")


@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server chud, {member.name}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    channel = message.channel

    message_to_me_one = "I'll... I'll spread the word"
    message_to_me_two = f"HOP ONNNNNN <@{my_user_id}>!!!!!!"
    
    if ("play" in message.content.lower() or "hop on" in message.content.lower() or "hoppin" in message.content.lower()) and "league" in message.content.lower() and message.author.id != my_user_id:
        await channel.send(f"DID SOMEBODY SAY LEAGUE???")
        await asyncio.sleep(0.5)
        await channel.send(message_to_me_one)
        await asyncio.sleep(0.5)
        await channel.send(message_to_me_two)

    if ("play" in message.content.lower() or "hop on" in message.content.lower() or "hoppin" in message.content.lower()) and "roblox" in message.content.lower() and message.author.id != my_user_id:
        await channel.send(f"DID SOMEBODY SAY BOBLOX???")
        await asyncio.sleep(0.5)
        await channel.send(message_to_me_one)
        await asyncio.sleep(0.5)
        await channel.send(message_to_me_two)

    await bot.process_commands(message)


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


@bot.command()
async def assign(ctx):
    # can be used to assign roles later on
    # role = discord.utils.get(ctx.guild.roles, name="whatevarole")
    # if role:
    #   await ctx.author.add_roles(role)
    #   await ctx.send(f"{ctx.author.mention} is now assigned to whatevarole")
    # else:
    #   await ctx.send("Role doesn't exist")
    
    return

@bot.command()
async def unassign(ctx):
    # can be used to unassign roles later on
    # role = discord.utils.get(ctx.guild.roles, name="whatevarole")
    # if role:
    #   await ctx.author.remove_roles(role)
    #   await ctx.send(f"Removed whatevarole from {ctx.author.mention}")
    # else:
    #   await ctx.send("Role doesn't exist")
    
    return


@bot.command()
async def registerMessaging(ctx):
    
    if await notInServer(ctx):
        return

    await registerChannel(ctx, 'registered_message_channels')
    
    await ctx.send(f"Registered this channel for message override")


@bot.command()
async def unregisterMessaging(ctx):

    if await notInServer(ctx):
        return

    await unregisterChannel(ctx, 'registered_message_channels')
    
    await ctx.send(f"Unregistered this channel for message override")


@bot.command()
async def registerClips(ctx):

    if await notInServer(ctx):
        return

    with open('data.json', 'r') as f:
        data = json.load(f)

    await registerChannel(ctx, 'registered_clip_channels')
    
    await ctx.send(f"Registered this channel for sending clips")


@bot.command()
async def unregisterClips(ctx):

    if await notInServer(ctx):
        return

    await unregisterChannel(ctx, 'registered_clip_channels')
    
    await ctx.send(f"Unregistered this channel for sending clips")

'''
@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send("You have the secret role woahg")
    
    return

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You don't have permission for dat twin")
    
    return


@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"you wanted me to send you: {msg}")




@bot.command()
async def reply(ctx):
    await ctx.reply("this is a reply twin")




@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="New Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("❤️")
    await poll_message.add_reaction("🧡")
    await poll_message.add_reaction("💚")
    await poll_message.add_reaction("💙")
'''


# Helper Functions

async def notInServer(ctx):
    if ctx.guild is None:
        await ctx.send("This command can only be used in a server")
        return True
    return False

async def registerChannel(ctx, channelType):
    with open('data.json', 'r') as f:
        data = json.load(f)

    serverId = str(ctx.guild.id)
    channelId = str(ctx.channel.id)

    if serverId not in data[channelType]:
        data[channelType][serverId] = []

    if channelId in data[channelType][serverId]:
        await ctx.send(f"Channel has already been registered")
        return

    data[channelType][serverId].append(channelId)

    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)


async def unregisterChannel(ctx, channelType):
    with open('data.json', 'r') as f:
        data = json.load(f)

    serverId = str(ctx.guild.id)
    channelId = str(ctx.channel.id)

    if serverId not in data[channelType]:
        await ctx.send("This channel has not been registered")
        return
    elif channelId not in data[channelType][serverId]:
        await ctx.send("This channel has not been registered")
        return
    
    data[channelType][serverId].remove(channelId)

    if data[channelType][serverId] == []:
        del data[channelType][serverId]

    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)


bot.run(token, log_handler=handler, log_level=logging.DEBUG)