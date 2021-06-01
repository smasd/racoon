import discord
import lib.Settings as s

config = s.Settings('discord.json')


class Discord:
    def __init__(self):
        self.token = config.get('token')
        self.channel = config.get('channel')

        self.client = discord.Client()

        self.on_ready = self.client.event(self.on_ready)
        self.on_message = self.client.event(self.on_message)


