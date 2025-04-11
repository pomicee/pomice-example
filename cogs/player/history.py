import discord
from discord import app_commands
from discord.ext import commands
import pomice
from config import EMBED_COLOR, ERROR_COLOR, SUCCESS_COLOR
import json
import os

class History(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.history_file = "data/history.json"
        self.history = self.load_history()
        
    def load_history(self):
        """Load history from file"""
        if not os.path.exists("data"):
            os.makedirs("data")
            
        if not os.path.exists(self.history_file):
            return {}
            
        try:
            with open(self.history_file, "r") as f:
                return json.load(f)
        except:
            return {}
            
    def save_history(self):
        """Save history to file"""
        if not os.path.exists("data"):
            os.makedirs("data")
            
        with open(self.history_file, "w") as f:
            json.dump(self.history, f)
            
    def add_to_history(self, user_id, track):
        """Add a track to a user's history"""
        if str(user_id) not in self.history:
            self.history[str(user_id)] = []
            
        # Add track to history
        track_info = {
            "title": track.title,
            "author": track.author,
            "uri": track.uri,
            "length": track.length,
            "timestamp": discord.utils.utcnow().isoformat()
        }
        
        self.history[str(user_id)].append(track_info)
        
        if len(self.history[str(user_id)]) > 20:
            self.history[str(user_id)] = self.history[str(user_id)][-20:]
            
        self.save_history()
        
    @commands.hybrid_command(name="history", description="View your recently played tracks")
    async def history(self, ctx):
        """View your recently played tracks"""
        if not ctx.guild:
            return await ctx.send(embed=discord.Embed(
                title="Error",
                description="This command can only be used in a server!",
                color=ERROR_COLOR
            ))
            
        user_id = str(ctx.author.id)
        
        if user_id not in self.history or not self.history[user_id]:
            return await ctx.send(embed=discord.Embed(
                title="History",
                description="You haven't played any tracks yet!",
                color=EMBED_COLOR
            ))
            
        embed = discord.Embed(
            title=f"Recently Played Tracks for {ctx.author.name}",
            color=EMBED_COLOR
        )
        
        # Add tracks to embed
        for i, track in enumerate(reversed(self.history[user_id][-10:]), 1):
            duration = self.format_duration(track["length"])
            embed.add_field(
                name=f"{i}. {track['title']}",
                value=f"by {track['author']} • {duration}",
                inline=False
            )
            
        await ctx.send(embed=embed)
        
    def format_duration(self, duration):
        """Format duration in milliseconds to a human-readable string"""
        minutes, seconds = divmod(duration // 1000, 60)
        hours, minutes = divmod(minutes, 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
            
    @commands.Cog.listener()
    async def on_pomice_track_end(self, player, track, reason):
        """Add track to history when it ends"""
        if hasattr(player, "ctx") and player.ctx and player.ctx.author:
            self.add_to_history(player.ctx.author.id, track)

async def setup(bot):
    await bot.add_cog(History(bot)) 