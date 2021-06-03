from lib import Settings as s, Twitter as t, Discord as d, convert_to_ltz
from os import path, mkdir
from time import sleep
import re
import shutil
import requests
import threading
import objectpath

config = s.Settings('config.json')
twitter = t.Twitter()
discord = d.Discord()


class Tweet:
    def __init__(self):
        self.tag_re = re.compile(config.get("tag_re"), re.IGNORECASE)
        self.include_re = re.compile(config.get("filter_include_re"), re.IGNORECASE)
        self.exclude_re = re.compile(config.get("filter_exclude_re"), re.IGNORECASE)

        self.search_args = config.get("search_args")
        self.search_user = config.get("search_user")
        self.show_retweets = config.get("search_show_retweets")
        self.hide_replies = config.get("search_hide_replies")
        self.last_id = config.get("last_id")

        self.query_args = self.search_args.format(self.search_user, self.show_retweets, self.hide_replies, self.last_id)

        twitter.set_query_args(self.query_args)

        self.queue = config.get("queue")

        self.sleep_time = config.get("sleep_time")

    def parse_tweets(self):
        matched_tweets = []
        for resp in twitter.query():
            op = objectpath.Tree(resp)
            tweet_id = int(op.execute('$.id'))
            tweet_body = str(op.execute('$.full_text')).replace("&amp;", "&")
            created_at = convert_to_ltz(op.execute('$.created_at'), "%a %b %d %H:%M:%S %z %Y")

            tags = op.execute('$.entities.hashtags')
            if tags:
                for tag in tags:
                    if not self.tag_re.search(tag["text"]):
                        pass
            if config.get("filter_exclude_re") != "":
                if self.exclude_re.search(tweet_body):
                    pass
            if self.include_re.search(tweet_body):
                data = {
                    "id": tweet_id,
                    "created_at": created_at,
                    "body": tweet_body,
                    "media_url": op.execute('$.entities.media[0].media_url')
                }
                matched_tweets.append(data)
        for data in sorted(matched_tweets, key=lambda k: k['id']):
            self.queue.append(data)
        self.save_queue()
        self.set_last_id()
        self.send_queue()

    def save_queue(self):
        self.queue = sorted(self.queue, key=lambda k: k['id'])

        config.set("queue", self.queue)

    def send_queue(self):
        if discord.get_queue_state():
            while True:
                for payload in self.queue:
                    identifier = payload['id']
                    created_at = payload['created_at']
                    body = payload['body']
                    media_url = payload['media_url']
                    attachment = None

                    message = "{}:\n\n{}".format(created_at, body)

                    if media_url != "":
                        attachment = self.download_image(media_url, identifier)

                    discord.add_message(message, attachment)

                    self.queue.remove(payload)
                    self.save_queue()
                    break
                if not self.queue or not discord.get_queue_state():
                    break

    def set_last_id(self):
        if self.queue:
            self.last_id = max(self.queue, key=lambda k: k['id'])['id']
            config.set("last_id", self.last_id)

    @staticmethod
    def download_image(url, identifier):
        req = requests.get(url, stream=True)
        req.raw.decode_content = True

        if not path.exists("images"):
            mkdir("images")

        filename = str(identifier) + ".jpg"
        file_path = path.join("images", filename)
        with open(file_path, 'wb') as img:
            shutil.copyfileobj(req.raw, img)

        return file_path

    def run(self):
        while True:
            self.parse_tweets()
            sleep(self.sleep_time)


def main():
    tweet = Tweet()
    thread = threading.Thread(target=tweet.run)
    thread.start()
    discord.run()


if __name__ == "__main__":
    main()
