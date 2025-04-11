import discord
from discord import app_commands
from discord.ext import commands
import pomice
from config import EMBED_COLOR, ERROR_COLOR, SUCCESS_COLOR

class Volume(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name="volume", aliases=["vol"], description="Adjust the playback volume")
    @app_commands.describe(level="The volume level (0-100)")
    async def volume(self, ctx, level: int = None):
        """Adjust the playback volume"""
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
            
        if level is None:
            await ctx.send(embed=discord.Embed(
                title="Volume",
                description=f"Current volume: **{player.volume}%**",
                color=EMBED_COLOR
            ))
            return
            
        if level < 0 or level > 100:
            return await ctx.send(embed=discord.Embed(
                title="Error",
                description="Volume level must be between 0 and 100.",
                color=ERROR_COLOR
            ))
            
        await player.set_volume(level)
        
        await ctx.send(embed=discord.Embed(
            title="Volume",
            description=f"Volume set to **{level}%**.",
            color=SUCCESS_COLOR
        ))

async def setup(bot):
    await bot.add_cog(Volume(bot)) 