from .utils.http import Http


class Bot:
    
    def token(cookie):
        #x-csrf-token
        client = Http("auth.roblox.com")
        response = client.post(
            resource="/v2/login",
            data={},
            headers={"Cookie": f".ROBLOSECURITY={cookie}"}
        )
            
        return response[1].decode().split("csrf-token: ")[1].split("\r\n")[0]
        
    def allyRequest(cookie, target, group, proxy=None):

        client = Http("groups.roblox.com", proxy=proxy)
        response = client.post(
            resource=f"/v1/groups/{group}/relationships/allies/{target}",
            data={},
            headers={
                "Cookie": f".ROBLOSECURITY={cookie}",
                "X-CSRF-TOKEN": Bot.token(cookie)
            }
        )

        if response[0].decode() == "{}":
            return True

        else:
            return response[0].decode()
