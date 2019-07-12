#!/usr/bin/env python
import webbrowser
import signal
import sys

def help():
    print("Commands: placeholder, placeholder2" )


def buildURL():
    return ("http://www.google.com/search?q=test")


def gotoURL(url):
    webbrowser.open_new_tab(url)


def parse_cmd(cmd):
    if cmd == "help":
        help()

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
print("Type \"help\" for a list of commands")

while True:
    menu()

