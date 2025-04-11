import discord
from discord import app_commands
from discord.ext import commands
import pomice
from config import EMBED_COLOR, ERROR_COLOR, SUCCESS_COLOR

class Pause(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name="pause", description="Pause the current track")
    async def pause(self, ctx):
        """Pause the current track"""
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
            
        if not player.is_playing():
            return await ctx.send(embed=discord.Embed(
                title="Error",
                description="Nothing is playing right now!",
                color=ERROR_COLOR
            ))
            
        if player.is_paused():
            return await ctx.send(embed=discord.Embed(
                title="Error",
                description="The player is already paused!",
                color=ERROR_COLOR
            ))

        await player.pause()
        
        if isinstance(ctx, discord.Interaction):
            await ctx.response.send_message(embed=discord.Embed(
                title="Paused",
                description="Paused the current track.",
                color=SUCCESS_COLOR
            ))
        else:
            await ctx.send(embed=discord.Embed(
                title="Paused",
                description="Paused the current track.",
                color=SUCCESS_COLOR
            ))

async def setup(bot):
    await bot.add_cog(Pause(bot)) 