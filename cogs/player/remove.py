import discord
from discord import app_commands
from discord.ext import commands
import pomice
from config import EMBED_COLOR, ERROR_COLOR, SUCCESS_COLOR

class Remove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name="remove", description="Remove a track from the queue")
    @app_commands.describe(position="The position of the track to remove (1-based)")
    async def remove(self, ctx, position: int):
        """Remove a track from the queue"""
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
            
        if position < 1 or position > len(player.queue):
            return await ctx.send(embed=discord.Embed(
                title="Error",
                description=f"Invalid position. The queue has {len(player.queue)} tracks.",
                color=ERROR_COLOR
            ))
            
        index = position - 1
        
        removed_track = player.queue.pop(index)
        
        await ctx.send(embed=discord.Embed(
            title="Track Removed",
            description=f"Removed **{removed_track.title}** from the queue.",
            color=SUCCESS_COLOR
        ))

async def setup(bot):
    await bot.add_cog(Remove(bot)) 