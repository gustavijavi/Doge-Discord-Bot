import discord # regular discord import needed for bot
from discord.ext import commands # discord commands
import logging # allows logging to the discord.log
from dotenv import load_dotenv # allows script to grab data from .env file
import os # allows script to read data from origin file path
import asyncio # allows the bot to wait a certain amount of time
import json # allows you to read and write to json files
import requests # allows you to send requests to links to receive data
from medal_api import MedalAPI # medal API functions grabbed from other repository since they're smarter than me :(
from discord.ext import commands, tasks # command that allows looping every set amount of time within the bot

# loads the .env file
load_dotenv()

# grabs discord bot token from .env file
token = os.getenv('DISCORD_TOKEN')

# set file for log messages
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# declaring of intents such as the discord default, ability to read message content (i think), and ability to see members
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# sets the bot command prefix and sets the intents
bot = commands.Bot(command_prefix='d!', intents=intents)

# set up your own user id in the env file in case you want the bot to @ you specifically at certain points
my_user_id = int(os.getenv('USER_ID'))

# set up medal API key so that it may grab links or anything of the sort for clips uploaded to medal
medal_api_key = os.getenv('MEDAL_API_KEY')

# set up riot API key so it can be called for league data
riot_api_key = os.getenv('RIOT_API_KEY')

# intializes medal api through another github repo to get the user ID
medalApi = MedalAPI()

# bot booting up event
@bot.event
async def on_ready():

    # if data.json file doesn't exist, create one with all the required data storage outline
    if not os.path.exists('data.json'):
        data = {
            "registered_message_channels": {},
            "registered_clip_channels": {},
            "registered_users": {},
            "settings": {}
        }
        
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)

    # changes the bot status message to be a custom message
    await bot.change_presence(activity=discord.CustomActivity(name="wait, im coded ( ͡° ͜ʖ ͡°)"))

    # starts the loop to check for medal clips using the function defined below called checkMedal()
    checkMedal.start()
    
    # once all done, bot says it's ready
    print(f"{bot.user.name}, is ready to chud it out")


# on member join, make the bot do something
@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server chud, {member.name}")


# on message sent to a channel the bot is apart of
@bot.event
async def on_message(message):
    
    # makes sure that the bot doesn't recursively send messages if it sees a message sent by itself
    if message.author == bot.user:
        return

    # grabs the specific text channel from the message sent
    channel = message.channel

    # set up for my message to myself :3
    message_to_me_one = "I'll... I'll spread the word"
    message_to_me_two = f"HOP ONNNNNN <@{my_user_id}>!!!!!!"
    
    # checks for if someone says something along the lines of "play league" or "hop on league" to @ me :3
    if ("play" in message.content.lower() or "hop on" in message.content.lower() or "hoppin" in message.content.lower()) and "league" in message.content.lower() and message.author.id != my_user_id:
        await channel.send(f"DID SOMEBODY SAY LEAGUE???")
        await asyncio.sleep(0.5)
        await channel.send(message_to_me_one)
        await asyncio.sleep(0.5)
        await channel.send(message_to_me_two)

    # checks for if someone says something along the lines of "play roblox" or "hop on roblox" to @ me :3
    if ("play" in message.content.lower() or "hop on" in message.content.lower() or "hoppin" in message.content.lower()) and "roblox" in message.content.lower() and message.author.id != my_user_id:
        await channel.send(f"DID SOMEBODY SAY BOBLOX???")
        await asyncio.sleep(0.5)
        await channel.send(message_to_me_one)
        await asyncio.sleep(0.5)
        await channel.send(message_to_me_two)

    # always needed for on_message
    await bot.process_commands(message)


# regular ping command just to test bot
@bot.command()
async def ping(ctx):
    await ctx.send("pong")


@bot.command()
async def getLeagueStats(ctx, *, riotName):
    channel = ctx.channel

    poundIndex = riotName.find("#")

    if poundIndex == -1 or poundIndex == riotName.length() - 1:
        await channel.send("Not a valid name, try again")
        return

    name = riotName[0, poundIndex]
    tagLine = riotName[poundIndex + 1, riotName.length()]

    response = requests.get(f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tagLine}", 
                            headers={"Authorization": riot_api_key})
    
    responseCode = response.status_code

    if responseCode != 200:
        await channel.send("Invalid Riot name twin")

    responseData = response.json

    channel.send(responseData["puuid"])





# command to register channel for the messaging_override.py script
@bot.command()
async def registerMessaging(ctx):
    
    # calls on function to check if the command is being sent from a server, if not it returns false
    if await notInServer(ctx):
        return

    # registers server if not already in 'registered_message_channels' dict,
    # appends the channel no matter what to the server just added or already there
    await registerChannel(ctx, 'registered_message_channels')
    
    await ctx.send(f"Registered this channel for message override")


# command to unregister channel for the messaging_override.py script
@bot.command()
async def unregisterMessaging(ctx):

    # calls on function to check if the command is being sent from a server, if not it returns false
    if await notInServer(ctx):
        return

    # unregisters channel from the server in the 'registered_message_channels' dict
    # if channel was the last one for the server, server is also removed from the dict
    await unregisterChannel(ctx, 'registered_message_channels')
    
    await ctx.send(f"Unregistered this channel for message override")


