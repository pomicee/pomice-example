import discord
from discord import app_commands
from discord.ext import commands
import pomice
from config import EMBED_COLOR, ERROR_COLOR, SUCCESS_COLOR

class Previous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name="previous", aliases=["prev"], description="Play the previous track")
    async def previous(self, ctx):
        """Play the previous track"""
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
            
        if not hasattr(player, "previous_tracks") or not player.previous_tracks:
            return await ctx.send(embed=discord.Embed(
                title="Error",
                description="There are no previous tracks!",
                color=ERROR_COLOR
            ))
            
        previous_track = player.previous_tracks.pop()
        
        if player.current:
            if not hasattr(player, "previous_tracks"):
                player.previous_tracks = []
            player.previous_tracks.append(player.current)

        player.queue.insert(0, previous_track)
        
        await player.stop()
        
        await ctx.send(embed=discord.Embed(
            title="Previous Track",
            description=f"Playing **{previous_track.title}**.",
            color=SUCCESS_COLOR
        ))
        
    @commands.Cog.listener()
    async def on_pomice_track_end(self, player, track, reason):
        """Add track to previous tracks when it ends"""
        if not hasattr(player, "previous_tracks"):
            player.previous_tracks = []
            
        player.previous_tracks.append(track)
        
        if len(player.previous_tracks) > 10:
            player.previous_tracks = player.previous_tracks[-10:]

async def setup(bot):
    await bot.add_cog(Previous(bot)) 