import discord
from discord import app_commands
from discord.ext import commands
import pomice
from config import EMBED_COLOR, ERROR_COLOR, SUCCESS_COLOR

class Loop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name="loop", description="Toggle loop mode (off, single, all)")
    @app_commands.describe(mode="The loop mode to set (off, single, all)")
    async def loop(self, ctx, mode: str = None):
        """Toggle loop mode (off, single, all)"""
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
            
        if mode is None:
            if player.loop == pomice.LoopMode.NONE:
                mode = "single"
            elif player.loop == pomice.LoopMode.SINGLE:
                mode = "all"
            else:
                mode = "off"
                
        mode = mode.lower()
        
        if mode == "off":
            player.loop = pomice.LoopMode.NONE
            await ctx.send(embed=discord.Embed(
                title="Loop Mode",
                description="Loop mode turned off.",
                color=SUCCESS_COLOR
            ))
        elif mode == "single":
            player.loop = pomice.LoopMode.SINGLE
            await ctx.send(embed=discord.Embed(
                title="Loop Mode",
                description="Loop mode set to single track.",
                color=SUCCESS_COLOR
            ))
        elif mode == "all":
            player.loop = pomice.LoopMode.ALL
            await ctx.send(embed=discord.Embed(
                title="Loop Mode",
                description="Loop mode set to all tracks.",
                color=SUCCESS_COLOR
            ))
        else:
            await ctx.send(embed=discord.Embed(
                title="Error",
                description="Invalid loop mode. Use 'off', 'single', or 'all'.",
                color=ERROR_COLOR
            ))
            
    @commands.hybrid_command(name="loopstatus", description="Check the current loop mode")
    async def loopstatus(self, ctx):
        """Check the current loop mode"""
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
            
        if player.loop == pomice.LoopMode.NONE:
            mode = "off"
        elif player.loop == pomice.LoopMode.SINGLE:
            mode = "single"
        else:
            mode = "all"
            
        await ctx.send(embed=discord.Embed(
            title="Loop Mode",
            description=f"Current loop mode: **{mode}**",
            color=EMBED_COLOR
        ))

async def setup(bot):
    await bot.add_cog(Loop(bot)) 