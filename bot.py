import asyncio
import os
from time import sleep

from googleapiclient import discovery
import discord

client = discord.Client()

BOT_TOKEN = os.getenv('BOT_TOKEN')

# Instance information
PROJECT = 'nagi-minecraft'
ZONE = 'asia-east1-a'
INSTANCE = 'mc-server'

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
            m = await client.send_message(message.channel, 'Server starting up...')
            start_server(PROJECT, ZONE, INSTANCE)
            await client.edit_message(m, 'Success! Server started up.')
            sleep(10)
            await client.delete_messages([message, m])
        elif command == 'stop':
            m = await client.send_message(message.channel, 'Server stopping...')
            stop_server(PROJECT, ZONE, INSTANCE)
            await client.edit_message(m, 'Success! Server stopped.')
            sleep(10)
            await client.delete_messages([message, m])
        elif command == 'status':
            status = get_server_status(PROJECT, ZONE, INSTANCE)

            if status == 'RUNNING':
                m = await client.send_message(message.channel, 'Server is running! Please enjoy Minecraft!')
                sleep(10)
                await client.delete_messages([message, m])
            elif status in {'STOPPING', 'STOPPED'}:
                m = await client.send_message(message.channel,
                                'Server is stopped. If you play Minecraft, please chat in this channel, `/minecraft start`.')
                sleep(10)
                await client.delete_messages([message, m])
            else:
                m = await client.send_message(message.channel,
                                'Server is not running. Please wait for a while, and chat in this channel, `/minecraft start`.')
                sleep(10)
                await client.delete_messages([message, m])
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
