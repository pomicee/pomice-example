from .dbconnect import Database

def is_connected():
    db = Database()
    return db.client is not None and db.client.server_info() is not None

def get_language(user_id, guild_id):
    db = Database()
    language_collection = db.db['languages']
    result = language_collection.find_one({'user_id': user_id, 'guild_id': guild_id})
    return result['language'] if result else None

def upsert_language(user_id, guild_id, language):
    db = Database()
    language_collection = db.db['languages']
    language_collection.update_one(
        {'user_id': user_id, 'guild_id': guild_id},
        {'$set': {'language': language}},
        upsert=True
    )