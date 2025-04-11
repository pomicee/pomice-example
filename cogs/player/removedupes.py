import discord
from discord import app_commands
from discord.ext import commands
import pomice
from config import EMBED_COLOR, ERROR_COLOR, SUCCESS_COLOR

class RemoveDupes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name="removedupes", aliases=["dedupe"], description="Remove duplicate tracks from the queue")
    async def removedupes(self, ctx):
        """Remove duplicate tracks from the queue"""
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
            
        if not player.queue:
            return await ctx.send(embed=discord.Embed(
                title="Error",
                description="The queue is empty!",
                color=ERROR_COLOR
            ))
            
        current_track = player.current if player.is_playing() else None
        
        unique_tracks = []
        removed_count = 0
        
        if current_track:
            unique_tracks.append(current_track)
            
        for track in player.queue:
            if track.uri in [t.uri for t in unique_tracks]:
                removed_count += 1
            else:
                unique_tracks.append(track)
                
        player.queue = unique_tracks[1:] if current_track else unique_tracks
        
        await ctx.send(embed=discord.Embed(
            title="Duplicates Removed",
            description=f"Removed {removed_count} duplicate tracks from the queue.",
            color=SUCCESS_COLOR
        ))

async def setup(bot):
    await bot.add_cog(RemoveDupes(bot)) 