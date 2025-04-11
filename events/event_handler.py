import discord
from discord.ext import commands
import asyncio
import random
import pomice
from config import STATUS_MESSAGES, EMBED_COLOR

class EventHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.rotate_status())
        
    async def rotate_status(self):
        """Rotate the bot's status message"""
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            status = random.choice(STATUS_MESSAGES)
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.listening,
                    name=status
                )
            )
            await asyncio.sleep(60) 
            
    @commands.Cog.listener()
    async def on_ready(self):
        """Event fired when the bot is ready"""
        print(f"Logged in as {self.bot.user.name}")
        print(f"Bot ID: {self.bot.user.id}")
        print(f"Discord.py Version: {discord.__version__}")
        print("------")
        
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Event fired when the bot joins a guild"""
        embed = discord.Embed(
            title="Thanks for adding me!",
            description="I'm a music bot that can play songs from YouTube.\n\n"
                       "Use `/play` to start playing music!\n"
                       "Use `/help` to see all available commands.",
            color=EMBED_COLOR
        )
        if guild.system_channel:
            await guild.system_channel.send(embed=embed)
            
    @commands.Cog.listener()
    async def on_pomice_track_end(self, player: pomice.Player, track: pomice.Track, reason):
        """Event fired when a track ends"""
        if not player.queue.is_empty and not player.is_playing:
            await player.play(player.queue.get_wait())
            
    @commands.Cog.listener()
    async def on_pomice_track_stuck(self, player: pomice.Player, track: pomice.Track):
        """Event fired when a track gets stuck"""                                                        
        channel = player.guild.get_channel(player.channel.id)
        if channel:
            await channel.send("Track got stuck, skipping to next song...")
            await player.stop()
            
    @commands.Cog.listener()
    async def on_pomice_track_exception(self, player: pomice.Player, track: pomice.Track, error):
        """Event fired when a track encounters an exception"""
        channel = player.guild.get_channel(player.channel.id)
        if channel:
            await channel.send(f"An error occurred while playing the track: {error}")
            await player.stop()
            
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Event fired when a member's voice state changes"""
        if member.guild.voice_client and member.guild.voice_client.channel == before.channel:
            if len(before.channel.members) == 1 and before.channel.members[0] == self.bot.user:
                await member.guild.voice_client.disconnect()
                
async def setup(bot):
    await bot.add_cog(EventHandler(bot)) 
