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
my_user_id = int(os.getenv('USER_ID'))


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
    
    if "play" in message.content.lower() and "league" in message.content.lower() and message.author.id != my_user_id:
        await message.channel.send(f"DID SOMEBODY SAY LEAGUE???")
        await message.channel.send(message_to_me)

    if "play" in message.content.lower() and "roblox" in message.content.lower() and message.author.id != my_user_id:
        await message.channel.send(f"DID SOMEBODY SAY BOBLOX???")
        await message.channel.send(message_to_me)

    await bot.process_commands(message)


@bot.command()
async def ping(ctx):
    await ctx.send(f"pong {ctx.author.mention}")


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
async def dm(ctx, *, msg):
    await ctx.author.send(f"you wanted me to send you: {msg}")


bot.command()
async def reply(ctx):
    await ctx.reply("this is a reply twin")


bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="New Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("❤️")
    await poll_message.add_reaction("🧡")
    await poll_message.add_reaction("💚")
    await poll_message.add_reaction("💙")


@bot.command()
#@commands.has_role(secret_role)
async def secret(ctx):
    # await ctx.send("You have the secret role woahg")
    
    return

# @secret.error
async def secret_error(ctx, error):
    # if isinstance(error, commands.MissingRole):
    #     await ctx.send("You don't have permission for dat twin")
    
    return



bot.run(token, log_handler=handler, log_level=logging.DEBUG)