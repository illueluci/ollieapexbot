import praw
import os
import random
import datetime
from keep_alive_flask import keep_alive

reddit = praw.Reddit(client_id="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                     client_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                     username="xxxxxxxxxxxxxxxxxxxxx",
                     password="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                     user_agent="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

# print(reddit.user.me)

COOLDOWN = 30
LIST_OF_SUBREDDITS = ["hololive",
                      "holostars",
                      "KureijiOllie",
                      "Animemes",
                      "indowibu",
                      "okbuddyhololive",
                      "ImSorryYagoo",
                      "ollieapexbottest"]
temp = ""
for item in LIST_OF_SUBREDDITS:
    temp += item
    temp += "+"
STRING_OF_SUBREDDITS = temp.rstrip("+")
# print(STRING_OF_SUBREDDITS)

# banned from VirtualYoutubers and anime, goodanimemes not seeming to be welcoming,

with open('already_replied.txt', 'a') as aaa:
    pass


class RedditBot:
    def __init__(self):
        self.trigger_word = "apex"
        self.dont_trigger_word = ["u/illueluci", "bot", "peko"]
        self.response_list = ["DID SOMEBODY SAY APEX!?", "MABAR APEX YUK"]
        self.last_posted_time = datetime.datetime.now()
        self.link_id_already_replied_on = []
        with open('already_replied.txt', 'r') as file:
            for line in file:
                stripped_line = line.strip()
                self.link_id_already_replied_on.append(stripped_line)


    def find_match(self, comment):
        print(comment.body.casefold())
        # print(comment.link_id)
        condition1 = self.trigger_word in comment.body.casefold()
        condition2 = not(any([s in comment.body.casefold() for s in self.dont_trigger_word]))
        condition3 = comment.link_id not in self.link_id_already_replied_on
        if condition1 and condition2 and condition3:
            if self.cooled_down():
                self.make_reply(comment)
                self.link_id_already_replied_on.append(comment.link_id)
                with open('already_replied.txt', 'a') as file:
                    print(comment.link_id, file=file)
            else:
                print("*" * 50)
                print(f"Cooling down! Please wait "
                      f"{COOLDOWN - (datetime.datetime.now() - self.last_posted_time).total_seconds()} seconds.")
                print("*" * 50)

    def cooled_down(self):
        time_now = datetime.datetime.now()
        difference = time_now - self.last_posted_time
        if difference.total_seconds() > COOLDOWN:
            return True
        else:
            return False

    def make_reply(self, comment):
        dice_roll = random.randint(0,2)
        condition4 = (dice_roll == 0)  # 1 in 3 chances it comments
        if condition4:
            try:
                comment.reply(f"[{random.choice(self.response_list)}](https://youtu.be/VemenskFoBk)\n\n"
                              f"^^This ^^is ^^a ^^bot ^^by ^^u/illueluci")
                print("*" * 50)
                print("Commented on reddit!")
                print("*" * 50)
            except Exception as e:
                print(e)
            self.last_posted_time = datetime.datetime.now()
        else:
            print("*" * 50)
            print(f"Failed dice roll! The bot rolled {dice_roll}.")
            print("*" * 50)


keep_alive()

bot = RedditBot()
subreddit = reddit.subreddit(STRING_OF_SUBREDDITS)

while True:
    try:
        for c in subreddit.stream.comments(skip_existing=True):
            # print(c)
            bot.find_match(c)
    except:
        print("Error : not connected to internet, perhaps?")
