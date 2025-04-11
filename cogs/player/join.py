import discord
from discord import app_commands
from discord.ext import commands
import pomice
from config import EMBED_COLOR, ERROR_COLOR, SUCCESS_COLOR

class Join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name="join", description="Make the bot join your voice channel")
    async def join(self, ctx):
        """Make the bot join your voice channel"""
        if not ctx.guild:
            return await ctx.send(embed=discord.Embed(
                title="Error",
                description="This command can only be used in a server!",
                color=ERROR_COLOR
            ))
            
        if not ctx.author.voice:
            return await ctx.send(embed=discord.Embed(
                title="Error",
                description="You need to be in a voice channel to use this command!",
                color=ERROR_COLOR
            ))
            
        voice_channel = ctx.author.voice.channel
        
        if ctx.guild.voice_client:
            player = ctx.guild.voice_client
            if player.channel.id != voice_channel.id:
                await player.move_to(voice_channel)
                await ctx.send(embed=discord.Embed(
                    title="Moved",
                    description=f"Moved to {voice_channel.name}.",
                    color=SUCCESS_COLOR
                ))
            else:
                await ctx.send(embed=discord.Embed(
                    title="Already Connected",
                    description=f"I'm already connected to {voice_channel.name}.",
                    color=EMBED_COLOR
                ))
        else:
            try:
                await voice_channel.connect(cls=pomice.Player)
                await ctx.send(embed=discord.Embed(
                    title="Joined",
                    description=f"Joined {voice_channel.name}.",
                    color=SUCCESS_COLOR
                ))
            except Exception as e:
                return await ctx.send(embed=discord.Embed(
                    title="Error",
                    description=f"Failed to connect to voice channel: {str(e)}",
                    color=ERROR_COLOR
                ))

async def setup(bot):
    await bot.add_cog(Join(bot)) 