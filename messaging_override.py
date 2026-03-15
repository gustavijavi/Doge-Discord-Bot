import discord
import os
from dotenv import load_dotenv
import json
import asyncio

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)


async def async_input(prompt=""):
    return await asyncio.get_event_loop().run_in_executor(None, input, prompt)


@client.event
async def on_ready():
    # open json file with server/channel data for messaging
    with open('data.json', 'r') as f:
        data = json.load(f)

    # if there are no registered messaging servers, 
    if not data['registered_message_channels']:
        print(f"No possible servers to message into\nPlease register your server/channel you'd like the bot to talk in with d!registerMessaging")
        await client.close()


    print(f"-- Messaging Override Activated --\n")

    # Go through until script is exited
    while True:
        inputStr = await async_input(f"What would you like to do? (message/impersonate/stop): ")

        if inputStr.lower() == "message":

            print(f"\n-- Normal Messaging Override Activated --\n")

            while True:

                inputStr = await async_input(f"Please input the channel ID you would like to send messages into (id/cancel): ")

                channelId = 0

                for serverId in data['registered_message_channels']:
                    if inputStr in data['registered_message_channels'][serverId]:
                        channelId = int(inputStr)

                if channelId != 0:

                    channel = client.get_channel(channelId)

                    print("\nYou may now start chatting! Enter 'stop' to exit the program")

                    while True:
                        inputStr = await async_input()
                        if inputStr == "stop":
                            await client.close()
                        else:
                            await channel.send(inputStr)

                elif inputStr == "cancel":
                    break
                else:
                    print(f"Not a valid option, try again\n")

        elif inputStr.lower() == "impersonate":

            print(f"\n-- Impersonation Mode Activated --\n")

            while True:

                inputStr = await async_input(f"Please input the channel ID you would like to send messages into (id/cancel): ")

                channelId = 0

                for serverId in data['registered_message_channels']:
                    if inputStr in data['registered_message_channels'][serverId]:
                        channelId = int(inputStr)

                if channelId != 0:
                    
                    channel = client.get_channel(channelId)

                    while True:

                        inputStr = await async_input(f"Who would you like to impersonate? (username/cancel): ")

                        member = discord.utils.get(channel.guild.members, name=inputStr)

                        if inputStr == "cancel":
                            break
                        elif member is not None:
                            webhook = await channel.create_webhook(name="temp")

                            avatar = member.display_avatar.with_format('png').url

                            print(f"\nYou may now start chatting! Enter 'stop' to exit the program")

                            try:
                                while True:
                                    inputStr = await async_input()

                                    if inputStr == "stop":
                                        break
                                    else:
                                        await webhook.send(inputStr, username=member.display_name, avatar_url=avatar)
                            finally:
                                await webhook.delete()
                                await client.close()
                        else:
                            print(f"Could not find member by the username inputted, try again\n")

                    break
                elif inputStr == "cancel":
                    break
                else:
                    print(f"Not a valid option, try again\n")

        elif inputStr == "stop":
            await client.close()
        else:
            print(f"Not a valid option, try again\n")


client.run(token)