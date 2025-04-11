# Discord Music Bot

A feature-rich Discord music bot using discord.py and pomice.

## Features

- Slash commands for easy use
- YouTube music playback
- Queue system
- Basic music controls (play, pause, resume, skip, stop)
- Queue management
- Modern architecture with cogs
- Support for multiple music platforms (YouTube, Spotify, SoundCloud, etc.)
- Beautiful embeds for music information
- Volume control
- Shuffle and loop functionality
- Track history

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Install and set up Lavalink:
   - Download the latest Lavalink.jar from [GitHub](https://github.com/freyacodes/Lavalink/releases)
   - Create an `application.yml` file in the same directory as Lavalink.jar (use `application.yml.example` as a template)
   - Run Lavalink using: `java -jar Lavalink.jar`

3. Create a `.env` file in the root directory with your bot token:
```
TOKEN=your_bot_token_here
```

4. Run the bot:
```bash
python bot.py
```

## Commands

### Music Commands
- `/play <query>` - Play a song from YouTube, Spotify, SoundCloud, or a direct URL
- `/skip` - Skip the current song
- `/pause` - Pause the current song
- `/resume` - Resume the current song
- `/queue` - Show the current queue
- `/stop` - Stop playing and clear the queue
- `/disconnect` - Disconnect from the voice channel
- `/volume <level>` - Adjust the volume (0-100)
- `/shuffle` - Shuffle the current queue
- `/loop <mode>` - Set loop mode (none, track, queue)
- `/nowplaying` - Show information about the currently playing track
- `/previous` - Play the previous track
- `/search <query>` - Search for a song and select from results
- `/clear` - Clear the current queue
- `/remove <position>` - Remove a track from the queue
- `/move <from> <to>` - Move a track to a different position in the queue

### Utility Commands
- `/ping` - Check bot latency
- `/botinfo` - Get information about the bot

## Requirements

- Python 3.8+
- Java 11+ (for Lavalink)
- discord.py
- pomice
- python-dotenv
- pymongo (for database functionality)
- spotipy (for Spotify integration)

## Configuration

The bot uses a `config.py` file for various settings:

```python
import discord

EMBED_COLOR = discord.Color.from_str("#1e1f22")
ERROR_COLOR = discord.Color.from_str("#ff0000")
SUCCESS_COLOR = discord.Color.from_str("#00ff00")
```

## Project Structure

```
discord-music-bot/
├── bot.py
├── config.py
├── requirements.txt
├── .env
├── cogs/
│   ├── player/
│   │   ├── play.py
│   │   ├── pause.py
│   │   ├── resume.py
│   │   ├── skip.py
│   │   ├── stop.py
│   │   ├── queue.py
│   │   └── ...
│   └── ...
└── Lavalink.jar
```

## Publishing to GitHub

1. Create a new repository on GitHub
2. Initialize a Git repository in your project folder:
   ```bash
   git init
   ```
3. Add all files to the repository:
   ```bash
   git add .
   ```
4. Commit the files:
   ```bash
   git commit -m "Initial commit"
   ```
5. Add the remote repository:
   ```bash
   git remote add origin https://github.com/yourusername/your-repo-name.git
   ```
6. Push the code to GitHub:
   ```bash
   git push -u origin main
   ```

## Note

Make sure you have Java 11 or higher installed for Lavalink to work properly.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, join our [Discord server](https://discord.gg/jwZCyYMPBb).

## Credits

Created by [@pomice](https://discord.com/users/1252001166703853588)
