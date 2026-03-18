import discord
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


DEPLOY_CHANNEL_ID = 1377709832085180428


@client.event
async def on_ready():
    print(f'{client.user} is online!')
    channel = client.get_channel(DEPLOY_CHANNEL_ID)
    if channel:
        await channel.send('✅ Bot has been deployed and is online!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!hi':
        await message.channel.send(f'Hello, {message.author.name}!')

    if message.content == '!ping':
        await message.channel.send('Pong!')


client.run(TOKEN)
