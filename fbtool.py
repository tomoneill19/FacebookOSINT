#!/usr/bin/env python
import webbrowser
import signal
import sys
import requests
import re
import base64
from os import system, name

BANNER = '''
   ______ ____   ____   _____ _____ _   _ _______
  |  ____|  _ \ / __ \ / ____|_   _| \ | |__   __|
  | |__  | |_) | |  | | (___   | | |  \| |  | |
  |  __| |  _ <| |  | |\___ \  | | | . ` |  | |
  | |    | |_) | |__| |____) |_| |_| |\  |  | |
  |_|    |____/ \____/|_____/|_____|_| \_|  |_|

'''
Target = "No Target"
Keyword = "*"
Filters = []
URL_REGEX = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  #domain...
    r'localhost|'  #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$',
    re.IGNORECASE)


def get_fbid(fb_url):
    URL = "https://findmyfbid.com/"
    PARAMS = {'url': fb_url}
    try:
        r = requests.post(url=URL, params=PARAMS)
        return r.json().get("id")
    except Exception:
        return 0


def to_b64(data):
    encodedBytes = base64.b64encode(data.encode("utf-8"))
    return str(encodedBytes, "utf-8")


def helplist():
    print("\nsettarget [<target>]")
    print("setquery [<query>]")
    print("addfilter [<filter>]")
    print("getposts [url]")
    print("listvars\n")


def buildURL(search_type):
    joined_filters = "{" + ",".join(Filters) + "}"
    encoded_filters = to_b64(joined_filters).replace('=', '')
    search_url = "https://www.facebook.com/search/" + search_type + "/?q="
    search_url += Keyword + '&epa=FILTERS&filters=' + encoded_filters
    return search_url


def gotoURL(url):
    webbrowser.open_new_tab(url)


def printURL(url):
    print("URL: " + url)


def getID(arg):
    if len(arg) == 15 and arg.isnumeric():
        return arg
    if re.match(URL_REGEX, arg):
        return get_fbid(arg)
    return get_fbid("https://www.facebook.com/" + arg)


def set_target(arg=""):
    global Target
    if arg == "":
        print("Enter a username, url or ID to set the target")
        Target = getID(input("settarget> "))
    else:
        Target = getID(arg)
    if Target == 0:
        print("Target not found - API returned \"0\"")
    else:
        print("Target Set!")
        print("Target = " + str(Target) + "\n")
    Filters.append("\"rp_author\":{\"name\":\"author\",\"args\":\"" + str(Target) + "\"}")


def set_keyword(arg=""):
    global Keyword
    if arg == "":
        print("Enter a keyword to use in the search query...")
        Keyword = input("setquery> ")
    else:
        Keyword = arg
    print("Keyword set!")
    print("Keyword = " + str(Keyword) + "\n")


def add_filter(arg=""):
    print("Enter filter type to add...")
    print("filters: (inGroup,)")
    if arg == "":
        arg = input("addfilter> ")
    if arg == "inGroup":
        print("Enter the group name / url etc to enter as a filter...")
        group = input()
        Filters.append("{\"rp_group\":\"{\"name\":\"group_posts\",\"args\":\"" + getID(group) + "\"}\"")
    print("Filters = [" + ",".join(Filters) + "] \n")


def get_posts():
    gotoURL(buildURL("posts"))


def get_posts_url():
    printURL(buildURL("posts") + "\n")


def list_vars():
    print("Target = " + str(Target))
    print("query = " + str(Keyword))
    print("Filters = [" + ",".join(Filters) + "]")


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

        # for mac and linux
    else:
        _ = system('clear')
    print(BANNER)

def parse_cmd(cmd):
    if cmd[0] == "help":
        helplist()
    if cmd[0] == "settarget":
        if len(cmd) == 1:
            set_target()
        else:
            set_target(cmd[1])
    if cmd[0] == "addfilter":
        if len(cmd) == 1:
            add_filter()
        else:
            add_filter(cmd[1])
    if cmd[0] == "setquery":
        if len(cmd) == 1:
            set_keyword()
        else:
            set_keyword(cmd[1])
    if cmd[0] == "getposts":
        if len(cmd) == 1:
            get_posts()
        if len(cmd) == 2:
            if cmd[1] == "url":
                get_posts_url()
    if cmd[0] == "listvars":
        list_vars()
    if cmd[0] == "clear":
        clear()


def menu():
    print("Menu> ", end="")
    parse_cmd(input().lower().split(" "))


def exit_handle(signal, frame):
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_handle)

    print(BANNER)
    print("Welcome to the Facebook OSINT tool by Tom (@tomoneill19)\n")
    list_vars()
    print("\nType \"help\" for a list of commands...\n")

    while True:
        menu()
