#!/usr/bin/env python
import webbrowser

def buildURL():
    return ("http://www.google.com/search?q=test")

def gotoURL(url):
    webbrowser.open_new_tab(url)

if __name__ == "__main__":
    gotoURL(buildURL)
