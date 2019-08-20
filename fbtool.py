#!/usr/bin/env python
import webbrowser
import signal
import sys
import requests
import re
import base64

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
    print("Commands: settarget, setquery, addfilter, getposts, getpostsurl, listvars")


def buildURL(search_type):
    joined_filters = "{" + ",".join(Filters) + "}"
    encoded_filters = to_b64(joined_filters).replace('=', '')
    search_url = "https://www.facebook.com/search/" + search_type + "/?q="
    search_url += Keyword + '&epa=FILTERS&filters=' + encoded_filters
    return (search_url)


def gotoURL(url):
    webbrowser.open_new_tab(url)


def printURL(url):
    print("URL: " + url)


def getID(arg):
    if len(arg) == 15:
        return (arg)
    if re.match(URL_REGEX, arg):
        return get_fbid(arg)
    return get_fbid("https://www.facebook.com/" + arg)


def set_target():
    print("Enter a username, url or ID to set the target")
    print("settarget>", end=" ")
    Target = getID(input())
    if Target == 0:
        print("Malformed imput, target is \"0\"")
    else:
        print("Target Set!")
        print("Target = " + str(Target))
    Filters.append("\"rp_author\":{\"name\":\"author\",\"args\":\"" + str(Target) + "\"}")


def set_keyword():
    print("Enter a keyword to use in the search query...")
    print("setquery>", end=" ")
    global Keyword
    Keyword = input()
    print("Keyword set!")
    print("Keyword = " + str(Keyword))


def add_filter():
    print("Enter filter type to add...")
    print("filters: (inGroup,)")
    print("addfilter>", end=" ")
    if input() == "inGroup":
        print("Enter the group name / url etc to enter as a filter...")
        group = input()
        Filters.append("{\"rp_group\":\"{\"name\":\"group_posts\",\"args\":\"" + getID(group) + "\"}\"")
    print("Filters = [" + ",".join(Filters) + "]")


def get_posts():
    gotoURL(buildURL("posts"))


def get_posts_url():
    printURL(buildURL("posts"))


def list_vars():
    print("Target = " + str(Target))
    print("query = " + str(Keyword))
    print("Filters = [" + ",".join(Filters) + "]")


def parse_cmd(cmd):
    if cmd == "help":
        helplist()
    if cmd == "settarget":
        set_target()
    if cmd == "addfilter":
        add_filter()
    if cmd == "getposts":
        get_posts()
    if cmd == "getpostsurl":
        get_posts_url()
    if cmd == "setquery":
        set_keyword()
    if cmd == "listvars":
        list_vars()


def menu():
    print("Menu>", end=" ")
    parse_cmd(input().lower())


def exit_handle(signal, frame):
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_handle)

    print(BANNER)
    print("Welcome to the Facebook OSINT tool by Tom (@tomoneill19)")
    list_vars()
    print("Type \"help\" for a list of commands")

    while True:
        menu()
