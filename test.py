import lib.Discord as d
from pathlib import Path
from time import sleep
import threading

discord = d.Discord()


def add_test_message():
    attachment = "meme.jpg"
    discord.add_message("lol", attachment)


def main():
    thread = threading.Thread(target=add_test_message)
    thread.start()
    discord.run()


if __name__ == "__main__":
    main()
