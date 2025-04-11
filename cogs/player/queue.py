import discord
from discord import app_commands
from discord.ext import commands
import pomice
from config import EMBED_COLOR, ERROR_COLOR, SUCCESS_COLOR

class Queue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name="queue", aliases=["q"], description="Display the current music queue")
    @app_commands.describe(page="The page number to display (default: 1)")
    async def queue(self, ctx, page: int = 1):
        """Display the current music queue"""
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
            
        if not player.queue and not player.is_playing():
            return await ctx.send(embed=discord.Embed(
                title="Queue",
                description="The queue is empty!",
                color=EMBED_COLOR
            ))
            
        tracks_per_page = 10
        total_tracks = len(player.queue) + (1 if player.is_playing() else 0)
        total_pages = (total_tracks + tracks_per_page - 1) // tracks_per_page
        
        if page < 1 or page > total_pages:
            return await ctx.send(embed=discord.Embed(
                title="Error",
                description=f"Invalid page number. The queue has {total_pages} pages.",
                color=ERROR_COLOR
            ))
            
        start_index = (page - 1) * tracks_per_page
        end_index = min(start_index + tracks_per_page, total_tracks)
        
        embed = discord.Embed(
            title="Music Queue",
            color=EMBED_COLOR
        )

        if player.is_playing():
            current_track = player.current
            embed.add_field(
                name="Now Playing",
                value=f"**{current_track.title}** by {current_track.author} • {self.format_duration(current_track.length)}",
                inline=False
            )
            
        if player.queue:
            queue_text = ""
            
            for i, track in enumerate(player.queue[start_index:end_index], start_index + 1):
                queue_text += f"**{i}.** **{track.title}** by {track.author} • {self.format_duration(track.length)}\n"
                
            embed.add_field(name="Queue", value=queue_text, inline=False)
            
        embed.set_footer(text=f"Page {page}/{total_pages} • {total_tracks} tracks in queue")
        
        await ctx.send(embed=embed)
        
    def format_duration(self, duration):
        """Format duration in milliseconds to a human-readable string"""
        minutes, seconds = divmod(duration // 1000, 60)
        hours, minutes = divmod(minutes, 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"

async def setup(bot):
    await bot.add_cog(Queue(bot)) 