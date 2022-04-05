import praw
import os
import random
import datetime

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
                      "anime",
                      "indowibu",
                      "okbuddyhololive",
                      "ollieapexbottest"]
temp = ""
for item in LIST_OF_SUBREDDITS:
    temp += item
    temp += "+"
STRING_OF_SUBREDDITS = temp.rstrip("+")
# print(STRING_OF_SUBREDDITS)

# banned from VirtualYoutubers, goodanimemes not seeming to be welcoming,

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
                print(f"Cooling down! Please wait "
                      f"{COOLDOWN - (datetime.datetime.now() - self.last_posted_time).total_seconds()} seconds.")

    def cooled_down(self):
        time_now = datetime.datetime.now()
        difference = time_now - self.last_posted_time
        if difference.total_seconds() > COOLDOWN:
            return True
        else:
            return False

    def make_reply(self, comment):
        try:
            comment.reply(f"[{random.choice(self.response_list)}](https://youtu.be/VemenskFoBk)\n\n"
                          f"^This ^is ^a ^bot ^by ^u/illueluci")
            print("commented on reddit")
        except Exception as e:
            print(e)
        self.last_posted_time = datetime.datetime.now()


bot = RedditBot()

subreddit = reddit.subreddit(STRING_OF_SUBREDDITS)

while True:
    try:
        for c in subreddit.stream.comments(skip_existing=True):
            # print(c)
            bot.find_match(c)
    except:
        print("Error : not connected to internet, perhaps?")

