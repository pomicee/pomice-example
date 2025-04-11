import discord
from discord import app_commands
from discord.ext import commands
import pomice
from config import EMBED_COLOR, ERROR_COLOR, SUCCESS_COLOR

class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name="search", description="Search for tracks without playing them")
    @app_commands.describe(query="The search query")
    async def search(self, ctx, *, query: str):
        """Search for tracks without playing them"""
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
        else:
            try:
                player = await voice_channel.connect(cls=pomice.Player)
            except Exception as e:
                return await ctx.send(embed=discord.Embed(
                    title="Error",
                    description=f"Failed to connect to voice channel: {str(e)}",
                    color=ERROR_COLOR
                ))
        
        search_msg = await ctx.send(embed=discord.Embed(
            title="Searching",
            description=f"🔍 Searching for `{query}`...",
            color=EMBED_COLOR
        ))
        
        try:
            tracks = await player.get_tracks(query, ctx=ctx)
            
            if not tracks:
                return await search_msg.edit(embed=discord.Embed(
                    title="Error",
                    description="No results found for your query.",
                    color=ERROR_COLOR
                ))
                
            if isinstance(tracks, pomice.TrackPlaylist):
                embed = discord.Embed(
                    title=f"Search Results: {tracks.name}",
                    description=f"Found {len(tracks.tracks)} tracks in this playlist.",
                    color=EMBED_COLOR
                )
                
                for i, track in enumerate(tracks.tracks[:5], 1):
                    embed.add_field(
                        name=f"{i}. {track.title}",
                        value=f"by {track.author} • {self.format_duration(track.length)}",
                        inline=False
                    )
                    
                if len(tracks.tracks) > 5:
                    embed.add_field(
                        name="More Tracks",
                        value=f"... and {len(tracks.tracks) - 5} more tracks.",
                        inline=False
                    )
                    
                await search_msg.edit(embed=embed)
                
            else:
                embed = discord.Embed(
                    title="Search Results",
                    description=f"Found {len(tracks)} tracks for your query.",
                    color=EMBED_COLOR
                )
                
                for i, track in enumerate(tracks[:5], 1):
                    embed.add_field(
                        name=f"{i}. {track.title}",
                        value=f"by {track.author} • {self.format_duration(track.length)}",
                        inline=False
                    )
                    
                if len(tracks) > 5:
                    embed.add_field(
                        name="More Tracks",
                        value=f"... and {len(tracks) - 5} more tracks.",
                        inline=False
                    )
                    
                await search_msg.edit(embed=embed)
                
        except Exception as e:
            return await search_msg.edit(embed=discord.Embed(
                title="Error",
                description=f"An error occurred while searching: {str(e)}",
                color=ERROR_COLOR
            ))
            
    def format_duration(self, duration):
        """Format duration in milliseconds to a human-readable string"""
        minutes, seconds = divmod(duration // 1000, 60)
        hours, minutes = divmod(minutes, 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"

async def setup(bot):
    await bot.add_cog(Search(bot)) 