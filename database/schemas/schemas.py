from pymongo import MongoClient

class Database:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def close(self):
        self.client.close()

class Language:
    def __init__(self, db):
        self.collection = db['languages']

    def upsert(self, user_id, guild_id, language):
        self.collection.update_one(
            {'user_id': user_id, 'guild_id': guild_id},
            {'$set': {'language': language}},
            upsert=True
        )

    def get_language(self, user_id, guild_id):
        result = self.collection.find_one({'user_id': user_id, 'guild_id': guild_id})
        return result['language'] if result else None

class DJSettings:
    def __init__(self, db):
        self.collection = db['dj_settings']

    def upsert(self, guild_id, dj_role=None, dj_mode=False):
        self.collection.update_one(
            {'guild_id': guild_id},
            {'$set': {'dj_role': dj_role, 'dj_mode': dj_mode}},
            upsert=True
        )

    def get_settings(self, guild_id):
        result = self.collection.find_one({'guild_id': guild_id})
        return result if result else {'dj_role': None, 'dj_mode': False}

class GuildSettings:
    def __init__(self, db):
        self.collection = db['guild_settings']

    def upsert(self, guild_id, lyrics_enabled=False, autoplay_enabled=False, prefix="!"):
        self.collection.update_one(
            {'guild_id': guild_id},
            {'$set': {'lyrics_enabled': lyrics_enabled, 'autoplay_enabled': autoplay_enabled, 'prefix': prefix}},
            upsert=True
        )

    def get_settings(self, guild_id):
        result = self.collection.find_one({'guild_id': guild_id})
        return result if result else {'lyrics_enabled': False, 'autoplay_enabled': False, 'prefix': '!'}
