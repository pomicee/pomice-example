import discord
from discord import app_commands
from discord.ext import commands
import pomice
from config import EMBED_COLOR, ERROR_COLOR, SUCCESS_COLOR

class Skip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name="skip", description="Skip the current track")
    @app_commands.describe(amount="Number of tracks to skip (default: 1)")
    async def skip(self, ctx, amount: int = 1):
        """Skip the current track"""
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
            
        if not player.queue and amount > 1:
            return await ctx.send(embed=discord.Embed(
                title="Error",
                description="There are no more tracks in the queue!",
                color=ERROR_COLOR
            ))
            
        if amount == 1:
            await player.stop()
            await ctx.send(embed=discord.Embed(
                title="Skipped",
                description="Skipped the current track.",
                color=SUCCESS_COLOR
            ))
        else:
            if len(player.queue) < amount - 1:
                return await ctx.send(embed=discord.Embed(
                    title="Error",
                    description=f"There are only {len(player.queue) + 1} tracks in the queue!",
                    color=ERROR_COLOR
                ))
                
            for _ in range(amount - 1):
                player.queue.pop(0)
                
            await player.stop()
            
            await ctx.send(embed=discord.Embed(
                title="Skipped",
                description=f"Skipped {amount} tracks.",
                color=SUCCESS_COLOR
            ))

async def setup(bot):
    await bot.add_cog(Skip(bot)) 