import core
import random
import threading
import time


class Main:
    
    def __init__(self, threadsCount: int, groupId: int):
        self.threadsCount = threadsCount
        self.groupId = groupId
        
        self.cookies = {
            "EU": self.getCookies("eu.txt")
        }
        
    def getCookies(self, filename):
        with open(filename) as file:
            return [line.rstrip() for line in file]
        
    def run(self):
        proxyBot = core.Proxies(threadCount=100)
        proxyBot.scrape()
        self.proxies = proxyBot.proxies
        
        while True:
            for continent, cookies in self.cookies.items():
                for proxy in self.proxies[continent]:
                    time.sleep(20/self.threadsCount)
                    threading.Thread(target=self.sendAlly, args=(random.choice(cookies), proxy, continent,)).start()
        
    def sendAlly(self, cookie, proxy, continent):
        target = random.randint(1000000, 10000000)
        try:
            resp = core.Bot.allyRequest(
                cookie=cookie,
                target=target,
                group=self.groupId,
                proxy=proxy
            )
            
            if resp == True:
                print(f"Sent Ally -> {target} [{proxy}]")
                
            else:
                print(f"Error: {resp}")

        except:
            print(f"Bad Proxy -> {proxy}")
            
main = Main(threadsCount=input("Enter Thread Count -> "), groupId=input("Enter Group Id -> "))
main.run()
