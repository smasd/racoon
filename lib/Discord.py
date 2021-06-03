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

        # Will allow messages to be added to the queue but won't sent them
        self.pause = config.get("pause_messaging")

        # Will prevent messages from being added to the queue
        self.pause_input = config.get("pause_input")

        @self.client.event
        async def on_ready():
            while True:
                if not self.pause and not self.messages:
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
                else:
                    sleep(self.sleep_time)

        @self.client.event
        async def on_message(message):
            if not message.author == self.client.user:
                print("I got a message")

    def run(self):
        self.client.run(self.token, bot=True)

    def add_message(self, message, attachment=None):
        if not self.pause_input:
            content = {"message": message, "attachment": attachment}
            self.messages.append(content)
            self.save_messages()

            return True
        else:
            return False

    def save_messages(self):
        config.set("message_list", self.messages)
