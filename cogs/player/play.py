import discord
from discord import app_commands
from discord.ext import commands
import pomice
from config import EMBED_COLOR, ERROR_COLOR, SUCCESS_COLOR
import asyncio
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
from datetime import datetime

# Spotify configuration
SPOTIFY_CLIENT_ID = ""
SPOTIFY_CLIENT_SECRET = ""

# Initialize Spotify client
spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# Custom Player class to override pomice.Player behavior
class CustomPlayer(pomice.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx = None  # Store the context for reference
        
    async def send_ws(self, op, **data):
        # Override the send_ws method to prevent sending messages to voice channel
        # This is where pomice might be sending the "Now Playing" message
        if op == "play" and "track" in data:
            # We'll handle the "Now Playing" message ourselves in the event handler
            pass
        return await super().send_ws(op, **data)

class Play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.now_playing_messages = {}  # Store now playing messages for deletion
        self.text_channels = {}  # Store text channel IDs for each guild
        self.platform_icons = {
            "youtube": "https://i.ibb.co/tMCt924t/youtube.png",
            "youtube music": "https://i.ibb.co/60Lc423F/You-Tube-Music.png",
            "apple music": "https://i.ibb.co/1G6cYxCx/apple-Music.png",
            "tidal": "https://i.ibb.co/1JTyVzKZ/tidal.png",
            "spotify": "https://i.ibb.co/bjm2X5d5/Spotify.png",
            "soundcloud": "https://i.ibb.co/XfzLLLKn/soundcloud.png",
            "deezer": "https://i.ibb.co/qM3JQ5sc/deezer.png",
            "yandex": "https://i.ibb.co/79gt5W8/yandexmusic.png"
        }

    def format_duration(self, duration):
        """Format duration in milliseconds to mm:ss format"""
        if not duration or duration <= 0:
            return "Unknown Duration"
        if duration < 1000:
            duration *= 1000
        minutes = duration // 60000
        seconds = (duration % 60000) // 1000
        return f"{minutes:02d}:{seconds:02d}"

    def format_total_duration(self, tracks):
        """Format total duration of multiple tracks"""
        if not tracks:
            return "Unknown"
        total_ms = sum(track.length or 0 for track in tracks)
        if total_ms < 1000:
            total_ms *= 1000
        return self.format_duration(total_ms)

    def get_platform_icon(self, track_uri):
        """Get platform icon based on track URI"""
        if "youtube.com" in track_uri or "youtu.be" in track_uri:
            return self.platform_icons["youtube"]
        if "music.youtube.com" in track_uri:
            return self.platform_icons["youtube music"]
        if "apple.com" in track_uri:
            return self.platform_icons["apple music"]
        if "tidal.com" in track_uri:
            return self.platform_icons["tidal"]
        if "spotify.com" in track_uri:
            return self.platform_icons["spotify"]
        if "soundcloud.com" in track_uri:
            return self.platform_icons["soundcloud"]
        if "deezer.com" in track_uri:
            return self.platform_icons["deezer"]
        if "music.yandex.ru" in track_uri:
            return self.platform_icons["yandex"]
        if track_uri.endswith(".mp3"):
            return self.platform_icons["spotify"]
        return "🎵"

    async def create_now_playing_embed(self, player, track, channel):
        """Create and send now playing embed"""
        # Get track artwork from Spotify if available
        artwork = None
        if "spotify.com" in track.uri:
            try:
                track_id = re.search(r'track/([a-zA-Z0-9]+)', track.uri).group(1)
                track_info = spotify.track(track_id)
                artwork = track_info['album']['images'][0]['url']
            except:
                artwork = track.artwork

        embed = discord.Embed(
            color=EMBED_COLOR
        )
        
        embed.description = (
            f"- **[{track.title} by {track.author}]({track.uri})**\n"
            f"- **Duration:** `{self.format_duration(track.length)}`"
        )
        
        if hasattr(player, 'ctx') and player.ctx and player.ctx.author:
            embed.description += f" - <@{player.ctx.author.id}>"
        
        platform_icon = self.get_platform_icon(track.uri)
        embed.set_author(
            name="Started playing",
            icon_url=platform_icon
        )
        
        if artwork:
            embed.set_thumbnail(url=artwork)
            
        if channel.id in self.now_playing_messages:
            try:
                await self.now_playing_messages[channel.id].delete()
            except:
                pass
        message = await channel.send(embed=embed)
        self.now_playing_messages[channel.id] = message

    @commands.Cog.listener()
    async def on_pomice_track_start(self, player: pomice.Player, track: pomice.Track):
        """Event fired when a track starts playing"""
        guild_id = player.guild.id
        if guild_id in self.text_channels:
            channel = player.guild.get_channel(self.text_channels[guild_id])
            if channel:
                await self.create_now_playing_embed(player, track, channel)

    @commands.Cog.listener()
    async def on_pomice_track_end(self, player: pomice.Player, track: pomice.Track, reason):
        """Event fired when a track ends"""
        guild_id = player.guild.id
        if guild_id in self.text_channels:
            channel = player.guild.get_channel(self.text_channels[guild_id])
            if channel and channel.id in self.now_playing_messages:
                try:
                    await self.now_playing_messages[channel.id].delete()
                    del self.now_playing_messages[channel.id]
                except:
                    pass

        if not player.queue.empty() and not player.is_playing:
            next_track = await player.queue.get()
            await player.play(next_track)

    @commands.Cog.listener()
    async def on_pomice_track_stuck(self, player: pomice.Player, track: pomice.Track):
        """Event fired when a track gets stuck"""
        guild_id = player.guild.id
        if guild_id in self.text_channels:
            channel = player.guild.get_channel(self.text_channels[guild_id])
            if channel:
                if channel.id in self.now_playing_messages:
                    try:
                        await self.now_playing_messages[channel.id].delete()
                        del self.now_playing_messages[channel.id]
                    except:
                        pass

                await channel.send(embed=discord.Embed(
                    title="Error",
                    description="Track got stuck, skipping to next song...",
                    color=ERROR_COLOR
                ))
                await player.stop()

    @commands.Cog.listener()
    async def on_pomice_track_exception(self, player: pomice.Player, track: pomice.Track, error):
        """Event fired when a track encounters an exception"""
        guild_id = player.guild.id
        if guild_id in self.text_channels:
            channel = player.guild.get_channel(self.text_channels[guild_id])
            if channel:
                if channel.id in self.now_playing_messages:
                    try:
                        await self.now_playing_messages[channel.id].delete()
                        del self.now_playing_messages[channel.id]
                    except:
                        pass

                await channel.send(embed=discord.Embed(
                    title="Error",
                    description=f"An error occurred while playing the track: {error}",
                    color=ERROR_COLOR
                ))
                await player.stop()

    @commands.hybrid_command(name="play", description="Play a song from YouTube, Spotify, SoundCloud, or a direct URL")
    @app_commands.describe(query="The song to play (URL, search query, or playlist)")
    async def play(self, ctx, *, query: str):
        if not ctx.guild:
            return await ctx.send(embed=discord.Embed(
                title="Error",
                description="This command can only be used in a server!",
                color=ERROR_COLOR
            ))
            
        if not ctx.author.voice:
            return await ctx.send(embed=discord.Embed(
                title="Error",
                description="You need to be in a voice channel to use this command!",
                color=ERROR_COLOR
            ))
            
        voice_channel = ctx.author.voice.channel
        
        if ctx.guild.voice_client:
            player = ctx.guild.voice_client
            if player.channel.id != voice_channel.id:
                await player.move_to(voice_channel)
        else:
            try:
                player = await voice_channel.connect(cls=CustomPlayer)
                if not hasattr(player, 'queue'):
                    player.queue = asyncio.Queue()
                await player.set_volume(60)
            except Exception as e:
                return await ctx.send(embed=discord.Embed(
                    title="Error",
                    description=f"Failed to connect to voice channel: {str(e)}",
                    color=ERROR_COLOR
                ))
        
        self.text_channels[ctx.guild.id] = ctx.channel.id
        
        player.ctx = ctx
        
        search_msg = await ctx.send(embed=discord.Embed(
            title="Searching",
            description=f"🔍 Searching for `{query}`...",
            color=EMBED_COLOR
        ))
        
        try:
            results = await player.get_tracks(query, ctx=ctx)
            
            if not results:
                return await search_msg.edit(embed=discord.Embed(
                    title="Error",
                    description="No results were found for your query.",
                    color=ERROR_COLOR
                ))
            
            if isinstance(results, pomice.Playlist):
                for track in results.tracks:
                    await player.queue.put(track)
                
                await search_msg.edit(embed=discord.Embed(
                    title="Playlist Added",
                    description=f"Added **{len(results.tracks)}** tracks from playlist **{results.name}** to the queue.",
                    color=SUCCESS_COLOR
                ))
                
                if not player.is_playing:
                    track = await player.queue.get()
                    await player.play(track)
                    
            else:
                track = results[0]
                await player.queue.put(track)
                
                await search_msg.edit(embed=discord.Embed(
                    title="Track Added",
                    description=f"Added **{track.title}** to the queue.",
                    color=SUCCESS_COLOR
                ))
                
                if not player.is_playing:
                    track = await player.queue.get()
                    await player.play(track)
                    
        except Exception as e:
            return await search_msg.edit(embed=discord.Embed(
                title="Error",
                description=f"An error occurred while searching: {str(e)}",
                color=ERROR_COLOR
            ))

async def setup(bot):
    await bot.add_cog(Play(bot))
