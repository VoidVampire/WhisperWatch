# WhisperWatch

WhisperWatch is a small project designed to explore the functionalities of discord.py by building a bot that monitors multiple channels for specific keywords and sends notifications to designated channels in a Discord server. This project serves as a learning exercise to understand the basics of creating and managing a Discord bot.

## Features

- Monitor multiple Discord channels for specific keywords.
- Send notifications to designated channels in your server.
- Mention roles based on the keywords detected in messages.
- Handles multiple servers and channels with customizable configurations.

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/WhisperWatch.git
cd WhisperWatch
```

2. **Create and activate a virtual environment (optional but recommended):**

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. **Configure the bot:**

- Replace `YOUR_BOT_TOKEN` in `bot.py` with your actual bot token.
- Customize the `servers_to_scan` and `channels_to_post` dictionaries in `bot.py` to suit your needs.

## Running the Bot

Simply run the `bot.py` script:

```bash
python bot.py
```

The bot will log in and start monitoring the specified channels for the defined keywords.

## Configuration

### `servers_to_scan`

This dictionary holds the configurations for the servers and channels to be monitored. Each server has a list of channels and the associated keywords to look for.

```python
servers_to_scan = [
    {
        'id': 'SERVER_ID',
        'name': 'Server Name',
        'channels': {
            'CHANNEL_ID': {
                'keywords_to_roles': {
                    'Keyword1': 'Role1',
                    'Keyword2': 'Role2'
                },
                'last_message_id': 0
            }
        }
    }
]
```

### `channels_to_post`

This dictionary maps the roles to the channels where notifications should be posted.

```python
channels_to_post = {
    'Role1': 'CHANNEL_ID_FOR_NOTIFICATIONS',
    'Role2': 'CHANNEL_ID_FOR_NOTIFICATIONS'
}
```

### Note:

This project is primarily intended for educational purposes to learn about creating and managing Discord bots using discord.py.
