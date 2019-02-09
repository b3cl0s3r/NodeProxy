#!/usr/bin/python
# -*- coding: utf-8 -*-

from threading import Lock
import threading
import requests
from lxml import html
import cfscrape
import time
import datetime


def check_ip(ip):
    http_proxy = "http://"+ip+":8080"

    proxyDict = {
        "http" : http_proxy
    }

    try:
        r = requests.get("http://www.cualesmiip.com", proxies=proxyDict)
    except:
        return

    tree =  html.fromstring(r.content)
    prueba = tree.xpath('//div[@id="miip"]/b/text()')

    try:
        if not (prueba[2].startswith("No navegas a")):
            mutex.acquire()
            print ip
            f=open("ip_list", "a+")
            f.write(ip+"\n")
            f.close()
            mutex.release()
    except:
        pass


# Some usefull things
mutex = Lock()
url="https://hidemyna.me/es/proxy-list/?ports=8080&start="
url2="#list"
proxy_ips_list=[]
start=0

## Get Proxy list from hidemyna

while True:
    scraper = cfscrape.create_scraper()
    final_url=url+str(start)+url2
    r = scraper.get(final_url).content
    tree = html.fromstring(r)
    list = tree.xpath('//td[@class="tdl"]/text()')

    if not list:
        break
    else:
        proxy_ips_list = proxy_ips_list + list
    start=start+64

## Try if each proxy IP work
threads = []

start_time = time.time()

for i in proxy_ips_list:
    t = threading.Thread(target=check_ip, args=(i,))
    threads.append(t)
    t.start()

for i in threads:
    i.join()

elapsed_time = time.time() - start_time
print str(datetime.timedelta(seconds=elapsed_time)).split(".")[0]
