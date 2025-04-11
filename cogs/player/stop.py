import discord
from discord import app_commands
from discord.ext import commands
import pomice
from config import EMBED_COLOR, ERROR_COLOR, SUCCESS_COLOR

class Stop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name="stop", description="Stop playback and clear the queue")
    async def stop(self, ctx):
        """Stop playback and clear the queue"""
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
            
        if not player.is_playing() and not player.queue:
            return await ctx.send(embed=discord.Embed(
                title="Error",
                description="Nothing is playing and the queue is empty!",
                color=ERROR_COLOR
            ))
            
        queue_length = len(player.queue)
        player.queue.clear()
        
        if player.is_playing():
            await player.stop()
            
        await ctx.send(embed=discord.Embed(
            title="Playback Stopped",
            description=f"Stopped playback and cleared {queue_length} tracks from the queue.",
            color=SUCCESS_COLOR
        ))

async def setup(bot):
    await bot.add_cog(Stop(bot)) 