import requests
from bs4 import BeautifulSoup
import time
import datetime
from random import *


use_proxies = True
proxy_list = []
wait = 2
timeout_connect = 5
timeout_read = 5
proxy_loops = 0

def request_url(url,headers=None,timeout=(timeout_connect, timeout_read)):
    global wait,proxy_counter,use_proxies,proxy_list,proxy_loops
    maximum_loops = 50
    try:
        if proxy_loops >= maximum_loops:
            if use_proxies == True:
                print("Updating Proxies")
                proxy_list = update_proxies()
            else:
                proxy_list = None
            proxy_loops = 0
        if proxy_counter > (len(proxy_list)-1):
            proxy_counter = 0
            proxy_loops += 1
    except:
        proxy_counter = 0
    try:
        if headers == None:
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        try:
            headers["User-Agent"]
        except:
            headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        if use_proxies == True:
            #proxy_ip = proxy_list[randint(0,len(proxy_list)-1)][0]
            proxy_ip = proxy_list[proxy_counter][0]
            print("Counter: ("+str(proxy_counter)+"/"+str(len(proxy_list)-1)+")","Loop: ("+str(proxy_loops)+"/"+str(maximum_loops)+")")
            proxy = {"https":proxy_ip,"http":proxy_ip}
            print("Proxy Ip:",proxy_ip)
            proxy_counter += 1 #track position in the proxy list
            req = requests.get(url, headers=headers, proxies=proxy, timeout=timeout)
        else:
            req = requests.get(url, headers=headers, timeout=timeout)
        if req == None:
            print("Page returned nothing! Reloading")
            request_url(url,headers)
        else:
            return req
    except Exception as e:
        print("Page failed to load or Request timed out! Reloading",e)
        if use_proxies != True:
            time.sleep(wait)
        request_url(url,headers)

def update_proxies():
    unchecked_proxies = get_proxies()
    checked_proxies = check_proxies(unchecked_proxies)
    if (len(checked_proxies) == 0):
        update_proxies()
    else:
        return checked_proxies
    
def get_proxies():
    print("Getting proxies")
    unchecked_proxies = []
    proxies_page = requests.get("http://spys.one/en/anonymous-proxy-list/").text
    soup = BeautifulSoup(proxies_page, "lxml")
    legend_code = soup.find("script", attrs={"type": "text/javascript"}).contents[0].split(";")
    legend = {code.split("^")[0].split("=")[0]:code.split("^")[0].split("=")[1] for code in legend_code if code != code.split("^")[0]}
    rows = soup.findAll("tr", attrs={"onmouseover": "this.style.background='#002424'"})
    for row in rows:
        proxy_row = row.findAll("td", attrs={"colspan": "1"})
        proxy_element = proxy_row[0].find("font", attrs={"class": "spy14"})
        proxy_ip = proxy_element.text
        proxy_type = proxy_row[1].text.split()[0]
        proxy_port = "".join(legend[segment.split("^")[0]] for segment in proxy_element.contents[1].contents[0].split("(")[2:])
        proxy = str(proxy_ip)+":"+str(proxy_port)
        unchecked_proxies.append([proxy,proxy_type])
    return unchecked_proxies

def get_ip():
    status = 0
    while status != 200:
        try:
            url = "http://ip-check.info/?lang=en"
            req = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            html = req.text
            status = req.status_code
            #print(html,status)
            soup = BeautifulSoup(html, "lxml")
            current_ip = soup.findAll("a", attrs={"rel":"nofollow"})[1].text.strip()
        except:
            pass
    return current_ip

def check_proxies(unchecked_proxies):
    print("Checking proxies")
    global timeout_connect,timeout_read
    checked_proxies = []
    
    current_ip = get_ip()
    
    for host in unchecked_proxies:
        try:
            html = ""
            proxy = {"https":host[0],"http":host[0]}
            url = "http://ip-check.info/?lang=en"
            time1 = datetime.datetime.now()
            req = requests.get(url, headers={"User-Agent": "fight me"}, proxies=proxy, timeout=(timeout_connect, timeout_read))
            time2 = datetime.datetime.now()
            ping = str(int((time2 - time1).total_seconds() * 1000))+"ms"
            html = req.text
            soup = BeautifulSoup(html, "lxml")
            ip = soup.findAll("a", attrs={"rel":"nofollow"})[1].text.strip()
            status = req.status_code
            if ip == host[0].split(":")[0]:
                print("Working:",ping, host[0])
                checked_proxies.append(host)
            elif ip == current_ip:
                print("Not Working:",host[0])
            else:
                print("MultiLayered Working:",ping, ip, host[0])
                checked_proxies.append(host)
        except requests.exceptions.Timeout:
            print("Timed Out:",host[0])
        except:
            print("Not Working Fatal:",host[0])
    return checked_proxies

if use_proxies == True:
    proxy_list = update_proxies()
    print(proxy_list)
else:
    proxy_list = None

while True:
    headers = {"Origin": "http://vidstreaming.io",
               "Referer": "http://vidstreaming.io/",
               "User-Agent": "notlegitteehee 123/.0"}
    url = "http://www.youtube.com"
    res = request_url(url, headers=headers, timeout=(timeout_connect, timeout_read)) # automatically changes proxies after 50 uses
    print(res.code)
