import random
import requests
import os
import discord
from discord.ext import commands

# To set up the bot on the Discord page and a easy quick start, I recommend this video by @pixegami on Youtube
# https://youtu.be/2k9x0s3awss?si=uyhyB0b4i0Le04r5

# DISCORD DEVELOPERS PAGE
# https://discord.com/developers/applications

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_ID = "YOUR_CHANNEL_ID"

# Bot-Prefix
# Can be any character, for example "$"
PREFIX = "!"

# CONSTANTS
# Folder for in which there are images that you want to output via the command
IMAGE_FOLDER = "pics"

# API for the joke command
# From https://icanhazdadjoke.com/
JOKE_API_URL = "https://icanhazdadjoke.com/"

# API for the meme command
# https://github.com/D3vd/Meme_Api
MEME_API_URL = "https://meme-api.com/gimme"

# Create bot client
bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())

# Discord text formatting and emojis
HEART = ":heart:"   # Write a heart in the discord chat

# Function to make your string bold
def bold(string):
    return f"**{string}**"

# Function to put a box around your string
def box(string):
    return f"`{string}`"


# Event: When the bot starts
@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready.") #prints bot is ready into your console

    # Initializes channel with associated channel of channel_id
    channel = bot.get_channel(CHANNEL_ID)

    # Sends a message to your discord text-channel
    await channel.send(f"The {bot.user.name} is ready. Type {bold(box('!commands'))} for a short overview {HEART}")


# Event: When a specific message is written, the bot triggers and responds (here "Hello there"), you only need one event handler
@bot.event
async def on_message(message):
    # To prevent a infinite loop
    if message.author == bot.user:
        return

    # Trigger if your message contains "Hello there"
    if "Hello there" in message.content:
        await message.channel.send(f"General Kenobi.{HEART}")
    await bot.process_commands(message) # Important so that the bot can continue to process commands



# Command: Shows the diffrent commands
@bot.command()
async def commands(ctx): # ctx stands for context, so the bot can write back to the channel from which the command came
    await ctx.send(f"{bold(f'Commands for the {bot.user.name}: ')} \n"
                   f"{bold(box('!pic'))} - shows a picture. \n"
                   f"{bold(box('!coinflip'))} - toss a coin. \n"
                   f"{bold(box('!joke'))} - tells you a dad joke. \n"
                   f"{bold(box('!meme'))} - shows you a meme. \n")

# Command: Random picture form the IMAGE_FOLDER
@bot.command()
async def pic(ctx):
    files = os.listdir(IMAGE_FOLDER) # os module to get the IMAGE_FOLDER
    image_files = [file for file in files if file.endswith(("jpg", "jpeg", "png", "gif"))] # Checks if the file is a image

    if image_files:
        random_image_file = random.choice(image_files) # random module to choose a random picture
        image_path = os.path.join(IMAGE_FOLDER, random_image_file)

        with open(image_path, "rb") as f:
            file = discord.File(f)
            await ctx.send(file=file) # sends the choosen picture
    else:
        await ctx.send("There is no picture.")


# Command: Coinflip
@bot.command()
async def coinflip(ctx):
    coin = ["Head", "Tails"]
    result = random.choice(coin)
    await ctx.send(result)


# Command: joke gives you a random dad joke from the api
@bot.command()
async def joke(ctx):
    headers = {"Accept": "application/json"} # To get a response in json format
    response = requests.get(JOKE_API_URL, headers=headers) # Sends a request with the requests modul to get a joke from the api

    if response.status_code == 200:
        joke_data = response.json()
        joke = joke_data["joke"]    # Looking up the joke in the json response

        await ctx.send(joke)
    else:
        await ctx.send("There was a problem.")

# Command: meme gibt ein Meme zurück
@bot.command()
async def meme(ctx):
    response = requests.get(MEME_API_URL) # Sends a request with the requests modul to get a meme from the api

    if response.status_code == 200:
        meme_data = response.json()

        meme_image_url = meme_data["url"] # Looks up the url for the meme in the json response
        await ctx.send(meme_image_url)
    else:
        await ctx.send("There was a problem.")


# To start the bot
bot.run(BOT_TOKEN)