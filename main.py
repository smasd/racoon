from lib import Settings as s, Twitter as t
from datetime import datetime
import pytz
import tzlocal
import re
import objectpath

config = s.Settings('config.json')
twitter = t.Twitter()

tag_re = re.compile(config.get("tag_re"), re.IGNORECASE)
include_re = re.compile(config.get("filter_include_re"), re.IGNORECASE)
exclude_re = re.compile(config.get("filter_exclude_re"), re.IGNORECASE)


def main():
    search_args = config.get("search_args")
    search_user = config.get("search_user")
    show_retweets = config.get("search_show_retweets")
    hide_replies = config.get("search_hide_replies")
    last_id = config.get("last_id")

    query_args = search_args.format(search_user, show_retweets, hide_replies, last_id)

    twitter.set_query_args(query_args)

    matched_tweets = []
    for resp in twitter.query():
        op = objectpath.Tree(resp)
        tags = op.execute('$.entities.hashtags')
        full_body = str(op.execute('$.full_text')).replace("&amp;", "&")
        created_at = datetime.strptime(op.execute('$.created_at'), "%a %b %d %H:%M:%S %z %Y")
        if tags:
            for tag in tags:
                if not tag_re.search(tag["text"]):
                    pass
        if config.get("filter_exclude_re") != "":
            if exclude_re.search(full_body):
                pass
        if include_re.search(full_body):
            tweet_id = op.execute('$.id')
            media_url = op.execute('$.entities.media[0].media_url')
            created_at_ltz = created_at.replace(tzinfo=pytz.utc).astimezone(tzlocal.get_localzone()).strftime(
                "%Y-%m-%d %H:%M")
            data = {
                "id": tweet_id,
                "created_at": created_at_ltz,
                "body": full_body,
                "media_url": media_url
            }
            matched_tweets.append(data)


if __name__ == "__main__":
    main()
