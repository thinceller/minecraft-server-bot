import asyncio
import os

from googleapiclient import discovery
import discord

client = discord.Client()

BOT_TOKEN = os.getenv('BOT_TOKEN')

# Build and nitialize google api
compute = discovery.build('compute', 'v1')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('/minecraft'):
        # ex.) message.content: '/minecraft start' => command: 'start'
        command = message.content.split(' ')[1]

        if command == 'start':
            m = await client.send_message(message.channel, 'server starting up...')
            # await サーバー開始スクリプト
            await client.edit_message(m, 'Success! server started up.')
        elif command == 'stop':
            m = await client.send_message(message.channel, 'server stopping...')
            # await サーバー停止スクリプト
            await client.edit_message(m, 'Success! server stopped.')
        elif command == 'help':
            m = '''
            ```Usage: /minecraft [start][stop][status]
    start   Start up minecraft server
    stop    Stop minecraft server
    status  Show minecraft server status(running or stopped)```
            '''.strip()
            await client.send_message(message.channel, m)

def start_server(project, zone, instance):
    compute.instances().start(project=project, zone=zone, instance=instance).execute()

def stop_server(project, zone, instance):
    compute.instances().stop(project=project, zone=zone, instance=instance).execute()

def get_server_status(project, zone, instance):
    res = compute.instances().get(project=project, zone=zone, instance=instance).execute()
    return res['status']

client.run(BOT_TOKEN)
