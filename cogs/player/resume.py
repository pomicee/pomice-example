import discord
from discord import app_commands
from discord.ext import commands
import pomice
from config import EMBED_COLOR, ERROR_COLOR, SUCCESS_COLOR

class Resume(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name="resume", description="Resume playback after pausing")
    async def resume(self, ctx):
        """Resume playback after pausing"""
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
            
        if not player.is_paused():
            return await ctx.send(embed=discord.Embed(
                title="Error",
                description="The player is not paused!",
                color=ERROR_COLOR
            ))
            
        await player.resume()
        
        await ctx.send(embed=discord.Embed(
            title="Resumed",
            description="Resumed playback.",
            color=SUCCESS_COLOR
        ))

async def setup(bot):
    await bot.add_cog(Resume(bot)) 