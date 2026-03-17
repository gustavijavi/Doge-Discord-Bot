import discord # regular discord import needed for bot
import os # allows script to read data from origin file path
from dotenv import load_dotenv # allows script to grab data from .env file
import json # allows you to read and write to json files
import asyncio # allows the bot to wait a certain amount of time

# loads .env file
load_dotenv()

# grabs discord token from .env file
token = os.getenv('DISCORD_TOKEN')

# sets the intents of the client
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# setting as a client instead of a bot since this does not need normal bot functions
client = discord.Client(intents=intents)

# regular inputs to terminal can't be done normally because the bot is asynchronous
# this fixes that
async def async_input(prompt=""):
    return await asyncio.get_event_loop().run_in_executor(None, input, prompt)


# on bot being ready, starts going through the regular program
@client.event
async def on_ready():
    # open json file with server/channel data for messaging
    with open('data.json', 'r') as f:
        data = json.load(f)

    # if there are no registered messaging servers, close the program
    if not data['registered_message_channels']:
        print(f"No possible servers to message into\nPlease register your server/channel you'd like the bot to talk in with d!registerMessaging")
        await client.close()

    print(f"\n-- Messaging Override Activated --")

    await asyncio.sleep(1)

    # Go through until script is exited
    while True:
        inputStr = await async_input(f"\nWhat would you like to do? (message/impersonate/stop): ")

        await asyncio.sleep(1)

        # normal messaging mode, through the bot itself
        if inputStr.lower() == "message":

            print(f"\n-- Normal Messaging Override Activated --\n")

            await asyncio.sleep(1)

            while True:
                
                # under the normal messaging override, we loop through each server and channel ID to give a good menu for the user to
                # choose from when selecting which channel they'd like to message in
                for serverId in data['registered_message_channels']:
                    for channelId in data['registered_message_channels'][serverId]:
                        channel = client.get_channel(int(channelId))
                        print(f"{channel.guild.name} - #{channel.name}: {channelId}")

                inputStr = await async_input(f"\nPlease input the channel ID you would like to send messages into (id/cancel): ")

                await asyncio.sleep(1)

                channelId = 0

                # loops through channels to see if inputted channel Id matches one already registered
                for serverId in data['registered_message_channels']:
                    if inputStr in data['registered_message_channels'][serverId]:
                        channelId = int(inputStr)

                # if channel ID is one registered, allows the user to now chat through the bot
                if channelId != 0:

                    channel = client.get_channel(channelId)

                    print("\nYou may now start chatting! Enter 'stop' to exit the program")
                    
                    # grabs input of user to send through bot, if it equals 'stop' end program
                    while True:
                        inputStr = await async_input()
                        if inputStr == "stop":
                            await client.close()
                        else:
                            await channel.send(inputStr)

                elif inputStr == "cancel":
                    await asyncio.sleep(1)
                    break
                else:
                    print(f"Not a valid channel, try again\n")
                    await asyncio.sleep(1)

        # impersonation mode: grabs the user avatar and username from the username inputted to talk as them. Utilizes discord webhooks
        elif inputStr.lower() == "impersonate":

            print(f"\n-- Impersonation Mode Activated --\n")

            await asyncio.sleep(1)

            while True:
                
                # goes through each server and channel as a directory for the user
                for serverId in data['registered_message_channels']:
                    for channelId in data['registered_message_channels'][serverId]:
                        channel = client.get_channel(int(channelId))
                        print(f"{channel.guild.name} - #{channel.name}: {channelId}")

                inputStr = await async_input(f"\nPlease input the channel ID you would like to send messages into (id/cancel): ")

                await asyncio.sleep(1)

                channelId = 0

                # makes sure channel ID is valid
                for serverId in data['registered_message_channels']:
                    if inputStr in data['registered_message_channels'][serverId]:
                        channelId = int(inputStr)

                # if channel ID is valid, continue
                if channelId != 0:
                    
                    channel = client.get_channel(channelId)

                    while True:

                        inputStr = await async_input(f"\nWho would you like to impersonate? (username/cancel): ")

                        await asyncio.sleep(1)

                        # tries to grab member from inserted username
                        # will return None if no user is found from username inputted
                        member = discord.utils.get(channel.guild.members, name=inputStr)

                        if inputStr == "cancel":
                            break
                        elif member is not None:

                            # creates webhook to talk through
                            webhook = await channel.create_webhook(name="temp")

                            # grabs user avatar picture url
                            avatar = member.display_avatar.with_format('png').url

                            print(f"\nYou may now start chatting! Enter 'change' to change username or 'stop' to exit the program")

                            shouldExit = False

                            # allows you to now message as the inputted user although it's not perfect
                            try:
                                while True:
                                    inputStr = await async_input()

                                    # if user types 'change', allows you to change user you're impersonating
                                    # if user types 'stop', closes program
                                    if inputStr == "change":
                                        break
                                    elif inputStr == "stop":
                                        shouldExit = True
                                        break
                                    else:
                                        # sends message through webhook
                                        await webhook.send(inputStr, username=member.display_name, avatar_url=avatar)
                            finally:
                                # webhook must be deleted after use, otherwise it'll stay in the messaging channel as a webhook forever
                                # and more will build up over time with use. the try: finally: makes sure the webhook will always be deleted
                                # no matter if the user closes the program suddenly or whatnot
                                await webhook.delete()

                            if shouldExit:
                                # indicates that the client should close upon typing 'stop'
                                await client.close()
                        else:
                            # loops back through if user was not found
                            print(f"Could not find member by the username inputted, try again")
                            await asyncio.sleep(1)

                    break
                elif inputStr == "cancel":
                    break
                else:
                    print(f"Not a valid option, try again\n")
                    await asyncio.sleep(1)

        elif inputStr == "stop":
            await client.close()
        else:
            print(f"Not a valid option, try again\n")
            await asyncio.sleep(1)

# allows script to run under the bot as a client instead of a bot
client.run(token)