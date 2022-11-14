import requests
import threading
import time


class Proxies:
    
    def __init__(self, threadCount: int) -> None:
        self.threadCount = threadCount
        
        self.regions = {"EU": ["GB", "FR", "BE", "NL", "ES"]}
        self.proxies = {"EU": [], "US": [], "AS": []}
        self.sources = [
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
        ]
        
    def scrape(self):

        for link in self.sources:
            proxyList = requests.get(link).text
            threadList = []

            for proxy in proxyList.splitlines():
                threadList.append(threading.Thread(target=self.checkRegion, args=(proxy,)))
                
            for thread in threadList:
                thread.start()
                time.sleep(0.06)
            
            for thread in threadList:
                thread.join()
    
    def checkRegion(self, proxy):
        ip, port = proxy.split(":")
        response = requests.get(f"https://nordvpn.com/wp-admin/admin-ajax.php?action=get_user_info_data&ip={ip}", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'})
        try:
            ipRegion = response.json()["country_code"]
            for region, countries in self.regions.items():
                if ipRegion in countries:
                    print(f"{proxy} -> {region}")
                    self.proxies[region].append(proxy)
                    
        except:
            print(f"Error, Unable to find {proxy} Geolocation")
                
        
