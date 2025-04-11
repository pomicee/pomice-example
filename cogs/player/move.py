import discord
from discord import app_commands
from discord.ext import commands
import pomice
from config import EMBED_COLOR, ERROR_COLOR, SUCCESS_COLOR

class Move(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name="move", description="Move a track in the queue to a different position")
    @app_commands.describe(track="The track number to move", position="The new position (1-based)")
    async def move(self, ctx, track: int, position: int):
        """Move a track in the queue to a different position"""
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
            
        if track < 1 or track > len(player.queue):
            return await ctx.send(embed=discord.Embed(
                title="Error",
                description=f"Invalid track number. The queue has {len(player.queue)} tracks.",
                color=ERROR_COLOR
            ))
            
        if position < 1 or position > len(player.queue):
            return await ctx.send(embed=discord.Embed(
                title="Error",
                description=f"Invalid position. The queue has {len(player.queue)} tracks.",
                color=ERROR_COLOR
            ))
            
        track_index = track - 1
        position_index = position - 1
        
        track_to_move = player.queue.pop(track_index)
        
        player.queue.insert(position_index, track_to_move)
        
        await ctx.send(embed=discord.Embed(
            title="Track Moved",
            description=f"Moved track **{track_to_move.title}** to position {position}.",
            color=SUCCESS_COLOR
        ))

async def setup(bot):
    await bot.add_cog(Move(bot)) 