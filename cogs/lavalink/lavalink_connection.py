import discord
from discord.ext import commands
import pomice
import asyncio
import os
from dotenv import load_dotenv
from config import LAVALINK_HOST, LAVALINK_PORT, LAVALINK_PASSWORD
load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

class LavalinkConnection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.bot.loop.create_task(self.connect_nodes())  
        
    async def connect_nodes(self):
        """Connect to Lavalink nodes"""
        await self.bot.wait_until_ready()
        
        await pomice.NodePool.create_node(
            bot=self.bot,
            host=LAVALINK_HOST,
            port=LAVALINK_PORT,
            password=LAVALINK_PASSWORD,
            identifier="MAIN",
            spotify_client_id="",
            spotify_client_secret="",
            apple_music=""
            )
        print("Connected to Lavalink node with Spotify support")
        
    @commands.Cog.listener()
    async def on_pomice_node_ready(self, node: pomice.Node):
        """Event fired when a node is ready"""
        print(f"Node {node.identifier} is ready!")
        
    @commands.Cog.listener()
    async def on_pomice_node_error(self, node: pomice.Node, error: Exception):
        """Event fired when a node encounters an error"""
        print(f"Node {node.identifier} encountered an error: {error}")
        
    @commands.Cog.listener()
    async def on_pomice_node_closed(self, node: pomice.Node):
        """Event fired when a node is closed"""
        print(f"Node {node.identifier} was closed")

async def setup(bot):
    await bot.add_cog(LavalinkConnection(bot))
