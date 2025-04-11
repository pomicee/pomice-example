import discord

EMBED_COLOR = 0x3498db  
ERROR_COLOR = 0xe74c3c  
SUCCESS_COLOR = 0x2ecc71  
DEFAULT_VOLUME = 100
MAX_QUEUE_SIZE = 100

def format_duration(seconds):
    """Format duration in seconds to a human-readable string"""
    if not seconds:
        return "Unknown"
    
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

def create_error_embed(title, description):
    """Create an error embed"""
    return discord.Embed(
        title=title,
        description=description,
        color=ERROR_COLOR
    )

def create_success_embed(title, description):
    """Create a success embed"""
    return discord.Embed(
        title=title,
        description=description,
        color=SUCCESS_COLOR
    ) 
