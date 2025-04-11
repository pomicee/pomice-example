import discord
from discord import app_commands
from discord.ext import commands
import pomice
from config import EMBED_COLOR, ERROR_COLOR, SUCCESS_COLOR

class Restart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name="restart", description="Restart the current track")
    async def restart(self, ctx):
        """Restart the current track"""
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
            
        current_track = player.current
        
        player.queue.insert(0, current_track)
        
        await player.stop()
        
        await ctx.send(embed=discord.Embed(
            title="Track Restarted",
            description=f"Restarted **{current_track.title}**.",
            color=SUCCESS_COLOR
        ))

async def setup(bot):
    await bot.add_cog(Restart(bot)) 