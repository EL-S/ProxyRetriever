import requests
from bs4 import BeautifulSoup
import time

use_proxies = True
proxy_list = []
wait = 2

def request_url(url):
    global wait
    try:
        req = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"})
        data = req.text
        return data
    except Exception as e:
        print("Page failed to load! Reloading",e)
        time.sleep(wait)
        request_url(url)

def update_proxies():
    global proxy_list
    proxies_page = request_url("http://spys.one/en/anonymous-proxy-list/")
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
        proxy = row.find("td", attrs={"colspan": "1"}).find("font", attrs={"class": "spy14"}).text
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
        proxy_list.append(proxy)
    print(proxy_list)
if use_proxies == True:
    update_proxies()
