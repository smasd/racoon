import discord
import lib.Settings as s
from time import sleep

config = s.Settings('discord.json')


class Discord:
    def __init__(self):
        self.token = config.get('token')
        self.channel = int(config.get('channel'))
        self.sleep_time = config.get("sleep_time")

        self.client = discord.Client()

        self.messages = config.get("message_list")

        @self.client.event
        async def on_ready():
            while True:
                for payload in self.messages:
                    message = payload["message"]
                    attachment = payload["attachment"]

                    if attachment is not None:
                        await self.client.get_channel(self.channel).send(message, file=discord.File(attachment))
                    else:
                        await self.client.get_channel(self.channel).send(message)
                    self.messages.remove(payload)
                    self.save_messages()
                    break
                if not self.messages:
                    sleep(self.sleep_time)

        @self.client.event
        async def on_message(message):
            if not message.author == self.client.user:
                print("I got a message")

    def run(self):
        self.client.run(self.token, bot=True)

    def add_message(self, message, attachment=None):
        content = {"message": message, "attachment": attachment}
        self.messages.append(content)
        self.save_messages()

    def save_messages(self):
        config.set("message_list", self.messages)
