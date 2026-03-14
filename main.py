import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='d!', intents=intents)

# set up your own user id in the env file in case you want the bot to @ you specifically at certain points
my_user_id = os.getenv('USER_ID')

@bot.event
async def on_ready():
    print(f"{bot.user.name}, is ready to chud it out")


@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server chud, {member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    message_to_me = f"I'll... I'll spread the word\nWE PLAYIN <@{my_user_id}>!!!!!!"
    
    if "league" in message.content.lower() and message.author.id != my_user_id:
        await message.channel.send(f"DID SOMEBODY SAY LEAGUE???")
        await message.channel.sned(message_to_me)

    if "roblox" in message.content.lower() and message.author.id != my_user_id:
        await message.channel.send(f"DID SOMEBODY SAY BOBLOX???")
        await message.channel.send(message_to_me)

    await bot.process_commands(message)



bot.run(token, log_handler=handler, log_level=logging.DEBUG)