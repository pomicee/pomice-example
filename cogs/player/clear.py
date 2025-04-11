import discord
from discord import app_commands
from discord.ext import commands
import pomice
from config import EMBED_COLOR, ERROR_COLOR, SUCCESS_COLOR

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name="clear", description="Clear the music queue")
    async def clear(self, ctx):
        """Clear the music queue"""
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
                description="The queue is already empty!",
                color=ERROR_COLOR
            ))
        queue_length = len(player.queue)
        player.queue.clear()
        
        await ctx.send(embed=discord.Embed(
            title="Queue Cleared",
            description=f"Cleared {queue_length} tracks from the queue.",
            color=SUCCESS_COLOR
        ))

async def setup(bot):
    await bot.add_cog(Clear(bot)) 