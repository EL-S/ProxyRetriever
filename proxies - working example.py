import requests
from bs4 import BeautifulSoup
import time
import datetime
from random import *


use_proxies = True
proxy_list = []
wait = 2
timeout_connect = 1
timeout_read = 1
proxy_loops = 0

def request_url(url,headers=None):
    global wait,proxy_counter,use_proxies,proxy_list,proxy_loops
    maximum_loops = 50
    try:
        if proxy_loops >= maximum_loops:
            if use_proxies == True:
                print("Updating Proxies")
                proxy_list = update_proxies()
                print(proxy_list)
            else:
                proxy_list = None
            proxy_loops = 0
        if proxy_counter > (len(proxy_list)-1):
            proxy_counter = 0
            proxy_loops += 1
    except:
        proxy_counter = 0
    try:
        if use_proxies == True:
            #proxy_ip = proxy_list[randint(0,len(proxy_list)-1)][0]
            proxy_ip = proxy_list[proxy_counter][0]
            print("Counter: ("+str(proxy_counter)+"/"+str(len(proxy_list)-1)+")","Loop: ("+str(proxy_loops)+"/"+str(maximum_loops)+")")
            proxy = {"https":proxy_ip,"http":proxy_ip}
            print("Proxy Ip:",proxy_ip)
            proxy_counter += 1 #track position in the proxy list
            if headers == None:
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
            try:
                headers["User-Agent"]
            except:
                headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
            req = requests.get(url, headers=headers, proxies=proxy,timeout=3)
            data = req.text
        else:
            if headers == None:
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
            try:
                headers["User-Agent"]
            except:
                headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
            req = requests.get(url, headers=headers)
            data = req.text
        if data == None:
            print("Page returned nothing! Reloading")
            request_url(url,headers)
        elif data == "None":
            print("Page returned nothing string! Reloading")
            request_url(url,headers)
        else:
            return data
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
    unchecked_proxies = []
    proxies_page = requests.get("http://spys.one/en/anonymous-proxy-list/").text
    soup = BeautifulSoup(proxies_page, "lxml")
    legend_code = soup.find("script", attrs={"type": "text/javascript"}).text.split(";")
    legend_code2 = []
    legend = {}
    for code in legend_code:
        code_clean = code.split("^")[0]
        if code_clean != code:
            legend_code2.append(code_clean.split("="))
    for code2 in legend_code2:
        legend[code2[0]] = code2[1]
    rows = soup.findAll("tr", attrs={"onmouseover": "this.style.background='#002424'"})
    for row in rows:
        proxy_row = row.findAll("td", attrs={"colspan": "1"})
        proxy = proxy_row[0].find("font", attrs={"class": "spy14"}).text
        proxy_type = proxy_row[1].text
        proxy_code = proxy.split("(")
        port_code = []
        for proxy_code_segment in proxy_code:
            proxy_code_segment = proxy_code_segment.split(")")
            port_code.append(proxy_code_segment[0].split("^")[0])
            
        proxy_ip = port_code[0].split("d")[0]
        proxy_numbers = []
        for code_to_solve in port_code[2:]:
            number = legend[code_to_solve]
            proxy_numbers.append(number)
        proxy_port = "".join(proxy_numbers)
        proxy = str(proxy_ip)+":"+str(proxy_port)
        unchecked_proxies.append([proxy,proxy_type])
##    for i in unchecked_proxies:
##        print(i)
    return unchecked_proxies

def get_ip():
    status = 0
    while status != 200:
        try:
            url = "http://ip-check.info/?lang=en"
            req = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            html = req.text
            soup = BeautifulSoup(html, "lxml")
            current_ip = soup.findAll("script", attrs={"type":"text/javascript"})[3].text.split("'\">")[1].split(r"</a>")[0]
            status = req.status_code
        except:
            pass
    return current_ip

def check_proxies(unchecked_proxies):
    global timeout_connect,timeout_read
    checked_proxies = []
    
    current_ip = get_ip()
    
    for host in unchecked_proxies:
        try:
            proxy = {"https":host[0],"http":host[0]}
            url = "http://ip-check.info/?lang=en"
            time1 = datetime.datetime.now()
            req = requests.get(url, headers={"User-Agent": "fight me"}, proxies=proxy, timeout=(timeout_connect, timeout_read))
            time2 = datetime.datetime.now()
            ping = str(int((time2 - time1).total_seconds() * 1000))+"ms"
            html = req.text
            soup = BeautifulSoup(html, "lxml")
            ip = soup.findAll("script", attrs={"type":"text/javascript"})[3].text.split("'\">")[1].split(r"</a>")[0]
            status = req.status_code
            if ip == host[0].split(":")[0]:
                print("Working:",ping, host[0])
                checked_proxies.append(host)
            elif ip == current_ip:
                print("Not Working:",host[0])
            else:
                print("MultiLayered Working:",ping, ip, host[0])
                checked_proxies.append(host)
        except requests.exceptions. Timeout:
            print("Timed Out:",host[0])
        except:
            print("Not Working Fatal:",host[0])
    return checked_proxies

if use_proxies == True:
    proxy_list = update_proxies()
    print(proxy_list)
else:
    proxy_list = None

##headers = {"Origin": "https://vidstreaming.io",
##           "Referer": "https://vidstreaming.io/",
##           "User-Agent": "notlegitteehee 123/.0"}

#referer vidstreaming.io

while True:


    headers = {"Origin": "http://vidstreaming.io",
               "Referer": "http://vidstreaming.io/",
               "User-Agent": "notlegitteehee 123/.0"}

    #url = "http://hls12.mload.stream/hls/9a73328eaae6375b09e93541574a27b4/sub.4.m3u8"
    #url = "http://hls11x.mload.stream/hls/3cee59225bfe0e196edf87f828d8ce06/sub.12.360.m3u8"
    url = "http://hls11x.mload.stream/hls/3cee59225bfe0e196edf87f828d8ce06/sub.12.m3u8"
    #res = requests.get(url, headers=headers, proxies=proxy)
    data = request_url(url,headers=headers)
    print(data)

