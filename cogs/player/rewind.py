import discord
from discord import app_commands
from discord.ext import commands
import pomice
from config import EMBED_COLOR, ERROR_COLOR, SUCCESS_COLOR

class Rewind(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name="rewind", description="Rewind the current track by a specified amount")
    @app_commands.describe(seconds="The number of seconds to rewind (default: 10)")
    async def rewind(self, ctx, seconds: int = 10):
        """Rewind the current track by a specified amount"""
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
            
        current_position = player.position
        
        new_position = max(0, current_position - (seconds * 1000))
        
        await player.seek(new_position)
        
        await ctx.send(embed=discord.Embed(
            title="Track Rewound",
            description=f"Rewound the current track by {seconds} seconds.",
            color=SUCCESS_COLOR
        ))

async def setup(bot):
    await bot.add_cog(Rewind(bot)) 