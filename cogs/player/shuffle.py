import discord
from discord import app_commands
from discord.ext import commands
import pomice
from config import EMBED_COLOR, ERROR_COLOR, SUCCESS_COLOR
import random

class Shuffle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name="shuffle", description="Shuffle the music queue")
    async def shuffle(self, ctx):
        """Shuffle the music queue"""
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
            
        random.shuffle(player.queue)
        
        await ctx.send(embed=discord.Embed(
            title="Queue Shuffled",
            description=f"Shuffled {len(player.queue)} tracks in the queue.",
            color=SUCCESS_COLOR
        ))

async def setup(bot):
    await bot.add_cog(Shuffle(bot)) 