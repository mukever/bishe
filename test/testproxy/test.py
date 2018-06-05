import requests
import bs4
proxy_ip_port = requests.get('http://123.207.35.36:5010/get/').content.decode('utf8')
proxy = {'http': proxy_ip_port}
print(proxy)
print (bs4.BeautifulSoup(requests.get('http://ip.chinaz.com/',proxies=proxy).content).find("p",{"class":"getlist pl10"}).get_text())