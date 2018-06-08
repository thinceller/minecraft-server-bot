import asyncio
import os

import discord

client = discord.Client()

BOT_TOKEN = os.getenv('BOT_TOKEN')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('/minecraft'):
        if client.user != message.author:
            m = "minecraft is great."
            await client.send_message(message.channel, m)

client.run(BOT_TOKEN)
