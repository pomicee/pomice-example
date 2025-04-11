import discord
from discord import app_commands
from discord.ext import commands
import pomice
from config import EMBED_COLOR, ERROR_COLOR, SUCCESS_COLOR

class Disconnect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name="disconnect", description="Disconnect the bot from the voice channel")
    async def disconnect(self, ctx):
        """Disconnect the bot from the voice channel"""
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
            
        await player.disconnect()
        
        await ctx.send(embed=discord.Embed(
            title="Disconnected",
            description="Disconnected from the voice channel.",
            color=SUCCESS_COLOR
        ))

async def setup(bot):
    await bot.add_cog(Disconnect(bot)) 