import discord
from discord.ext import tasks
import datetime
import os
import asyncio

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = discord.Client(intents=intents)

TOKEN = ''  # Replace with your bot token

# Define the directory to store last message IDs
LAST_MESSAGE_DIR = 'last_message'
if not os.path.exists(LAST_MESSAGE_DIR):
    os.makedirs(LAST_MESSAGE_DIR)

# Define the servers and channels to scan
servers_to_scan = [
    {
        'id': '1254782687995236434',
        'name': 't1',
        'channels': {
            '1254782687995236437': {  # Channel ID
                'keywords_to_roles': {
                    'Series 1': 'Series1Role',
                    'Series 2': 'Series2Role'
                }
            }
        }
    },
    {
        'id': '1254784473900253235',
        'name': 'vtest3',
        'channels': {
            '1254784473900253238': {  # Channel ID
                'keywords_to_roles': {
                    'Series 5': 'Series5Role',
                }
            }
        }
    }
]

my_server_id = '1254784535426629712'  # Replace with your server ID
channels_to_post = {
    'Series1Role': '1254790441354919948',
    'Series2Role': '1254790441354919948',
    'Series3Role': '1254790469368676403',
    'Series4Role': '1254790469368676403',
    'Series5Role': '1254790485902360587'
}

def load_last_message_id(server_id, channel_id):
    try:
        with open(os.path.join(LAST_MESSAGE_DIR, f'{server_id}_{channel_id}.txt'), 'r') as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0
    except Exception as e:
        print(f"Error loading last message ID for {server_id}/{channel_id}: {e}")
        return 0

def save_last_message_id(server_id, channel_id, last_message_id):
    try:
        with open(os.path.join(LAST_MESSAGE_DIR, f'{server_id}_{channel_id}.txt'), 'w') as f:
            f.write(str(last_message_id))
    except Exception as e:
        print(f"Error saving last message ID for {server_id}/{channel_id}: {e}")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    # Load last message IDs
    for server in servers_to_scan:
        for channel_id in server['channels']:
            server['channels'][channel_id]['last_message_id'] = load_last_message_id(server['id'], channel_id)
    # Start scanning channels for new messages
    await scan_channels()

async def scan_channels():
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            for server in servers_to_scan:
                for channel_id, channel_data in server['channels'].items():
                    channel = bot.get_channel(int(channel_id))
                    if channel:
                        last_message_id = channel_data.get('last_message_id', 0)
                        async for message in channel.history(limit=100, after=discord.Object(id=last_message_id)):
                            if message.id > last_message_id:
                                # Process the message if it's newer than the last processed message
                                for keyword, role in channel_data['keywords_to_roles'].items():
                                    if keyword in message.content:
                                        resolution = check_for_resolution(message.content)
                                        if resolution:
                                            await notify_my_server(role, resolution, message)
                                # Update last message ID for this channel
                                last_message_id = message.id
                        # Update last message ID immediately after processing
                        channel_data['last_message_id'] = last_message_id
                        save_last_message_id(server['id'], channel_id, last_message_id)
                    else:
                        print(f"Channel {channel_id} not found or bot does not have access.")
        except discord.errors.Forbidden:
            print(f"Bot does not have permission to access one or more channels.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await asyncio.sleep(20)  # Wait 60 seconds before scanning again


async def notify_my_server(role_name, resolution, message):
    guild = bot.get_guild(int(my_server_id))
    if guild:
        role = discord.utils.get(guild.roles, name=role_name)
        if role:
            channel_id = channels_to_post.get(role_name)
            if channel_id:
                channel = bot.get_channel(int(channel_id))
                if channel:
                    message_link = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
                    await channel.send(f'{role.mention} New update: {role_name} - {resolution}\nOriginal Message: {message_link}')

def check_for_resolution(content):
    resolutions = ['480p', '720p', '1080p', '2160p', '4K']
    for resolution in resolutions:
        if resolution in content:
            return resolution
    return None

bot.run(TOKEN)