#!/usr/bin/env python
import webbrowser
import signal
import sys
import requests
import re

TARGET = "No Target"
URL_REGEX = re.compile(
                r'^(?:http|ftp)s?://' # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                r'localhost|' #localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?' # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def get_fbid(fb_url):
    URL = "https://findmyfbid.com/"
    PARAMS = {'url': fb_url}
    try:
        r = requests.post(url = URL, params= PARAMS)
        return r.json().get("id")
    except Exception:
        return 0


def help():
    print("Commands: settarget" )


def buildURL():
    return ("http://www.google.com/search?q=test")


def gotoURL(url):
    webbrowser.open_new_tab(url)


def getID(arg):
    if len(arg) == 15:
        return(arg)
    elif re.match(URL_REGEX, arg):
        return get_fbid(arg)
    else:
        return get_fbid("https://www.facebook.com/" + arg)

def set_target():
    print("Enter a username, url or ID to set the target")
    print("settarget>", end = "")
    TARGET = getID(input())
    print("Target Set! (0 implies malformed input)")
    print("Target = " + str(TARGET))

def parse_cmd(cmd):
    if cmd == "help":
        help()
    if cmd == "settarget":
        set_target()

def menu():
    print("Menu>", end = "")
    parse_cmd(input().lower())


def exit(signal, frame):
    sys.exit(0)


signal.signal(signal.SIGINT, exit)




banner = '''
   ______ ____   ____   _____ _____ _   _ _______
  |  ____|  _ \ / __ \ / ____|_   _| \ | |__   __|
  | |__  | |_) | |  | | (___   | | |  \| |  | |
  |  __| |  _ <| |  | |\___ \  | | | . ` |  | |
  | |    | |_) | |__| |____) |_| |_| |\  |  | |
  |_|    |____/ \____/|_____/|_____|_| \_|  |_|

'''
print(banner)
print("Welcome to the Facebook OSINT tool by Tom (@tomoneill19)")
print("Target = " + str(TARGET))
print("Type \"help\" for a list of commands")

while True:
    menu()

