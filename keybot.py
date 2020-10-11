from fake_useragent import UserAgent
import praw
import re
import os
import time
r = praw.Reddit('bot1')
fil = open("keys.txt", "w+")

with open("subreddits.txt") as f:
    lines = f.read().splitlines()


def userAgent():
    ua = UserAgent()
    return ua.random


def checkRepeat(text):
    count = {}
    returnlist = []
    for char in text:
        if char in count:
            count[char] += 1
        else:
            count[char] = 1
    for key in count:
        if count[key] > 2:
            returnlist.append(key)
    if len(returnlist) > 0:
        return True
    else:
        return False


def split(text):
    return text.upper().split()


def numDash(var):
    num = 0
    for x in var:
        if x == "-":
            num += 1
    if num == 2 or num == 4:
        return True
    return False


def checkList(key, droplist):
    if any(item in key for item in droplist):
        return True
    else:
        return False


def findKey(text, droplist):
    matched = []
    allkeys = []
    matchedkeys = []
    verifiedkeys = []
    text = split(text)
    text = [x for x in text if "-" in x]
    for x in text:
        if numDash(x):
            matched.append(x)
        else:
            continue
    keys = [x.replace("-", "") for x in matched]
    keys = [x for x in keys if len(x) == 15 or len(x) == 25]
    for x in keys:
        allkeys.append("-".join([x[i:i+5] for i in range(0, len(x), 5)]))
    for key in allkeys:
        fullkey = key.replace("-", "")
        if not checkRepeat(fullkey):
            verifiedkeys.append(key)
    for x in verifiedkeys:
        chunk = x.split("-")
        for part in chunk:
            if len(chunk) == 5 or len(chunk) == 3 or len(chunk) == 2:
                if not "*" in x and not "@" in x and not "£" in x and not "$" in x and not "ホ" in x and not "ル" in x and not "ッ" in x:
                    if not checkList(x, droplist):
                        matchedkeys.append(x)
                    if not checkList(x, droplist2):
                        matchedkeys.append(x)
    return matchedkeys


def getPosts(limit, droplist, cache):
    fil = open("keys.txt", "w+")
    for subs in lines:
        subreddit = r.subreddit(subs)
        for submission in subreddit.new(limit=limit):
            m = findKey(submission.selftext, droplist)
            if len(m) > 0:
                if "steam" or "Steam" or "free" or "Free" in submission.title.lower:
                    print("")
                    print("")
                    print("Key found in Subreddit: ", subreddit)
                    print("Title: ", end='')
                    if len(submission.title) >= 50:
                        print(submission.title[:50] + "...")
                    else:
                        print(submission.title)
                        print("Comment: ", end='')
                        print(submission.selftext[:50] + "...")
                        print("Key: ", end='')
                        print(m[0])
                        fil.write(
                            "https://store.steampowered.com/account/registerkey?key=")
                        fil.write(m[0])
                        fil.write("\n")
                        fil.flush()


droplist = ["GABEN", "G4B3N", "SCUM", "HLED", "OPITR"]
droplist2 = ["23ABCDGHJLPRST", "23"]

cache = []

fil = open("keys.txt", "w+")
print("List of used Subreddits: ", end='')
for define in lines:
    print(define, end='')
    print(" - ", end='')
getPosts(100000000000, droplist, cache)
print("")
print("")
print("Done.")
fil.close()
os.system('read -n1 -r -p "Press any key to continue..." key')
