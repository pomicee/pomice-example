import discord
from discord import app_commands
from discord.ext import commands
import pomice
from config import EMBED_COLOR, ERROR_COLOR, SUCCESS_COLOR
import asyncio

class NowPlaying(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name="nowplaying", aliases=["np"], description="Display information about the currently playing track")
    async def nowplaying(self, ctx):
        """Display information about the currently playing track"""
        if not ctx.guild:
            return await ctx.send(embed=discord.Embed(
                title="Error",
                description="This command can only be used in a server!",
                color=ERROR_COLOR
            ))
            
        player = ctx.guild.voice_client
        
        if not player:
            return await ctx.send(embed=discord.Embed(
                title="Error",
                description="I'm not connected to a voice channel!",
                color=ERROR_COLOR
            ))
            
        if not player.is_playing():
            return await ctx.send(embed=discord.Embed(
                title="Error",
                description="Nothing is playing right now!",
                color=ERROR_COLOR
            ))
            
        track = player.current
        
        embed = discord.Embed(
            title="Now Playing",
            color=EMBED_COLOR
        )
        
        embed.add_field(name="Title", value=track.title, inline=False)
        embed.add_field(name="Author", value=track.author, inline=True)
        
        position = player.position
        duration = track.length
             
        progress = int((position / duration) * 20)
        progress_bar = "▰" * progress + "▱" * (20 - progress)
        
        position_str = self.format_duration(position)
        duration_str = self.format_duration(duration)
        
        embed.add_field(
            name="Duration",
            value=f"{position_str}/{duration_str}\n{progress_bar}",
            inline=False
        )
        
        if player.queue:
            embed.add_field(
                name="Queue",
                value=f"{len(player.queue)} tracks in queue",
                inline=True
            )
            
        if player.loop == pomice.LoopMode.NONE:
            loop_mode = "Off"
        elif player.loop == pomice.LoopMode.SINGLE:
            loop_mode = "Single Track"
        else:
            loop_mode = "All Tracks"
            
        embed.add_field(name="Loop Mode", value=loop_mode, inline=True)
        
        embed.add_field(name="Volume", value=f"{player.volume}%", inline=True)
        
        if track.artwork:
            embed.set_thumbnail(url=track.artwork)
            
        if track.uri:
            embed.add_field(name="URL", value=f"[Click here]({track.uri})", inline=False)
            
        await ctx.send(embed=embed)
        
    def format_duration(self, duration):
        """Format duration in milliseconds to a human-readable string"""
        minutes, seconds = divmod(duration // 1000, 60)
        hours, minutes = divmod(minutes, 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"

async def setup(bot):
    await bot.add_cog(NowPlaying(bot)) 