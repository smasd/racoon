# racoon

Script to scrape daily COVID19 stats from @VicGovDH and post to Discord

Example twitter.json

    {
        "consumer_key": "<consumer_key>",
        "consumer_secret": "<consumer_secret>",
        "access_token": "<access_token>",
        "access_secret": "<access_secret>",
        "base_url": "https://api.twitter.com/1.1/statuses/user_timeline.json"
    }
    
Example discord.json

    {
        "token": "<token>",
        "channel": "<channel_id>",
        "sleep_time": 30,
        "pause_messaging": false,
        "pause_input": false,
        "message_list": []
    }