# command to register channel for medal clips to be sent to
@bot.command()
async def registerClips(ctx):

    # calls on function to check if the command is being sent from a server, if not it returns false
    if await notInServer(ctx):
        return

    # registers server if not already in 'registered_clip_channels' dict,
    # appends the channel no matter what to the server just added or already there
    await registerChannel(ctx, 'registered_clip_channels')
    
    await ctx.send(f"Registered this channel for sending clips")


# command to unregister channel for medal clips to be sent to
@bot.command()
async def unregisterClips(ctx):

    # calls on function to check if the command is being sent from a server, if not it returns false
    if await notInServer(ctx):
        return

    # unregisters channel from the server in the 'registered_message_channels' dict
    # if channel was the last one for the server, server is also removed from the dict
    await unregisterChannel(ctx, 'registered_clip_channels')
    
    await ctx.send(f"Unregistered this channel for sending clips")


# command to register username sent by the message author for grabbing medal clips from
@bot.command()
async def register(ctx, *, msg):
    
    # calls on the medal API set at the beginning to get the medal user data from the message inputted by the message author
    user = medalApi.get_user(msg)

    # medal API will return [] if no user is found by that username
    if user == []:
        await ctx.send(f"Medal user not found blud")
        return
    
    # grabs the user ID from the user data received from medal api
    userId = user[0]['userId']

    # reads data.json
    with open('data.json', 'r') as f:
        data = json.load(f)

    # checks to see if the user has already been registered
    if msg in data['registered_users']:
        await ctx.send(f"This Medal user has already been registered blud")
        return
    
    # sets up the username as a dict key with an array as its value
    data['registered_users'][msg] = []

    # appends the user ID and an empty string to the username key array for the last video contentID posted by the user on medal
    # set default to "" so that it may immediately start grabbing the latest video once the user has been registered
    data['registered_users'][msg].append(userId)
    data['registered_users'][msg].append("")

    # writes the new data of the user to the data.json file for saving
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

    await ctx.send(f"{msg} has been registered twin")

# command to unregister username sent by the message author for grabbing medal clips from
@bot.command()
async def unregister(ctx, *, msg):

    # reads data.json
    with open('data.json', 'r') as f:
        data = json.load(f)

    # checks if the username inputted by the message author is in the register_users dict
    if msg not in data['registered_users']:
        await ctx.send(f"Medal user has not been registered yet blud")
        return
    
    # deletes user data from data.json
    del data['registered_users'][msg]

    # writes the new data, without the user that was just deleted, to the data.json file for saving
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

    await ctx.send(f"{msg} has been unregistered twin")


# function to loop every 10 seconds to grab new clips from medal profile
@tasks.loop(seconds=10.0)
async def checkMedal():
    
    # reads data.json
    with open('data.json', 'r') as f:
        data = json.load(f)

    # loop through each username in 'registered_users' dict
    for username in data['registered_users']:
        
        # uses the request function to grab data sent back from requesting the link given
        # gets all sorts of data for the latest video sent by the 'registered_user' on medal
        response = requests.get(f"https://developers.medal.tv/v1/latest?userId={data['registered_users'][username][0]}&limit=1",
                                headers={"Authorization": medal_api_key})
        
        # sets the response to a json so that you can read the data in python
        responseData = response.json()

        # if 'contentObjects' dict is empty, theres no videos to even grab from medal profile so we skip to the next user
        if not responseData['contentObjects']:
            continue

        # if the contentID that was stored within the 'registered_users' username array does not equal the new one grabbed from the medal
        # API, then set them equal to each other
        if data['registered_users'][username][1] != responseData['contentObjects'][0]['contentId']:
            data['registered_users'][username][1] = responseData['contentObjects'][0]['contentId']

            # goes through each server and channel within each server to send the clips into
            for serverId in data['registered_clip_channels']:
                for channelId in data['registered_clip_channels'][serverId]:
                    
                    channel = bot.get_channel(int(channelId))

                    await channel.send(f"### {username} just posted a new [clip]({responseData['contentObjects'][0]['directClipUrl']})")
    
    # writes the new contentIDs to the data.json file
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)


# -- Helper Functions --

# checks if the guild is None, meaning the command was not sent in server. Sends True if so
async def notInServer(ctx):
    if ctx.guild is None:
        await ctx.send("This command can only be used in a server")
        return True
    return False


# registers the channel to the specific channel type located in data.json. Should be pretty self explanatory from 
# everything already made within here
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

# unregisters channel from channel type in data.json
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


@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name="whatevarole")
    if role:
      await ctx.author.add_roles(role)
      await ctx.send(f"{ctx.author.mention} is now assigned to whatevarole")
    else:
      await ctx.send("Role doesn't exist")
    
    return

@bot.command()
async def unassign(ctx):
    role = discord.utils.get(ctx.guild.roles, name="whatevarole")
    if role:
      await ctx.author.remove_roles(role)
      await ctx.send(f"Removed whatevarole from {ctx.author.mention}")
    else:
      await ctx.send("Role doesn't exist")
    
    return
'''


# needed at the end of main.py for bot to run
bot.run(token, log_handler=handler, log_level=logging.DEBUG)